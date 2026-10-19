import type { Metadata } from 'next';
import './globals.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import StructuredData from '@/components/StructuredData';
import { siteConfig } from '@/config/siteConfig';

export const metadata: Metadata = {
  title: {
    default: `${siteConfig.business.name} | ${siteConfig.business.tagline}`,
    template: `%s | ${siteConfig.business.name}`,
  },
  description: siteConfig.business.description,
  keywords: [
    'Grizo Enterprises',
    'E-commerce India',
    'Online Retail',
    'Amazon India Seller',
    'Product Research',
    'E-commerce Management Software',
    'GST Registered Business',
    'Indian Sole Proprietorship',
  ],
  authors: [{ name: siteConfig.business.name }],
  creator: siteConfig.business.name,
  publisher: siteConfig.business.name,
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_IN',
    siteName: siteConfig.business.name,
    title: `${siteConfig.business.name} | ${siteConfig.business.tagline}`,
    description: siteConfig.business.description,
  },
  twitter: {
    card: 'summary_large_image',
    title: `${siteConfig.business.name} | ${siteConfig.business.tagline}`,
    description: siteConfig.business.description,
  },
  icons: {
    icon: '/favicon.svg',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <StructuredData />
      </head>
      <body className="flex flex-col min-h-screen bg-white text-slate-900 antialiased selection:bg-sky-100 selection:text-sky-900">
        {/* Skip to main content link for keyboard accessibility */}
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 z-50 px-4 py-2 bg-brand-accent text-white font-medium rounded-md shadow-md"
        >
          Skip to main content
        </a>
        <Header />
        <main id="main-content" className="flex-grow">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
