import { useEffect, useState } from "react";
import InputForm from "../components/Input-Form"; 
import Layout from "../components/Layout";
import Section from "../components/Section";
import Container from "../components/Container";
import Sidebar from "../components/Sidebar";
import styles from "../styles/Home.module.css";

import disco from '../public/disco-ball.gif';
import Image from 'next/image'
import Link from 'next/link';

import { useRouter } from 'next/router';

export default function Details() {
  const [address, setAddress] = useState("");
  const [time, setTime] = useState("");
  const [coordinates, setCoordinates] = useState();

  const router = useRouter();

  /////////////////////////// LOAD VALUES FROM CACHE ///////////////////////////////////////////
  // Load saved values if they exist

  useEffect(() => {
    const savedAddress = localStorage.getItem("address");
    const savedTime = localStorage.getItem("time");

    if (savedAddress) setAddress(savedAddress);
    if (savedTime) setTime(savedTime);
  }, []);

  // Save local at every UI update
  useEffect(() => {
    localStorage.setItem("address", address);
  }, [address]);
  useEffect(() => {
    localStorage.setItem("time", time);
  }, [time]);

  /////////////////////////////// SET TRANSMITTED COORDINATES ///////////////////////////////////////
  // Prepare centering around input address

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch coordinates: ${response.statusText}`);
      }
      const data = await response.json();
      if (data.length === 0) {
        throw new Error("No results found for the provided address.");
      }

      const { lat, lon } = data[0];
      setCoordinates({ lat, lon });
      console.log("Coordinates fetched successfully:", { lat, lon });

      // Ajoute les secondes à zéro par cohérence 
      const datetime = time.toString().replace("T", " ").slice(0, 16) + ":00";

      // Redirect to the map page, passing coordinates as query parameters
      router.push(`/map?lat=${lat}&lng=${lon}&zoom=16.5&time=${datetime}`);
      
    } catch (error) {
      console.error("Error fetching coordinates:", error);
      alert(error.message);
    }
  };
  
  return (
    <Layout>
      <Sidebar />
      <div style={{ marginLeft: "300px" }}>
        <Section>
          <Container>
            <h1 className={styles.title}>Bike Sharing Predictor - Details</h1>
            <p className={styles.description}>
              <code className={styles.code}>Pick a place and a time</code>
            </p>
            <div className={styles.view}>
              <InputForm
                address={address}
                setAddress={setAddress}
                time={time}
                setTime={setTime}
                handleSubmit={handleSubmit}
              />
            </div>
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
            style={{ marginLeft: "1800px", marginTop: '170px'}} // Adjust the value as needed
        />
      </Link> 
    </Layout>
  );
}
