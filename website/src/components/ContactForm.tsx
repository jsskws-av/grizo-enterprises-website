'use client';

import React, { useState, FormEvent } from 'react';
import Link from 'next/link';
import { AlertCircle, CheckCircle2, Send, Info } from 'lucide-react';
import { siteConfig } from '@/config/siteConfig';

interface FormData {
  name: string;
  email: string;
  subject: string;
  message: string;
  consent: boolean;
  honeypot: string; // anti-spam hidden field
}

interface FormErrors {
  name?: string;
  email?: string;
  subject?: string;
  message?: string;
  consent?: string;
}

export default function ContactForm() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    subject: '',
    message: '',
    consent: false,
    honeypot: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionStatus, setSubmissionStatus] = useState<
    'idle' | 'success' | 'backend_unconfigured' | 'error'
  >('idle');

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Please provide your full name.';
    } else if (formData.name.trim().length < 2) {
      newErrors.name = 'Name must be at least 2 characters long.';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Please provide your email address.';
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.email.trim())) {
        newErrors.email = 'Please enter a valid email address.';
      }
    }

    if (!formData.subject.trim()) {
      newErrors.subject = 'Please specify the subject of your inquiry.';
    } else if (formData.subject.trim().length < 3) {
      newErrors.subject = 'Subject must be at least 3 characters.';
    }

    if (!formData.message.trim()) {
      newErrors.message = 'Please enter your message.';
    } else if (formData.message.trim().length < 15) {
      newErrors.message = 'Please provide a message with at least 15 characters.';
    }

    if (!formData.consent) {
      newErrors.consent =
        'You must acknowledge our privacy policy before sending your inquiry.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Check anti-spam honeypot
    if (formData.honeypot) {
      return;
    }

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);
    setSubmissionStatus('idle');

    // Simulate backend verification check
    try {
      if (!siteConfig.application.isBackendEmailConfigured) {
        // Honest transparency: Do NOT claim message sent when backend email is not yet hooked up
        setTimeout(() => {
          setIsSubmitting(false);
          setSubmissionStatus('backend_unconfigured');
        }, 500);
        return;
      }

      // If backend is configured, real dispatch would happen here:
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (res.ok) {
        setSubmissionStatus('success');
        setFormData({
          name: '',
          email: '',
          subject: '',
          message: '',
          consent: false,
          honeypot: '',
        });
      } else {
        setSubmissionStatus('error');
      }
    } catch {
      setSubmissionStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 sm:p-8 shadow-xs">
      {/* Notice regarding backend status */}
      {!siteConfig.application.isBackendEmailConfigured && (
        <div className="mb-6 p-4 rounded-lg bg-sky-50 border border-sky-200 text-sky-950 text-sm flex items-start gap-3">
          <Info className="w-5 h-5 text-sky-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
          <div className="space-y-1">
            <p className="font-semibold text-sky-900">
              Inquiry Dispatch Notice
            </p>
            <p className="text-sky-800 text-xs leading-relaxed">
              Automated web dispatch is currently in pre-activation mode while our official business email infrastructure is finalized. Form submissions are validated client-side to test accessibility and format compliance, but will not be sent to an inbox until email routing is activated.
            </p>
          </div>
        </div>
      )}

      {submissionStatus === 'backend_unconfigured' && (
        <div
          role="alert"
          className="mb-6 p-4 rounded-lg bg-amber-50 border border-amber-300 text-amber-950 text-sm flex items-start gap-3"
        >
          <AlertCircle className="w-5 h-5 text-amber-700 flex-shrink-0 mt-0.5" aria-hidden="true" />
          <div className="space-y-1">
            <p className="font-semibold text-amber-900">
              Form Validated — Message Not Dispatched
            </p>
            <p className="text-amber-800 text-xs leading-relaxed">
              Your inquiry passed input validation successfully. However, because our production mail gateway is not yet linked, your submission has not been recorded or dispatched. Once our business domain and mail service are fully activated, this form will deliver messages directly to our operations inbox.
            </p>
          </div>
        </div>
      )}

      {submissionStatus === 'success' && (
        <div
          role="status"
          className="mb-6 p-4 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-950 text-sm flex items-start gap-3"
        >
          <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
          <div>
            <p className="font-semibold text-emerald-900">Message Dispatched</p>
            <p className="text-emerald-800 text-xs">
              Thank you for contacting Grizo Enterprises. Your message has been received.
            </p>
          </div>
        </div>
      )}

      {submissionStatus === 'error' && (
        <div
          role="alert"
          className="mb-6 p-4 rounded-lg bg-rose-50 border border-rose-300 text-rose-950 text-sm flex items-start gap-3"
        >
          <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
          <div>
            <p className="font-semibold text-rose-900">Submission Error</p>
            <p className="text-rose-800 text-xs">
              An unexpected error occurred while processing your request. Please try again later.
            </p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate className="space-y-5">
        {/* Anti-spam honeypot */}
        <div className="hidden" aria-hidden="true">
          <label htmlFor="hp_field">Do not fill this</label>
          <input
            id="hp_field"
            type="text"
            tabIndex={-1}
            autoComplete="off"
            value={formData.honeypot}
            onChange={(e) => setFormData({ ...formData, honeypot: e.target.value })}
          />
        </div>

        {/* Name and Email Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-1">
              Your Name <span className="text-rose-500">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={(e) => {
                setFormData({ ...formData, name: e.target.value });
                if (errors.name) setErrors({ ...errors, name: undefined });
              }}
              aria-invalid={errors.name ? 'true' : 'false'}
              aria-describedby={errors.name ? 'name-error' : undefined}
              className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 ${
                errors.name
                  ? 'border-rose-400 focus:ring-rose-400 bg-rose-50/20'
                  : 'border-slate-300 focus:border-brand-accent focus:ring-brand-accent/20'
              }`}
              placeholder="e.g., Rajesh Sharma"
            />
            {errors.name && (
              <p id="name-error" className="mt-1 text-xs text-rose-600">
                {errors.name}
              </p>
            )}
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">
              Your Email Address <span className="text-rose-500">*</span>
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={(e) => {
                setFormData({ ...formData, email: e.target.value });
                if (errors.email) setErrors({ ...errors, email: undefined });
              }}
              aria-invalid={errors.email ? 'true' : 'false'}
              aria-describedby={errors.email ? 'email-error' : undefined}
              className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 ${
                errors.email
                  ? 'border-rose-400 focus:ring-rose-400 bg-rose-50/20'
                  : 'border-slate-300 focus:border-brand-accent focus:ring-brand-accent/20'
              }`}
              placeholder="name@example.com"
            />
            {errors.email && (
              <p id="email-error" className="mt-1 text-xs text-rose-600">
                {errors.email}
              </p>
            )}
          </div>
        </div>

        {/* Subject */}
        <div>
          <label htmlFor="subject" className="block text-sm font-medium text-slate-700 mb-1">
            Subject <span className="text-rose-500">*</span>
          </label>
          <input
            type="text"
            id="subject"
            name="subject"
            value={formData.subject}
            onChange={(e) => {
              setFormData({ ...formData, subject: e.target.value });
              if (errors.subject) setErrors({ ...errors, subject: undefined });
            }}
            aria-invalid={errors.subject ? 'true' : 'false'}
            aria-describedby={errors.subject ? 'subject-error' : undefined}
            className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 ${
              errors.subject
                ? 'border-rose-400 focus:ring-rose-400 bg-rose-50/20'
                : 'border-slate-300 focus:border-brand-accent focus:ring-brand-accent/20'
            }`}
            placeholder="e.g., Supplier inquiry, product collaboration, or operational contact"
          />
          {errors.subject && (
            <p id="subject-error" className="mt-1 text-xs text-rose-600">
              {errors.subject}
            </p>
          )}
        </div>

        {/* Message */}
        <div>
          <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-1">
            Message Content <span className="text-rose-500">*</span>
          </label>
          <textarea
            id="message"
            name="message"
            rows={5}
            value={formData.message}
            onChange={(e) => {
              setFormData({ ...formData, message: e.target.value });
              if (errors.message) setErrors({ ...errors, message: undefined });
            }}
            aria-invalid={errors.message ? 'true' : 'false'}
            aria-describedby={errors.message ? 'message-error' : undefined}
            className={`w-full px-3.5 py-2.5 rounded-lg border text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 ${
              errors.message
                ? 'border-rose-400 focus:ring-rose-400 bg-rose-50/20'
                : 'border-slate-300 focus:border-brand-accent focus:ring-brand-accent/20'
            }`}
            placeholder="Please detail your inquiry, company details, or relevant questions..."
          />
          {errors.message && (
            <p id="message-error" className="mt-1 text-xs text-rose-600">
              {errors.message}
            </p>
          )}
        </div>

        {/* Privacy Consent Checkbox */}
        <div className="pt-1">
          <div className="flex items-start">
            <div className="flex items-center h-5">
              <input
                id="consent"
                name="consent"
                type="checkbox"
                checked={formData.consent}
                onChange={(e) => {
                  setFormData({ ...formData, consent: e.target.checked });
                  if (errors.consent) setErrors({ ...errors, consent: undefined });
                }}
                className="h-4 w-4 rounded border-slate-300 text-brand-accent focus:ring-brand-accent"
                aria-describedby={errors.consent ? 'consent-error' : undefined}
              />
            </div>
            <div className="ml-3 text-xs text-slate-600 leading-normal">
              <label htmlFor="consent" className="cursor-pointer">
                I understand that the information I submit will be processed solely to review and respond to my commercial inquiry in accordance with Grizo Enterprises&apos;{' '}
                <Link
                  href="/privacy-policy"
                  className="text-brand-accent underline hover:text-brand-accentHover"
                  target="_blank"
                >
                  Privacy Policy
                </Link>
                . <span className="text-rose-500">*</span>
              </label>
            </div>
          </div>
          {errors.consent && (
            <p id="consent-error" className="mt-1.5 text-xs text-rose-600">
              {errors.consent}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg text-sm font-semibold text-white bg-slate-900 hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed transition-colors shadow-xs"
          >
            {isSubmitting ? (
              <span>Validating Submission...</span>
            ) : (
              <>
                <Send className="w-4 h-4" aria-hidden="true" />
                <span>Submit Inquiry</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
