

document.querySelector("#subirFoto").onclick = async () => {
    let formData = new FormData();
    const fileField = document.querySelector("#foto");
    const usuario = document.querySelector("#usuario").value;
    const apikey = document.querySelector("#apikey").value;
    const url = document.querySelector("#subirFoto").getAttribute("path");
    
    formData.append('usuario', usuario);
    formData.append('apikey', apikey);
    formData.append('foto', fileField.files[0]);
    
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
    const url = document.querySelector("#publicar").getAttribute("path");
    
    formData.append('usuario', usuario);
    formData.append('foto', fileField.files[0]);
    
    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => location.reload())
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
                    <p>${post.titulo}</p>
                    <p>${post.texto}</p>
                </div>
                `
        });
        const section = document.querySelector("#posteos");
        section.innerHTML = accumulator;
    })

