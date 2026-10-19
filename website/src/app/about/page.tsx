import React from 'react';
import Link from 'next/link';
import {
  Building2,
  Compass,
  Cpu,
  ShieldCheck,
  CheckCircle2,
  ArrowRight,
  FileCheck,
} from 'lucide-react';
import StatusBadge from '@/components/StatusBadge';
import { siteConfig } from '@/config/siteConfig';

export const metadata = {
  title: 'About Grizo Enterprises | Business Profile & Overview',
  description:
    'Grizo Enterprises is an India-based sole proprietorship registered under GST, focusing on online retail, market analysis, and internal technology development for e-commerce.',
};

export default function AboutPage() {
  return (
    <div className="py-12 sm:py-16 lg:py-20 space-y-16 lg:space-y-24">
      {/* Page Header */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl space-y-4">
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
              Organizational Profile
            </span>
            <StatusBadge />
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 tracking-tight">
            About Grizo Enterprises
          </h1>
          <p className="text-lg text-slate-600 leading-relaxed">
            {siteConfig.business.tagline}
          </p>
        </div>
      </section>

      {/* Approved Core Business Introduction */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-50 border border-slate-200/90 rounded-2xl p-8 sm:p-10 lg:p-12 space-y-6">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Official Business Statement
          </h2>
          <div className="space-y-4 text-slate-800 text-base sm:text-lg leading-relaxed font-normal">
            <p>
              Grizo Enterprises is an India-based sole proprietorship registered under GST. The business focuses on e-commerce and online retail, with an emphasis on improving product research, commercial analysis, and day-to-day business operations through technology.
            </p>
            <p>
              As part of its technology development initiative, Grizo Enterprises is developing an internal application intended to assist with product opportunity research, pricing analysis, listing preparation, inventory monitoring, and profitability calculations.
            </p>
            <p>
              The objective is to make business operations more organised, measurable, and data-informed while retaining human oversight of important commercial decisions.
            </p>
          </div>
          <div className="pt-4 border-t border-slate-200 flex flex-wrap items-center gap-6 text-xs text-slate-600 font-medium">
            <span>• Structure: Sole Proprietorship</span>
            <span>• Registration: GST Registered</span>
            <span>• Jurisdiction: India</span>
            <span>• Operating Focus: Amazon India</span>
          </div>
        </div>
      </section>

      {/* Section 1: Our Business */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          <div className="lg:col-span-4 space-y-3">
            <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-brand-accent">
              <Building2 className="w-4 h-4" aria-hidden="true" />
              <span>Section 01</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Our Business
            </h2>
            <p className="text-sm text-slate-600 leading-relaxed">
              Commercial retail structure, legal identity, and marketplace context.
            </p>
          </div>

          <div className="lg:col-span-8 space-y-4 text-slate-700 text-sm sm:text-base leading-relaxed bg-white border border-slate-200 p-6 sm:p-8 rounded-xl shadow-xs">
            <p>
              Grizo Enterprises operates as an independent Indian sole proprietorship dedicated to contemporary digital commerce. Our commercial activities centre on identifying, sourcing, and retailing products across prominent digital marketplaces, with a primary emphasis on Amazon India (amazon.in).
            </p>
            <p>
              As a legally registered taxpayer under India’s Goods and Services Tax (GST) framework, Grizo Enterprises upholds full regulatory compliance. All transactions, from domestic procurement through manufacturer and supplier channels to end-consumer marketplace sales, are managed in strict accordance with statutory invoicing, taxation, and disclosure norms.
            </p>
            <p>
              We treat retail as an operational discipline requiring consistency, accurate documentation, and strict product compliance—ensuring that every stock keeping unit (SKU) offered meets mandatory consumer protection and legal metrology standards.
            </p>
          </div>
        </div>
      </section>

      {/* Section 2: Our Approach */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          <div className="lg:col-span-4 space-y-3">
            <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-brand-accent">
              <Compass className="w-4 h-4" aria-hidden="true" />
              <span>Section 02</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Our Approach
            </h2>
            <p className="text-sm text-slate-600 leading-relaxed">
              Methodical research, unit economics verification, and risk mitigation.
            </p>
          </div>

          <div className="lg:col-span-8 space-y-6">
            <div className="bg-white border border-slate-200 p-6 sm:p-8 rounded-xl shadow-xs space-y-4 text-slate-700 text-sm sm:text-base leading-relaxed">
              <p>
                Our commercial approach is grounded in empirical verification rather than speculation. Before committing working capital to any merchandise category, Grizo Enterprises applies a multi-stage review process:
              </p>
              <ul className="space-y-3 pt-2">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-brand-accent flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <span>
                    <strong className="text-slate-900 font-semibold">Demand Validation:</strong> Assessing legitimate consumer purchase intent through historical review volumes, sales rank trends, and seasonal cycles.
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-brand-accent flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <span>
                    <strong className="text-slate-900 font-semibold">Comprehensive Cost Accounting:</strong> Factoring in complete logistical costs including Amazon referral fees, closing fees, weight handling, GST input tax credits, return allowance, and packaging expenses.
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-brand-accent flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <span>
                    <strong className="text-slate-900 font-semibold">Quality & Supplier Reliability:</strong> Evaluating manufacturing consistency, packaging durability, sample inspections, and domestic lead times before placing commercial purchase orders.
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: Technology and Innovation */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          <div className="lg:col-span-4 space-y-3">
            <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-brand-accent">
              <Cpu className="w-4 h-4" aria-hidden="true" />
              <span>Section 03</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Technology & Innovation
            </h2>
            <p className="text-sm text-slate-600 leading-relaxed">
              Internal software engineering in Google Antigravity.
            </p>
          </div>

          <div className="lg:col-span-8 space-y-4 text-slate-700 text-sm sm:text-base leading-relaxed bg-white border border-slate-200 p-6 sm:p-8 rounded-xl shadow-xs">
            <p>
              In parallel with our retail activities, Grizo Enterprises invests in developing specialized internal software. Engineered within the Google Antigravity development environment, this application cluster addresses the operational bottlenecks typical of e-commerce seller management.
            </p>
            <p>
              The system combines deterministic computational engines (for exact financial, tax, and inventory formulas) with language models (for keyword taxonomy research and customer feedback analysis).
            </p>
            <p>
              We design our tools strictly for internal enterprise consumption. We do not offer software-as-a-service (SaaS) or manage third-party accounts; our technology is tailored exclusively to heighten the accuracy and speed of our own retail operations.
            </p>
            <div className="pt-2">
              <Link
                href="/technology"
                className="inline-flex items-center gap-1.5 text-sm font-semibold text-brand-accent hover:text-brand-accentHover"
              >
                <span>Explore the architectural details of our internal tooling</span>
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Section 4: Responsible Business Operations */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          <div className="lg:col-span-4 space-y-3">
            <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-brand-accent">
              <ShieldCheck className="w-4 h-4" aria-hidden="true" />
              <span>Section 04</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Responsible Business Operations
            </h2>
            <p className="text-sm text-slate-600 leading-relaxed">
              Human oversight, compliance safeguards, and ethical data governance.
            </p>
          </div>

          <div className="lg:col-span-8 space-y-6">
            <div className="bg-slate-50 border border-slate-200 p-6 sm:p-8 rounded-xl space-y-4 text-slate-700 text-sm sm:text-base leading-relaxed">
              <p>
                Grizo Enterprises recognizes that commercial success in e-commerce depends upon customer trust, supplier integrity, and strict adherence to platform standards. We enforce rigid operational governance:
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div className="p-4 rounded-lg bg-white border border-slate-200">
                  <h4 className="text-sm font-semibold text-slate-900 mb-1">Human Accountability</h4>
                  <p className="text-xs text-slate-600">
                    No automated script has the authority to disburse funds, execute purchase orders, or alter pricing without human confirmation.
                  </p>
                </div>
                <div className="p-4 rounded-lg bg-white border border-slate-200">
                  <h4 className="text-sm font-semibold text-slate-900 mb-1">Data Respect & Integrity</h4>
                  <p className="text-xs text-slate-600">
                    We strictly use permitted data sources and respect marketplace developer policies, avoiding unauthorized scraping or improper data sharing.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Navigation CTA */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 border-t border-slate-200">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-600">
            Learn more about our practical day-to-day operations:
          </p>
          <div className="flex items-center gap-4">
            <Link
              href="/activities"
              className="inline-flex items-center gap-2 text-sm font-semibold text-brand-accent hover:text-brand-accentHover"
            >
              <span>View Business Activities</span>
              <ArrowRight className="w-4 h-4" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
