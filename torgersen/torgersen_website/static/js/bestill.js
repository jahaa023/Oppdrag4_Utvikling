// JavaScript file for ordering page

// Event listener for dropdown button for mobile
document.getElementById("mobile-dropdown-button").addEventListener("click", function() {
    var dropdownContainer = document.getElementById("mobile-dropdown-container");
    var dropdownButton = document.getElementById("mobile-dropdown-button");
    dropdownButton.disabled = true;

    if (window.getComputedStyle(dropdownContainer).display == "none") {
        // Show dropdown
        dropdownContainer.style.display = "flex";
        dropdownButton.style.backgroundImage = "url(/static/img/icons/x-white.svg)";
        setTimeout(function() {
            dropdownButton.disabled = false;
        }, 200)
    } else {
        // Hide dropdown
        dropdownContainer.style.display = "none";
        dropdownButton.style.backgroundImage = "url(/static/img/icons/dropdown-white.svg)";
        setTimeout(function() {
            dropdownButton.disabled = false;
        }, 200)
    }
})

// Event listener for order form
document.getElementById("order-form").addEventListener("submit", function(e) {
    e.preventDefault();
    formData = new FormData(this);

    // Disable button to prevent spam
    var submitbutton = document.getElementById("order-button");
    submitbutton.disabled = true;

    // Do post request
    var url = "/place_order";
    fetch(url, {
        method:'POST',
        body: formData
    })

    // Convert response to json
    .then(response => response.json())

    .then(data => {
        // Enable button after 200 ms
        setTimeout(function(){
            submitbutton.disabled = false;
        }, 200)

        // Switch for potential errors
        switch(data.error) {
            case "invalid":
                // If formdata is invalid (inputs are empty or email isnt an email etc.)
                showError("Noe gikk galt. Vær sikker på at informasjonen du skrev inn er riktig.");
                break;
        }

        // If everything went well
        if (data.ok == 1) {
            // Show thank you modal when user has ordered
            var url = "/thank_you_modal";

            // POST the form to get the author and book name
            fetch(url, {
                method:'POST',
                body: formData
            })

            // Convert the response into the html it responded with
            .then(response => response.text())

            // Put the html into a container that covers screen with a transparent black background
            .then(html => {
                var darkContainer = document.getElementById("dark-container");
                darkContainer.innerHTML = html;
                darkContainer.style.display = "inline"
            })

            // Add event listener for "ok" button inside the modal
            .then(function() {
                document.getElementById("hide-modal").addEventListener("click", function() {
                    var darkContainer = document.getElementById("dark-container");
                    darkContainer.style.display = "none";
                    darkContainer.innerHTML = "";
                })
            })

            .catch(error => {
                // Fail safe if modal fails to load
                alert("Tusen takk for din bestilling.")
            });
        }
    })

    .catch(error => {
        // If there was an error
        setTimeout(function(){
            submitbutton.disabled = false;
        }, 200)
        showError("Noe gikk galt. Vennligst prøv igjen senere.")
    });
});