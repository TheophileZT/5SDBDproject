import Container from '../Container';

import styles from './Footer.module.css';

const Footer = ({ ...rest }) => {
  return (
    <footer className={styles.footer} {...rest}>
      <Container className={`${styles.footerContainer} ${styles.footerLegal}`}>
        <p>
          &copy; <a href="https://github.com/TheophileZT/5SDBDproject">5SDBD INSA Toulouse</a>, {new Date().getFullYear()}
        </p>
      </Container>
    </footer>
  );
};
export default Footer;
