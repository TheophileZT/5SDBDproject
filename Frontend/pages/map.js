'use-client';

import dynamic from "next/dynamic";
import Layout from "../components/Layout";
import Section from "../components/Section";
import Container from "../components/Container";
import Sidebar from "../components/Sidebar";
import TimeReferenceButtons from "../components/TimeReferenceButtons";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { currentDateWithOffsetString } from "../lib/dateTime";

import disco from '../public/disco-ball.gif';
import Image from 'next/image'
import Link from 'next/link';

import styles from "../styles/Home.module.css";

const Map = dynamic(() => import("../components/Map"), {
  ssr: false,
  loading: () => <p>Loading map...</p>,
});

//////////////////////////////////////////////////////////////////////////////////////////////////
export default function MapPage( ) {
  const searchParams = useSearchParams();
  const [stations, setStations] = useState([]);

  // Extract from search parameters OR Default
  const lat = parseFloat(searchParams.get("lat")) || 43.605642;
  const lng = parseFloat(searchParams.get("lng")) || 1.448919;
  const zoom = parseFloat(searchParams.get("zoom")) || 12;
  const detailsTime = searchParams.get("time") || currentDateWithOffsetString(0);
  
  // Preliminary fetch of inference
  useEffect(() => {
    async function fetchStations() {
      try {
        const response = await fetch(`api/predict?datetime=${encodeURIComponent(detailsTime)}`);
        if (!response.ok) throw new Error("Failed to fetch station data");
        const stationsData = await response.json();
        setStations(stationsData);
      } catch (error) {
        console.error("Error fetching stations:", error);
      }
    }
    fetchStations();
  }, []);

  // On predict button only
  async function handlePredict(time) {
    const datetime = currentDateWithOffsetString(time);
    try {
      const response = await fetch(`api/predict?datetime=${encodeURIComponent(datetime)}`, {
          method: 'GET',
        });
      if (!response.ok) throw new Error("Failed to fetch station data");
      const stationsData = await response.json();
      setStations(stationsData);
    } catch (error) {
      console.error("Error fetching prediction data:", error);
    }
  }

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

            <Map initialCenter={[lat, lng]} zoom={zoom} stations={stations} />

            <TimeReferenceButtons onPredict={handlePredict}/>

          </Container>
        </Section>
      </div>
      <Link href="http://20.199.41.36/dance" passHref>
        <Image
            src={disco}
            width={40}
            height={40}
            unoptimized
            priority
            style={{ marginLeft: "1800px", marginTop: '0px'}}
        />
      </Link> 
    </Layout>
  );
}