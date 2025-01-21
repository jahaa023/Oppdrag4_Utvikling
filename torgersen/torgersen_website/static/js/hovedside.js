// JavaScript file for main page

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