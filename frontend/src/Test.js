import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default Leaflet icons in React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Configure default icon
const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const Map = ({ center = [48.7859896, 2.5122759], zoom = 13 }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);

  useEffect(() => {
	// Initialize map only once
	if (!mapInstanceRef.current && mapRef.current) {
	  mapInstanceRef.current = L.map(mapRef.current).setView(center, zoom);

	  // Add tile layer (OpenStreetMap)
	  L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
		attribution: '© OpenStreetMap contributors'
	  }).addTo(mapInstanceRef.current);

	  // Add a marker
	  L.marker(center)
		.addTo(mapInstanceRef.current)
		.bindPopup('Hello from React 19!')
		.openPopup();
	}

	// Cleanup on unmount
	return () => {
	  if (mapInstanceRef.current) {
		mapInstanceRef.current.remove();
		mapInstanceRef.current = null;
	  }
	};
  }, [center, zoom]);

  return (
	<div 
	  ref={mapRef} 
	  style={{ 
		marginLeft: '10px',
		marginRight: '10px',
		width: '95%', 
		height: '50em', 
		borderRadius: '8px',
		boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
	  }} 
	/>
  );
};

export default Map;