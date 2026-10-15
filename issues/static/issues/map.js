
document.addEventListener("DOMContentLoaded", function () {

    const mapDiv = document.getElementById("map");
    const openMapBtn = document.getElementById("open-map");

    let map = null;
    let marker = null;

    openMapBtn.addEventListener("click", function () {

        // Show map
        mapDiv.style.display = "block";

        // Create map only once
        if (!map) {

            map = L.map("map").setView([18.5204, 73.8567], 13);

            L.tileLayer(
                "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                {
                    attribution: "&copy; OpenStreetMap contributors"
                }
            ).addTo(map);
            L.Control.geocoder({
    defaultMarkGeocode: false
})
.on('markgeocode', function(e) {

    const latlng = e.geocode.center;

    // Move map to searched location
    map.setView(latlng, 16);

    // Remove previous marker
    if (marker) {
        map.removeLayer(marker);
    }

    // Add marker
    marker = L.marker(latlng).addTo(map);

    // Set latitude
    document.getElementById("id_latitude").value =
        latlng.lat;

    // Set longitude
    document.getElementById("id_longitude").value =
        latlng.lng;

    // Set location name
    document.getElementById("id_location").value =
        e.geocode.name;

})
.addTo(map);

            // Select location by clicking on map
            map.on("click", function (e) {

                // Remove old marker
                if (marker) {
                    map.removeLayer(marker);
                }

                // Add new marker
                marker = L.marker(e.latlng).addTo(map);

                // Set latitude
                document.getElementById("id_latitude").value =
                    e.latlng.lat;

                // Set longitude
                document.getElementById("id_longitude").value =
                    e.latlng.lng;

                // Reverse geocoding
                fetch(
                    `https://nominatim.openstreetmap.org/reverse?lat=${e.latlng.lat}&lon=${e.latlng.lng}&format=json`
                )
                .then(response => response.json())
                .then(data => {

                    // Set location/address
                    document.getElementById("id_location").value =
                        data.display_name;

                })
                .catch(error => {
                    console.error("Error getting location:", error);

                    document.getElementById("id_location").value =
                        `Lat: ${e.latlng.lat}, Lng: ${e.latlng.lng}`;
                });

            });
        }

        // Fix Leaflet rendering when map was initially hidden
        setTimeout(function () {
            map.invalidateSize();
        }, 100);

    });

});

