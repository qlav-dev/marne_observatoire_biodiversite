import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Map from './Map';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div>
      <h1 className="h1">Observatoire de la Biodiversité dans la Marne</h1>
      <p className="intro"> Ce site permet de visualiser les données de biodiversité collectées dans le département de la Marne. Ces données ont été récoltées à partir de database disponibles librement en ligne.</p>
    </div>



    <div class="wrapper">
      <div class="one">
        <Map />
      </div>
      <div class="two">Paramètres</div>

      <div class="three"> <div className="checkbox-container">


        <div class="accordion-body">
          <div class="accordion">

            <div class="container">
              <div className="label">
                <span>Points d'eau </span>
                <span className="icon-toggle">+</span>
              </div>

              <div class="checkBoxContainer" id="Point_deau"> </div>
            </div>

            <hr></hr>
            <div class="container">
              <div className="label">
                <span>Espèces protégées</span>
                <span className="icon-toggle">+</span></div>
              <div class="checkBoxContainer">
                <div class="checkbox-container">
                  <input type="checkbox" id="monCheckboxUnique" className="custom-checkbox-input" />
                  <label htmlFor="monCheckboxUnique" className="custom-checkbox-label"> Essai 3 </label> </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>

      <div class="quatre"> Ce site a été réalisé par des Etudiants des Mines</div>

    </div>

  </React.StrictMode>
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
setTimeout(() => {
  const containers = document.querySelectorAll('.accordion .container');

  containers.forEach(container => {
    // On cible uniquement le label pour le clic (évite les zones mortes trop larges)
    const label = container.querySelector('.label');

    if (label) {
      label.addEventListener('click', function (e) {
        // Bloque le clic si on touche une case à cocher
        if (e.target.type === 'checkbox' || e.target.tagName === 'LABEL') return;

        // Alterne la classe active sur le container parent
        container.classList.toggle('active');

        // Trouve le bouton + de CE container et le transforme en -
        const icon = container.querySelector('.icon-toggle');
        if (icon) {
          icon.textContent = container.classList.contains('active') ? '−' : '+';
        }
      });
    }
  });
}, 200);