// Enable image overlay with hover effects
enableImageOverlay();

function readURL(input) {
    if (input.files && input.files[0]) {
        // Create a new FileReader instance
        var reader = new FileReader();
        showLoadingIndicator();

        reader.onload = function (e) {
            // Disable overlay effects for cropping mode
            disableImageOverlay();

            var imageField = document.getElementById('id_profile_image_display');
            imageField.src = e.target.result;

            // Initialize Cropper instance
            if (window.cropper) {
                window.cropper.destroy(); // Destroy any existing cropper instance
            }

            window.cropper = new Cropper(imageField, {
                aspectRatio: 1, // Keep the image square
                viewMode: 1, // Restrict cropping box to the image area
            });

            // Confirm button event: crop and upload image
            document.getElementById('id_confirm').addEventListener('click', function () {
                var croppedCanvas = cropper.getCroppedCanvas();
                croppedCanvas.toBlob(function (blob) {
                    // Convert the cropped blob to a file-like object
                    var file = new File([blob], input.files[0].name, { type: input.files[0].type });
                    uploadCroppedImage(file);
                });
            });

            hideLoadingIndicator();
        };

        // Read the uploaded file as a Data URL
        reader.readAsDataURL(input.files[0]);
    }
}

// Show loading indicator
function showLoadingIndicator() {
    var loadingIndicator = document.getElementById('loading-indicator');
    loadingIndicator.classList.remove('d-none');
}

// Hide loading indicator
function hideLoadingIndicator() {
    var loadingIndicator = document.getElementById('loading-indicator');
    loadingIndicator.classList.add('d-none');
}

// Upload the cropped image to the server
function uploadCroppedImage(file) {
    var reader = new FileReader();

    // Set up a callback once the file is read
    reader.onload = function(e) {
        // Get the base64 string
        var base64String = e.target.result;

        // Debugging: Log the base64 string and CSRF token
        console.log('Base64 String:', base64String);
        console.log('CSRF Token:', document.querySelector('[name=csrfmiddlewaretoken]').value);

        // Create FormData object and append the base64 string
        var formData = new FormData();
        formData.append('image', base64String);

        // Send the base64 string to the backend
        fetch('/upload-cropped-image/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Server Response:', data);
            if (data.success) {
                window.location.reload(); // Reload the page or redirect to the profile
            } else {
                alert(`Failed to upload image: ${data.error || 'Unknown error'}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    };

    // Read the file as a data URL (base64 string)
    reader.readAsDataURL(file);
}


// Enable hover effects and image selection
function enableImageOverlay() {
    var text = document.getElementById("id_text");
    var profileImage = document.getElementById("id_profile_image_display");
    var middleContainer = document.getElementById("id_middle_container");
    var imageContainer = document.getElementById("id_image_container");
    var cropConfirm = document.getElementById("id_image_crop_confirm");

    // Apply styles
    text.style.backgroundColor = "#0066ff";
    text.style.color = "white";
    text.style.fontSize = "16px";
    text.style.padding = "16px 32px";
    text.style.cursor = "pointer";

    middleContainer.style.transition = ".5s ease";
    middleContainer.style.opacity = "0";
    middleContainer.style.position = "absolute";
    middleContainer.style.top = "50%";
    middleContainer.style.left = "50%";
    middleContainer.style.transform = "translate(-50%, -50%)";
    middleContainer.style.textAlign = "center";

    // Hover effects
    imageContainer.addEventListener("mouseover", function () {
        profileImage.style.opacity = "0.3";
        middleContainer.style.opacity = "1";
    });

    imageContainer.addEventListener("mouseout", function () {
        profileImage.style.opacity = "1";
        middleContainer.style.opacity = "0";
    });

    // Click to open file input
    imageContainer.addEventListener("click", function () {
        document.getElementById('id_profile_image').click();
    });

    // Hide crop controls
    cropConfirm.classList.add("d-none");
}

// Disable hover effects and enable cropping controls
function disableImageOverlay() {
    var profileImage = document.getElementById("id_profile_image_display");
    var middleContainer = document.getElementById("id_middle_container");
    var imageContainer = document.getElementById("id_image_container");
    var text = document.getElementById("id_text");
    var cropConfirm = document.getElementById("id_image_crop_confirm");

    // Remove hover effects
    profileImage.style.opacity = "1";
    middleContainer.style.opacity = "0";
    text.style.cursor = "default";
    text.style.opacity = "0";

    // Remove event listeners
    imageContainer.replaceWith(imageContainer.cloneNode(true));

    // Show crop controls
    cropConfirm.classList.remove("d-none");
    cropConfirm.classList.add("d-flex", "flex-row", "justify-content-between");

    // Cancel button: reload the page
    document.getElementById("id_cancel").addEventListener("click", function () {
        window.location.reload();
    });
}
