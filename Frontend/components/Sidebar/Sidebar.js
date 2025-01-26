import Link from "next/link";
import styles from "./Sidebar.module.css";

export default function Sidebar({ selectedView, setSelectedView }) {
  // selected view for later on
  return (
    <div className={styles.sidebar}>
      <h2 className={styles.title}>Navigation</h2>
      <ul className={styles.navList}>

      <Link href={{ 
            pathname: '/details',
            query: { lat: 43.605642 , lng: 1.448919}
          }}
          className={styles.link}>

        <li 
          className={styles.active}
        >Details & Prediction</li>
          
      </Link>

      <Link href="/map" className={styles.link}>
        <li 
          className={styles.active}
        >Map</li>
      </Link>
        
      </ul>
    </div>
  );
}
