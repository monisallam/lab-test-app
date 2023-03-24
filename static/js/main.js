// main.js

$(document).ready(function () {
    $("#login-form").on("submit", function (event) {
        event.preventDefault();

        $.ajax({
            url: "/login_action",
            method: "POST",
            data: $(this).serialize(),
            success: function (response) {
                if (response.status === "success") {
                    //window.location.href = "/"; // Redirect to the home page
                    window.location.replace("/"); // Replace the current resource with the home page
                } else {
                    alert(response.message);
                }
            },
        });
    });

    $("#signup-form").on("submit", function (event) {
        event.preventDefault();

        $.ajax({
            url: "/signup_action",
            method: "POST",
            data: $(this).serialize(),
            success: function (response) {
                if (response.status === "success") {
                    alert("You have successfully signed up!");
                    //window.location.href = "login.html";
                    window.location.replace("/login");

                } else {
                    alert(response.message);
                }
            },
        });
    });

    $("#upload-form").on("submit", function (event) {
        event.preventDefault();
        let formData = new FormData(this);
        formData.append('csrf_token', $('#csrf_token').val());


        $.ajax({
            url: "/upload",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.status === "success") {
                    alert("File uploaded successfully");
                } else {
                    alert(response.message);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('Error: ' + textStatus + ' - ' + errorThrown); // Display any error message related to the AJAX request itself
                console.log('Error: ' + textStatus); // Log the textStatus
                console.log('Error Thrown: ' + errorThrown); // Log the errorThrown
                console.log(jqXHR); // Log the complete jqXHR object
                //alert('An error occurred. Please try again.'); // Show a generic error message
            }
            
        });
    });
});
