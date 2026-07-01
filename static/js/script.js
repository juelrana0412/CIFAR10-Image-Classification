const imageInput = document.getElementById("imageInput");

const previewImage = document.getElementById("previewImage");

const form = document.getElementById("predictionForm");

const loading = document.getElementById("loading");

const predictButton = document.getElementById("predictButton");


// ======================================
// Image Preview
// ======================================

imageInput.addEventListener("change", function(){

    const file = this.files[0];

    if(file){

        const reader = new FileReader();

        reader.onload = function(e){

            previewImage.src = e.target.result;

            previewImage.style.display = "block";

        }

        reader.readAsDataURL(file);

    }

});


// ======================================
// Submit
// ======================================

form.addEventListener("submit", function(){

    loading.style.display = "block";

    predictButton.disabled = true;

    predictButton.innerHTML = `
        <span class="spinner-border spinner-border-sm"></span>
        Predicting...
    `;

});


// ======================================
// Drag & Drop
// ======================================

const dropArea = previewImage.parentElement;

dropArea.addEventListener("dragover",(e)=>{

    e.preventDefault();

});

dropArea.addEventListener("drop",(e)=>{

    e.preventDefault();

    const file = e.dataTransfer.files[0];

    if(!file) return;

    imageInput.files = e.dataTransfer.files;

    const reader = new FileReader();

    reader.onload=(event)=>{

        previewImage.src=event.target.result;

        previewImage.style.display="block";

    }

    reader.readAsDataURL(file);

});


// ======================================
// Validate Image
// ======================================

imageInput.addEventListener("change",()=>{

    const file=imageInput.files[0];

    if(!file) return;

    const types=[
        "image/jpeg",
        "image/png",
        "image/jpg",
        "image/webp"
    ];

    if(!types.includes(file.type)){

        alert("Please upload JPG, PNG or WEBP image.");

        imageInput.value="";

        previewImage.style.display="none";

    }

});


// ======================================
// Reset Spinner if User Returns
// ======================================

window.onload=function(){

    loading.style.display="none";

    predictButton.disabled=false;

    predictButton.innerHTML=`
        <i class="bi bi-magic"></i>
        Predict
    `;

}