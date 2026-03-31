import { marked } from 'marked';

export function renderMarkdown(text: string): string {
  return marked.parse(text, { async: false }) as string;
}

export function renderInlineMarkdown(text: string): string {
  return marked.parseInline(text, { async: false }) as string;
}
