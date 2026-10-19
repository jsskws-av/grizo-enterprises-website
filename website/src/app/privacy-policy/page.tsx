import React from 'react';
import Link from 'next/link';
import {
  ShieldCheck,
  Lock,
  Eye,
  FileText,
  AlertTriangle,
  Server,
  UserX,
  RefreshCw,
  Mail,
  CheckCircle2,
} from 'lucide-react';
import StatusBadge from '@/components/StatusBadge';
import { siteConfig } from '@/config/siteConfig';

export const metadata = {
  title: 'Privacy Policy | Grizo Enterprises',
  description:
    'Official Privacy Policy for Grizo Enterprises detailing our data handling practices, internal software development status, and user privacy protections.',
};

export default function PrivacyPolicyPage() {
  const effectiveDate = siteConfig.privacyEffectiveDate;
  const businessName = siteConfig.business.name;
  const country = siteConfig.business.country;
  const contactEmail = siteConfig.contact.email;

  return (
    <div className="py-12 sm:py-16 lg:py-20 space-y-12 lg:space-y-16">
      {/* Header */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-4">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
            Legal & Governance
          </span>
          <StatusBadge />
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-950 tracking-tight">
          Privacy Policy
        </h1>
        <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 pb-4 border-b border-slate-200">
          <span>Effective Date: <strong>{effectiveDate}</strong></span>
          <span>•</span>
          <span>Entity: <strong>{businessName}</strong> ({siteConfig.business.legalStructure})</span>
          <span>•</span>
          <span>Jurisdiction: <strong>{country}</strong></span>
        </div>
      </section>

      {/* Development Status Notice */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-sky-50 border border-sky-200 rounded-xl p-5 sm:p-6 text-xs sm:text-sm text-sky-950 space-y-2">
          <div className="flex items-center gap-2 font-bold text-sky-900">
            <Lock className="w-4 h-4 text-sky-600" aria-hidden="true" />
            <span>Operational Context & Scope Notice</span>
          </div>
          <p className="leading-relaxed">
            This Privacy Policy governs the public website of Grizo Enterprises and outlines the data handling framework designed for our internal e-commerce management workflows. As our marketplace API integrations are currently in active development and not yet live in production, no consumer marketplace order data is currently ingested via this website.
          </p>
        </div>
      </section>

      {/* 10 Sections Content */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="prose prose-slate max-w-none space-y-10 text-slate-700 text-sm sm:text-base leading-relaxed">
          
          {/* Section 1 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">1.</span> Introduction
            </h2>
            <p>
              Grizo Enterprises (&ldquo;the Business,&rdquo; &ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;) is an Indian sole proprietorship registered under the Goods and Services Tax (GST) framework. We respect the privacy of individuals and entities that interact with our commercial website and are committed to handling personal and business data transparently, conservatively, and in compliance with applicable Indian digital data protection standards.
            </p>
            <p>
              This policy describes what information we may receive when you visit this website, how commercial inquiries are managed, and how data governance is structured within our internal operational software.
            </p>
          </div>

          {/* Section 2 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">2.</span> Information We May Collect
            </h2>
            <p>
              The information we collect depends strictly upon how you interact with our website:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong>Direct Communications & Inquiries:</strong> When you contact us via our contact form or official email, we may collect your name, email address, corporate affiliation, telephone number (if provided), and the subject/message content you supply.
              </li>
              <li>
                <strong>Technical Browsing Data:</strong> When navigating our website, standard web server logs may temporarily register non-identifying technical data such as your IP address, browser type, operating system version, referring URL, and timestamp. We do not use third-party behavioral profiling or cross-site tracking cookies.
              </li>
              <li>
                <strong>Supplier & Procurement Records:</strong> Where manufacturers or suppliers submit product catalogs, pricing sheets, or GST documentation, such commercial records are retained exclusively for procurement due diligence.
              </li>
            </ul>
          </div>

          {/* Section 3 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">3.</span> Purpose of Information Processing
            </h2>
            <p>
              We process received information strictly for legitimate commercial and administrative purposes:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>To evaluate, respond to, and document business inquiries submitted by potential suppliers, partners, or platform administrators.</li>
              <li>To maintain website security, prevent spam, and protect against malicious cyber attacks or unauthorized server access.</li>
              <li>To meet statutory recordkeeping, commercial invoicing, and tax obligations under Indian tax laws.</li>
              <li>To test and refine our internal operational workflows in isolated development environments.</li>
            </ul>
            <p>
              We do not sell, rent, lease, or monetize personal information to third-party data brokers or marketing aggregators.
            </p>
          </div>

          {/* Section 4 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">4.</span> Marketplace API Information
            </h2>
            <p>
              Grizo Enterprises is developing internal software intended to interface with authorized marketplace APIs (specifically the Amazon Selling Partner API). We establish clear parameters regarding marketplace data:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong>Current Status:</strong> Our marketplace API integration is actively under development. No live Amazon customer data or seller account feeds are currently ingested by this public website.
              </li>
              <li>
                <strong>Planned Operational Scope:</strong> If authorized, API data access will be strictly restricted to the seller account of Grizo Enterprises for inventory management, listing auditing, and financial settlement verification.
              </li>
              <li>
                <strong>Data Minimization:</strong> Our internal systems will request only the specific API roles and scopes necessary to fulfill verified operational functions.
              </li>
              <li>
                <strong>Compliance with Developer Policies:</strong> All future handling of Amazon marketplace data will strictly adhere to Amazon&apos;s Acceptable Use Policy and Data Protection Policy.
              </li>
            </ul>
          </div>

          {/* Section 5 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">5.</span> Data Storage and Security
            </h2>
            <p>
              We apply practical, defense-in-depth measures to safeguard information:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong>Encrypted Web Transit:</strong> All website traffic is served over Hypertext Transfer Protocol Secure (HTTPS) using Transport Layer Security (TLS) certificates.
              </li>
              <li>
                <strong>Credential Protection:</strong> Development environment secrets, API tokens, and administrative keys are stored strictly in secure server-side environment configurations and are never committed to client-side code or public version control.
              </li>
              <li>
                <strong>Access Control:</strong> Administrative access to website hosting and development repositories is restricted to authorized administrative personnel via multi-factor authentication.
              </li>
            </ul>
            <p className="text-xs text-slate-500 italic">
              Note: While we implement prudent security practices, no Internet transmission or digital storage architecture can be guaranteed to be 100% impenetrable. We do not claim third-party certifications (e.g. ISO 27001 or SOC 2) that have not been independently awarded.
            </p>
          </div>

          {/* Section 6 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">6.</span> Data Sharing and Third-Party Processors
            </h2>
            <p>
              We do not share your personal information except with necessary infrastructure service providers operating under confidentiality obligations:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong>Hosting and Infrastructure Providers:</strong> Our website assets and build pipelines are hosted on secure cloud infrastructure platforms (such as Vercel or cloud web providers) that process technical traffic data to deliver web pages.
              </li>
              <li>
                <strong>Email Delivery Services:</strong> When our email communication gateway is activated, messages submitted through our contact form may be processed through reputable email infrastructure providers solely to route correspondence to our inbox.
              </li>
              <li>
                <strong>Legal and Statutory Mandates:</strong> We may disclose information if required to do so by applicable Indian law, court order, or formal request from statutory tax or regulatory authorities.
              </li>
            </ul>
          </div>

          {/* Section 7 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">7.</span> Data Retention and Deletion
            </h2>
            <p>
              We retain personal data only for as long as necessary to fulfill the operational purpose for which it was collected:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>
                <strong>Inquiry Records:</strong> General commercial correspondence is retained for the duration of the commercial relationship or until resolution of the inquiry, after which records are archived or deleted.
              </li>
              <li>
                <strong>Tax & Statutory Records:</strong> Formal procurement invoices and tax documents are retained for the statutory period mandated by Indian tax and GST legislation (ordinarily up to six years).
              </li>
              <li>
                <strong>Deletion Requests:</strong> You may request the deletion of non-statutory communication records at any time by contacting our privacy email.
              </li>
            </ul>
          </div>

          {/* Section 8 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">8.</span> Individual Privacy Rights
            </h2>
            <p>
              In accordance with applicable data protection principles, individuals who submit personal information have the right to:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>Request confirmation of whether we process personal data relating to them.</li>
              <li>Request access to or a summary of personal information we hold about them.</li>
              <li>Request correction or updating of inaccurate or incomplete personal records.</li>
              <li>Request erasure of personal information where statutory retention requirements do not apply.</li>
            </ul>
            <p>
              To exercise any of these rights, please submit a written request using the contact information below.
            </p>
          </div>

          {/* Section 9 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">9.</span> Policy Updates
            </h2>
            <p>
              We may update this Privacy Policy periodically to reflect changes in our operational procedures, marketplace integrations, or relevant legal requirements. When updates are published, the revised &ldquo;Effective Date&rdquo; at the top of this page will be updated accordingly. Continued interaction with our website following such revisions constitutes acknowledgment of the updated terms.
            </p>
          </div>

          {/* Section 10 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">10.</span> Contact Information
            </h2>
            <p>
              For any questions, clarifications, or privacy requests regarding this policy or our data management approach, please reach out to:
            </p>
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 text-sm space-y-2 not-prose">
              <p>
                <strong className="text-slate-900">Entity:</strong> {businessName} ({siteConfig.business.legalStructure})
              </p>
              <p>
                <strong className="text-slate-900">Jurisdiction:</strong> {country}
              </p>
              {contactEmail ? (
                <p>
                  <strong className="text-slate-900">Email:</strong>{' '}
                  <a href={`mailto:${contactEmail}`} className="text-brand-accent hover:underline">
                    {contactEmail}
                  </a>
                </p>
              ) : (
                <p className="text-xs text-slate-500 italic">
                  Official privacy contact email will be published upon domain activation. You may also contact us via our website contact form.
                </p>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Owner Pre-Publication Verification Checklist */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-6 space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-amber-900">
            <CheckCircle2 className="w-4 h-4 text-amber-700" aria-hidden="true" />
            <span>Pre-Publication Verification Checklist for Business Owner</span>
          </div>
          <p className="text-xs text-amber-950 leading-relaxed">
            Prior to submitting this website to Amazon SP-API developer registration or publishing it live to production, the business owner must confirm:
          </p>
          <ul className="space-y-2 text-xs text-amber-900">
            <li className="flex items-start gap-2">
              <span className="font-bold">•</span>
              <span>The actual production domain is owned, active, and points to this website.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-bold">•</span>
              <span>A monitored business email address (e.g. contact@yourdomain.com) has been configured in <code>siteConfig.ts</code>.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-bold">•</span>
              <span>Third-party hosting and data processors used correspond to the actual deployment setup.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-bold">•</span>
              <span>No claims of active marketplace API access are made until authorization is formally received.</span>
            </li>
          </ul>
        </div>
      </section>
    </div>
  );
}
