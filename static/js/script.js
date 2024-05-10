/* hide messages errors after 5 second*/

var message  =  document.getElementById("messages")
if(message !== null){
    setTimeout(() => {
        message.style.display = 'none';
    }, 7000);
}
/* end  hide messages errors after 5 second*/



// Add event listener to all file input elements
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(fileInput) {    
        fileInput.addEventListener('change', checkAllFileSizes);
    });
});

function checkAllFileSizes() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(fileInput) {
        const file = fileInput.files[0];
        if (file) {
            const fileSize = file.size / (1024 * 1024); // Convert bytes to MB
            if (fileSize > 20) {
                const modal = new bootstrap.Modal(document.getElementById('fileSizeModal'));
                modal.show();
                fileInput.value = '';
            }
        }
    });
}
