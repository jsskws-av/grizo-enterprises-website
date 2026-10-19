import React from 'react';
import { siteConfig } from '@/config/siteConfig';

interface StatusBadgeProps {
  className?: string;
  showIcon?: boolean;
}

export default function StatusBadge({
  className = '',
  showIcon = true,
}: StatusBadgeProps) {
  const status = siteConfig.application.status;

  return (
    <div
      className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border bg-amber-50 text-amber-900 border-amber-200/80 shadow-xs ${className}`}
      role="status"
      aria-label={`Application Status: ${status}`}
    >
      {showIcon && (
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
        </span>
      )}
      <span>Internal application under development</span>
    </div>
  );
}
