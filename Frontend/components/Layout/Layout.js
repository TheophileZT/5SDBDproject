import Head from 'next/head';

import Header from '../Header';
import Footer from '../Footer';

import styles from './Layout.module.scss';

export const metadat = {
  title : 'Bike app',
  description : 'Bike predictions'
};

const Layout = ({ children, className, ...rest }) => {
  return (
    <div className={styles.layout}>
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Header />
      <main className={styles.main}>{children}</main>
      <Footer />
    </div>
  );
};

export default Layout;
