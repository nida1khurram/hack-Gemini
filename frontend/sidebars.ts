import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: Introduction to ROS 2',
      link: {type: 'doc', id: 'module1'},
      items: ['module1_chapter1', 'module1_chapter2', 'module1_chapter3', 'module1_chapter4'],
    },
    {
      type: 'category',
      label: 'Humanoid Robotics',
      link: {type: 'doc', id: 'module2'},
      items: [
        {type: 'doc', id: 'module2_chapter1', label: 'Introduction to Humanoid Robotics'},
        {type: 'doc', id: 'module2_chapter2', label: 'Robot Kinematics'},
        'module2_chapter3',
        'module2_chapter4'
      ],
    },
    {
      type: 'category',
      label: 'AI Integration',
      link: {type: 'doc', id: 'module3'},
      items: ['module3_chapter1', 'module3_chapter2', 'module3_chapter3', 'module3_chapter4'],
    },
    {
      type: 'category',
      label: 'Advanced Topics',
      link: {type: 'doc', id: 'module4'},
      items: ['module4_chapter1', 'module4_chapter2', 'module4_chapter3', 'module4_chapter4'],
    },
  ],
};

export default sidebars;
