import React from 'react';
import Link from 'next/link';
import Wordmark from './Wordmark';
import { siteConfig } from '@/config/siteConfig';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-slate-900 text-slate-300 border-t border-slate-800" aria-labelledby="footer-heading">
      <h2 id="footer-heading" className="sr-only">Footer</h2>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
          
          {/* Column 1: Organization Overview */}
          <div className="space-y-4">
            <Wordmark variant="light" size="md" />
            <p className="text-sm text-slate-400 leading-relaxed">
              {siteConfig.business.tagline}
            </p>
            <p className="text-xs text-slate-400 leading-relaxed">
              An Indian sole proprietorship registered under GST, focused on online retail, market analysis, and internal technology development for e-commerce operations.
            </p>
            <div className="pt-2">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">
                <span>Country of Registration:</span>
                <strong className="text-white font-semibold">India</strong>
              </span>
            </div>
          </div>

          {/* Column 2: Navigation Links */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white mb-4">
              Website Navigation
            </h3>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link href="/" className="hover:text-white transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/about" className="hover:text-white transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/activities" className="hover:text-white transition-colors">
                  Business Activities
                </Link>
              </li>
              <li>
                <Link href="/technology" className="hover:text-white transition-colors">
                  Technology & Operations
                </Link>
              </li>
              <li>
                <Link href="/marketplace-integrations" className="hover:text-white transition-colors">
                  Marketplace Integrations
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Legal & Governance */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white mb-4">
              Governance & Policies
            </h3>
            <ul className="space-y-2.5 text-sm">
              <li>
                <Link href="/privacy-policy" className="hover:text-white transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms-of-use" className="hover:text-white transition-colors">
                  Terms of Use
                </Link>
              </li>
              <li>
                <Link href="/marketplace-integrations" className="hover:text-white transition-colors">
                  API & Data Use Disclosure
                </Link>
              </li>
              <li>
                <Link href="/contact" className="hover:text-white transition-colors">
                  Contact Grizo Enterprises
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 4: Contact & Verification */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-white mb-4">
              Business Information
            </h3>
            <div className="space-y-2.5 text-sm text-slate-400">
              <p>
                <strong className="text-slate-200">Legal Entity:</strong>{' '}
                {siteConfig.business.name} ({siteConfig.business.legalStructure})
              </p>
              <p>
                <strong className="text-slate-200">Registration:</strong> GST-Registered Business
              </p>
              <p>
                <strong className="text-slate-200">Location:</strong> India
              </p>
              {siteConfig.contact.email ? (
                <p>
                  <strong className="text-slate-200">Official Email:</strong>{' '}
                  <a
                    href={`mailto:${siteConfig.contact.email}`}
                    className="text-sky-400 hover:underline"
                  >
                    {siteConfig.contact.email}
                  </a>
                </p>
              ) : (
                <p className="text-xs text-slate-400 italic">
                  Official communication channel will be verified and displayed upon public domain deployment.
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Separator & Trademark Disclosure */}
        <div className="mt-12 pt-8 border-t border-slate-800 space-y-4">
          <p className="text-xs text-slate-400 leading-relaxed">
            <strong className="text-slate-300">Marketplace Trademark Disclaimer:</strong> Amazon, Amazon India, Amazon Services, Selling Partner API (SP-API), and any associated brand marks are trademarks or registered trademarks of Amazon.com, Inc. or its affiliates. Grizo Enterprises is an independent commercial entity. The mention of marketplace services reflects internal technological development and planned operational workflows; it does not indicate any sponsorship, endorsement, certification, or formal partnership with Amazon.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-4 pt-4 border-t border-slate-800/60">
            <p>
              &copy; {currentYear} {siteConfig.business.name}. All rights reserved. Indian Sole Proprietorship.
            </p>
            <div className="flex items-center space-x-6">
              <Link href="/privacy-policy" className="hover:text-slate-300">
                Privacy
              </Link>
              <Link href="/terms-of-use" className="hover:text-slate-300">
                Terms
              </Link>
              <Link href="/contact" className="hover:text-slate-300">
                Contact
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
