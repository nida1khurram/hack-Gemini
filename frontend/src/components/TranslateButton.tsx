import React, { useState } from 'react';
import axios from 'axios';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

interface TranslateButtonProps {
  textToTranslate: string;
  onTranslationComplete: (translatedText: string) => void;
}

const TranslateButton: React.FC<TranslateButtonProps> = ({ textToTranslate, onTranslationComplete }) => {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields?.backendUrl || 'http://localhost:8000';

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTranslate = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await axios.post(
        `${backendUrl}/translate`,
        { text: textToTranslate }
      );
      onTranslationComplete(res.data.translated_text);
    } catch (err) {
      console.error('Translation error:', err);
      setError('Failed to translate text.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ margin: '10px 0' }}>
      <button onClick={handleTranslate} disabled={loading} style={{ padding: '8px 15px' }}>
        {loading ? 'Translating...' : 'Translate to Urdu'}
      </button>
      {error && <p style={{ color: 'red', marginTop: '5px' }}>{error}</p>}
    </div>
  );
};

export default TranslateButton;
