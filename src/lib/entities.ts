/**
 * Entity registry: maps organization names to brand colors and optional logos.
 * Colors are used for styled inline mentions; logos appear in the experience timeline.
 */

export interface Entity {
  /** Display name (used for matching in text) */
  name: string;
  /** Alternative names / abbreviations to also match */
  aliases?: string[];
  /** Brand color (light mode) */
  color: string;
  /** Brand color (dark mode) — defaults to color if not set */
  colorDark?: string;
  /** Path to logo image in /public (optional, for experience page) */
  logo?: string;
  /** Alternative logo for dark mode */
  logoDark?: string;
}

export const entities: Entity[] = [
  {
    name: 'University of Illinois Urbana-Champaign',
    aliases: ['UIUC'],
    color: '#E84A27',
    colorDark: '#E84A27',
    logo: '/logos/uiuc.svg',
  },
  {
    name: 'University of Michigan',
    aliases: ['UMich'],
    color: '#FFCB05',
    colorDark: '#FFCB05',
    logo: '/logos/umich.png',
  },
  {
    name: 'Shanghai Jiao Tong University',
    aliases: ['SJTU'],
    color: '#9D2235',
    colorDark: '#9D2235',
    logo: '/logos/sjtu.png',
  },
  {
    name: 'Anthropic',
    color: '#C4813A',
    colorDark: '#D4A574',
    logo: '/logos/anthropic.svg',
  },
  {
    name: 'Amazon AWS AI Lab',
    aliases: ['Amazon AWS AI'],
    color: '#FF9900',
    colorDark: '#FF9900',
    logo: '/logos/amazon.png',
    logoDark: '/logos/amazon-dark.png',
  },
  {
    name: 'Susquehanna International Group',
    aliases: ['SIG', 'SIG Deep Learning Team'],
    color: '#2E6DB4',
    colorDark: '#2E6DB4',
    logo: '/logos/sig.jpeg',
  },
  {
    name: 'National Institute of Informatics',
    aliases: ['NII'],
    color: '#7B5EA7',
    colorDark: '#7B5EA7',
    logo: '/logos/nii.png',
    logoDark: '/logos/nii.png',
  },
];

/** Build a lookup from all names/aliases to their entity */
const entityLookup = new Map<string, Entity>();
for (const e of entities) {
  entityLookup.set(e.name, e);
  for (const alias of e.aliases ?? []) {
    entityLookup.set(alias, e);
  }
}

/**
 * Post-process rendered HTML to wrap entity mentions in styled spans.
 * Only matches text that is already inside <em> or <strong> tags (i.e., markdown emphasis),
 * so plain mentions are not affected.
 */
export function highlightEntities(html: string): string {
  for (const [name, entity] of entityLookup) {
    const escapedName = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    let logoHtml = '';
    if (entity.logo && entity.logoDark) {
      logoHtml = `<img src="${entity.logo}" alt="" class="entity-icon entity-icon-light" /><img src="${entity.logoDark}" alt="" class="entity-icon entity-icon-dark" />`;
    } else if (entity.logo) {
      logoHtml = `<img src="${entity.logo}" alt="" class="entity-icon" />`;
    }

    // Pattern: <em>Name</em>
    const emPattern = new RegExp(`<em>(${escapedName})</em>`, 'g');
    const darkColor = entity.colorDark ?? entity.color;
    html = html.replace(emPattern, (_match, text) => {
      return `<em class="entity-mention" style="--entity-color: ${entity.color}; --entity-color-dark: ${darkColor}">${logoHtml}${text}</em>`;
    });
  }
  return html;
}

/** Get entity by org name */
export function getEntity(orgName: string): Entity | undefined {
  return entityLookup.get(orgName);
}
