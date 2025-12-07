import React from 'react';
import styles from './ModuleCard.module.css';

interface ModuleCardProps {
  title: string;
  items: string[];
}

const ModuleCard: React.FC<ModuleCardProps> = ({ title, items }) => {
  return (
    <div className={styles.card}>
      <h3 className={styles.title}>{title}</h3>
      <ul className={styles.list}>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
};

export default ModuleCard;
