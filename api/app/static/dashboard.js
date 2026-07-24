const estadoAPI = document.getElementById("estado-api");
const textoAPI = document.getElementById("texto-api");
const textoDB = document.getElementById("texto-db");
const cantidad = document.getElementById("cantidad-componentes");
const latencia = document.getElementById("latencia-health");
const tabla = document.getElementById("tabla-componentes");
const resultado = document.getElementById("resultado-benchmark");
const registro = document.getElementById("registro");

function log(mensaje){
    registro.innerHTML += "<br>" + new Date().toLocaleTimeString() + " - " + mensaje;
    registro.scrollTop = registro.scrollHeight;
}

async function cargarHealth(){

    const inicio = performance.now();

    const respuesta = await fetch("/health");

    const datos = await respuesta.json();

    const tiempo = Math.round(performance.now()-inicio);

    textoAPI.textContent = datos.status;
    textoDB.textContent = datos.database;
    latencia.textContent = tiempo + " ms";

    if(datos.status==="ok"){

        estadoAPI.textContent="API ACTIVA";
        estadoAPI.className="estado estado-ok";

    }else{

        estadoAPI.textContent="ERROR";
        estadoAPI.className="estado estado-error";

    }

    log("Health consultado");
}

async function cargarComponentes(){

    const respuesta = await fetch("/api/components");

    const datos = await respuesta.json();

    cantidad.textContent = datos.cantidad;

    tabla.innerHTML="";

    datos.componentes.forEach(c=>{

        tabla.innerHTML+=`
        <tr>
            <td>${c.id}</td>
            <td>${c.name}</td>
            <td>${c.manufacturer}</td>
            <td>${c.component_type.name}</td>
            <td>${c.power_consumption_w} W</td>
            <td>${c.release_year}</td>
        </tr>
        `;

    });

    log("Inventario actualizado");

}

async function benchmark(){

    const iteraciones=document.getElementById("iteraciones").value;

    resultado.innerHTML="Ejecutando...";

    const respuesta=await fetch("/api/benchmarks/cpu?iterations="+iteraciones);

    const datos=await respuesta.json();

    resultado.innerHTML=`
        <b>Iteraciones:</b> ${datos.iterations}<br>
        <b>Tiempo:</b> ${datos.duration_ms} ms<br>
        <b>Checksum:</b> ${datos.checksum}
    `;

    log("Benchmark ejecutado");

}

document
.getElementById("boton-recargar")
.onclick=cargarComponentes;

document
.getElementById("boton-benchmark")
.onclick=benchmark;

cargarHealth();

cargarComponentes();

setInterval(cargarHealth,5000);
