import React from 'react';
import Link from 'next/link';
import { Home, ArrowLeft, HelpCircle } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 sm:px-6 lg:px-8 py-16 bg-slate-50">
      <div className="max-w-md w-full text-center space-y-6 bg-white p-8 sm:p-10 rounded-2xl border border-slate-200 shadow-sm">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 text-slate-700">
          <HelpCircle className="w-8 h-8 text-brand-accent" aria-hidden="true" />
        </div>

        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Error 404
          </span>
          <h1 className="mt-1 text-2xl font-bold text-slate-900 tracking-tight">
            Page Not Found
          </h1>
          <p className="mt-2 text-sm text-slate-600 leading-relaxed">
            The page you are looking for does not exist or may have been relocated within our website directory.
          </p>
        </div>

        <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            href="/"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg text-sm font-semibold text-white bg-slate-900 hover:bg-slate-800 transition-colors shadow-xs"
          >
            <Home className="w-4 h-4" aria-hidden="true" />
            <span>Return to Home</span>
          </Link>
          <Link
            href="/contact"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" aria-hidden="true" />
            <span>Contact Support</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
