# Grizo Enterprises — Official Business Website

Official, production-grade corporate website for **Grizo Enterprises**, an Indian sole proprietorship registered under GST.

This website establishes a professional online presence and transparently details the business's e-commerce operations, commercial research workflows, and the active internal development of its proprietary e-commerce management software. It is specifically designed and verified to support Amazon Selling Partner API (SP-API) developer registration without false claims or unverified statements.

---

## 1. Verified Business Profile

* **Legal Entity Name:** Grizo Enterprises
* **Business Structure:** Sole Proprietorship
* **Country of Registration:** India
* **Tax Status:** GST-Registered Taxpayer
* **Primary Activities:** E-commerce, online retail, product and category research, pricing evaluation, and internal operational software development
* **Primary Target Marketplace:** Amazon India (`amazon.in`)
* **Technology Development Environment:** Google Antigravity
* **Internal Software Status:** Actively Under Development (Internal use only)
* **Website Currency:** Indian Rupee (INR / ₹)
* **Proprietor Information:** Maintained in accordance with privacy protection standards; not publicly broadcasted without necessity.

---

## 2. Implemented Pages & Information Architecture

All pages are pre-rendered statically (SSG) with semantic HTML5, accessible ARIA attributes, and responsive mobile-first layouts:

1. **Home (`/`)**:
   * Header with original geometric wordmark logo and responsive navigation drawer.
   * Hero section with business identity, verified tagline (*“Smarter Commerce. Better Decisions.”*), and factual description.
   * Business Overview introducing the GST-registered sole proprietorship.
   * 6 Business Activities overview cards.
   * Technology & Automation section detailing internal tool capabilities.
   * Subtle status badge: *“Internal application under development.”*
   * Responsible Technology Statement (Human-in-the-Loop governance).
   * Compliant corporate footer with statutory and trademark notices.
2. **About Us (`/about`)**:
   * Official verbatim business statement.
   * Four comprehensive sections: *Our Business*, *Our Approach*, *Technology & Innovation*, and *Responsible Business Operations*.
   * Factual narrative with zero fabricated employee counts or revenues.
3. **Business Activities (`/activities`)**:
   * Comprehensive operational scope across all 9 commercial and technological functions:
     1. Online retail and e-commerce operations.
     2. Product category and market research.
     3. Supplier and procurement research.
     4. Product cost and profitability evaluation.
     5. Product catalogue and listing preparation.
     6. Pricing and competition analysis.
     7. Inventory and order monitoring.
     8. Sales performance reporting.
     9. Internal software and workflow development.
   * Disclaimers clarifying that research outcomes depend on permitted data availability and do not constitute sales guarantees.
4. **Technology & E-Commerce Automation (`/technology`)**:
   * Detailed breakdown of modules being engineered in Google Antigravity:
     * Section A: Product Opportunity Research.
     * Section B: Profitability & Unit Economics Analysis (with explicit fee and GST formulas).
     * Section C: Listing Support & Catalogue Content.
     * Section D: Inventory & Stock Monitoring.
     * Section E: Operational Reporting & Executive Briefings.
     * Section F: Mandatory Human Approval for Commercial Commitments (purchases, payments, pricing, listings).
     * Section G: Data Accuracy, Classification, and Evidence Provenance (distinguishing official data, market estimates, mathematical calculations, and AI drafts).
5. **Marketplace Integrations & Data Use (`/marketplace-integrations`)**:
   * Official disclosure regarding planned use of authorized marketplace APIs (Amazon SP-API).
   * Strict non-affiliation and trademark disclaimer.
   * Explicit statements that Grizo Enterprises is an independent entity and does not claim endorsement or certification from Amazon.
   * Data governance commitments (zero third-party data selling, encryption in transit, least-privilege access).
6. **Privacy Policy (`/privacy-policy`)**:
   * Comprehensive 10-section privacy policy drafted conservatively.
   * Transparent declaration that marketplace API integration is currently in development.
   * Pre-publication verification checklist for the business owner.
7. **Terms of Use (`/terms-of-use`)**:
   * Website purpose, accuracy, acceptable use, intellectual property, and external links.
   * Explicit disclaimer that market research and technology descriptions do not guarantee commercial outcomes.
8. **Contact Us (`/contact`)**:
   * Business entity details, country of operation, and configurable fields.
   * Interactive contact form with client-side validation, anti-spam honeypot, and privacy consent checkbox.
   * Transparent status notice informing visitors that backend email dispatch is in pre-activation mode (never silently discards submissions or shows false confirmation).
9. **Custom 404 (`/not-found`)**:
   * Accessible, branded error page with navigation shortcuts back to core sections.
