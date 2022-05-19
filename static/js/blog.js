
// The x-www-form-urlencoded is used more generally to send
// text data to the server
// while multipart/form-data is used to send binary data,
// most notably for uploading files to the server.

document.querySelector("#foto").onchange = () => {
    const fileField = document.querySelector("#foto");
    if(fileField.files[0].size > 1*1024*1024) { // more than 1MB
        alert(`El archivo ${fileField.files[0].name} es mayor a 1MB.`);
        fileField.value = null;
    }
};

document.querySelector("#subirFoto").onclick = async () => {
    let formData = new FormData();
    const fileField = document.querySelector("#foto");
    const usuario = document.querySelector("#usuario").value;
    const apikey = document.querySelector("#apikey").value;
    const url = document.querySelector("#subirFoto").getAttribute("path");
    
    formData.append('usuario', usuario);
    formData.append('apikey', apikey);
    formData.append('foto', fileField.files[0]);
    
    // Como estamos enviando un archivo el fetch
    // configurara el body y header para enviar
    // datos binarios (multipart/form-data)
    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => location.reload())
    .catch(error => console.error('Error:', error))
}

document.querySelector("#publicar").onclick = async () => {
    let formData = new FormData();
    const usuario = document.querySelector("#usuario").value;
    const apikey = document.querySelector("#apikey").value;
    const titulo = document.querySelector("#titulo").value;
    const texto = document.querySelector("#texto").value;
    const url = document.querySelector("#publicar").getAttribute("path");
    
    const data = {
        usuario: usuario,
        apikey: apikey,
        titulo: titulo,
        texto: texto,
    }
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => window.location.reload(true))
    .catch(error => console.error('Error:', error))
}


const usuario = document.querySelector("#usuario").value;
const apikey = document.querySelector("#apikey").value;
const url = document.querySelector("#publicar").getAttribute("path");

const params = { 
    usuario: usuario,
    apikey: apikey,
};
// this line takes the params object and builds the query string
const query = Object.keys(params)
             .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
             .join('&');

fetch(url + "?" + query)
    .then(response => response.json())
    .then(data => data.posts)
    .then(posts => {
        let accumulator = ""
        
        posts.forEach(post => {
            accumulator += 
                `
                <div>
                    <p id="titulo">${post.titulo}</p>
                    <p id="texto">${post.texto}</p>
                    <hr>
                </div>
                `
        });
        const section = document.querySelector("#posteos");
        section.innerHTML = accumulator;
    })

