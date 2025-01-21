// JavaScript file for page for seeing your placed orders

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

// Get csrftoken from cookie
const csrfToken = document.cookie.split(';')
    .find(cookie => cookie.trim().startsWith('csrftoken='))
    ?.split('=')[1];

// Function for showing modal for confirming cancellation of book
function cancelOrderModal(order_id) {
    var url = "/cancel_order_modal";

    // POST to server and get modal back
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        credentials: "same-origin",
        body: JSON.stringify({
            order_id : order_id
        })
    })

    // Convert the response into the html it responded with
    .then(response => response.text())

    // Put the html into a container that covers screen with a transparent black background
    .then(html => {
        if (html == "error") {
            showError("Noe gikk galt.")
        } else {
            var darkContainer = document.getElementById("dark-container");
            darkContainer.innerHTML = html;
            darkContainer.style.display = "inline"
        }
    })

    // Add event listener form and button to cancel cancellation
    .then(function() {
        document.getElementById("hide-modal").addEventListener("click", function() {
            var darkContainer = document.getElementById("dark-container");
            darkContainer.style.display = "none";
            darkContainer.innerHTML = "";
        })

        document.getElementById("cancel-form").addEventListener("submit", function(e) {
            e.preventDefault();
            formData = new FormData(this)

            // Do post request to cancel order
            var url = "/cancel_order";
            fetch(url, {
                method:'POST',
                body: formData
            })

            // Convert response to json
            .then(response => response.json())

            // Handle response data
            .then(data => {
                switch(data.error) {
                    case "error":
                        // If anything went wrong, hide modal and tell user
                        hideModal();
                        break;
                }

                if (data.ok == 1) {
                    // If order was cancelled successfully

                    // Delete div containing order
                    document.getElementById(data.div_id).remove();

                    var modal = document.getElementById("cancel-modal");

                    // Change modal
                    modal.innerHTML = "<h1>Bestillingen ble kansellert.<h1><button id='ok-button' onclick='hideModal()'>Ok</button>";
                }
            })

            .catch(error => {
                // If anything went wrong, hide modal and tell user
                hideModal();
                showError("Noe gikk galt.");
            });
        })
    })

    .catch(error => {
        // If modal fails to load
        showError("Noe gikk galt.")
    });
}

// Hides modal
function hideModal() {
    var darkContainer = document.getElementById("dark-container");
    darkContainer.style.display = "none";
    darkContainer.innerHTML = "";
}