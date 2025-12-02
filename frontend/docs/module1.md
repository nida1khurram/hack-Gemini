import Chatbot from '@site/src/components/Chatbot';
import ConditionalContent from '@site/src/components/ConditionalContent';
import TranslateButton from '@site/src/components/TranslateButton'; // Import TranslateButton
import React, { useState } from 'react'; // Import React and useState

---
id: module1
title: "Module 1: Robotic Nervous System (ROS 2)"
---

export const ModuleContent = () => {
  const [translatedContent, setTranslatedContent] = useState<string | null>(null);
  const contentToTranslate = `This is the introductory page for Module 1, focusing on ROS 2.`; // The content to translate

  return (
    <>
      {translatedContent ? (
        <p><strong>Urdu Translation:</strong> {translatedContent}</p>
      ) : (
        <p>{contentToTranslate}</p>
      )}

      <TranslateButton textToTranslate={contentToTranslate} onTranslationComplete={setTranslatedContent} />

      <ConditionalContent allowedBackgrounds={['beginner']}>
        <p>This content is visible only to **beginner** users.</p>
        <p>It provides a very basic overview of ROS 2 concepts.</p>
      </ConditionalContent>

      <ConditionalContent allowedBackgrounds={['intermediate', 'expert']}>
        <p>This content is visible to **intermediate** and **expert** users.</p>
        <p>It includes more technical details and assumes some prior knowledge.</p>
      </ConditionalContent>

      <Chatbot />
    </>
  );
};

<ModuleContent />
