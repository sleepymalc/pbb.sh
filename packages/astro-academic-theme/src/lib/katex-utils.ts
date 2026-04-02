import katex from 'katex';

export function renderInlineKatex(text: string): string {
  return text.replace(/\$([^$]+)\$/g, (_match: string, tex: string) =>
    katex.renderToString(tex, { throwOnError: false }));
}
