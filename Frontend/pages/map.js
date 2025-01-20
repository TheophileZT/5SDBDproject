import dynamic from "next/dynamic";
import Layout from "../components/Layout";
import Section from "../components/Section";
import Container from "../components/Container";
import Sidebar from "../components/Sidebar";
import styles from "../styles/Home.module.css";

const DEFAULT_CENTER = [38.907132, -77.036546];

// Dynamically import the Map component with ssr: false to avoid server-side rendering issues
const Map = dynamic(() => import("../components/Map"), {
  ssr: false,
  loading: () => <p>Loading map...</p>,
});

export default function MapPage() {
  return (
    <Layout>
      <Sidebar />
      <div style={{ marginLeft: "300px" }}>
        <Section>
          <Container>
            <h1 className={styles.title}>Bike Sharing Predictor - Map</h1>
            <p className={styles.description}>
              <code className={styles.code}>Explore the map</code>
            </p>
            <Map/>
          </Container>
        </Section>
      </div>
    </Layout>
  );
}
