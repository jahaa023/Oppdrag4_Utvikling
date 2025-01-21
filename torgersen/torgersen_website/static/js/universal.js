// JavaScript file for every page

// Shows an error in red text when something goes wrong
function showError(error, indiv) {
    var errorContainer = document.getElementById("error-warning");

    // Replace norwegian charchters with unicode escape sequences
    error = error.replace("æ", "\u00E6")
    error = error.replace("ø", "\u00F8")
    error = error.replace("å", "\u00E5")

    error = error.replace("Æ", "\u00C6")
    error = error.replace("Ø", "\u00D8")
    error = error.replace("Å", "\u00C5")

    errorContainer.innerText = error;
    errorContainer.style.display = "block";

    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (indiv == "indiv") {
        errorContainer.scrollIntoView()
    }
}