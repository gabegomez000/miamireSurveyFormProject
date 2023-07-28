// Function to get the current date
function getCurrentDate() {
    const now = new Date();
    const date = now.toISOString().slice(0, 10); // Get the date in YYYY-MM-DD format
    return { date: date};
}

// Populate the hidden field with the current date
window.addEventListener("DOMContentLoaded", function() {
    const dateTime = getCurrentDate();
    document.getElementById("submissionDate").value = dateTime.date;
});