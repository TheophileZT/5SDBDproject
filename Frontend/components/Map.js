import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

import {ICON_BLACK, ICON_BLUE, ICON_GREEN, ICON_GREY, ICON_ORANGE, ICON_RED, ICON_VIOLET} from "../lib/icons";

// Return corresponding icon for station state
function iconFromStatus(status) {
    switch (status) {
      case "Critically Underloaded":
        return ICON_GREY;
      case "Underloaded":
        return ICON_BLUE;
      case "Balanced":
        return ICON_GREEN;
      case "Overloaded":
        return ICON_ORANGE;
      case "Critically Overloaded":
        return ICON_RED;
      default:
        return ICON_BLACK;
    }
  }

export default function Map( {initialCenter, zoom, stations}) {
  return (
    <div className=" w-full h-full">
        <MapContainer center={initialCenter} zoom={zoom} style={{ height: "400px", width: "100%" }}>
          <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
          />
          
          {stations.map((station, index) => (
            <Marker
              key={index}
              icon={iconFromStatus(station.status)}
              position={[station.lat, station.lng]}
            >
              <Popup>Bike available : {station.available_bikes}</Popup>
            </Marker>
          ))}
        </MapContainer>
    </div>
  );
}
