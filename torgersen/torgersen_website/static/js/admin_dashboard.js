// JavaScript file for admin dashboard

// Shows a popup for 3 seconds
function showPopUp(message) {
    var popup = document.getElementById("popup");
    popup.innerHTML = message;
    popup.style.display = "inline";
    setTimeout(function(){
        popup.style.display = "none";
    }, 3000);
}

// Get csrftoken from cookie
const csrfToken = document.cookie.split(';')
    .find(cookie => cookie.trim().startsWith('csrftoken='))
    ?.split('=')[1];

// Function for changing role of user
function changeRole(user_id) {
    var url = "/admin_change_role";

    // POST user id to server
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: "same-origin",
        body: JSON.stringify({
            user_id:user_id
        })
    })

    // Convert response to JSON
    .then(response => response.json())

    // Handle the response
    .then(data => {
        switch(data.error) {
            case "error":
                showPopUp("Noe gikk galt.")
                break;
        }

        if (data.success == 1) {
            document.getElementById(data.div_id).innerHTML = data.newrole
            showPopUp("Rolle endret.")
        }
    })

    .catch(error => {
        // If something goes wrong
        showPopUp("Noe gikk galt.")
    });
}