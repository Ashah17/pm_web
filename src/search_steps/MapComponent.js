import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

function MapComponent({ mappingData }) {
  return (
    <MapContainer center={[42.3601, -71.0589]} zoom={13} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {Object.keys(mappingData).map((place) => {
        const clusters = mappingData[place];
        return Object.keys(clusters).map((clusterId) => {
          const { points, centroid, route } = clusters[clusterId];
          return (
            <React.Fragment key={clusterId}>
              {/* Plot Points */}
              {points.map((point, index) => (
                <Marker key={index} position={point}>
                  <Popup>{`Cluster ${clusterId} Point ${index + 1}`}</Popup>
                </Marker>
              ))}
              {/* Plot Centroid */}
              <Marker
                position={centroid}
                icon={L.icon({
                  iconUrl: 'http://leafletjs.com/examples/custom-icons/leaf-green.png',
                  iconSize: [38, 95],
                })}
              >
                <Popup>{`Cluster ${clusterId} Centroid`}</Popup>
              </Marker>
              {/* Plot Route */}
              <Polyline positions={route} color="blue" />
            </React.Fragment>
          );
        });
      })}
    </MapContainer>
  );
}

export default MapComponent;