10. **Technical SEO Endpoints**:
    * Dynamic XML Sitemap (`/sitemap.xml`) indexing all public routes.
    * Dynamic Robots.txt (`/robots.txt`) with sitemap declaration.

---

## 3. Technology Stack & Design Specifications

* **Framework:** Next.js 16 (App Router, Static Site Generation)
* **Language:** TypeScript 5.9 (Strict mode enabled)
* **Styling:** Tailwind CSS 3.4 with custom corporate design tokens
* **Icons:** Lucide React (Clean, lightweight SVG icons)
* **Security Headers:**
  * `X-Frame-Options: SAMEORIGIN`
  * `X-Content-Type-Options: nosniff`
  * `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
  * `Referrer-Policy: strict-origin-when-cross-origin`
  * `Permissions-Policy: camera=(), microphone=(), geolocation=(), browsing-topics=()`
* **Structured Data:** JSON-LD `Organization` schema strictly reflecting verified business facts.

---

## 4. Local Development & Testing Instructions

### Prerequisites
* Node.js v18+ (Node.js v20 LTS recommended)
* npm v9+

### 1. Running Locally
Navigate to the `website` directory and run:

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Open `http://localhost:3000` in your web browser.

### 2. Creating a Production Build
To verify production compilation and static page generation:

```bash
npm run build
```

### 3. Serving the Production Build Locally
```bash
npm run start
```

---

## 5. Configuration Guide

All customizable business fields are centralized in `src/config/siteConfig.ts` and can also be overridden via environment variables:

| Variable | Config Path | Description | Default / Current Value |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_SITE_URL` | `siteConfig.domain` | Production domain | *Empty (configured upon domain purchase)* |
| `NEXT_PUBLIC_CONTACT_EMAIL` | `siteConfig.contact.email` | Official business email | *Empty (configured upon domain activation)* |
| `NEXT_PUBLIC_CONTACT_PHONE` | `siteConfig.contact.phone` | Business telephone | *Empty (optional)* |
| `NEXT_PUBLIC_BUSINESS_ADDRESS` | `siteConfig.contact.address` | Registered address | *Empty (optional for public disclosure)* |
| `NEXT_PUBLIC_BUSINESS_GSTIN` | `siteConfig.business.gstin` | GSTIN identifier | *Empty (optional for public disclosure)* |
| `NEXT_PUBLIC_ENABLE_CONTACT_BACKEND` | `siteConfig.application.isBackendEmailConfigured` | Activates contact form API | `false` |

> **Privacy Guard:** Unconfigured fields are displayed with clean, professional contextual notes rather than broken tokens (such as `[INSERT EMAIL HERE]`).

---

## 6. Deployment Instructions (Vercel / Netlify / Custom Domain)

### Deploying to Vercel (Recommended)
1. Push this repository to your GitHub, GitLab, or Bitbucket account.
2. Sign in to [Vercel](https://vercel.com) and click **"Add New Project"**.
3. Import your repository.
4. In the project settings:
   * **Root Directory:** Set to `website`
   * **Framework Preset:** Next.js
   * **Build Command:** `npm run build`
   * **Output Directory:** `.next`
5. Under **Environment Variables**, add:
   * `NEXT_PUBLIC_SITE_URL`: `https://yourdomain.com` (your genuine custom domain)
   * `NEXT_PUBLIC_CONTACT_EMAIL`: `contact@yourdomain.com`
6. Click **Deploy**. Vercel will build and deploy the website with automated global CDN distribution and SSL/TLS HTTPS certificates.

### Connecting Your Custom Domain
1. In Vercel, navigate to **Project Settings > Domains**.
2. Enter your registered domain name (e.g. `grizoenterprises.in` or `grizoenterprises.com`).
3. Add the DNS records (CNAME and A record) provided by Vercel to your domain registrar (e.g., GoDaddy, Namecheap, Google Domains).
4. Vercel will automatically provision a free Let's Encrypt SSL certificate once DNS propagates.

---

## 7. Amazon SP-API Developer Registration Guidance

When filling out your **Amazon Selling Partner API (SP-API) Developer Registration Form**:

1. **Organization Website:** Provide your live HTTPS domain (e.g., `https://grizoenterprises.in`).
2. **Organization / Legal Entity Name:** Enter `Grizo Enterprises`.
3. **Application Type:** Select **Private Developer** (internal application for your own seller account).
4. **Application Purpose & Data Governance:** 
   * Direct the reviewer to your **Marketplace Integrations** page (`/marketplace-integrations`) and **Technology** page (`/technology`).
   * Highlight your **Human-in-the-Loop approval gates** (Section F of the Technology page) and strict **Data Governance Commitments** (Section G).
5. **Data Protection & Privacy Policy:** Provide the direct link to `/privacy-policy`.
