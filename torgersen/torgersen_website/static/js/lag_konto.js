// JavaScript file for account creation page

// Event listener for account creation form
document.getElementById("create-account-form").addEventListener("submit", function(e) {
    e.preventDefault();
    formData = new FormData(this);

    // Do post request
    var url = "/create_account_form_handler";
    fetch(url, {
        method:'POST',
        body: formData
    })

    .then(response => response.json())

    .then(data => {
        switch(data.error) {
            case "invalid":
                showError("Noe gikk galt. Vær sikker på at informasjonen du skrev inn er riktig.");
                break;
            case "username_taken":
                showError("Dette brukernavnet er tatt. Vennligst prøv et annet.")
                break;
            case "email_registered":
                showError("Denne e-post adressen er allerede registrert til en konto.")
                break;
            case "ascii":
                showError("Brukernavnet ditt kan ikke inneholde norske bokstaver.")
                break;
        }

        if (data.redirect == 1) {
            alert("ok")
        }
    })

    .catch(error => {
        alert("error")
    });
});