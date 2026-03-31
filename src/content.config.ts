import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    tags: z.array(z.string()).default([]),
    date: z.coerce.date(),
    path: z.string(),
    excerpt: z.string().default(''),
    cover: z.string().optional(),
    selected: z.boolean().optional(),
    priority: z.number().optional(),
  }),
});

const research = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/research' }),
  schema: z.object({
    title: z.string(),
    tags: z.array(z.string()).default([]),
    date: z.coerce.date(),
    path: z.string(),
    excerpt: z.string().default(''),
    cover: z.string().optional(),
    venue: z.string().optional(),
    authors: z.array(z.object({
      name: z.string(),
      url: z.string().optional(),
    })).default([]),
    links: z.array(z.object({
      name: z.string(),
      url: z.string(),
    })).default([]),
    selected: z.boolean().optional(),
    priority: z.number().optional(),
  }),
});

export const collections = { posts, research };
