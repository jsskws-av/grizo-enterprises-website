import React from 'react';
import Link from 'next/link';
import { FileText, AlertTriangle, Scale, ShieldCheck } from 'lucide-react';
import StatusBadge from '@/components/StatusBadge';
import { siteConfig } from '@/config/siteConfig';

export const metadata = {
  title: 'Terms of Use | Grizo Enterprises',
  description:
    'Terms of Use governing the use of the Grizo Enterprises business website and informational materials.',
};

export default function TermsOfUsePage() {
  const effectiveDate = siteConfig.termsEffectiveDate;
  const businessName = siteConfig.business.name;
  const country = siteConfig.business.country;
  const contactEmail = siteConfig.contact.email;

  return (
    <div className="py-12 sm:py-16 lg:py-20 space-y-12 lg:space-y-16">
      {/* Header */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-4">
        <div className="flex flex-wrap items-center gap-3">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
            Legal Terms
          </span>
          <StatusBadge />
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-950 tracking-tight">
          Terms of Use
        </h1>
        <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 pb-4 border-b border-slate-200">
          <span>Effective Date: <strong>{effectiveDate}</strong></span>
          <span>•</span>
          <span>Entity: <strong>{businessName}</strong> ({siteConfig.business.legalStructure})</span>
          <span>•</span>
          <span>Jurisdiction: <strong>{country}</strong></span>
        </div>
      </section>

      {/* Main Content */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="prose prose-slate max-w-none space-y-10 text-slate-700 text-sm sm:text-base leading-relaxed">
          
          {/* Section 1 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">1.</span> Website Purpose
            </h2>
            <p>
              This website is published and maintained by Grizo Enterprises, an Indian sole proprietorship registered under GST. The purpose of this website is to provide truthful, professional information about our business operations, online retail activities, and internal technological initiatives. It serves as an official online presence for suppliers, marketplace administrators, and commercial contacts.
            </p>
          </div>

          {/* Section 2 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">2.</span> Accuracy and Availability of Information
            </h2>
            <p>
              While we endeavor to keep all information on this website accurate and up to date, the materials and descriptions are provided on an &ldquo;as is&rdquo; and &ldquo;as available&rdquo; basis. E-commerce marketplace policies, fee structures, and internal software capabilities evolve over time. Grizo Enterprises makes no representations or warranties regarding the uninterrupted availability or exhaustive completeness of this website.
            </p>
          </div>

          {/* Section 3 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">3.</span> Intellectual Property
            </h2>
            <p>
              All original content, text, layout design, wordmark styling, and conceptual materials appearing on this website are the property of Grizo Enterprises and are protected by applicable intellectual property and copyright laws.
            </p>
            <p>
              Third-party trade names, trademarks, and brand references—including &ldquo;Amazon,&rdquo; &ldquo;Amazon India,&rdquo; &ldquo;Selling Partner API (SP-API),&rdquo; &ldquo;FBA,&rdquo; and &ldquo;Easy Ship&rdquo;—are the intellectual property of their respective owners (Amazon.com, Inc. or its affiliates). Their appearance on this website is descriptive only and does not imply endorsement, affiliation, or commercial sponsorship.
            </p>
          </div>

          {/* Section 4 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">4.</span> Acceptable Use
            </h2>
            <p>
              When visiting this website, you agree not to:
            </p>
            <ul className="list-disc pl-5 space-y-2">
              <li>Use the website in any manner that disrupts, disables, or impairs its security or availability.</li>
              <li>Attempt unauthorized access to server infrastructure, configuration files, or related repositories.</li>
              <li>Use automated scrapers, bots, or data harvesting scripts to duplicate or extract content without written permission.</li>
              <li>Submit abusive, misleading, fraudulent, or spam messages through our contact channels.</li>
            </ul>
          </div>

          {/* Section 5 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">5.</span> External Links
            </h2>
            <p>
              This website may occasionally contain links to external third-party websites or services (e.g. marketplace documentation, statutory portals, or developer guidelines). Grizo Enterprises has no control over the content, privacy practices, or availability of external sites and assumes no liability for damages or losses arising from their use.
            </p>
          </div>

          {/* Section 6 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">6.</span> Limitations of Informational Content & No Commercial Guarantees
            </h2>
            <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200 text-amber-950 space-y-2">
              <p className="font-semibold text-amber-900">
                Notice Regarding Commercial Projections & Technology Descriptions:
              </p>
              <p className="text-xs sm:text-sm leading-relaxed">
                The market research methodologies, profitability calculation structures, and software features described on this website represent our operational philosophy and developmental workflows. <strong>Nothing on this website constitutes a commercial promise, sales guarantee, return-on-investment commitment, or financial warranty.</strong>
              </p>
              <p className="text-xs sm:text-sm leading-relaxed">
                E-commerce retail operations involve marketplace dynamics, supplier dependencies, customer return rates, and regulatory factors beyond automated control. Grizo Enterprises explicitly disclaims any liability for financial actions taken by external parties based on informational materials published on this website.
              </p>
            </div>
          </div>

          {/* Section 7 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">7.</span> Changes to the Website and Terms
            </h2>
            <p>
              Grizo Enterprises reserves the right to modify, update, or discontinue any aspect of this website or these Terms of Use at our sole discretion. Any changes become effective immediately upon being published to this page with an updated effective date.
            </p>
          </div>

          {/* Section 8 */}
          <div className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <span className="text-brand-accent text-sm font-mono">8.</span> Governing Law and Contact
            </h2>
            <p>
              These Terms of Use are governed by and construed in accordance with the laws of India. For any inquiries regarding these terms, please contact:
            </p>
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 text-sm space-y-2 not-prose">
              <p>
                <strong className="text-slate-900">Business Entity:</strong> {businessName} ({siteConfig.business.legalStructure})
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
                  Inquiries may be directed through our website Contact Us page.
                </p>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
