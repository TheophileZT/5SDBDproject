import Container from '../Container';

import styles from './Footer.module.scss';

const Footer = ({ ...rest }) => {
  return (
    <footer className={styles.footer} {...rest}>
      <Container className={`${styles.footerContainer} ${styles.footerLegal}`}>
        <p>
          &copy; <a href="https://spacejelly.dev">5SDBD INSA Toulouse</a>, {new Date().getFullYear()}
        </p>
      </Container>
    </footer>
  );
};
// TODO : Mettre le lien du github ici merci
export default Footer;
