import React from 'react';
import { siteConfig, getCanonicalUrl } from '@/config/siteConfig';

export default function StructuredData() {
  const schema: Record<string, any> = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: siteConfig.business.name,
    legalName: siteConfig.business.name,
    description: siteConfig.business.description,
    url: siteConfig.domain ? siteConfig.domain : undefined,
    areaServed: {
      '@type': 'Country',
      name: 'India',
    },
    knowsAbout: [
      'E-commerce',
      'Online Retail',
      'Product Research',
      'Inventory Management',
      'Commercial Operations',
    ],
  };

  // Only include contactPoint if email is actually configured
  if (siteConfig.contact.email) {
    schema.contactPoint = {
      '@type': 'ContactPoint',
      contactType: 'Customer Support and Inquiries',
      email: siteConfig.contact.email,
      availableLanguage: ['English', 'Hindi'],
    };
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
