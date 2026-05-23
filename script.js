// Upload filename preview

const fileInput = document.querySelector('input[type="file"]');
const uploadText = document.querySelector('.upload-content span');

fileInput.addEventListener('change', function(){

    if(fileInput.files.length > 0){

        uploadText.textContent =
            fileInput.files[0].name;

    }

});