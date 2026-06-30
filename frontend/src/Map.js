import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './map.css';

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

	const resizeMap = () => {
            if (mapInstanceRef.current) {
                console.log('Resizing map...');
                mapInstanceRef.current.invalidateSize();
            }
        };

        // Initial resize with multiple delays to ensure container is ready
        const timers = [
            setTimeout(resizeMap, 100),
            setTimeout(resizeMap, 300),
            setTimeout(resizeMap, 500)
        ];

        // Resize on window changes
        const handleResize = () => {
            if (mapInstanceRef.current) {
                mapInstanceRef.current.invalidateSize();
            }
        };
        window.addEventListener('resize', handleResize);

	  // Add a marker
	L.marker(center)
		.addTo(mapInstanceRef.current)
		.bindPopup('Hello from React 19!')
		.openPopup();
	};

	mapInstanceRef.current.on('move', function() {
		// Get bounds in lat/lng
		const bounds = this.getBounds();
		
		// Extract individual corners
		const southWest = bounds.getSouthWest();
		const northEast = bounds.getNorthEast();
		
		console.log('Map Bounds:');
		console.log('South-West:', southWest.lat, southWest.lng);
		console.log('North-East:', northEast.lat, northEast.lng);
		console.log('Center:', this.getCenter());
	});


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
		class="map"
	/>
	);
};

export default Map;