import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import ModuleCard from '../ModuleCard'; // Import the new ModuleCard component


export default function HomepageFeatures(): ReactNode {
  const module1Items = [
    "ROS 2 Workspaces and Package Creation",
    "ROS 2 Communication: Deep Dive into Topics",
    "ROS 2 Communication: Services and Actions",
  ];

  const module2Items = [
    "Digital Twin (Gazebo & Unity)",
    "Introduction to Humanoid Robotics",
    "Robot Kinematics: Forward and Inverse",
    "Balance and Locomotion Control",
    "Human-Robot Interaction (HRI)",
  ];

  const module3Items = [
    "Introduction to AI in Robotics",
    "Perception for Robotic Systems",
    "Planning and Decision-Making",
    "Machine Learning for Robot Control",
  ];

  const module4Items = [
    "Multi-Robot Systems and Swarm Robotics",
    "Humanoid Robot Design and Biomechanics",
    "Ethical and Societal Implications of Humanoid AI",
    "Future Trends in Physical AI and Robotics",
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.sectionHeading}>
          <Heading as="h2" className="hero__title">A New Standard in AI Education</Heading>
          <p className="hero__subtitle">
            Physical AI & Humanoid Robotics delivers clear, hands-on learning that makes advanced robotics accessible.
          </p>
        </div>
        <div className={clsx("row", styles.moduleCardsRow)}>
          <div className="col col--6">
            <ModuleCard title="Module 1: Introduction to ROS 2" items={module1Items} />
          </div>
          <div className="col col--6">
            <ModuleCard title="Module 2: Humanoid Robotics" items={module2Items} />
          </div>
        </div>
        <div className={clsx("row", styles.moduleCardsRow)}>
          <div className="col col--6">
            <ModuleCard title="Module 3: AI-Robot Brain (NVIDIA Isaac)" items={module3Items} />
          </div>
          <div className="col col--6">
            <ModuleCard title="Module 4: Vision-Language-Action (VLA)" items={module4Items} />
          </div>
        </div>
       
      </div>
    </section>
  );
}
