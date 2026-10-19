import { MetadataRoute } from 'next';
import { siteConfig } from '@/config/siteConfig';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = siteConfig.domain
    ? siteConfig.domain.replace(/\/+$/, '')
    : 'https://www.grizoenterprises.co.in';

  const routes = [
    { path: '', priority: 1.0, changeFrequency: 'weekly' as const },
    { path: '/about', priority: 0.9, changeFrequency: 'monthly' as const },
    { path: '/activities', priority: 0.9, changeFrequency: 'weekly' as const },
    { path: '/technology', priority: 0.8, changeFrequency: 'weekly' as const },
    { path: '/marketplace-integrations', priority: 0.8, changeFrequency: 'monthly' as const },
    { path: '/privacy-policy', priority: 0.6, changeFrequency: 'monthly' as const },
    { path: '/terms-of-use', priority: 0.6, changeFrequency: 'monthly' as const },
    { path: '/contact', priority: 0.7, changeFrequency: 'monthly' as const },
  ];

  return routes.map((route) => ({
    url: `${baseUrl}${route.path}`,
    lastModified: new Date(),
    changeFrequency: route.changeFrequency,
    priority: route.priority,
  }));
}
