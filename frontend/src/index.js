import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Map from './Map';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div>
      
    </div>
   
    <h1>Observatoire de la Biodiversité</h1>
    <div class= "wrapper">
      <div class="one">
        <Map />
      </div>
      <div class="two">Paramètres</div>
      <div class="three">Trois</div>
      
    </div>
  </React.StrictMode>
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
