import type { SiteConfig } from '../types.js';

export interface NavItem {
  label: string;
  href: string;
  exact: boolean;
}

export function getNavItems(config: SiteConfig): NavItem[] {
  return [
    { label: 'About', href: '/', exact: true },
    { label: 'Experience', href: '/experience/', exact: false },
    { label: 'Research', href: `/${config.pages.research}/`, exact: false },
    { label: 'Posts', href: `/${config.pages.posts}/`, exact: false },
  ];
}

export function isNavActive(currentPath: string, href: string, exact: boolean): boolean {
  if (exact) return currentPath === href || currentPath === href.replace(/\/$/, '');
  return currentPath.startsWith(href) || currentPath.startsWith(href.replace(/\/$/, ''));
}
