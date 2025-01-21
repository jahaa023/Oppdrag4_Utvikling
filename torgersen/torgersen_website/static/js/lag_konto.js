// JavaScript file for account creation page

// Event listener for account creation form
document.getElementById("create-account-form").addEventListener("submit", function(e) {
    e.preventDefault();
    formData = new FormData(this);

    // Disable button to prevent spam
    var submitbutton = document.getElementById("create-account-button");
    submitbutton.disabled = true;

    // Do post request
    var url = "/create_account_form_handler";
    fetch(url, {
        method:'POST',
        body: formData
    })

    // Convert response to json
    .then(response => response.json())

    .then(data => {
        setTimeout(function(){
            submitbutton.disabled = false;
        }, 200)
        // Switch for potential errors
        switch(data.error) {
            case "invalid":
                // If form data is invalid
                showError("Noe gikk galt. Vær sikker på at informasjonen du skrev inn er riktig.", "indiv");
                break;
            case "username_taken":
                showError("Dette brukernavnet er tatt. Vennligst prøv et annet.", "indiv");
                break;
            case "email_registered":
                showError("Denne e-post adressen er allerede registrert til en konto.", "indiv");
                break;
            case "ascii":
                // If username contains non english chars
                showError("Brukernavnet ditt kan ikke inneholde norske bokstaver eller mellomrom.", "indiv");
                break;
            case "numeric":
                // If username only contains numbers
                showError("Brukernavnet ditt kan ikke bare inneholde tall.", "indiv");
                break;
        }

        // If account was created
        if (data.redirect == 1) {
            window.location = "/hovedside"
        }
    })

    .catch(error => {
        // If anything goes wrong
        setTimeout(function(){
            submitbutton.disabled = false;
        }, 200)
        showError("Noe gikk galt. Vennligst prøv igjen senere.", "indiv")
    });
});

// Get csrftoken from cookie
const csrfToken = document.cookie.split(';')
    .find(cookie => cookie.trim().startsWith('csrftoken='))
    ?.split('=')[1];

// When username input is typed into, post to username validator. Has to post to backend to check if username is taken
document.getElementById("id_username").addEventListener("keyup", function() {
    // Full opacity after username input has been inputted
    document.getElementById("username-validate-p").style.opacity = "1";
    document.getElementById("username-validate-ul").style.opacity = "1";

    // Do post request
    var url = "/username_validate";
    var username = document.getElementById("id_username").value;
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: "same-origin",
        body: JSON.stringify({username : username})
    })

    .then(response => response.json())

    .then(data => {
        // If username contains non english charss
        if (data.ascii == 1) {
            document.getElementById("ascii").style.color = "var(--warning-red)"
        } else {
            document.getElementById("ascii").style.color = "var(--primary-green)"
        }

        // If username has spaces
        if (data.whitespace == 1) {
            document.getElementById("whitespace").style.color = "var(--warning-red)"
        } else {
            document.getElementById("whitespace").style.color = "var(--primary-green)"
        }

        // If username is only numbers
        if (data.numeric == 1) {
            document.getElementById("numeric").style.color = "var(--warning-red)"
        } else {
            document.getElementById("numeric").style.color = "var(--primary-green)"
        }

        // If username is not between 5 to 32 chars
        if (data.between == 1) {
            document.getElementById("between").style.color = "var(--warning-red)"
        } else {
            document.getElementById("between").style.color = "var(--primary-green)"
        }

        // If username is taken
        if (data.taken == 1) {
            document.getElementById("taken").style.color = "var(--warning-red)"
        } else {
            document.getElementById("taken").style.color = "var(--primary-green)"
        }
    })

    .catch(error => {
        // If post request fails
        document.getElementById("username-validate-container").innerHTML = "Noe gikk galt."
    });
})

// Switches visibility of password input
document.getElementById("password-visibility-checkbox").addEventListener("click", function() {
    if (document.getElementById("password-visibility-checkbox").checked) {
        document.getElementById("id_password").type = "text";
    } else {
        document.getElementById("id_password").type = "password";
    }
})

// When password is typed, show suggestion for security. Can be done on frontend because its just a suggestion
document.getElementById("id_password").addEventListener("keyup", function() {
    document.getElementById("password-validate-p").style.opacity = "1";
    document.getElementById("password-validate-ul").style.opacity = "1";

    // Get password
    var password = document.getElementById("id_password").value;

    // Check if password contains special chars
    document.getElementById("password-special").style.color = "var(--warning-red)";

    // For each letter in password, check if letter is not inside blacklist
    var blacklist = "abcdefghijklmnopqrstuvxyz0123456789";
    var char = "";
    for (let i = 0; i < password.length; i++) {
        char = password.charAt(i);
        char = char.toLowerCase();
        if (!blacklist.includes(char)) {
            document.getElementById("password-special").style.color = "var(--primary-green)";
        }
    }

    // Check if password contains both lower and upper case letters
    const upper = /[A-Z]/.test(password);
    const lower = /[a-z]/.test(password);
    if (upper && lower) {
        document.getElementById("password-case").style.color = "var(--primary-green)";
    } else {
        document.getElementById("password-case").style.color = "var(--warning-red)";
    }

    // Check if password is atleast 10 letters
    if (password.length >= 10) {
        document.getElementById("password-lenght").style.color = "var(--primary-green)";
    } else {
        document.getElementById("password-lenght").style.color = "var(--warning-red)";
    }
})