import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Interactive Learning Platform',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://nida1khurram.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<project-name>/'
  baseUrl: '/',
  trailingSlash: true, // Add this line to explicitly handle trailing slashes

  customFields: {
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000', // Default to localhost for development
  },

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'nida1khurram', // Usually your GitHub org/user name.
  projectName: 'hack-Gemini', // Usually your repo name.
  deploymentBranch: 'gh-pages', // The branch Docusaurus will deploy to

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/nida1khurram/hack-Gemini/tree/main',
        },
        blog: { // Re-enable blog plugin
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
          'https://github.com/nida1khurram/hack-Gemini/tree/main',
            // 'https://github.com/your-github-org-or-username/physical-ai-humanoid-robotics/tree/main/frontend/',
        },

        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Site Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Modules',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/nida1khurram/hack-Gemini/tree/main',
          label: 'GitHub',
          position: 'right',
        },
        {
          label: 'Login', // Custom login button
          to: '/docs/login', // You might want to create a login page or link to an auth service
          position: 'right',
          className: 'navbar-login-btn', // Optional: for custom styling
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'ROS 2',
              to: '/docs/module1',
            },
            {
              label: 'Humanoid Robotics',
              to: '/docs/module2',
            },
            {
              label: 'AI Integration',
              to: '/docs/module3',
            },
            {
              label: 'Advanced Topics',
              to: '/docs/module4',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/nida1khurram/hack-Gemini/tree/main',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    // Dark/light mode toggle
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
  } satisfies Preset.ThemeConfig,

  // Plugin for local search
  plugins: [
    // [
    //   require.resolve('@easyops-cn/docusaurus-search-local'),
    //   {
    //     hashed: true,
    //   },
    // ],
  ],
};

export default config;