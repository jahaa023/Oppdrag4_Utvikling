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

    .then(response => response.json())

    .then(data => {
        setTimeout(function(){
            submitbutton.disabled = false;
        }, 200)
        switch(data.error) {
            case "invalid":
                showError("Noe gikk galt. Vær sikker på at informasjonen du skrev inn er riktig.", "indiv");
                break;
        }

        if (data.ok == 1) {
            showError("Bestilling lagret! Du kan se dine bestillinger på 'Min kø'.")
        }
    })

    .catch(error => {
        setTimeout(function(){
            submitbutton.disabled = false;
        }, 200)
        showError("Noe gikk galt. Vennligst prøv igjen senere.", "indiv")
    });
});