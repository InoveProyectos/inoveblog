document.querySelector("#ingresar").onclick = async () => {
    const usuario = document.querySelector("#usuario").value;
    const password = document.querySelector("#password").value;
    if(usuario == "" || password == "") {   
        alert("Indique usuario y contraseña");
        return;
    }
    const formData = new FormData();
    formData.append("usuario", usuario);
    formData.append("password", password);

    const url = document.querySelector("#ingresar").getAttribute("path");
    const redirect = document.querySelector("#ingresar").getAttribute("redirect");
    // const data = {"usuario": usuario, "password": password};            
    // const resp = await fetch(url, {
    //                 method: 'POST',
    //                 body: JSON.stringify(data),
    //                 headers:{
    //                     'Content-Type': 'application/json'
    //                     }
    //                 }
    //             );
    const resp = await fetch(url, {
                method: 'POST',
                body: formData,
            });
    if(resp.ok) {
        window.location.href = redirect;
    }           
}