document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Point Relais Logic (Only runs if elements exist)
    const btnSelectRelay = document.getElementById('btn-select-relay');
    if (btnSelectRelay) {
        btnSelectRelay.addEventListener('click', function () {
            // Check if Sendcloud is loaded
            if (typeof sendcloud === 'undefined') {
                console.error("Sendcloud API not loaded");
                alert("Erreur: Le service de point relais n'est pas disponible pour le moment.");
                return;
            }

            // Open Sendcloud Map
            sendcloud.servicePoints.open({
                apiKey: '8d725091-20cc-4379-a3dd-700c74e35c55',
                country: 'fr',
                language: 'fr-fr'
            },
                function (point) {
                    // Display Result
                    const resultDiv = document.getElementById('resultat-visuel');
                    const spanNom = document.getElementById('span-nom');
                    const spanAdresse = document.getElementById('span-adresse');

                    if (resultDiv && spanNom && spanAdresse) {
                        resultDiv.style.display = 'block';
                        spanNom.innerText = point.name;
                        spanAdresse.innerText = `${point.street} ${point.house_number}, ${point.postal_code} ${point.city}`;
                    }

                    // Fill Hidden Inputs (if form submission is needed later)
                    const inputId = document.getElementById('input_relais_id');
                    const inputNom = document.getElementById('input_relais_nom');
                    const inputAdresse = document.getElementById('input_relais_adresse');
                    const inputCarrier = document.getElementById('input_relais_carrier');

                    if (inputId) inputId.value = point.id;
                    if (inputNom) inputNom.value = point.name;
                    if (inputAdresse) inputAdresse.value = `${point.street} ${point.house_number}, ${point.postal_code} ${point.city}`;
                    if (inputCarrier) inputCarrier.value = point.carrier;

                    console.log("Point relais selected:", point);
                },
                function (errors) {
                    console.error("Sendcloud Error:", errors);
                });
        });
    }
});
