import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: Robotic Nervous System (ROS 2)',
      link: {
        type: 'doc',
        id: 'module1', // Link to the module overview page
      },
      items: [
        'module1_chapter1',
        'module1_chapter2',
        'module1_chapter3',
        'module1_chapter4',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin (Gazebo & Unity)',
      link: {
        type: 'doc',
        id: 'module2',
      },
      items: [
        'module2_chapter1',
        'module2_chapter2',
        'module2_chapter3',
        'module2_chapter4',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: AI-Robot Brain (NVIDIA Isaac)',
      link: {
        type: 'doc',
        id: 'module3',
      },
      items: [
        'module3_chapter1',
        'module3_chapter2',
        'module3_chapter3',
        'module3_chapter4',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      link: {
        type: 'doc',
        id: 'module4',
      },
      items: [
        'module4_chapter1',
        'module4_chapter2',
        'module4_chapter3',
      ],
    },
  ],
};

export default sidebars;
