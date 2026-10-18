# AI-Powered E-Commerce Research, Listing and Management System
### Marketplace: Amazon India (`amazon.in` • Marketplace ID: `A21TJRUUN4KGV`)

---

## 1. Overview & Architecture

A production-oriented, multi-agent e-commerce automation platform designed for inventory-based reselling on **Amazon India**, with an extensible architecture ready for **Flipkart** and **Meesho**.

The system is built on the philosophy of **Deterministic Core + Probabilistic Assistants**:
- **Financial, stock, fee, and risk calculations** are 100% deterministic (Python mathematical models with verified unit tests).
- **AI agents** are constrained to research synthesis, sentiment/complaint extraction, copy drafting, and structured recommendations.
- **Evidence Provenance**: Every data point is tagged with `Source`, `Timestamp`, `Confidence`, and Classification (`ACTUAL`, `REPORTED_ESTIMATE`, or `AI_HYPOTHESIS`).
- **Human-in-the-Loop Governance**: Strict state machine requiring explicit user sign-off before placing purchase orders, paying suppliers, publishing listings, or spending ad budgets.
- **1-Click Emergency Stop**: Instant global software circuit breaker that freezes all external write operations without data loss.

---

## 2. Technology Stack & Design Decisions

- **Backend**: Python 3.9+ with **FastAPI**, **Pydantic v2**, and **SQLAlchemy 2.0**
- **Database**: SQLite in **WAL (Write-Ahead Logging)** mode (local zero-dependency deployment, fully compatible with PostgreSQL)
- **Credential Vault**: AES/HMAC symmetric cipher securing Amazon SP-API refresh tokens, Gemini keys, and Telegram credentials
- **Frontend Dashboard**: Native responsive Single Page Application (HTML5, Modern CSS Glassmorphic design system, Chart.js, Vanilla JS) served directly by FastAPI—**zero Node.js/NPM build dependencies required**
- **Scheduler**: Asynchronous daily cron runner (Morning Sync 07:30 IST, Midday Monitoring 13:00 IST, Evening Report 20:00 IST)

---

## 3. The 12-Specialized AI Agent Cluster

| Agent | Module | Responsibility & Guarantees |
| :--- | :--- | :--- |
| **1. Product Discovery** | `agents/discovery_agent.py` | Identifies candidate products. Uses empirical BSR power-law curves for Amazon India sales estimates. Never fabricates sales. |
| **2. Market & Competition** | `agents/market_analyst.py` | Assesses review moats (>1,500 reviews), Buy Box saturation, price war risks, and extracts customer complaints. |
| **3. Cost & Profitability** | `agents/cost_profit_agent.py` | **Deterministic Engine**: Amazon Referral & Closing fees, Easy Ship/FBA logistics, 18% GST, net margins, ROI, break-even price. |
| **4. Supplier Research** | `agents/supplier_agent.py` | Ingests supplier quotes (IndiaMART, TradeIndia, direct foundries), MOQs, lead times, and verification checklists. |
| **5. Risk & Compliance** | `agents/risk_agent.py` | Screens for Indian Legal Metrology declarations, BIS certification orders, trademark infringement, and Hazmat rules. |
| **6. Keyword Research** | `agents/keyword_agent.py` | High-intent keywords; enforces Amazon India's strict **249-byte backend search terms** limit without word repetition. |
| **7. Product Image Studio** | `agents/image_agent.py` | Enforces 1000px+ resolution, pure white RGB (255,255,255) background on Main slot, and plans a 6-slot visual roadmap. |
| **8. Listing Creation** | `agents/listing_agent.py` | Compiles complete compliant drafts: titles (<=200 chars), 5 benefit-driven bullets, description, and queues human approval. |
| **9. Inventory Management** | `agents/inventory_agent.py` | **Deterministic Engine**: Computes Reorder Point $\text{ROP} = (\text{Daily Demand} \times \text{Lead Time}) + \text{Safety Stock}$. |
| **10. Price Optimisation** | `agents/price_agent.py` | Evaluates price elasticity; protects configured margin floors and prevents destructive price wars. |
| **11. Listing Health** | `agents/health_agent.py` | Monitors Buy Box ownership, return velocity, customer ratings, and listing suppression alerts. |
| **12. Daily Reporting** | `agents/reporting_agent.py` | Aggregates 12-point executive intelligence briefing, replenishment alerts, CSV exports, and Telegram alerts. |

