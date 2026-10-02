/**
 * Helpers for rendering venue strings and presentation distinctions
 * (Oral, Spotlight, Best Paper, …) as a highlighted `.honor-badge` pill.
 * The pill's styles live in styles/global.css so that both Venue.astro and
 * post-processed markdown (e.g. news items) share one look.
 */

/** Parenthetical distinctions that deserve a highlighted badge. */
export const DISTINCTION = /\b(oral|spotlight|best|award|outstanding|honou?rable|featured|highlight|notable)\b/i;

export interface VenueParts {
  /** Venue name with the distinction removed, e.g. "NeurIPS 2024 D&B". */
  name: string;
  /** The distinction itself, e.g. "Spotlight", or null if none. */
  honor: string | null;
}

/** Split "NeurIPS 2024 D&B (Spotlight)" into its venue name and distinction. */
export function splitVenue(venue: string): VenueParts {
  const m = venue.match(/^(.*?)\s*\(([^()]+)\)\s*$/);
  if (m && DISTINCTION.test(m[2])) {
    return { name: m[1], honor: m[2].trim() };
  }
  return { name: venue, honor: null };
}

/** HTML for a single honor badge. `text` must already be HTML-escaped. */
export function honorBadge(text: string): string {
  const key = text.toLowerCase().replace(/"/g, '&quot;');
  return `<span class="honor-badge" data-honor="${key}">${text}</span>`;
}

/**
 * Post-process rendered markdown: bold-italic distinctions such as
 * `***Oral***` (rendered as nested <em>/<strong>) become honor badges.
 * Other bold-italic text is left untouched.
 */
export function highlightHonors(html: string): string {
  return html.replace(
    /<(em|strong)><(em|strong)>([^<]+)<\/\2><\/\1>/g,
    (match, _outer, _inner, text: string) => (DISTINCTION.test(text) ? honorBadge(text) : match),
  );
}
