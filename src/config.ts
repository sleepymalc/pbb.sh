import type { SiteConfig } from 'astro-academic-theme';

export const siteConfig: SiteConfig = {
  title: 'Pingbang Hu',
  description: "Pingbang Hu's website.",
  siteUrl: 'https://pbb.wtf',
  author: 'Pingbang Hu',
  authorAlternative: '胡平邦',
  avatar: 'avatar.png',
  location: 'San Francisco, CA',

  pages: {
    home: '/',
    posts: 'posts',
    contact: 'contact',
    resume: 'resume',
    tags: 'tags',
    research: 'research',
  },

  professions: [],
  quote: 'I speak $\\TeX$',

  introduction: [
    "I'm a third-year Ph.D. candidate at [*University of Illinois Urbana-Champaign*](https://illinois.edu/) (UIUC) advised by [Jiaqi Ma](https://jiaqima.github.io/), and I also work closely with [Han Zhao](https://hanzhaoml.github.io/). Currently, I'm also an [*Anthropic*](https://www.anthropic.com/) AI Safety Research Fellow and an incoming Ph.D. ML intern at [*Susquehanna International Group*](https://sig.com/).",
    "Previously, I've spent time at [*Amazon AWS AI Lab*](https://aws.amazon.com/ai/) and [*National Institute of Informatics*](https://www.nii.ac.jp/en/). I obtained my Master degree from [*UIUC*](https://illinois.edu/) and [dual Bachelor degree](https://gc.sjtu.edu.cn/academics/ipo/study-abroad/degree-programs/) from [*University of Michigan*](https://umich.edu/) and [*Shanghai Jiao Tong University*](https://www.sjtu.edu.cn/).",
  ],

  researchIntro: [
    "Research-wise, I'm interested in the broad area of ML and AI, with the goal being to draw theoretical insights from practical problems and develop algorithms with provable guarantees and desirable properties such as *efficiency*, *robustness*, and *fairness*. Recently, my research focuses on *understanding **data***, including the following three aspects:",
    '1. **Data Attribution**: Understanding how training data *influences* AI models.\n2. **Data Curation**: How to curate/generate/augment (synthetic) data that further helps models *generalize*?\n3. **Data-Centric Privacy**: Can above be done *without* compromising privacy when safety-critical or sensitive data is involved? This includes (differential) privacy, machine unlearning, etc.',
    "Previously I have worked on *graph neural networks* with [Jiaqi Ma](https://jiaqima.github.io/) and *fast graph algorithms* with [Thatchaphol Saranurak](https://sites.google.com/site/thsaranurak/). Generally speaking, I held (actually *hold*) a strong interest in theoretical stuffs that involves *geometry*.",
  ],

  news: [
    { date: 'Jun. 2026', text: "💼 Incoming intern at [*SIG*](https://sig.com/) Deep Learning team, come hanging out in Philly!" },
    { date: 'Feb. 2026', text: "🏛️ We are organizing the [Data Foundations of AI](https://data-foundations-of-ai.github.io/), come check out if you work on data as well!" },
    { date: 'Jan. 2026', text: "📝 One paper accepted by *ICLR 2026*.", papers: [
      { title: 'PNL', href: './research/PNL/' },
    ] },
    { date: 'Jan. 2026', text: "💼 Starting as an AI safety fellow at [*Anthropic*](https://www.anthropic.com/), come hanging out in San Francisco!" },
    { date: 'Oct. 2025', text: "🏛️ We are organizing the *Symposium on Information Retrieval and Language Models* at *UIUC*!" },
    { date: 'Oct. 2025', text: "🎤 Giving a [tutorial](https://trais-lab.github.io/dattri-reading-group/recording/2025/13/) on recent tricks in computing gradient-based data attribution!", papers: [
      { title: 'GraSS', href: './research/GraSS/' },
    ] },
    { date: 'Sep. 2025', text: "📝 Please check out our new survey paper on data attribution!", papers: [
      { title: 'Survey', href: './research/Data-Attribution-Survey/' },
    ] },
    { date: 'Sep. 2025', text: "📝 Two papers accepted by *NeurIPS 2025*!", papers: [
      { title: 'GraSS', href: './research/GraSS/' },
      { title: 'Unlearning', href: './research/Unlearning-Sample-Inference-Game/' },
    ] },
    { date: 'Aug. 2025', text: "🎓 Get my M.S. Applied Math Degree at *UIUC*!" },
    { date: 'Jul. 2025', text: "🏛️ We are organizing the [3rd Workshop on Regulatable Machine Learning](https://regulatableml.github.io/) in conjunction with *NeurIPS 2025*!" },
    { date: 'Jul. 2025', text: "🎤 Giving a talk on Data Attribution at the [*Guided Generation Group (GGG)*](https://github.com/GuidedGenerationGroup)!", papers: [
      { title: 'Slide', href: './else/Intro-to-DA.pdf', icon: 'fas fa-desktop' },
    ] },
    { date: 'Jun. 2025', text: "✈️ Attending the first [AI Startup School](https://events.ycombinator.com/ai-sus) held by [*Y Combinator*](https://www.ycombinator.com/), see you in San Francisco!" },
    { date: 'Mar. 2025', text: "💼 Interning at [*Amazon AWS AI*](https://aws.amazon.com/ai/) Deep Engine Science team, come hanging out in New York!" },
    { date: 'Jan. 2025', text: "📝 One paper accepted by *ICLR 2025*.", papers: [
      { title: 'Adversarial DA', href: './research/Adversarial-Attack-on-Data-Attribution/' },
    ] },
    { date: 'Nov. 2024', text: "🏆 Received the **Graduate Conference Travel Award** from *UIUC*!" },
    { date: 'Oct. 2024', text: "🏆 Received the **NeurIPS 2024 Scholar Award**, see you in Vancouver!" },
    { date: 'Sep. 2024', text: "📝 Two papers accepted by *NeurIPS 2024* with one ***Spotlight***.", papers: [
      { title: 'dattri', href: './research/dattri/' },
      { title: 'MISS', href: './research/MISS/' },
    ] },
    { date: 'Jun. 2024', text: "📖 We launched the ongoing [*Data Attribution Reading Group*](https://trais-lab.github.io/dattri-reading-group/)." },
    { date: 'May 2024', text: "💼 Interning at [*NII*](https://www.nii.ac.jp/en/), come hanging out in Tokyo!" },
  ],

  misc: "I'm from Taiwan 🇹🇼! In my spare time, I enjoy [*street photography*](https://www.instagram.com/streetmalc/) 📷 and playing drums 🥁.",

  education: [
    {
      date: 'Aug. 2023 - Present',
      icon: 'user-graduate',
      title: 'Ph.D. in Information Science',
      location: 'University of Illinois Urbana-Champaign',
    },
    {
      date: 'Aug. 2023 - Aug. 2025',
      icon: 'scroll',
      title: 'M.S. in Mathematics',
      location: 'University of Illinois Urbana-Champaign',
    },
    {
      date: 'Sep. 2021 - May 2023',
      icon: 'graduation-cap',
      title: 'B.S. in Computer Science',
      minor: 'Mathematics',
      location: 'University of Michigan',
    },
    {
      date: 'Sep. 2019 - Aug. 2023',
      icon: 'graduation-cap',
      title: 'B.E. in Electrical and Computer Engineering',
      minor: 'Computer Science',
      location: 'Shanghai Jiao Tong University',
    },
  ],

  social: [
    { url: '/cv.pdf', icon: ['ai', 'cv'] },
    { url: 'https://scholar.google.com/citations?user=lPlQpqoAAAAJ&hl=en', icon: ['fa', 'graduation-cap'] },
    { url: 'https://github.com/sleepymalc', icon: ['fab', 'github'] },
    { url: 'https://www.linkedin.com/in/ping-bang-hu-78a190215/', icon: ['fab', 'linkedin'] },
    { url: 'https://X.com/PingbangHu', icon: ['fab', 'x-twitter'] },
    { url: 'mailto:pbb@illinois.edu', icon: ['fa', 'envelope'] },
  ],

  awards: [
    { date: 'Oct. 2025', title: 'Anthropic AI Safety Research Fellowship', organization: 'Anthropic' },
    { date: 'Oct. 2021', title: 'Hong Kong, Macao and Taiwan Overseas Chinese Student Scholarship', organization: 'Shanghai Jiao Tong University' },
    { date: 'Nov. 2020', title: 'Undergraduate Excellent Scholarship', organization: 'Shanghai Jiao Tong University' },
    { date: 'Jun. 2020', title: 'Bao Gang Excellent Scholarship', organization: 'Shanghai Jiao Tong University' },
    { date: 'Dec. 2019', title: 'Hong Kong, Macao and Taiwan Overseas Chinese Student Scholarship', organization: 'Shanghai Jiao Tong University' },
  ],

  interests: [
    { icon: 'hand-holding-usd', title: 'Data Valuation' },
    { icon: 'laptop-code', title: 'Algorithmic Design' },
    { icon: 'chart-line', title: 'Mathematical Statistics' },
    { icon: 'square-root-variable', title: 'Mathematical Analysis' },
    { icon: 'brain', title: 'Learning Theory' },
    { icon: 'project-diagram', title: 'Graph Theory' },
    { icon: 'shapes', title: 'Geometry & Topology' },
  ],

  experience: [],

  researchExperience: [
    {
      role: 'Machine Learning Ph.D. Intern',
      organization: 'Susquehanna International Group',
      date: 'Jun. 2026 - Aug. 2026',
      description: 'TBA',
      icon: 'briefcase',
    },
    {
      role: 'AI Safety Research Fellow',
      organization: 'Anthropic',
      date: 'Jan. 2026 - May 2026',
      description: '<strong>Data-Safety</strong>: Secret.',
      icon: 'shield-halved',
    },
    {
      role: 'Applied Scientist Intern',
      organization: 'Amazon AWS AI Lab',
      date: 'May 2025 - Aug. 2025',
      description:
        '<strong>Data Curation</strong>: Investigate data attribution with synthetic data generation to curate high-quality dataset.',
      icon: 'briefcase',
    },
    {
      role: 'Research Intern',
      organization: 'National Institute of Informatics',
      date: 'May 2024 - Aug. 2024',
      description:
        '<a href="/research/PNL/"><strong>Pseudo-Nonlinear Data Augmentation</strong></a>: Develop an information-geometric data augmentation algorithm advised by <a href="https://mahito.info/index_e.html">Mahito Sugiyama</a>. Won the <strong>Excellent Internship Evaluation</strong> 😬',
      icon: 'flask',
    },
    {
      role: 'Undergraduate Researcher',
      organization: 'University of Michigan',
      date: 'May 2022 - Apr. 2023',
      description:
        '<strong>Deep Learning Foundation</strong>: Develop various techniques to understand deep neural networks advised by <a href="https://weihu.me/">Wei Hu</a> under the <a href="https://sure.engin.umich.edu/">SURE Program</a>.',
      icon: 'microscope',
    },
    {
      role: 'Undergraduate Researcher',
      organization: 'University of Michigan',
      date: 'Mar. 2022 - Dec. 2022',
      description:
        '<strong>Detection Sets</strong>: Design the first almost linear time algorithm on finding minimal balanced cuts advised by <a href="https://sites.google.com/site/thsaranurak/">Thatchaphol Saranurak</a>.',
      icon: 'microscope',
    },
  ],

  teachingExperience: [
    {
      course: '<a href="https://ischool.illinois.edu/degrees-programs/courses/is527">IS527 Network Analysis</a>',
      level: 'Graduate',
      role: 'Graduate Teaching Assistant',
      institution: 'University of Illinois Urbana-Champaign',
      date: 'Jan. 2025 - May 2025, Jan. 2026 - May 2026',
      icon: 'chalkboard-user',
    },
    {
      course: '<a href="https://mahdi.ch/eecs475/">EECS475 Introduction to Cryptography</a>',
      level: 'Undergraduate',
      role: 'Instructional Aide',
      institution: 'University of Michigan',
      date: 'Jan. 2023 - May 2023',
      notes: '<a href="/posts/Notes#introduction-to-cryptography-eecs475-university-of-michigan-ta">Notes</a> available.',
      icon: 'lock',
    },
    {
      course: '<a href="https://mahdi.ch/eecs572/">EECS572 Randomness and Computation</a>',
      level: 'Graduate',
      role: 'Instructional Aide',
      institution: 'University of Michigan',
      date: 'Aug. 2022 - Dec. 2022',
      notes: '<a href="/posts/Notes#randomness-and-computation-eecs572-university-of-michigan-ta">Notes</a> available.',
      icon: 'dice',
    },
    {
      course: '<a href="https://umji.sjtu.edu.cn/~horst/teaching/vv285.html">VV285 Honor Mathematics III</a>',
      level: 'Undergraduate',
      role: 'Teaching Assistant',
      institution: 'Shanghai Jiao Tong University',
      date: 'May 2021 - Aug. 2021',
      notes: 'Also organized the first <a href="https://github.com/sleepymalc/JIntegrationBee"><em>JIntegration Bee</em></a> competition!',
      icon: 'square-root-variable',
    },
    {
      course: '<a href="https://umji.sjtu.edu.cn/~horst/teaching/vv186.html">VV186 Honor Mathematics II</a>',
      level: 'Undergraduate',
      role: 'Teaching Assistant',
      institution: 'Shanghai Jiao Tong University',
      date: 'Sep. 2020 - Dec. 2020',
      icon: 'square-root-variable',
    },
  ],

  service: {
    organizing: [
      {
        role: 'Workshop Organizer',
        title: '<a href="https://regulatableml.github.io/">The 3rd Workshop on Regulatable ML</a> @NeurIPS 2025',
        date: 'Dec. 2025',
        description: 'Toward bridging the gap between state-of-the-art ML safety/security research and evolving regulatory frameworks.',
        icon: 'users',
      },
      {
        role: 'Community Organizer',
        title: '<a href="https://data-foundations-of-ai.github.io/">Data Foundations of AI</a>',
        date: 'Feb. 2026 - Present',
        description: 'Focus on the recent advances of data foundations of modern generative AI.',
        icon: 'globe',
      },
      {
        role: 'Reading Group Organizer',
        title: '<a href="https://trais-lab.github.io/dattri-reading-group/">Data Attribution Reading Group</a>',
        date: 'Jun. 2024 - Present',
        description: 'Focus on the recent advances of data attribution methods in the era of Generative AI.',
        icon: 'book-open',
      },
      {
        role: 'Reading Group Organizer',
        title: 'Statistical Learning Theory',
        date: 'Jan. 2024 - Jan. 2025',
        description:
          'A thorough reading on <a href="https://www.math.uci.edu/~rvershyn/">Roman Vershynin</a>\'s <a href="https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-book.html">High-Dimensional Probability</a>. <a href="/else/HDP_solution.pdf">Solution</a> available.',
        icon: 'book-open',
      },
    ],
    reviewing: {
      conferences: 'ICML 2026, ICLR 2026, NeurIPS 2025, ICLR 2025, ICML 2024, IEEE BigData 2023',
      journals: 'TMLR',
      programCommittee: 'AAAI 2025',
    },
  },

  tagColors: [
    'magenta', 'red', 'volcano', 'orange', 'gold',
    'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple',
  ],

  tags: [
    { id: 'python', name: 'Python', description: 'A general purpose programming language.', color: '#f9c646' },
    { id: 'data', name: 'Data', description: 'Data-related research.', color: '#096dd9' },
    { id: 'attribution', name: 'Attribution', description: 'Data attribution methods.', color: '#531dab' },
    { id: 'privacy', name: 'Privacy', description: 'Privacy-preserving techniques.', color: '#c41d7f' },
    { id: 'graph', name: 'Graph', description: 'Graph theory and algorithms.', color: '#389e0d' },
    { id: 'math', name: 'Math', description: 'Mathematics and analysis.', color: '#d46b08' },
    { id: 'latex', name: 'LaTeX', description: 'LaTeX typesetting.', color: '#08979c' },
    { id: 'tools', name: 'Tools', description: 'Developer tools and workflows.', color: '#1d39c4' },
  ],

  defaultLanguage: 'en',
  contactFormUrl: 'https://getform.io/f/09a3066f-c638-40db-ad59-05e4ed71e451',
  googleAnalyticsId: 'G-734WCNHH4E',

  wakatime: {
    username: 'sleepymalc',
    activity: 'eb201619-dfe8-485e-b683-11ce3475ad61',
    language: 'cccb943f-2bfc-47e5-b218-c56b858c1a90',
  },
};
