import React from 'react';
import Link from 'next/link';
import {
  Mail,
  MapPin,
  Phone,
  Building,
  CheckCircle2,
  Clock,
  ShieldCheck,
  AlertCircle,
} from 'lucide-react';
import ContactForm from '@/components/ContactForm';
import StatusBadge from '@/components/StatusBadge';
import { siteConfig } from '@/config/siteConfig';

export const metadata = {
  title: 'Contact Us | Grizo Enterprises',
  description:
    'Get in touch with Grizo Enterprises for commercial supplier inquiries, business partnerships, or marketplace communications.',
};

export default function ContactPage() {
  const business = siteConfig.business;
  const contact = siteConfig.contact;

  return (
    <div className="py-12 sm:py-16 lg:py-20 space-y-16">
      {/* Header */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-accent">
              Commercial Communications
            </span>
            <StatusBadge />
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 tracking-tight">
            Contact Grizo Enterprises
          </h1>
          <p className="text-lg text-slate-600 leading-relaxed">
            We welcome correspondence from verified manufacturers, domestic suppliers, marketplace representatives, and commercial collaborators.
          </p>
        </div>
      </section>

      {/* Main Grid: Contact Details on Left, Form on Right */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
          
          {/* Left Column: Verified Business Information & Config Status */}
          <div className="lg:col-span-5 space-y-8">
            <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 sm:p-8 space-y-6">
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Building className="w-5 h-5 text-brand-accent" aria-hidden="true" />
                <span>Business Information</span>
              </h2>

              <div className="space-y-4 text-sm text-slate-700">
                <div>
                  <span className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Business Entity
                  </span>
                  <p className="font-semibold text-slate-900 mt-0.5">
                    {business.name}
                  </p>
                  <p className="text-xs text-slate-500">
                    Structure: {business.legalStructure}
                  </p>
                </div>

                <div>
                  <span className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Country of Operation
                  </span>
                  <p className="font-semibold text-slate-900 mt-0.5">
                    {business.country}
                  </p>
                  <p className="text-xs text-slate-500">
                    Status: GST-Registered Taxpayer
                  </p>
                </div>

                <div>
                  <span className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Primary Marketplace
                  </span>
                  <p className="font-semibold text-slate-900 mt-0.5">
                    {business.primaryMarketplace}
                  </p>
                </div>

                {/* Email Address Block */}
                <div>
                  <span className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Official Business Email
                  </span>
                  {contact.email ? (
                    <a
                      href={`mailto:${contact.email}`}
                      className="font-semibold text-brand-accent hover:underline block mt-0.5"
                    >
                      {contact.email}
                    </a>
                  ) : (
                    <div className="mt-1 p-2.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 space-y-1">
                      <p className="font-medium text-slate-700">Pending Domain Email Configuration</p>
                      <p className="text-slate-500">
                        The business owner will supply an official business domain email before live deployment.
                      </p>
                    </div>
                  )}
                </div>

                {/* Phone Block if configured */}
                {contact.phone && (
                  <div>
                    <span className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
                      Telephone
                    </span>
                    <p className="font-semibold text-slate-900 mt-0.5">
                      {contact.phone}
                    </p>
                  </div>
                )}

                {/* Address Block if configured */}
                {contact.address && (
                  <div>
                    <span className="block text-xs font-semibold uppercase tracking-wider text-slate-400">
                      Registered Business Address
                    </span>
                    <p className="text-slate-800 mt-0.5 whitespace-pre-line text-xs">
                      {contact.address}
                    </p>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-slate-200 text-xs text-slate-500 space-y-2">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-600" aria-hidden="true" />
                  <span>GST-compliant commercial invoicing for all transactions.</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-brand-accent" aria-hidden="true" />
                  <span>Standard inquiry review window: 1–2 business days.</span>
                </div>
              </div>
            </div>

            {/* Note on Transparency & SP-API Review */}
            <div className="p-5 rounded-xl bg-sky-50 border border-sky-200 text-xs text-sky-950 space-y-2">
              <h3 className="font-bold text-sky-900 flex items-center gap-1.5">
                <AlertCircle className="w-4 h-4 text-sky-600" aria-hidden="true" />
                <span>Notice for Marketplace Review Teams</span>
              </h3>
              <p className="leading-relaxed">
                This website is submitted in support of Grizo Enterprises&apos; application for Amazon Selling Partner API developer access. If additional corporate or identity verification documents are required, please direct requests to the business email provided in the official Amazon developer submission portal.
              </p>
            </div>
          </div>

          {/* Right Column: Interactive Form */}
          <div className="lg:col-span-7 space-y-4">
            <div className="space-y-1 mb-2">
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
                Send a Commercial Inquiry
              </h2>
              <p className="text-sm text-slate-600">
                Please complete the form below. All inquiries are screened and responded to by our operational management.
              </p>
            </div>
            <ContactForm />
          </div>

        </div>
      </section>
    </div>
  );
}
