

document.querySelector("#subirFoto").onclick = async () => {
    let formData = new FormData();
    const fileField = document.querySelector("#foto");
    const usuario = document.querySelector("#usuario").value;
    const url = document.querySelector("#subirFoto").getAttribute("path");
    
    formData.append('usuario', usuario);
    formData.append('foto', fileField.files[0]);
    
    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => location.reload())
    .catch(error => console.error('Error:', error))
}

