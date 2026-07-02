import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './map.css';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

async function getStationsInZone(lat1, lat2, lon1, lon2) {
    try {
        const url = `http://127.0.0.1:8000/stations-zone?lat1=${lat1}&lat2=${lat2}&lon1=${lon1}&lon2=${lon2}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erreur lors de la récupération des stations:', error);
		return { stations: [] };
    }
}

async function getObservations(station_id)
{
    try {
        const url = `http://127.0.0.1:8000/station-observations?code_station=${station_id}`;
        const response = await fetch(url)
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        return data;
    }

    catch (error)
    {
        console.error('Erreur lors de la recuperation des observations', error);
        return {}
    }

}

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

    const loadStations = async (map) => {
        if (!map) return;
        
        const bounds = map.getBounds();
        const southWest = bounds.getSouthWest();
        const northEast = bounds.getNorthEast();

        try {
            const stations_in_zone = await getStationsInZone(
                southWest.lat, northEast.lat, southWest.lng, northEast.lng
            );

            // Remove old markers
            map.eachLayer((layer) => {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });

            // Add new markers
            stations_in_zone.stations?.forEach((station) => {
                const marker = L.marker([station.latitude, station.longitude])
                    .addTo(map)
                    .bindPopup(station.nom);

				marker.on("click", async function(e) {
                    const observations = await getObservations(station.code);
					console.log(observations)
				});
            });

        } catch (error) {
            console.error('Error loading stations:', error);
        }
    };

    useEffect(() => {
        if (!mapInstanceRef.current && mapRef.current) {
            mapInstanceRef.current = L.map(mapRef.current).setView(center, zoom);

            L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
                attribution: '© OpenStreetMap contributors'
            }).addTo(mapInstanceRef.current);

            // Resize handling
            const resizeMap = () => {
                if (mapInstanceRef.current) {
                    mapInstanceRef.current.invalidateSize();
                }
            };

            setTimeout(resizeMap, 100);
            setTimeout(resizeMap, 300);
            setTimeout(resizeMap, 500);

            const handleResize = () => {
                if (mapInstanceRef.current) {
                    mapInstanceRef.current.invalidateSize();
                }
            };
            window.addEventListener('resize', handleResize);

            // Load initial stations
            setTimeout(() => {
                if (mapInstanceRef.current) {
                    loadStations(mapInstanceRef.current);
                }
            }, 600);

            // FIX: Event listener INSIDE useEffect and pass 'this'
            mapInstanceRef.current.on('moveend', function() {
                loadStations(this); // Pass the map instance
            });

            return () => {
                window.removeEventListener('resize', handleResize);
                if (mapInstanceRef.current) {
                    mapInstanceRef.current.remove();
                    mapInstanceRef.current = null;
                }
            };
        }
    }, [center, zoom]);

    return <div ref={mapRef} className="map" style={{ width: '100%', height: '500px' }} />;
};

export default Map;