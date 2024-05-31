document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("submitButton").addEventListener("click", function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Show loading indicator and disable button
    document.getElementById("buttonText").style.display = "none";
    document.getElementById("loadingIndicator").style.display = "inline-block";
    document.getElementById("submitButton").disabled = true;

    // Submit the form programmatically
    document.getElementById("myForm").submit();
  });
});

