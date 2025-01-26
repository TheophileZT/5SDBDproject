import Link from 'next/link';
import Container from '../Container';

import styles from './Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      <Container className={styles.headerContainer}>
        <p className={styles.headerTitle}>
          <Link href="/">
            Predicting the availability of bike sharing systems
          </Link>
        </p>
        <ul className={styles.headerLinks}>
          <li>
            <a href="https://github.com/colbyfayock/next-leaflet-starter" rel="noreferrer">
            </a>
          </li>
        </ul>
      </Container>
    </header>
  );
};

export default Header;
