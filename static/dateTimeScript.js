// Function to get the current date and time
function getCurrentDateTime() {
    const now = new Date();
    const date = now.toISOString().slice(0, 10); // Get the date in YYYY-MM-DD format
    const time = now.toTimeString().slice(0, 8); // Get the time in HH:MM:SS format
    return { date: date, time: time };
}

// Populate the hidden fields with the current date and time
window.addEventListener("DOMContentLoaded", function() {
    const dateTime = getCurrentDateTime();
    document.getElementById("submissionDate").value = dateTime.date;
    document.getElementById("submissionTime").value = dateTime.time;
});