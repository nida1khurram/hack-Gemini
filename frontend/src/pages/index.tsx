import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={clsx('container', styles.heroContainer)}>
        <div className={styles.heroImage}>
          <img src="/static/img/home-pic.png" alt="Hero Image" />
        </div>
        <div className={styles.heroText}>
          <Heading as="h1" className="hero__title">
            Welcome to the Future of Physical AI
          </Heading>
          <p className="hero__subtitle">
            Explore the intersection of artificial intelligence and humanoid robotics.
          </p>
          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro">
              Start Reading
            </Link>
            <Link
              className="button button--secondary button--lg"
              style={{marginLeft: 10}}
              to="https://github.com/nida1khurram/hack-Gemini/tree/main">
              View on GitHub
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
