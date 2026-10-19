import React from 'react';
import Link from 'next/link';
import {
  ShieldCheck,
  Lock,
  FileCheck,
  AlertOctagon,
  CheckCircle2,
  HelpCircle,
  ExternalLink,
  ArrowRight,
  Database,
} from 'lucide-react';
import StatusBadge from '@/components/StatusBadge';
import { siteConfig } from '@/config/siteConfig';

export const metadata = {
  title: 'Marketplace Integrations and Data Use | Grizo Enterprises',
  description:
    'Official disclosure regarding Grizo Enterprises planned use of marketplace APIs, including the Amazon Selling Partner API (SP-API), data governance, and non-affiliation statements.',
};

export default function MarketplaceIntegrationsPage() {
  return (
    <div className="py-12 sm:py-16 lg:py-20 space-y-16 lg:space-y-24">
      {/* Header */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
              Regulatory & Developer Disclosure
            </span>
            <StatusBadge />
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 tracking-tight">
            Marketplace Integrations and Data Use
          </h1>
          <p className="text-lg text-slate-600 leading-relaxed">
            Transparent disclosure of our integration objectives, planned application architecture, data governance principles, and strict non-affiliation statements.
          </p>
        </div>
      </section>

      {/* Mandatory Statutory Statement Card */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-900 text-white rounded-2xl p-8 sm:p-10 lg:p-12 space-y-6 shadow-sm">
          <h2 className="text-xs font-bold uppercase tracking-wider text-sky-400">
            Official Organization Statement
          </h2>
          <div className="space-y-4 text-slate-200 text-base sm:text-lg leading-relaxed">
            <p>
              Grizo Enterprises is developing an internal software application to support its own e-commerce operations. Where approved and available, the application is intended to use authorised marketplace APIs to access relevant business information and support eligible operational workflows.
            </p>
            <p className="text-sky-200">
              Any use of Amazon Selling Partner APIs is subject to Amazon’s registration requirements, applicable permissions, contractual terms, and data protection policies. The development and availability of specific integrations depend on approval, authorisation, and implementation.
            </p>
          </div>
          <div className="pt-4 border-t border-slate-800 flex flex-wrap gap-4 text-xs text-slate-400">
            <span>• Registration Status: In Developer Registration Preparation</span>
            <span>• System Nature: Private Internal Application</span>
            <span>• User Base: Grizo Enterprises Sole Proprietorship</span>
          </div>
        </div>
      </section>

      {/* Explicit Non-Affiliation and Trademark Notice */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="corp-card p-6 sm:p-8 lg:p-10 border-2 border-slate-200 space-y-6">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500">
            <AlertOctagon className="w-4 h-4 text-amber-600" aria-hidden="true" />
            <span>Independence & Trademark Notice</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Commercial Independence & Non-Affiliation Statement
          </h2>
          <div className="space-y-4 text-sm sm:text-base text-slate-700 leading-relaxed">
            <p>
              To maintain complete transparency for marketplace reviewers, customers, and business contacts, Grizo Enterprises states unequivocally:
            </p>
            <ul className="space-y-3 pt-2">
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
                <span>
                  <strong>Independent Commercial Entity:</strong> Grizo Enterprises is an independent Indian sole proprietorship. The business is not a subsidiary, joint venture, partner, or commercial representative of Amazon.com, Inc., Amazon Seller Services Private Limited, or any of their affiliates.
                </span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
                <span>
                  <strong>No Claims of Certification:</strong> Grizo Enterprises does not claim to be an &ldquo;Amazon Certified Partner,&rdquo; &ldquo;Official Amazon Developer,&rdquo; or endorsed by Amazon in any capacity.
                </span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
                <span>
                  <strong>Trademark Ownership:</strong> Amazon, Amazon India, Selling Partner API (SP-API), Amazon.in, and all associated logos, designs, and product badges are trademarks or registered trademarks of Amazon.com, Inc. or its affiliates. Their mention on this website is descriptive and identifies external services with which our internal software is engineered to interface.
                </span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Intended API Usage & Scope */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="space-y-8">
          <div className="space-y-2">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
              Architectural Intent
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Intended Selling Partner API Scope
            </h2>
            <p className="text-sm text-slate-600 max-w-2xl">
              Where permissions are granted by Amazon, the internal application is planned to interact with the following API roles solely for our own account operations:
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-lg bg-sky-50 text-brand-accent flex items-center justify-center font-bold">
                01
              </div>
              <h3 className="text-base font-bold text-slate-900">Listings & Catalogue Feeds</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Interfacing with Listings Items APIs and Feeds APIs to publish, update, and audit product attributes, bullet points, and pricing for Grizo Enterprises&apos; own catalogue.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-lg bg-sky-50 text-brand-accent flex items-center justify-center font-bold">
                02
              </div>
              <h3 className="text-base font-bold text-slate-900">Orders & Fulfillment Tracking</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Reading order fulfillment statuses to verify prompt shipment handling and monitor delivery milestones via Easy Ship or FBA networks.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-lg bg-sky-50 text-brand-accent flex items-center justify-center font-bold">
                03
              </div>
              <h3 className="text-base font-bold text-slate-900">FBA & Inventory Synchronisation</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Retrieving real-time inventory counts and inbound shipment reconciliations to maintain timely replenishment schedules and prevent stockouts.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-lg bg-sky-50 text-brand-accent flex items-center justify-center font-bold">
                04
              </div>
              <h3 className="text-base font-bold text-slate-900">Pricing & Product Fees</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Querying Product Pricing APIs and My Fees Estimate APIs to verify accurate referral fee and closing fee schedules for deterministic unit economics.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-lg bg-sky-50 text-brand-accent flex items-center justify-center font-bold">
                05
              </div>
              <h3 className="text-base font-bold text-slate-900">Financial Events & Settlement</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Ingesting Finances API settlement reports to reconcile actual marketplace fee withholdings, GST withholdings (TCS/TDS), and final disbursement figures.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3">
              <div className="w-10 h-10 rounded-lg bg-sky-50 text-brand-accent flex items-center justify-center font-bold">
                06
              </div>
              <h3 className="text-base font-bold text-slate-900">Periodic Reporting & Analytics</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Requesting scheduled sales and traffic reports via Reports APIs to produce internal executive briefings for Grizo Enterprises management.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Data Protection & Governance Commitments */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-8 sm:p-10 space-y-6">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-brand-accent">
            <Lock className="w-4 h-4" aria-hidden="true" />
            <span>Security & Data Governance</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Data Governance Commitments
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-slate-700">
            <div className="space-y-2">
              <h3 className="font-bold text-slate-900">Authorized Purpose Only</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Access to marketplace API information will be strictly limited to legitimate business operations of Grizo Enterprises. Information will never be accessed for unauthorized exploratory purposes.
              </p>
            </div>

            <div className="space-y-2">
              <h3 className="font-bold text-slate-900">Zero Third-Party Data Monetization</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Grizo Enterprises will never intentionally misuse, sell, trade, rent, or improperly disclose protected marketplace information or customer data to third-party data brokers or marketing platforms.
              </p>
            </div>

            <div className="space-y-2">
              <h3 className="font-bold text-slate-900">Secure Architecture & Isolation</h3>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                All API keys, refresh tokens, and operational records are isolated from client-side public code and protected via server-side encryption with strict principle-of-least-privilege access.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Bottom Link */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-slate-200 pt-6">
          <p className="text-sm text-slate-600">
            Review how data is handled across our web properties:
          </p>
          <Link
            href="/privacy-policy"
            className="inline-flex items-center gap-2 text-sm font-semibold text-brand-accent hover:text-brand-accentHover"
          >
            <span>Review Privacy Policy</span>
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </Link>
        </div>
      </section>
    </div>
  );
}