---

## 4. Quickstart & Installation

### Option A: 1-Click Launch Script
```bash
./run.sh
```

### Option B: Manual Step-by-Step
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Seed baseline database & default admin
PYTHONPATH=. python database/seed_data.py

# 4. Start the Application Server
PYTHONPATH=. uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Once started:
- **Web Dashboard**: `http://localhost:8000`
- **Interactive OpenAPI Documentation**: `http://localhost:8000/docs`

---

## 5. Automated Test Suite

Run the complete automated test suite verifying mathematical precision, rejection gates, and workflows:

```bash
PYTHONPATH=. .venv/bin/pytest tests/ -v
```

All 17 automated tests cover:
- Amazon India category referral fee slabs (Home & Kitchen, Electronics, Office, Beauty)
- Closing fee slabs for Easy Ship vs FBA
- Weight handling rates (National, Regional, Local)
- Deterministic unit economics, 18% GST calculation, and scenario monotonicity
- Inventory Reorder Point (ROP) and safety stock formulas
- Mandatory rejection gates (Hazmat rejection, sub-par margin disqualification)
- Approval state transitions (`DISCOVERED` -> `ANALYSED` -> `AWAITING_APPROVAL` -> `APPROVED` -> `ACTION_EXECUTED`)
- Global emergency stop write-freeze validation
- End-to-end API lifecycle and CSV portfolio export

---

## 6. External Integrations Setup Guide

### 1. Amazon Selling Partner API (SP-API)
1. Register as a developer on **Amazon Seller Central India** (`sellercentral.amazon.in`).
2. Create an IAM Role in AWS and link it to your Developer Application.
3. Obtain your **LWA (Login with Amazon) App Client ID**, **Client Secret**, and generate a **Refresh Token**.
4. In the Dashboard, navigate to **🔌 SP-API & Settings** and save your credentials. They are encrypted using the local AES vault.
5. *Note: If credentials are not yet configured, the system operates in verified Offline / Simulation Mode with zero fake data.*

### 2. Google Gemini AI API
1. Get a free API key from **Google AI Studio** (`aistudio.google.com`).
2. Enter the key in **🔌 SP-API & Settings** or set the environment variable:
   ```bash
   export GEMINI_API_KEY="AIzaSy..."
   ```

### 3. Telegram Instant Briefing Alerts (100% Free)
1. Open Telegram and message `@BotFather` to create a new bot and copy the token.
2. Message `@userinfobot` to get your Telegram `chat_id`.
3. Enter both in **🔌 SP-API & Settings**. Daily executive briefings and critical low-stock alerts will be dispatched directly to your phone.

---

## 7. 24/7 Cloud Deployment (Scheduled Operation)

To keep scheduled jobs and background monitoring active 24/7 when your local computer is powered off, deploy the platform to a cloud VPS (e.g. Ubuntu on AWS Lightsail, Hetzner, or DigitalOcean):

### Systemd Service Configuration (`/etc/systemd/system/ecom-os.service`)
```ini
[Unit]
Description=AI E-Commerce Management Platform (Amazon India)
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/Atigravity_Project
ExecStart=/opt/Atigravity_Project/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
Environment="PATH=/opt/Atigravity_Project/.venv/bin"
Environment="PYTHONPATH=/opt/Atigravity_Project"

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ecom-os
```

---

## 8. Operating Cost Estimate

| Expense Item | Minimum / Development | Production (Scale) |
| :--- | :--- | :--- |
| **Application Hosting** | Local Mac (₹0) | Cloud VPS (2GB RAM): **~₹500 / month** |
| **Amazon Professional Seller** | ₹1,499 + 18% GST = **₹1,769 / month** | **₹1,769 / month** |
| **Gemini AI API** | Free tier (Google AI Studio) | Pay-as-you-go: **~₹200 – ₹500 / month** |
| **Telegram Alerts** | 100% Free (₹0) | 100% Free (₹0) |
| **Total Monthly Outlay** | **~₹1,769 / month** | **~₹2,469 – ₹2,769 / month** |
