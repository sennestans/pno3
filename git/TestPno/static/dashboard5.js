// dashboard4.js

const ctx4 = document.getElementById("lineChart4").getContext('2d');

// Voer een AJAX-verzoek uit om gegevens op te halen van de Python-server
fetch('/get-data') // Pas deze route aan op basis van je Flask-applicatie
    .then(response => response.json())
    .then(data => {
        createChart4(data);
    })
    .catch(error => {
        console.error('Fout bij het ophalen van gegevens:', error);
    });

function createChart4(data) {
    new Chart(ctx4, {
        type: 'line',
        data: {
            labels: Array.from({ length: data.length }, (_, i) => i),
            datasets: [{
                label: 'Gegevens',
                data: data,
                borderColor: 'rgba(255, 0, 0, 1)', // Rood
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Uur'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Waarde'
                    }
                }
            }
        }
    });
}
