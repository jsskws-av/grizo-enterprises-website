import React from 'react';
import Link from 'next/link';

interface WordmarkProps {
  className?: string;
  variant?: 'dark' | 'light';
  size?: 'sm' | 'md' | 'lg';
}

export default function Wordmark({
  className = '',
  variant = 'dark',
  size = 'md',
}: WordmarkProps) {
  const isLight = variant === 'light';

  const iconSizes = {
    sm: 'w-7 h-7',
    md: 'w-8 h-8',
    lg: 'w-10 h-10',
  };

  const titleSizes = {
    sm: 'text-base',
    md: 'text-lg',
    lg: 'text-2xl',
  };

  const subSizes = {
    sm: 'text-[9px] tracking-[0.2em]',
    md: 'text-[10px] tracking-[0.24em]',
    lg: 'text-xs tracking-[0.28em]',
  };

  return (
    <Link
      href="/"
      aria-label="Grizo Enterprises Home"
      className={`inline-flex items-center gap-3 group transition-opacity hover:opacity-90 ${className}`}
    >
      {/* Modern original geometric monogram emblem */}
      <div
        className={`relative ${iconSizes[size]} flex items-center justify-center rounded-lg ${
          isLight ? 'bg-white/10 text-white' : 'bg-brand-primary text-white'
        } shadow-sm border ${isLight ? 'border-white/20' : 'border-slate-800'}`}
      >
        <svg
          viewBox="0 0 32 32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-5/6 h-5/6"
          aria-hidden="true"
        >
          {/* Geometric angular 'G' mark */}
          <path
            d="M24 10C22.2 7.6 19.3 6 16 6C10.477 6 6 10.477 6 16C6 21.523 10.477 26 16 26C20.5 26 24.3 23 25.5 19H16V14.5H26V16C26 22 21 27.5 16 27.5C9.648 27.5 4.5 22.351 4.5 16C4.5 9.648 9.648 4.5 16 4.5C19.8 4.5 23.2 6.4 25.2 9.4L24 10Z"
            fill="currentColor"
          />
          {/* Subtle accent vertex */}
          <circle cx="21" cy="14.5" r="2" fill="#0284C7" />
        </svg>
      </div>

      {/* Typography */}
      <div className="flex flex-col">
        <span
          className={`font-bold font-sans tracking-tight leading-none ${titleSizes[size]} ${
            isLight ? 'text-white' : 'text-slate-900'
          }`}
        >
          GRIZO
        </span>
        <span
          className={`font-semibold uppercase ${subSizes[size]} mt-0.5 leading-none ${
            isLight ? 'text-slate-400' : 'text-slate-500'
          }`}
        >
          ENTERPRISES
        </span>
      </div>
    </Link>
  );
}
