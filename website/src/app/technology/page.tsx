import React from 'react';
import Link from 'next/link';
import {
  Cpu,
  Search,
  Calculator,
  FileEdit,
  Layers,
  BarChart,
  UserCheck,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Database,
  ShieldAlert,
  GitBranch,
} from 'lucide-react';
import StatusBadge from '@/components/StatusBadge';
import { siteConfig } from '@/config/siteConfig';

export const metadata = {
  title: 'Technology-Enabled E-Commerce Operations | Grizo Enterprises',
  description:
    'Overview of Grizo Enterprises internal e-commerce management software and AI-assisted workflows being developed in Google Antigravity.',
};

export default function TechnologyPage() {
  const sections = [
    {
      letter: 'A',
      title: 'Product Opportunity Research',
      icon: Search,
      badge: 'Analytical Discovery',
      description:
        'The internal application is designed to systematically evaluate potential consumer product opportunities using permitted signals and public marketplace data.',
      capabilities: [
        'Aggregating indicators of customer demand, including historical category rank and seasonal spikes.',
        'Reviewing price distributions, customer review counts, and common consumer pain points within candidate niches.',
        'Evaluating product compliance parameters against Indian legal frameworks (e.g., Legal Metrology and BIS standards).',
      ],
      caution:
        'All research results are treated as directional indicators rather than verified purchase commitments.',
    },
    {
      letter: 'B',
      title: 'Profitability & Unit Economics Analysis',
      icon: Calculator,
      badge: 'Deterministic Math',
      description:
        'The software incorporates an explicit, deterministic mathematical engine to calculate projected margins before any inventory investment.',
      inputs: [
        'Product procurement cost (quoted by verified domestic manufacturers)',
        'Applicable Goods & Services Tax (GST) rates (5%, 12%, or 18% with input tax credits)',
        'Marketplace category referral fees and closing fee slabs',
        'Fulfillment & logistics fees (Easy Ship / FBA weight handling and pick-and-pack charges)',
        'Protective packaging, labeling, and domestic transport expenses',
        'Estimated return rate allowances and return processing costs',
        'Advertising and promotional budget allocations',
      ],
      caution:
        'Profitability outputs are computational estimates that depend strictly on the completeness and accuracy of the underlying business inputs and rate schedules.',
    },
    {
      letter: 'C',
      title: 'Listing Support & Catalogue Content',
      icon: FileEdit,
      badge: 'Content Assistance',
      description:
        'Assisting the business in drafting structured, compliant, and accurate product listings aligned with marketplace style guides.',
      capabilities: [
        'Drafting clear, factual product titles adhering to marketplace character restrictions.',
        'Compiling 5 benefit-driven bullet points highlighting true physical product specifications.',
        'Structuring required backend attributes, search terms, and mandatory legal metrology declarations.',
      ],
      caution:
        'All AI-assisted drafted content is subject to mandatory human editorial review prior to catalogue submission.',
    },
    {
      letter: 'D',
      title: 'Inventory & Stock Monitoring',
      icon: Layers,
      badge: 'Supply Chain Sync',
      description:
        'The application is intended to monitor available inventory, sales velocity, and stock replenishment triggers where authorized marketplace API permissions are granted.',
      capabilities: [
        'Calculating formulaic Reorder Points: ROP = (Daily Velocity × Lead Time) + Safety Stock buffer.',
        'Flagging aging stock to prevent excessive long-term storage fees.',
        'Generating low-stock warnings to avoid disruptive stockouts during peak demand cycles.',
      ],
      caution:
        'Live inventory synchronization is contingent upon official marketplace API registration, authorization, and technical implementation.',
    },
    {
      letter: 'E',
      title: 'Operational Reporting & Executive Briefings',
      icon: BarChart,
      badge: 'Business Intelligence',
      description:
        'Generating structured periodic summaries of inventory status, operational expenses, returns, and sales metrics.',
      capabilities: [
        'Consolidating key operational metrics into clean, actionable dashboards.',
        'Providing unit margin variance reports comparing projected economics against actual settlement reports.',
        'Highlighting operational anomalies such as sudden return surges or unexpected fee deductions.',
      ],
      caution:
        'Reports reflect aggregated internal records and authorized data feeds, designed for internal managerial review.',
    },
  ];

  return (
    <div className="py-12 sm:py-16 lg:py-20 space-y-16 lg:space-y-24">
      {/* Page Header */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
              Internal Software Development
            </span>
            <StatusBadge />
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 tracking-tight">
            Technology-Enabled E-Commerce Operations
          </h1>
          <p className="text-lg text-slate-600 leading-relaxed">
            Grizo Enterprises is developing an internal software application within Google Antigravity to support data-informed research, financial modeling, and operational management for our Amazon India seller business.
          </p>
        </div>
      </section>

      {/* Prominent Development Status Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-amber-50/80 border border-amber-300/80 rounded-2xl p-6 sm:p-8 space-y-3">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-700" aria-hidden="true" />
            <h2 className="text-base font-bold text-amber-950">
              Application Development Status Notice
            </h2>
          </div>
          <p className="text-sm text-amber-900 leading-relaxed">
            {siteConfig.application.statusNote}
          </p>
          <div className="text-xs text-amber-800 pt-2 flex flex-wrap gap-4 border-t border-amber-200">
            <span>• Environment: {siteConfig.business.techEnvironment}</span>
            <span>• Purpose: Internal Operations Only</span>
            <span>• Commercial SaaS Availability: None (Not a public product)</span>
            <span>• Live Marketplace Status: Pending Authorization & Developer Registration</span>
          </div>
        </div>
      </section>

      {/* Section F: Human Approval Governance (Prominently Featured) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-900 text-white rounded-2xl p-8 sm:p-10 lg:p-12 space-y-6">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-sky-400">
            <UserCheck className="w-4 h-4" aria-hidden="true" />
            <span>Human-in-the-Loop Governance</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">
            Section F: Mandatory Human Approval for Commercial Commitments
          </h2>
          <div className="space-y-4 text-slate-300 text-sm sm:text-base leading-relaxed max-w-4xl">
            <p>
              We firmly reject fully autonomous execution for critical business actions. The internal application serves purely as an advisory and analytical assistant. All important commercial decisions require explicit, documented human verification by the business proprietor:
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-4">
              <div className="p-4 rounded-xl bg-slate-800 border border-slate-700 space-y-2">
                <span className="text-xs font-bold text-sky-400">Gate 01</span>
                <h4 className="text-sm font-semibold text-white">Inventory Purchasing</h4>
                <p className="text-xs text-slate-400">
                  Placing purchase orders or allocating working capital to suppliers.
                </p>
              </div>
              <div className="p-4 rounded-xl bg-slate-800 border border-slate-700 space-y-2">
                <span className="text-xs font-bold text-sky-400">Gate 02</span>
                <h4 className="text-sm font-semibold text-white">Financial Commitments</h4>
                <p className="text-xs text-slate-400">
                  Authorizing supplier disbursements, freight invoices, or advertising budgets.
                </p>
              </div>
              <div className="p-4 rounded-xl bg-slate-800 border border-slate-700 space-y-2">
                <span className="text-xs font-bold text-sky-400">Gate 03</span>
                <h4 className="text-sm font-semibold text-white">Catalogue Publishing</h4>
                <p className="text-xs text-slate-400">
                  Publishing or modifying product titles, specifications, and legal declarations.
                </p>
              </div>
              <div className="p-4 rounded-xl bg-slate-800 border border-slate-700 space-y-2">
                <span className="text-xs font-bold text-sky-400">Gate 04</span>
                <h4 className="text-sm font-semibold text-white">Pricing Adjustments</h4>
                <p className="text-xs text-slate-400">
                  Adjusting marketplace consumer selling prices or floor margins.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sections A to E: Core Capabilities */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
            Application Functional Modules
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Intended Functional Capabilities
          </h2>
          <p className="text-sm text-slate-600 max-w-2xl">
            Detailed breakdown of modules designed to support our Amazon India operations upon completion and authorization.
          </p>
        </div>

        <div className="space-y-8">
          {sections.map((sec) => {
            const Icon = sec.icon;
            return (
              <div
                key={sec.letter}
                className="corp-card p-6 sm:p-8 lg:p-10 border border-slate-200"
              >
                <div className="space-y-6">
                  {/* Top Bar */}
                  <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-slate-100 text-slate-900 flex items-center justify-center font-bold text-sm">
                        {sec.letter}
                      </div>
                      <div>
                        <span className="text-xs font-semibold px-2 py-0.5 rounded bg-sky-50 text-sky-800 border border-sky-200">
                          {sec.badge}
                        </span>
                        <h3 className="text-xl font-bold text-slate-900 tracking-tight mt-1">
                          {sec.title}
                        </h3>
                      </div>
                    </div>
                  </div>

                  <p className="text-sm sm:text-base text-slate-700 leading-relaxed">
                    {sec.description}
                  </p>

                  {/* Capabilities List if present */}
                  {sec.capabilities && (
                    <div className="space-y-2.5 bg-slate-50 p-5 rounded-xl border border-slate-200/80">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                        Intended Scope of Functionality:
                      </h4>
                      <ul className="space-y-2">
                        {sec.capabilities.map((item, idx) => (
                          <li key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-700">
                            <CheckCircle2 className="w-4 h-4 text-brand-accent flex-shrink-0 mt-0.5" aria-hidden="true" />
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Inputs List for Profitability */}
                  {sec.inputs && (
                    <div className="space-y-2.5 bg-slate-50 p-5 rounded-xl border border-slate-200/80">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                        Explicit Computational Inputs & Fee Formulas:
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                        {sec.inputs.map((input, idx) => (
                          <div key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-slate-700">
                            <span className="text-brand-accent font-bold">•</span>
                            <span>{input}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Caution / Grounding Note */}
                  <div className="p-3.5 rounded-lg bg-amber-50/60 border border-amber-200 text-xs text-amber-900 flex items-start gap-2.5">
                    <AlertTriangle className="w-4 h-4 text-amber-700 flex-shrink-0 mt-0.5" aria-hidden="true" />
                    <span>
                      <strong>Grounding Note:</strong> {sec.caution}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Section G: Data Accuracy & Provenance */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="corp-card p-6 sm:p-8 lg:p-10 border-2 border-slate-200 space-y-6">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-brand-accent">
            <ShieldAlert className="w-4 h-4" aria-hidden="true" />
            <span>Data Integrity Standard</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Section G: Data Accuracy, Classification, and Evidence Provenance
          </h2>
          <p className="text-sm sm:text-base text-slate-600 leading-relaxed">
            To ensure complete truthfulness and prevent deceptive modeling, our internal architecture enforces rigorous categorization of all data points. Every metric handled by our systems is explicitly tagged under one of four distinct classes:
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
            <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
                  Category 1: Authorized Official Sources
                </span>
                <span className="text-xs px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded font-semibold">
                  Verified Fact
                </span>
              </div>
              <h4 className="text-base font-bold text-slate-900">Official Data Feeds</h4>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Direct statutory information, GST invoices from verified suppliers, official marketplace fee schedules, and data retrieved via authorized developer APIs with seller consent.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-amber-700">
                  Category 2: Third-Party Market Estimates
                </span>
                <span className="text-xs px-2 py-0.5 bg-amber-100 text-amber-800 rounded font-semibold">
                  Estimated Signal
                </span>
              </div>
              <h4 className="text-base font-bold text-slate-900">Third-Party Market Estimates</h4>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Aggregated search trends, estimated sales curves, and category popularity indicators derived from permitted public sources. <em>Never represented as verified sales figures.</em>
              </p>
            </div>

            <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-blue-700">
                  Category 3: Calculated Financial Estimates
                </span>
                <span className="text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded font-semibold">
                  Mathematical Output
                </span>
              </div>
              <h4 className="text-base font-bold text-slate-900">Calculated Projections</h4>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Outputs from mathematical models determining break-even prices, net margins, return provisions, and inventory reorder points based on user-supplied variables.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-purple-700">
                  Category 4: AI-Generated Drafts
                </span>
                <span className="text-xs px-2 py-0.5 bg-purple-100 text-purple-800 rounded font-semibold">
                  Hypothesis / Draft
                </span>
              </div>
              <h4 className="text-base font-bold text-slate-900">Assisted Recommendations</h4>
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Draft titles, bullet points, customer feedback summaries, and keyword suggestions generated through language models. Stored exclusively as proposals requiring human verification.
              </p>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-900 leading-relaxed font-medium">
            <strong>Strict Truthfulness Rule:</strong> Grizo Enterprises never presents estimated competitor sales as verified Amazon sales figures. Inquiries and internal deliberations clearly maintain the demarcation between verified facts and computational hypotheses.
          </div>
        </div>
      </section>

      {/* Link to Integrations */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-t border-slate-200 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-600">
            For specific disclosures regarding Amazon Selling Partner API (SP-API) usage:
          </p>
          <Link
            href="/marketplace-integrations"
            className="inline-flex items-center gap-2 text-sm font-semibold text-brand-accent hover:text-brand-accentHover"
          >
            <span>Read Marketplace Integrations & Data Use Disclosure</span>
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </Link>
        </div>
      </section>
    </div>
  );
}
