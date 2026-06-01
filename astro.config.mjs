// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { rehypeHeadingIds } from '@astrojs/markdown-remark';

export default defineConfig({
  site: 'https://pbb.wtf',
  trailingSlash: 'always',
  integrations: [
    mdx(),
    sitemap(),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    remarkPlugins: [remarkMath],
    // Collect heading IDs/text BEFORE KaTeX runs, otherwise the TOC picks up
    // KaTeX's triplicated text (visible HTML + MathML + TeX annotation), e.g. "$K$" → "KKK".
    rehypePlugins: [rehypeHeadingIds, rehypeKatex],
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
    },
  },
});
