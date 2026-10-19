/**
 * Central Business and Site Configuration for Grizo Enterprises
 * 
 * All details here represent verified business facts as specified by the business owner.
 * Any unconfigured fields are handled gracefully by UI components without exposing raw placeholder tokens.
 */

export interface BusinessConfig {
  name: string;
  legalStructure: string;
  country: string;
  gstRegistered: boolean;
  gstin?: string;
  tagline: string;
  supportingPhrase: string;
  description: string;
  primaryMarketplace: string;
  techEnvironment: string;
  currency: string;
}

export interface ContactConfig {
  email: string;
  phone?: string;
  address?: string;
}

export interface ApplicationConfig {
  status: 'Under Development' | 'Operational' | 'Testing Phase';
  statusNote: string;
  isBackendEmailConfigured: boolean;
}

export interface SiteConfig {
  business: BusinessConfig;
  contact: ContactConfig;
  application: ApplicationConfig;
  domain: string;
  privacyEffectiveDate: string;
  termsEffectiveDate: string;
  socialLinks: Array<{ label: string; url: string }>;
  navigation: Array<{ label: string; href: string }>;
}

export const siteConfig: SiteConfig = {
  business: {
    name: "Grizo Enterprises",
    legalStructure: "Sole Proprietorship",
    country: "India",
    gstRegistered: true,
    gstin: process.env.NEXT_PUBLIC_BUSINESS_GSTIN || "",
    tagline: "Smarter Commerce. Better Decisions.",
    supportingPhrase: "Building efficient, data-informed e-commerce operations.",
    description:
      "Grizo Enterprises is an India-based sole proprietorship focused on e-commerce and online retail. We are developing technology-enabled workflows to support product research, market analysis, pricing decisions, listing management, and inventory planning.",
    primaryMarketplace: "Amazon India (amazon.in)",
    techEnvironment: "Google Antigravity",
    currency: "INR (₹)",
  },
  contact: {
    email: process.env.NEXT_PUBLIC_CONTACT_EMAIL || "jsskws.av@gmail.com",
    phone: process.env.NEXT_PUBLIC_CONTACT_PHONE || "",
    address: process.env.NEXT_PUBLIC_BUSINESS_ADDRESS || "",
  },
  application: {
    status: "Under Development",
    statusNote:
      "Internal application under development. Software workflows and marketplace API integrations are actively being engineered for internal business operations and are not yet operational in live marketplace production.",
    // Contact form backend status: false until an actual email/SMTP service is integrated
    isBackendEmailConfigured: process.env.NEXT_PUBLIC_ENABLE_CONTACT_BACKEND === "true",
  },
  // Production domain verified by business owner
  domain: process.env.NEXT_PUBLIC_SITE_URL || "https://www.grizoenterprises.co.in",
  privacyEffectiveDate: "October 2026",
  termsEffectiveDate: "October 2026",
  // No fabricated social media accounts
  socialLinks: [],
  navigation: [
    { label: "Home", href: "/" },
    { label: "About Us", href: "/about" },
    { label: "Business Activities", href: "/activities" },
    { label: "Technology", href: "/technology" },
    { label: "Marketplace Integrations", href: "/marketplace-integrations" },
    { label: "Privacy Policy", href: "/privacy-policy" },
    { label: "Contact Us", href: "/contact" },
  ],
};

/**
 * Returns canonical URL if configured, otherwise returns relative path
 */
export function getCanonicalUrl(path: string = ""): string {
  if (siteConfig.domain && siteConfig.domain.startsWith("http")) {
    const cleanDomain = siteConfig.domain.replace(/\/+$/, "");
    const cleanPath = path.startsWith("/") ? path : `/${path}`;
    return `${cleanDomain}${cleanPath}`;
  }
  return path.startsWith("/") ? path : `/${path}`;
}
