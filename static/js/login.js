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

    const resp = await fetch(url, {
            method: 'POST',
            body: formData,
        });
    if(resp.ok) {
        window.location.href = redirect;
    }           
}

document.querySelector("#usuario").onkeypress = (e) => {
    // Si el usuario presionó "enter"
    // ejecutar la rutina del boton
    if (e.key === "Enter") {
        // Cancel the default action, if needed
        e.preventDefault();
        // Trigger the button element with a click
        document.querySelector("#ingresar").click();
      }   
};

document.querySelector("#password").onkeypress = (e) => {
    // Si el usuario presionó "enter"
    // ejecutar la rutina del boton
    if (e.key === "Enter") {
        // Cancel the default action, if needed
        e.preventDefault();
        // Trigger the button element with a click
        document.querySelector("#ingresar").click();
      }   
};