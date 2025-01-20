import { useState } from "react";

import Layout from '../components/Layout';
import Section from '../components/Section';
import Container from '../components/Container';

import styles from '../styles/Home.module.css';

import Sidebar from "../components/Sidebar";

const DEFAULT_CENTER = [38.907132, -77.036546]


// Update boolean for correct connection
export const getServerSideProps = async () => {
  try {
    await client.connect() // Will use the default database passed in the MONGODB_URI
    return {
      props: { isConnected: true }
    }
  } catch (e) {
    console.error(e)
    return {
      props: { isConnected: false }
    }
  }
}


export default function Home(isConnected) {
  const [address, setAddress] = useState("");
  const [time, setTime] = useState("");
  const [prediction, setPrediction] = useState(null);

  return (
    <Layout>
        <Sidebar />
        <div style={{ marginLeft: '300px', padding: '20px' }}>
          <Section>
            <Container>
              <h1 className={styles.title}>Welcome to Bike Sharing Predictor</h1>

              <p className={styles.description}>
                Use this app to predict bike availability based on location and time. 
                <br/>
                <br/>
                This app is meant for regular or occasional users of bike sharing systems in Toulouse, 
                but also for VêloToulouse administators looking to monitor the evolution of bike availability throughout the city.
                <br/>
                The code behind this project is accessible throught the link in the Footer.
                <br/>
                <br/>
                To test our model, please refer to Details & Prediction in the Navigation bar.
                
              </p>
            </Container>
          </Section>
        </div>
      </Layout>
  );
}



