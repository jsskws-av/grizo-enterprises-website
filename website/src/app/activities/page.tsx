import React from 'react';
import Link from 'next/link';
import {
  ShoppingBag,
  TrendingUp,
  Truck,
  Calculator,
  FileSpreadsheet,
  LineChart,
  Boxes,
  BarChart3,
  Code2,
  AlertTriangle,
  ArrowRight,
  CheckCircle,
} from 'lucide-react';
import StatusBadge from '@/components/StatusBadge';
import { siteConfig } from '@/config/siteConfig';

export const metadata = {
  title: 'Our Business Activities | Grizo Enterprises',
  description:
    'Detailed overview of the 9 commercial, research, analytical, and software development activities conducted by Grizo Enterprises.',
};

export default function ActivitiesPage() {
  const activities = [
    {
      id: '01',
      title: 'Online Retail and E-Commerce Operations',
      icon: ShoppingBag,
      summary:
        'Managing direct retail merchandising across Indian marketplace channels with an emphasis on catalog accuracy and fulfillment compliance.',
      details: [
        'Curating consumer product offerings aligned with marketplace demand trends.',
        'Ensuring compliant product handling, packaging standards, and timely dispatches via marketplace logistics programs (e.g., Easy Ship / Fulfillment by Amazon).',
        'Maintaining high fulfillment ratings through accurate product representation and responsive customer resolution.',
      ],
      scope: 'Commercial Operation',
    },
    {
      id: '02',
      title: 'Product Category and Market Research',
      icon: TrendingUp,
      summary:
        'Systematic study of market demand, seasonal shifts, customer review sentiments, and category dynamics.',
      details: [
        'Analyzing customer dissatisfaction points in existing market offerings to identify opportunities for improved packaging or features.',
        'Reviewing search volume indications, Best Sellers Rank (BSR) patterns, and category saturation.',
        'Clarification: Research outcomes depend strictly on the availability, accuracy, and reliability of permitted marketplace signals and public data sources.',
      ],
      scope: 'Market Research',
    },
    {
      id: '03',
      title: 'Supplier and Procurement Research',
      icon: Truck,
      summary:
        'Identifying, evaluating, and conducting due diligence on domestic Indian manufacturers and wholesale distributors.',
      details: [
        'Verifying supplier GST credentials, business legitimacy, and production facilities.',
        'Negotiating minimum order quantities (MOQs), sample delivery schedules, and wholesale rate structures.',
        'Conducting physical sample evaluations to verify build quality, packaging resilience, and compliance with statutory labeling rules.',
      ],
      scope: 'Procurement & Logistics',
    },
    {
      id: '04',
      title: 'Product Cost and Profitability Evaluation',
      icon: Calculator,
      summary:
        'Deterministic financial modeling of complete product unit economics prior to capital deployment.',
      details: [
        'Calculating landed costs: supplier unit price, domestic transport, packaging materials, and GST input credits.',
        'Modeling marketplace deduction matrices: referral fees by category, closing fees, weight handling slabs, and storage costs.',
        'Simulating break-even price thresholds and target net margins under variable return rate and promotional scenarios.',
      ],
      scope: 'Financial Modeling',
    },
    {
      id: '05',
      title: 'Product Catalogue and Listing Preparation',
      icon: FileSpreadsheet,
      summary:
        'Creating clear, compliant, and accurate product listings that assist consumer purchasing choices.',
      details: [
        'Drafting titles, informative bullet points, and detailed product descriptions strictly within marketplace character and byte guidelines.',
        'Ensuring compliance with the Legal Metrology (Packaged Commodities) Rules, including manufacturer details, country of origin, net quantity, and maximum retail price (MRP).',
        'Planning multi-angle imagery showing actual product dimensions, materials, and usage scenarios.',
      ],
      scope: 'Listing Governance',
    },
    {
      id: '06',
      title: 'Pricing and Competition Analysis',
      icon: LineChart,
      summary:
        'Monitoring prevailing market price ranges and Buy Box dynamics using authorized and public data.',
      details: [
        'Studying historical price movement trends to understand elasticity across seasonal peaks and regular retail periods.',
        'Establishing strict price floors below which items are not sold, protecting sustainable gross margins and preventing destructive price competition.',
        'Respecting marketplace policies regarding fair pricing and transparent consumer offers.',
      ],
      scope: 'Commercial Strategy',
    },
    {
      id: '07',
      title: 'Inventory and Order Monitoring',
      icon: Boxes,
      summary:
        'Supervising stock levels, reorder triggers, and shipment lifecycles to maintain healthy inventory coverage.',
      details: [
        'Formulating Reorder Points (ROP) combining supplier manufacturing lead time, transit duration, and buffer safety stock.',
        'Tracking fulfillment processing stages from initial order reception through carrier dispatch and delivery confirmation.',
        'Managing storage aging and inventory velocity to avoid redundant holding fees or unexpected stockouts.',
      ],
      scope: 'Inventory Operations',
    },
    {
      id: '08',
      title: 'Sales Performance Reporting',
      icon: BarChart3,
      summary:
        'Aggregating periodic internal operational summaries to evaluate SKU performance and working capital allocation.',
      details: [
        'Consolidating sales volume, return rates, customer feedback, and advertising spend into structured internal reports.',
        'Identifying underperforming SKUs for timely clearance and top-performing lines for inventory replenishment.',
        'Presenting clear data summaries to support human managerial decisions.',
      ],
      scope: 'Executive Reporting',
    },
    {
      id: '09',
      title: 'Internal Software and Workflow Development',
      icon: Code2,
      summary:
        'Engineering custom software tooling and AI-assisted workflows within Google Antigravity for internal business administration.',
      details: [
        'Building computational modules that automate financial formula calculations, search term verification, and alert generation.',
        'Developing prototype integrations intended to interface with authorized marketplace APIs (such as Amazon SP-API) upon formal review and authorization.',
        'Engineering strict internal governance: isolating draft data from production and maintaining mandatory human approval gates.',
      ],
      scope: 'Internal Technology',
    },
  ];

  return (
    <div className="py-12 sm:py-16 lg:py-20 space-y-16 lg:space-y-24">
      {/* Header */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl space-y-4">
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
              Operational Scope
            </span>
            <StatusBadge />
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 tracking-tight">
            Our Business Activities
          </h1>
          <p className="text-lg text-slate-600 leading-relaxed">
            Grizo Enterprises engages in online retail, rigorous market research, financial modeling, and proprietary internal software development for its own Amazon seller operations.
          </p>
        </div>
      </section>

      {/* Disclaimers & Realistic Scope Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-6 sm:p-7 flex items-start gap-4">
          <AlertTriangle className="w-5 h-5 text-amber-700 flex-shrink-0 mt-0.5" aria-hidden="true" />
          <div className="space-y-2 text-xs sm:text-sm text-amber-950 leading-relaxed">
            <p className="font-semibold text-amber-900">
              Commercial Research & Operational Disclosures
            </p>
            <p>
              1. <strong>Data Dependency:</strong> All research, pricing observations, and market indicators depend strictly upon the availability, completeness, and accuracy of permitted public and authorized data sources.
            </p>
            <p>
              2. <strong>No Commercial Guarantees:</strong> Grizo Enterprises does not assert or claim guaranteed product demand, guaranteed profit margins, or assured sales performance. All commercial ventures carry inherent market and consumer preference risks.
            </p>
            <p>
              3. <strong>Internal Use Only:</strong> Our analytical and software activities are undertaken exclusively for Grizo Enterprises&apos; own retail management. We do not provide public consulting, retail agency services, or third-party account management.
            </p>
          </div>
        </div>
      </section>

      {/* 9 Activities Detailed List */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="space-y-8">
          {activities.map((act) => {
            const Icon = act.icon;
            return (
              <div
                key={act.id}
                className="corp-card p-6 sm:p-8 lg:p-10 border border-slate-200"
              >
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-start">
                  {/* Left Column: Number & Icon */}
                  <div className="lg:col-span-4 space-y-4">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-xl bg-slate-900 text-white flex items-center justify-center font-bold text-base shadow-xs">
                        {act.id}
                      </div>
                      <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 border border-slate-200">
                        {act.scope}
                      </span>
                    </div>
                    <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
                      {act.title}
                    </h2>
                    <p className="text-sm text-slate-600 leading-relaxed">
                      {act.summary}
                    </p>
                  </div>

                  {/* Right Column: Detailed points */}
                  <div className="lg:col-span-8 bg-slate-50/70 border border-slate-200/80 rounded-xl p-5 sm:p-6">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
                      Operational Workflow & Scope
                    </h3>
                    <ul className="space-y-3">
                      {act.details.map((detail, idx) => (
                        <li key={idx} className="flex items-start gap-3 text-sm text-slate-700 leading-relaxed">
                          <CheckCircle className="w-4 h-4 text-brand-accent flex-shrink-0 mt-1" aria-hidden="true" />
                          <span>{detail}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Transition to Technology Page */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-900 text-white rounded-2xl p-8 sm:p-12 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <h2 className="text-2xl font-bold tracking-tight">
              Curious About How We Support These Activities With Technology?
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Read about the internal software application and AI-assisted workflows we are currently developing in Google Antigravity.
            </p>
          </div>
          <Link
            href="/technology"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-semibold text-slate-900 bg-white hover:bg-slate-100 transition-colors whitespace-nowrap shadow-sm"
          >
            <span>Technology Overview</span>
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </Link>
        </div>
      </section>
    </div>
  );
}
