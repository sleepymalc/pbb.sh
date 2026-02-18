module.exports = {
	avatar: 'avatar.png',
	pathPrefix: '',
	tocMaxDepth: 2,
	excerptMaxLength: 500,
	postsForArchivePage: 3,
	siteUrl: 'https://pbb.sh/',
	title: 'Pingbang Hu',
	description: 'Pingbang Hu\'s website.',
	author: 'Pingbang Hu',
	authorAlternative: '胡平邦',
	// birthday: 'Nov. 10, 2000',
	location: 'San Francisco, CA',
	// email: 'pbb@illinois.edu',
	pages: {
		home: '/',
		posts: 'posts',
		contact: 'contact',
		resume: 'resume',
		tags: 'tags',
		research: 'research',
	},
	professions: [
		'I speak TeX'
	],
	introduction: [
		'I\'m a third-year Ph.D. candidate at [*University of Illinois Urbana-Champaign* (UIUC)](https://illinois.edu/) 🌽 advised by [Jiaqi Ma](https://jiaqima.github.io/), and I also work closely with [Han Zhao](https://hanzhaoml.github.io/). Currently, I\'m also an [*Anthropic*](https://www.anthropic.com/) AI Safety Research Fellow and an incoming Ph.D. ML intern at [*Susquehanna International Group*](https://sig.com/) 🦅.',
		'Previously, I\'ve spent time at [*Amazon AWS AI Lab*](https://aws.amazon.com/ai/) 🗽 as an Applied Scientist intern, and [*National Institute of Informatics*](https://www.nii.ac.jp/en/) 🇯🇵 as a research intern. I obtained my Master degree from [UIUC](https://illinois.edu/) and [dual Bachelor degree](https://www.ji.sjtu.edu.cn/academics/ipo/study-abroad/degree-programs/) from [*University of Michigan*](https://umich.edu/) 〽️ and [*Shanghai Jiao Tong University*](https://www.sjtu.edu.cn/) 🇨🇳.',

		'Research-wise, I\'m interested in the broad area of ML and AI, with the goal being to draw theoretical insights from practical problems and develop algorithms with provable guarantees and desirable properties such as *efficiency*, *robustness*, and *fairness*. Recently, my research focuses on *understanding data*, including the following three aspects:',
		'1. **Data Attribution**: Understanding how training data *influences* AI models.',
		'2. **Data Curation**: How to curate/generate/augment (synthetic) data that further helps models *generalize*?',
		'3. **Data-Centric Privacy**: Can above be done *without* compromising privacy when safety-critical or sensitive data is involved? This includes (differential) privacy, machine unlearning, etc.',
		'Previously I have worked on *graph neural networks* with [Jiaqi Ma](https://jiaqima.github.io/) and *fast graph algorithms* with [Thatchaphol Saranurak](https://sites.google.com/site/thsaranurak/). Generally speaking, I held (actually *hold*) a strong interest in theoretical stuffs that involves *geometry*.',

		'### 🗞️ News',
		'- [Jun. 2026] 🚀 Incoming intern @[*SIG*](https://sig.com/) Deep Learning team, come hanging out in Philly 🦅!',
		'- [Jan. 2026] 🍻 One paper accepted by *ICLR 2026*.',
		'- [Jan. 2026] 👨‍🎓 Starting as an AI safety fellow @[*Anthropic*](https://www.anthropic.com/) Alignment Science team, come hanging out in San Francisco 🌉!',
		'- [Oct. 2025] 📚 We are organizing the *Symposium on Information Retrieval and Language Models* at UIUC!',
		'- [Oct. 2025] 🎙️ Giving a [tutorial](https://trais-lab.github.io/dattri-reading-group/recording/2025/13/) on recent tricks in computing gradient-based data attribution, including [GraSS](./research/GraSS/)!',
		'- [Sep. 2025] 🍻 Please check out our new [survey paper](./research/Data-Attribution-Survey/) on data attribution!',
		'- [Sep. 2025] 🍻 Two papers accepted by *NeurIPS 2025* with one first-authored and one co-first-authored!',
		'- [Aug. 2025] 🎓 Get my M.S. Applied Math Degree at UIUC!',
		'- [Jul. 2025] 📚 We are organizing the [3rd Workshop on Regulatable Machine Learning](https://regulatableml.github.io/) in conjunction with *NeurIPS 2025*!',
		'- [Jul. 2025] 🎙️ Giving a talk on [Data Attribution](./else/Intro-to-DA.pdf) at the [*Guided Generation Group (GGG)*](https://github.com/GuidedGenerationGroup)!',
		'- [Jun. 2025] 🤖 Attending the first [AI Startup School](https://events.ycombinator.com/ai-sus) held by [*Y Combinator*](https://www.ycombinator.com/), see you in San Francisco 🌉!',
		'- [Mar. 2025] 🚀 Interning @[*Amazon AWS AI*](https://aws.amazon.com/ai/) Deep Engine Science team, come hanging out in New York 🗽!',
		'- [Jan. 2025] 🍻 One paper accepted by *ICLR 2025*.',
		'- [Nov. 2024] 🏆 Received the **Graduate Conference Travel Award** from UIUC!',
		'- [Oct. 2024] 🏆 Received the **NeurIPS 2024 Scholar Award**, see you in Vancouver!',
		'- [Sep. 2024] 🍻 Two papers accepted by *NeurIPS 2024* with one ***Spotlight***.',
		'- [Jun. 2024] 📚 We launched the ongoing [*Data Attribution Reading Group*](https://trais-lab.github.io/dattri-reading-group/).',
		'- [May 2024] 🚀 Interning @[*National Institute of Informatics*](https://www.nii.ac.jp/en/), come hanging out in Tokyo 🇯🇵!',
		// '- [Jan. 2024] 📚 I initiated the *Statistical Learning Theory* Reading Group.',
		'',
		'### 🔖 Misc',
		'I\'m from Taiwan 🇹🇼! In my spare time, I enjoy [*street photography*](https://www.instagram.com/streetmalc/) 📷 and playing drums 🥁.',
	],
	education: [
		{
			date: 'Aug. 2023 - Present',
			icon: 'university',
			title: 'Ph.D. in Information Science',
			location: 'University of Illinois Urbana-Champaign',
		}, {
			date: 'Aug. 2023 - Aug. 2025',
			icon: 'university',
			title: 'M.S. in Mathematics',
			location: 'University of Illinois Urbana-Champaign',
		}, {
			date: 'Sep. 2021 - May 2023',
			icon: 'university',
			title: 'B.S. in Computer Science | minor in Mathematics',
			location: 'University of Michigan',
		}, {
			date: 'Sep. 2019 - Aug. 2023',
			icon: 'university',
			title: 'B.E. in Electrical and Computer Engineering | minor in Computer Science',
			location: 'Shanghai Jiao Tong University',
		}
	],
	social: [
		{
			url: '/cv.pdf',
			icon: ['ai', 'cv'],
		}, {
			url: 'https://scholar.google.com/citations?user=lPlQpqoAAAAJ&hl=en',
			icon: ['fa', 'graduation-cap'],
		}, {
			url: 'https://github.com/sleepymalc',
			icon: ['fab', 'github'],
		}, {
			url: 'https://www.linkedin.com/in/ping-bang-hu-78a190215/',
			icon: ['fab', 'linkedin'],
		}, {
			url: 'https://X.com/PingbangHu',
			icon: ['fab', 'twitter'],
		}, {
			url: "mailto:pbb@illinois.edu",
			icon: ['fa', 'envelope'],
		},
	],
	awards: [
		{
			date: 'Oct. 2025',
			title: 'Anthropic AI Safety Research Fellowship',
		},
		{
			date: 'Nov. 2024',
			title: 'Graduate Conference Travel Award',
		},
		{
			date: 'Oct. 2024',
			title: 'NeurIPS 2024 Scholar Award',
		},
		{
			date: 'Aug. 2024',
			title: 'Excellent Internship Award at National Institute of Informatics',
		},
		{
			date: 'Oct. 2021',
			title: 'Hong Kong, Macao and Taiwan Overseas Chinese Student Scholarship',
		},
		{
			date: 'Nov. 2020',
			title: 'Undergraduate Excellent Scholarship',
		},
		{
			date: 'Jun. 2020',
			title: 'Bao Gang Excellent Scholarship',
		},
		{
			date: 'Dec. 2019',
			title: 'Hong Kong, Macao and Taiwan Overseas Chinese Student Scholarship',
		},
	],
	interests: [
		{
			icon: `hands-usd`,
			title: `Data Valuation`,
		}, {
			icon: `laptop-code`,
			title: `Algorithmic Design`,
		}, {
			icon: 'chart-line',
			title: 'Mathematical Statistics',
		}, {
			icon: 'function',
			title: 'Mathematical Analysis',
		}, {
			icon: 'brain',
			title: 'Learning Theory',
		}, {
			icon: 'chart-network',
			title: 'Graph Theory',
		}, {
			icon: 'shapes',
			title: 'Geometry \& Topology',
		},
	],
	experience: [
		{
			title: 'Research and Industry Experience',
			position: 'left',
			data: [
				{
					title: 'Machine Learning Ph.D. Intern',
					date: 'Jun. 2026 - Aug. 2026',
					location: 'SIG Deep Learning Team',
					description:
						'TBA'
				},
				{
					title: 'AI Safety Research Fellow',
					date: 'Jan. 2026 - May 2026',
					location: 'Anthropic Alignment Science Team',
					description:
						'TBA'
				},
				{
					title: 'Applied Scientist Intern',
					date: 'May 2025 - Aug. 2025',
					location: 'Amazon AWS AI Lab',
					description:
						'**Data Curation**: ' +
						'Investigate data attribution with synthetic data generation to curate high-quality dataset.'
				},
				{
					title: 'Research Intern',
					date: 'May 2024 - Aug. 2024',
					location: 'National Institute of Informatics',
					description:
						'[**Pseudo-Nonlinear Data Augmentation**](../research/PNL/): ' +
						'Develop an information-geometric data augmentation algorithm advised by [Mahito Sugiyama](https://mahito.info/index_e.html). ' +
						'Won the **Excellent Internship Evaluation**.',
				},
				{
					title: 'Undergraduate Researcher',
					date: 'Mar. 2022 - Dec. 2022',
					location: 'University of Michigan',
					description:
						'**Detection Sets**: ' +
						'Design the first almost linear time algorithm on finding minimal balanced cuts advised by [Thatchaphol Saranurak](https://sites.google.com/site/thsaranurak/).',
				},
				{
					title: 'Undergraduate Researcher',
					date: 'May 2022 - Apr. 2023',
					location: 'University of Michigan',
					description:
						'**Deep Learning Foundation**: ' +
						'Develop various techniques to understand deep neural networks advised by [Wei Hu](https://weihu.me/) under the [SURE Program](https://sure.engin.umich.edu/).',
				},
			],
		},
		{
			title: 'Reading Group',
			position: 'left',
			data: [
				{
					title: 'Organizer',
					date: 'Jun. 2024 - Present',
					location: 'University of Illinois Urbana-Champaign',
					description:
						`**Data Attribution Reading Group**: ` +
						`Focus on the recent advances of data attribution methods in the era of Generative AI. Please see the [official website](https://trais-lab.github.io/dattri-reading-group/).`,
				},
				{
					title: 'Organizer',
					date: 'Jan. 2024 - Present',
					location: 'University of Illinois Urbana-Champaign',
					description:
						`**Statistical Learning Theory**: ` +
						`A thorough reading on [Roman Vershynin](https://www.math.uci.edu/~rvershyn/)'s [High-Dimensional Probability](https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-book.html), focusing on statistical learning theory. [Solution](../else/HDP_solution.pdf) is available.`,
				},
				{
					title: 'Presenter',
					date: 'Oct. 2023 - Jul. 2024',
					location: 'Virtual',
					description:
						`**[VIDA Reading Group](https://wanghh7.github.io/VIDY-paper-reading-group/)**: ` +
						`A reading group focuses on recent advances in graph machine learning, and also the foundational theory for statistical learning.`,
				},
				{
					title: 'Organizer',
					date: 'May 2023 - Dec. 2023',
					location: 'University of Illinois Urbana-Champaign',
					description:
						`**Sparse Graph Limit Theory**: ` +
						`A thorough reading on [László Lovász](https://en.wikipedia.org/wiki/L%C3%A1szl%C3%B3_Lov%C3%A1sz)'s [Large networks and graph limits](https://lovasz.web.elte.hu//bookxx/hombook-almost.final.pdf), focusing on Chapter 18 and onwards.`,
				},
			],
		},
		{
			title: 'Teaching',
			position: 'right',
			data: [
				{
					title: 'Graduate Teaching Assistant',
					date: 'Jan. 2025 - May 2025, Jan. 2026 - May 2026',
					location: 'University of Illinois Urbana-Champaign',
					description:
						'**[IS527 Network Analysis](https://ischool.illinois.edu/degrees-programs/courses/is527)** (Graduate): ' +
						'An introduction to the theory and applications of social network analysis on the M.S. IS track.',
				},
				{
					title: 'Instructional Aide',
					date: 'Jan. 2023 - May 2023',
					location: 'University of Michigan',
					description:
						'**[EECS475 Introduction to Cryptography](https://mahdi.ch/eecs475/)** (Undergraduate): ' +
						'An introduction to the theoretical cryptography on the B.Sc. CS track. [Notes](../posts/Notes#introduction-to-cryptography-eecs475-university-of-michigan-ta) are available.',
				},
				{
					title: 'Instructional Aide',
					date: 'Aug. 2022 - Dec. 2022',
					location: 'University of Michigan',
					description:
						'**[EECS572 Randomness and Computation](https://mahdi.ch/eecs572/)** (Graduate): ' +
						'A course about randomness in modern computations on the M.S. CS theory track. [Notes](../posts/Notes#randomness-and-computation-eecs572-university-of-michigan-ta) are available.',
				},
				{
					date: 'May 2021 - Aug. 2021',
					title: 'Teaching Assistant',
					location: 'Shanghai Jiao Tong University',
					description:
						'**[VV285 Honor Mathematics III](https://umji.sjtu.edu.cn/~horst/teaching/vv285.html)** (Undergraduate): ' +
						'A follow-up course of VV186 on the B.Eng. ECE track. We also hold the first [*JIntegration Bee* competition](https://github.com/sleepymalc/JIntegrationBee)!',
				},
				{
					title: 'Teaching Assistant',
					date: 'Sep. 2020 - Dec. 2020',
					location: 'Shanghai Jiao Tong University',
					description:
						'**[VV186 Honor Mathematics II](https://umji.sjtu.edu.cn/~horst/teaching/vv186.html)** (Undergraduate): ' +
						'The first rigorous analysis course on the B.Eng. ECE track.',
				},
			],
		},
		{
			title: 'Professional Service',
			position: 'right',
			data: [
				{
					title: 'Conference Reviewer',
					date: 'NA',
					location: 'Virtual',
					description:
						'ICLR *2026*, NeurIPS *2025*, ICLR *2025*, ICML *2024*, IEEE BigData *2023*',
				},
				{
					title: 'Journal Reviewer',
					date: 'NA',
					location: 'Virtual',
					description:
						'TMLR',
				},
				{
					title: 'Program Committee',
					date: 'NA',
					location: 'Virtual',
					description:
						'AAAI *2025*',
				},
			],
		},
		{
			title: 'Software Development',
			position: 'right',
			data: [
				{
					title: 'Backend Developer',
					date: 'Oct. 2020 - Jun. 2021',
					location: 'Virtual',
					description:
						'**foodall**: ' +
						'A food order platform in Taiwan, built with *Golang*, *Gin*, and *MongoDB*, with RESTful API design.',
				},
			],
		},
	],
	tagColors: [
		'magenta', 'red', 'volcano', 'orange', 'gold',
		'lime', 'green', 'cyan', 'blue', 'geekblue', 'purple',
	],
	tags: [
		{
			id: 'javascript',
			name: 'javascript',
			description: 'JavaScript is an object-oriented programming language used alongside HTML and CSS to give functionality to web pages.',
			color: '#f0da50',
		},
		{
			id: 'nodejs',
			name: 'Node.js',
			description: 'Node.js is a tool for executing JavaScript in a variety of environments.',
			color: '#90c53f',
		},
		{
			id: 'rxjs',
			name: 'RxJS',
			description: 'RxJS is a library for reactive programming using Observables, for asynchronous operations.',
			color: '#eb428e',
		},
		{
			id: 'typescript',
			name: 'typescript',
			description: 'TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.',
			color: '#257acc',
		},
		{
			id: 'reactjs',
			name: 'reactjs',
			description: 'React is an open source JavaScript library used for designing user interfaces.',
			color: '#61dbfa',
		},
		{
			id: 'gatsby',
			name: 'Gatsby.js',
			description: 'A framework built over ReactJS to generate static page web application.  ',
			color: '#6f309f',
		},
		{
			id: 'html',
			name: 'HTML',
			description: 'A markup language that powers the web. All websites use HTML for structuring the content.',
			color: '#dd3431',
		},
		{
			id: 'css',
			name: 'css',
			description: 'CSS is used to style the HTML element and to give a very fancy look for the web application.',
			color: '#43ace0',
		},
		{
			id: 'python',
			name: 'python',
			description: 'A general purpose programming language that is widely used for developing various applications.',
			color: '#f9c646',
		},

	],
	defaultLanguage: 'en',
	contactFormUrl: process.env.CONTACT_FORM_ENDPOINT
		|| 'https://getform.io/f/09a3066f-c638-40db-ad59-05e4ed71e451',
	googleAnalyticTrackingId: process.env.GA_TRACKING_ID || 'G-734WCNHH4E',
	disqusScript: process.env.DISQUS_SCRIPT
		|| 'https://tc-imba.disqus.com/embed.js',
	wakatime: {
		username: 'sleepymalc',
		activity: 'eb201619-dfe8-485e-b683-11ce3475ad61',
		language: 'cccb943f-2bfc-47e5-b218-c56b858c1a90',
	},
};
