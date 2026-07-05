document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // RESTORE POSISI PETA
    // ==========================

    let savedCenter = localStorage.getItem("mapCenter");
    let savedZoom = localStorage.getItem("mapZoom");

    let map;

    if (savedCenter && savedZoom) {

        savedCenter = JSON.parse(savedCenter);

        map = L.map('map').setView(
            [savedCenter.lat, savedCenter.lng],
            parseInt(savedZoom)
        );

    } else {

        map = L.map('map').setView(
            [-2.5489, 118.0149],
            5
        );

    }

    // ==========================
    // TILE MAP
    // ==========================

    L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            attribution: '© OpenStreetMap'
        }
    ).addTo(map);

    // ==========================
    // SIMPAN POSISI PETA
    // ==========================

    map.on('moveend', function () {

        const center = map.getCenter();

        localStorage.setItem(
            "mapCenter",
            JSON.stringify(center)
        );

        localStorage.setItem(
            "mapZoom",
            map.getZoom()
        );

    });

    // ==========================
    // CLUSTER
    // ==========================

    const markers = L.markerClusterGroup();

    // ==========================
    // DROPDOWN
    // ==========================

    const kotaSelect =
        document.getElementById("kota");

    // ==========================
    // LOAD JSON
    // ==========================

    fetch('/static/indonesia_regions.json')

        .then(response => response.json())

        .then(cities => {

            cities.sort((a, b) =>
                a.name.localeCompare(b.name)
            );

            cities.forEach(city => {

                // ==========================
                // OPTION DROPDOWN
                // ==========================

                const option =
                    document.createElement("option");

                option.value = city.name;

                option.textContent =
                    `${city.name} (${city.province})`;

                kotaSelect.appendChild(option);

                // ==========================
                // MARKER
                // ==========================

                const marker = L.marker([
                    city.lat,
                    city.lng
                ]);

                marker.bindPopup(`
                    <b>${city.name}</b><br>
                    ${city.province}
                `);

                // ==========================
                // KLIK MARKER
                // ==========================

                marker.on('click', function () {

                    // Simpan posisi terakhir

                    localStorage.setItem(
                        "mapCenter",
                        JSON.stringify(map.getCenter())
                    );

                    localStorage.setItem(
                        "mapZoom",
                        map.getZoom()
                    );

                    kotaSelect.value =
                        city.name;

                    document
                        .querySelector('form')
                        .submit();

                });

                markers.addLayer(marker);

            });

            map.addLayer(markers);

        })

        .catch(error => {

            console.error(
                "Gagal memuat data kota:",
                error
            );

        });

    // ==========================
    // CHART SUHU
    // ==========================

    if (
        typeof temps !== 'undefined' &&
        document.getElementById('weatherChart')
    ) {

        const ctx =
            document.getElementById('weatherChart');

        new Chart(ctx, {

            type: 'line',

            data: {

                labels: labels,

                datasets: [{

                    label: 'Suhu (°C)',

                    data: temps,

                    borderColor: '#facc15',

                    backgroundColor:
                        'rgba(250,204,21,0.2)',

                    tension: 0.4,

                    fill: true

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        labels: {

                            color: 'white'

                        }

                    }

                },

                scales: {

                    x: {

                        ticks: {

                            color: 'white'

                        }

                    },

                    y: {

                        ticks: {

                            color: 'white'

                        }

                    }

                }

            }

        });

    }

});