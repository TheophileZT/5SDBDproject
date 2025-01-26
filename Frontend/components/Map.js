import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

import {ICON_BLACK, ICON_BLUE, ICON_GREEN, ICON_GREY, ICON_ORANGE, ICON_RED, ICON_VIOLET} from "../lib/icons";

// Return corresponding icon for station state
function iconFromStatus(number) {
    switch (number) {
      case 0:
        return ICON_GREY;
      case 1:
        return ICON_BLUE;
      case 2:
        return ICON_GREEN;
      case 3:
        return ICON_ORANGE;
      case 4:
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
              icon={iconFromStatus(station.status_bike)}
              position={[station.lat, station.lng]}
            >
              <Popup>Bike available : {station.nb_bike}</Popup>
            </Marker>
          ))}
        </MapContainer>
    </div>
  );
}
