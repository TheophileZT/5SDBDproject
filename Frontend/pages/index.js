import { useState } from "react";

import Layout from '../components/Layout';
import Section from '../components/Section';
import Container from '../components/Container';
import Sidebar from "../components/Sidebar";

import disco from '../public/disco-ball.gif';
import Image from 'next/image'
import Link from 'next/link';

import styles from '../styles/Home.module.css';

const DEFAULT_CENTER = [38.907132, -77.036546]

export default function Home(isConnected) {
  const [address, setAddress] = useState("");
  const [time, setTime] = useState("");
  const [prediction, setPrediction] = useState(null);

  return (
    <Layout style={{paddingBottom: '3px', paddingBottom: '3px' }}>
        <Sidebar />
        <div style={{ marginLeft: '300px', padding: '20px' }}>
          <Section className={`${styles.sectionOverride}`}>
            <Container>
              <h1 className={styles.title}>Welcome to Bike Sharing Predictor</h1>

              <p className={styles.description}>
                Use this app to predict bike availability based on location and time. 
                <br/>
                <br/>
                This app is meant primarly for VêloToulouse administators looking to monitor the evolution of bike availability throughout the city.
                You can enter a specific address, in order to consult the state of the stations around it for a given time. 
                You can also freely explore the map, and consult the state of all stations available on Toulouse, in the next hours. 
                <br/>
                <br/>
                The code behind this project is accessible throught the link in the Footer.
                <br/>
                <br/>
                To test our model, please refer to Details & Prediction in the Navigation bar.
                
              </p>
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



