import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
import BrowserOnly from '@docusaurus/BrowserOnly';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment'; // Import ExecutionEnvironment

let RobotArm2D = () => null; // Default to a no-op component
let Chatbot = () => null; // Default to a no-op component (now used for inline, but hidden)

if (ExecutionEnvironment.canUseDOM) {
  // Dynamically import RobotArm2D and the new InlineChatbot (which is hidden) only in the browser
  RobotArm2D = require('@site/src/components/RobotArm2D').default;
  Chatbot = require('@site/src/components/InlineChatbot').default; // Use the hidden inline version
}

export default {
  ...MDXComponents,
  RobotArm2D: RobotArm2D, // Expose the conditionally loaded component
  Chatbot: Chatbot, // Expose the conditionally loaded component (now hidden)
  BrowserOnly,
};
