import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useEffect, useState } from "react";
import Papa from "papaparse";

// Map center at Toulouse
const mapCenter = [43.605642, 1.448919];

export default function Map() {
  const [markers, setMarkers] = useState([]);

  const loadCsvData = async () => {
    try {
      const response = await fetch('/stations.csv');
      const text = await response.text();

      Papa.parse(text, {
        complete: (result) => {
          console.log('Parsed CSV data:', result.data);

          const markerData = result.data.map((row) => {
            const lat = parseFloat(row.lat);
            const lng = parseFloat(row.lng);

            // Bug relating to last line of csv being interpreted as [NaN,NaN]
            // Check if lat/lng are valid numbers  
            if (isNaN(lat) || isNaN(lng)) {
              console.warn(`Invalid lat/lng: ${row.lat}, ${row.lng}`);
              return null;
            }

            return { lat, lng };
          }).filter(marker => marker !== null); // Remove invalid markers

          setMarkers(markerData);
        },
        header: true,
      });
    } catch (error) {
      console.error("Error loading CSV file:", error);
    }
  };

  useEffect(() => {
    loadCsvData(); // Load the CSV data only when the component mounts
  }, []);


  return (
    <div className=" w-full h-full">
        <MapContainer center={mapCenter} zoom={13} style={{ height: "400px", width: "100%" }}>
          <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
          />

          {/* TODO : Create different types of icons for business level */}
          {markers.map((marker, index) => (
            <Marker key={index} position={[marker.lat, marker.lng]}>
              <Popup> Bike Station {index+1} </Popup>
            </Marker>
          ))}
        </MapContainer>
    </div>
  );
}
