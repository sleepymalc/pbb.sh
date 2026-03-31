/**
 * Entity registry: maps organization names to brand colors and optional logos.
 * Colors are used for styled inline mentions; logos appear in the experience timeline.
 */

export interface Entity {
  /** Display name (used for matching in text) */
  name: string;
  /** Alternative names / abbreviations to also match */
  aliases?: string[];
  /** Brand color */
  color: string;
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
    logo: '/logos/uiuc.png',
  },
  {
    name: 'University of Michigan',
    aliases: ['UMich'],
    color: '#FFCB05',
    logo: '/logos/umich.png',
  },
  {
    name: 'Shanghai Jiao Tong University',
    aliases: ['SJTU'],
    color: '#9D2235',
    logo: '/logos/sjtu.png',
  },
  {
    name: 'Anthropic',
    color: '#D4A574',
    logo: '/logos/anthropic.svg',
  },
  {
    name: 'Amazon AWS AI Lab',
    aliases: ['Amazon AWS AI'],
    color: '#FF9900',
    logo: '/logos/amazon.png',
    logoDark: '/logos/amazon-dark.png',
  },
  {
    name: 'Susquehanna International Group',
    aliases: ['SIG', 'SIG Deep Learning Team'],
    color: '#003366',
    logo: '/logos/sig.jpeg',
  },
  {
    name: 'National Institute of Informatics',
    aliases: ['NII'],
    color: '#1B4F72',
    logo: '/logos/nii.png',
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
    html = html.replace(emPattern, (_match, text) => {
      return `<em class="entity-mention" style="--entity-color: ${entity.color}">${logoHtml}${text}</em>`;
    });
  }
  return html;
}

/** Get entity by org name */
export function getEntity(orgName: string): Entity | undefined {
  return entityLookup.get(orgName);
}
