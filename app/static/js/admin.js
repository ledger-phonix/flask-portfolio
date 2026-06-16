
// admin side file upload preview
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name-display');
    const imagePreview = document.getElementById('image-preview');
    const uploadIcon = document.getElementById('upload-icon');
    const uploadText = document.getElementById('upload-text');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];

            if (file) {
                // 1. Show the file name
                fileNameDisplay.textContent = `Selected: ${file.name}`;
                uploadText.textContent = "Change File";

                // 2. Create an Image Preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.classList.remove('hidden'); // Show the image
                    uploadIcon.classList.add('text-blue-500'); // Change icon color
                }
                reader.readAsDataURL(file);
            }
        });
    }
});


