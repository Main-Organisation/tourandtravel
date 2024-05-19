// Example to toggle the display of forms or data tables
function toggleDisplay(elementId) {
    var element = document.getElementById(elementId);
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

// Add your JavaScript and AJAX functions here
document.getElementById("supplierForm").addEventListener("submit", function(event){
    event.preventDefault();
    // Add your code here to handle the form submission, like sending data to a server or validating input
    alert("Form submitted!");
});
