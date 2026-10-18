"""
Encrypted Credential Vault
Stores sensitive API keys and SP-API tokens using AES/Fernet encryption.
Prevents plain-text token exposure in databases, logs, and dumps.
"""

import os
import base64
import hashlib
import hmac
import json
from typing import Dict, Any, Optional

try:
    from cryptography.fernet import Fernet
    HAS_FERNET = True
except ImportError:
    HAS_FERNET = False

from config.settings import settings


class CredentialVault:
    def __init__(self, master_key: Optional[str] = None):
        raw_key = master_key or settings.vault_master_key
        # Ensure 32-byte url-safe base64 key
        hashed = hashlib.sha256(raw_key.encode()).digest()
        self._key_bytes = hashed
        self._fernet_key = base64.urlsafe_b64encode(hashed)
        if HAS_FERNET:
            self._cipher = Fernet(self._fernet_key)
        else:
            self._cipher = None

    def encrypt(self, payload: Dict[str, Any]) -> str:
        """Serialize and encrypt a dictionary into a safe cipher string."""
        serialized = json.dumps(payload).encode("utf-8")
        if HAS_FERNET and self._cipher:
            return self._cipher.encrypt(serialized).decode("utf-8")
        else:
            # Fallback XOR-HMAC stream cipher for environments without C-extensions
            iv = os.urandom(16)
            stream_key = hmac.new(self._key_bytes, iv, hashlib.sha256).digest()
            # Expand key stream
            while len(stream_key) < len(serialized):
                stream_key += hmac.new(self._key_bytes, stream_key, hashlib.sha256).digest()
            ciphertext = bytes([b ^ k for b, k in zip(serialized, stream_key)])
            mac = hmac.new(self._key_bytes, iv + ciphertext, hashlib.sha256).digest()
            packed = base64.b64encode(iv + mac + ciphertext).decode("utf-8")
            return f"V1:{packed}"

    def decrypt(self, encrypted_str: str) -> Dict[str, Any]:
        """Decrypt a cipher string back into its original dictionary."""
        if not encrypted_str:
            return {}
        try:
            if HAS_FERNET and self._cipher and not encrypted_str.startswith("V1:"):
                decrypted_bytes = self._cipher.decrypt(encrypted_str.encode("utf-8"))
                return json.loads(decrypted_bytes.decode("utf-8"))
            elif encrypted_str.startswith("V1:"):
                raw = base64.b64decode(encrypted_str[3:].encode("utf-8"))
                iv = raw[:16]
                mac = raw[16:48]
                ciphertext = raw[48:]
                expected_mac = hmac.new(self._key_bytes, iv + ciphertext, hashlib.sha256).digest()
                if not hmac.compare_digest(mac, expected_mac):
                    raise ValueError("Vault authentication tag mismatch: corrupt or tampered cipher")
                stream_key = hmac.new(self._key_bytes, iv, hashlib.sha256).digest()
                while len(stream_key) < len(ciphertext):
                    stream_key += hmac.new(self._key_bytes, stream_key, hashlib.sha256).digest()
                decrypted = bytes([b ^ k for b, k in zip(ciphertext, stream_key)])
                return json.loads(decrypted.decode("utf-8"))
            elif HAS_FERNET and self._cipher:
                decrypted_bytes = self._cipher.decrypt(encrypted_str.encode("utf-8"))
                return json.loads(decrypted_bytes.decode("utf-8"))
            else:
                raise ValueError("Unsupported cipher format or missing cryptography provider")
        except Exception as e:
            return {"error": f"Failed to decrypt credentials: {str(e)}"}


vault = CredentialVault()
