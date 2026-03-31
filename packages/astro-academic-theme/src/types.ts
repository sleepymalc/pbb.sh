export interface SiteConfig {
  title: string;
  description: string;
  siteUrl: string;
  author: string;
  authorAlternative?: string;
  avatar: string;
  location?: string;
  email?: string;
  birthday?: string;

  pages: {
    home: string;
    posts: string;
    contact: string;
    resume: string;
    tags: string;
    research: string;
  };

  professions: string[];
  introduction: string[];

  education: Education[];
  social: SocialLink[];
  awards: Award[];
  interests: Interest[];
  experience: ExperienceGroup[];
  researchExperience?: ResearchExperience[];
  teachingExperience?: TeachingExperience[];
  service?: ServiceSection;

  tagColors: string[];
  tags: TagDefinition[];

  defaultLanguage?: string;
  contactFormUrl?: string;
  googleAnalyticsId?: string;
  disqusScript?: string;
  wakatime?: WakatimeConfig;
}

export interface Education {
  date: string;
  icon?: string;
  title: string;
  minor?: string;
  location: string;
}

export interface SocialLink {
  url: string;
  icon: string | [string, string];
  label?: string;
}

export interface Award {
  date: string;
  title: string;
}

export interface Interest {
  icon: string;
  title: string;
}

export interface ExperienceGroup {
  title: string;
  position: 'left' | 'right';
  data: ExperienceItem[];
}

export interface ExperienceItem {
  title: string;
  date: string;
  location: string;
  description: string;
}

export interface ResearchExperience {
  role: string;
  organization: string;
  date: string;
  description: string;
  icon?: string;
}

export interface TeachingExperience {
  course: string;
  level: string;
  role: string;
  institution: string;
  date: string;
  notes?: string;
  icon?: string;
}

export interface OrganizingEntry {
  role: string;
  title: string;
  date: string;
  description: string;
  icon?: string;
}

export interface ServiceSection {
  organizing: OrganizingEntry[];
  reviewing: {
    conferences: string;
    journals: string;
    programCommittee: string;
  };
}

export interface TagDefinition {
  id: string;
  name: string;
  description: string;
  color: string;
}

export interface WakatimeConfig {
  username: string;
  activity: string;
  language: string;
  editor?: string;
  os?: string;
}

export interface ResearchFrontmatter {
  title: string;
  tags: string[];
  date: Date;
  path: string;
  excerpt: string;
  cover?: string;
  venue?: string;
  authors?: Author[];
  links?: ResearchLink[];
  selected?: boolean;
  priority?: number;
}

export interface Author {
  name: string;
  url?: string;
}

export interface ResearchLink {
  name: string;
  url: string;
}

export interface PostFrontmatter {
  title: string;
  tags: string[];
  date: Date;
  path: string;
  excerpt: string;
  cover?: string;
}
