import React from 'react';
import Link from 'next/link';
import {
  ShoppingBag,
  TrendingUp,
  Calculator,
  FileText,
  Boxes,
  Code2,
  ShieldCheck,
  ArrowRight,
  Database,
  Cpu,
  CheckCircle2,
  AlertCircle,
  Eye,
  SlidersHorizontal,
} from 'lucide-react';
import StatusBadge from '@/components/StatusBadge';
import { siteConfig } from '@/config/siteConfig';

export const metadata = {
  title: 'Grizo Enterprises | Smarter Commerce. Better Decisions.',
  description:
    'Grizo Enterprises is an India-based sole proprietorship focused on e-commerce, online retail, and the development of internal technology workflows for operational management.',
};

export default function HomePage() {
  const activities = [
    {
      title: 'E-commerce & Online Retail',
      icon: ShoppingBag,
      description:
        'Active retail operations across major Indian online marketplaces, with a primary focus on consumer goods, compliant catalogue maintenance, and customer-first fulfillment.',
      tag: 'Core Commerce',
    },
    {
      title: 'Product & Market Research',
      icon: TrendingUp,
      description:
        'Systematic evaluation of market demand, seasonal shifts, customer feedback patterns, and category dynamics using permitted industry data sources.',
      tag: 'Market Intelligence',
    },
    {
      title: 'Pricing & Profitability Analysis',
      icon: Calculator,
      description:
        'Deterministic financial modeling factoring in supplier costs, applicable GST rates, platform referral fees, shipping logistics, and packaging expenses.',
      tag: 'Financial Discipline',
    },
    {
      title: 'Product Listing Management',
      icon: FileText,
      description:
        'Structured catalogue curation, compliant title construction, benefit-driven bullet points, and adherence to marketplace legal metrology guidelines.',
      tag: 'Catalogue Operations',
    },
    {
      title: 'Inventory & Sales Monitoring',
      icon: Boxes,
      description:
        'Ongoing tracking of replenishment levels, lead-time planning, safety stock thresholds, and stock turn velocity to reduce holding risk.',
      tag: 'Supply Chain',
    },
    {
      title: 'Internal Software Development',
      icon: Code2,
      description:
        'Engineering internal tools and AI-assisted workflows within Google Antigravity to streamline analytical workflows for our own seller accounts.',
      tag: 'Automation Lab',
    },
  ];

  const techFeatures = [
    {
      title: 'Product Opportunity Research',
      desc: 'Evaluating catalog gaps and demand indicators based on permitted data points and category insights.',
    },
    {
      title: 'Competitor & Price Analysis',
      desc: 'Benchmarking price trends and review moats using publicly accessible and authorized marketplace data.',
    },
    {
      title: 'Cost & Profit Calculations',
      desc: 'Formula-based calculations of net margins, return on investment (ROI), and break-even pricing floors.',
    },
    {
      title: 'Listing Content Preparation',
      desc: 'Drafting structured product specifications, descriptions, and backend search terms aligned with marketplace rules.',
    },
    {
      title: 'Inventory & Stock Monitoring',
      desc: 'Assisting in calculating reorder points and monitoring stock coverage where API permissions permit.',
    },
    {
      title: 'Sales & Operational Reporting',
      desc: 'Aggregating periodic performance summaries and critical operational alerts for human business review.',
    },
  ];

  return (
    <div className="space-y-20 lg:space-y-28 pb-20">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-50 via-white to-white border-b border-slate-200/80 pt-16 pb-20 lg:pt-24 lg:pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl space-y-6">
            {/* Business Status Pill */}
            <div className="flex flex-wrap items-center gap-3">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-200">
                GST-Registered Sole Proprietorship • India
              </span>
              <StatusBadge />
            </div>

            {/* Main Heading */}
            <div className="space-y-2">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-950 tracking-tight leading-[1.1]">
                Grizo Enterprises
              </h1>
              <p className="text-xl sm:text-2xl font-semibold text-brand-accent tracking-tight">
                {siteConfig.business.tagline}
              </p>
            </div>

            {/* Factual Description */}
            <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl">
              Grizo Enterprises is an India-based sole proprietorship focused on e-commerce and online retail. We are developing technology-enabled workflows to support product research, market analysis, pricing decisions, listing management, and inventory planning.
            </p>

            {/* CTAs */}
            <div className="pt-4 flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5">
              <Link
                href="/activities"
                className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg text-sm font-semibold text-white bg-slate-900 hover:bg-slate-800 transition-colors shadow-sm"
              >
                <span>Explore Our Business</span>
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </Link>
              <Link
                href="/contact"
                className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg text-sm font-semibold text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 hover:text-slate-900 transition-colors shadow-xs"
              >
                <span>Contact Us</span>
              </Link>
            </div>

            {/* Verified Entity Context Banner */}
            <div className="pt-8 border-t border-slate-200 grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs text-slate-600">
              <div>
                <span className="block text-slate-400 font-medium">Business Structure</span>
                <strong className="text-slate-800 text-sm font-semibold">Sole Proprietorship</strong>
              </div>
              <div>
                <span className="block text-slate-400 font-medium">Country of Origin</span>
                <strong className="text-slate-800 text-sm font-semibold">India (GST Registered)</strong>
              </div>
              <div className="col-span-2 sm:col-span-1">
                <span className="block text-slate-400 font-medium">Market Focus</span>
                <strong className="text-slate-800 text-sm font-semibold">Amazon India (amazon.in)</strong>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Business Overview Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-6 space-y-5">
            <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-brand-accent">
              <ShieldCheck className="w-4 h-4" aria-hidden="true" />
              <span>Who We Are</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight leading-tight">
              A Disciplined Approach to Indian E-Commerce
            </h2>
            <div className="space-y-4 text-slate-600 text-sm sm:text-base leading-relaxed">
              <p>
                Grizo Enterprises is an independent commercial sole proprietorship based in India, registered under the Goods and Services Tax (GST) framework. Our core enterprise focuses on managing online retail operations, identifying viable commercial goods, and fulfilling consumer needs with operational efficiency.
              </p>
              <p>
                Rather than relying on ungrounded intuition, we approach online selling through structured analytical methods. We systematically assess commercial demand, supplier viability, product compliance under Indian legal frameworks, and full unit economics before bringing products to market.
              </p>
              <p>
                To support and scale these operations, we are engineering proprietary internal software workflows within Google Antigravity. This tooling is developed exclusively for our own internal business management, ensuring every inventory and pricing commitment is backed by rigorous data analysis.
              </p>
            </div>
            <div className="pt-2">
              <Link
                href="/about"
                className="inline-flex items-center gap-2 text-sm font-semibold text-brand-accent hover:text-brand-accentHover"
              >
                <span>Read our full organizational profile</span>
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </Link>
            </div>
          </div>

          <div className="lg:col-span-6">
            <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 sm:p-8 space-y-6">
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Cpu className="w-5 h-5 text-brand-accent" aria-hidden="true" />
                <span>Foundational Principles</span>
              </h3>
              <ul className="space-y-4 text-sm text-slate-700">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <div>
                    <strong className="text-slate-900 font-semibold">GST Compliance & Legitimacy:</strong> All purchasing, commercial invoicing, and sales transactions strictly adhere to Indian commercial tax and statutory invoicing mandates.
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <div>
                    <strong className="text-slate-900 font-semibold">Data-Informed Decisions:</strong> We evaluate unit economics with mathematical models rather than arbitrary projections or unverified sales estimates.
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <div>
                    <strong className="text-slate-900 font-semibold">Human Governance:</strong> Technology assists with research and drafting; critical decisions such as inventory purchases and contractual terms always require explicit human verification.
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <div>
                    <strong className="text-slate-900 font-semibold">Strict Marketplace Policy Adherence:</strong> We honor marketplace policies, data security guidelines, and intellectual property requirements across all partner channels.
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Business Activities Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12 lg:mb-16 space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
            Core Scope of Operations
          </span>
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight">
            Our Business Activities
          </h2>
          <p className="text-sm sm:text-base text-slate-600">
            A comprehensive overview of the daily commercial, analytical, and technological functions undertaken by Grizo Enterprises.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {activities.map((act, index) => {
            const Icon = act.icon;
            return (
              <div
                key={index}
                className="corp-card p-6 sm:p-7 flex flex-col justify-between space-y-4"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center text-slate-800">
                      <Icon className="w-6 h-6 text-brand-accent" aria-hidden="true" />
                    </div>
                    <span className="text-xs font-medium px-2.5 py-1 rounded bg-slate-100 text-slate-600 border border-slate-200">
                      {act.tag}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 tracking-tight">
                    {act.title}
                  </h3>
                  <p className="text-sm text-slate-600 leading-relaxed">
                    {act.description}
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 text-xs text-slate-500">
                  Operated for Grizo Enterprises internal business
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-8 text-center">
          <Link
            href="/activities"
            className="inline-flex items-center gap-2 text-sm font-semibold text-slate-900 hover:text-brand-accent transition-colors"
          >
            <span>View detailed operational descriptions across all 9 activities</span>
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </Link>
        </div>
      </section>

      {/* Technology & Automation Section */}
      <section className="bg-slate-900 text-white py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl space-y-4 mb-12">
            <div className="flex items-center gap-3">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-sky-950 text-sky-300 border border-sky-800">
                Technology Development Initiative
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-amber-900/60 text-amber-200 border border-amber-700/60">
                Status: In Active Engineering
              </span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-white">
              Internal E-Commerce Automation & Analysis
            </h2>
            <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
              To support our own Amazon India seller account, Grizo Enterprises is actively designing and building an internal software suite. The objective is to automate labor-intensive research, standardize margin calculations, and provide operational alerts.
            </p>
            <p className="text-xs text-slate-400 italic">
              Note: This internal software application is currently under development and is engineered strictly for our own internal business operations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {techFeatures.map((item, idx) => (
              <div
                key={idx}
                className="p-6 rounded-xl bg-slate-800/80 border border-slate-700/80 space-y-3 hover:border-slate-600 transition-colors"
              >
                <div className="text-xs font-bold text-sky-400">0{idx + 1}.</div>
                <h3 className="text-base font-semibold text-white">{item.title}</h3>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  {item.desc}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-12 p-6 rounded-xl bg-slate-800/50 border border-slate-700 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
            <div className="space-y-1">
              <h4 className="text-sm font-semibold text-white">
                Marketplace API Integration Notice
              </h4>
              <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
                Planned connections to the Amazon Selling Partner API (SP-API) are subject to official Amazon developer registration, technical review, and strict data governance policies.
              </p>
            </div>
            <Link
              href="/marketplace-integrations"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold text-slate-900 bg-white hover:bg-slate-100 transition-colors whitespace-nowrap"
            >
              <span>Review API Disclosures</span>
              <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>

      {/* Responsible Technology Statement */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-r from-sky-50 via-slate-50 to-slate-50 border border-sky-100 rounded-2xl p-8 sm:p-10 space-y-6">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-brand-accent">
            <SlidersHorizontal className="w-4 h-4" aria-hidden="true" />
            <span>Operational Governance</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Responsible Technology Statement
          </h2>
          <div className="space-y-4 text-slate-700 text-sm sm:text-base leading-relaxed">
            <p>
              At Grizo Enterprises, technology and computational assistants exist to inform decisions, not replace human judgment. While our internal application evaluates data points, generates copy drafts, and calculates financial scenarios, all substantial commercial commitments remain under direct human control.
            </p>
            <p>
              Specifically, placing inventory purchase orders with suppliers, executing monetary disbursements, committing to advertising expenditure, and publishing major catalogue or pricing revisions require explicit verification and sign-off by the business proprietor.
            </p>
            <p>
              We firmly distinguish between empirical facts (such as direct supplier quotations or verified platform fees) and probabilistic estimates (such as estimated category demand). We do not treat automated models as guarantees of commercial results.
            </p>
          </div>
          <div className="pt-2 flex flex-wrap gap-4 text-xs font-medium text-slate-600">
            <span className="inline-flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" aria-hidden="true" />
              Human-in-the-Loop Approval Required
            </span>
            <span className="inline-flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" aria-hidden="true" />
              Formulaic Margin Verification
            </span>
            <span className="inline-flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" aria-hidden="true" />
              Zero Autonomous Financial Commitments
            </span>
          </div>
        </div>
      </section>

      {/* Final Inquiry Call to Action */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
        <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
          Interested in Collaborating or Learning More?
        </h2>
        <p className="text-sm sm:text-base text-slate-600 max-w-xl mx-auto">
          We welcome inquiries from verified product manufacturers, trade partners, and platform representatives.
        </p>
        <div>
          <Link
            href="/contact"
            className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg text-sm font-semibold text-white bg-slate-900 hover:bg-slate-800 transition-colors shadow-sm"
          >
            <span>Contact Grizo Enterprises</span>
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </Link>
        </div>
      </section>
    </div>
  );
}
