// JavaScript file for login page

// Event listener for login form
document.getElementById("login-form").addEventListener("submit", function(e) {
    // Disable button to prevent spam
    var submitbutton = document.getElementById("login-button");
    submitbutton.disabled = true;

    e.preventDefault();
    formData = new FormData(this);

    // Do post request
    var url = "/login_form_handler";
    fetch(url, {
        method:'POST',
        body: formData
    })

    // Convert response to json
    .then(response => response.json())

    // Handle response data
    .then(data => {
        setTimeout(function(){
            submitbutton.disabled = false;
        }, 200)

        switch(data.error) {
            case "invalid":
                showError("Noe gikk galt. Vær sikker på at informasjonen du skrev inn er riktig.");
                break;
            case "wrong":
                showError("Brukernavn eller passord feil.")
                break;
        }

        if (data.redirect == 1) {
            window.location = "/hovedside";
        }
    })

    .catch(error => {
        setTimeout(function(){
            submitbutton.disabled = false;
        }, 200)
        showError("Noe gikk galt. Prøv igjen senere.");
    });
});

// Switches visibility of password input
document.getElementById("password-visibility-checkbox").addEventListener("click", function() {
    if (document.getElementById("password-visibility-checkbox").checked) {
        document.getElementById("id_password").type = "text";
    } else {
        document.getElementById("id_password").type = "password";
    }
})