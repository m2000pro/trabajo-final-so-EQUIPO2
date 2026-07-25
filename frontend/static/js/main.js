// Configuración de la API (Apunta a tu Máquina Virtual)
const API_BASE = "http://192.168.18.88:8080";

const consoleOut = document.getElementById('console-output');
const statusBadge = document.getElementById('status-badge');

// Utilidad para mostrar datos
function log(data) {
    consoleOut.textContent = JSON.stringify(data, null, 2);
}

// GET / y GET /health
async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();
        log(data);
        statusBadge.textContent = data.status === "ok" ? "API Conectada" : "Error de BD";
        statusBadge.style.background = data.status === "ok" ? "#2ecc71" : "#e74c3c";
    } catch (e) {
        statusBadge.textContent = "API Desconectada";
        statusBadge.style.background = "#e74c3c";
    }
}

// GET /api/benchmarks/cpu
async function runBenchmark() {
    log("Iniciando prueba de estrés... Observa el docker stats en Ubuntu.");
    const res = await fetch(`${API_BASE}/api/benchmarks/cpu?iterations=500000`);
    const data = await res.json();
    log(data);
}

// GET /api/component-types
async function loadTypes() {
    const res = await fetch(`${API_BASE}/api/component-types`);
    const data = await res.json();
    const list = document.getElementById('list-tipos');
    list.innerHTML = data.tipos.map(t => `<li>[ID: ${t.id}] ${t.name}</li>`).join('');
    log(data);
}

// GET /api/components
async function loadComponents() {
    const res = await fetch(`${API_BASE}/api/components`);
    const data = await res.json();
    const list = document.getElementById('list-componentes');
    list.innerHTML = data.componentes.map(c => `<li>[ID: ${c.id}] ${c.name} - ${c.model}</li>`).join('');
    log(data);
}

// POST /api/component-types (Usando FormData gracias al tag <form>)
document.getElementById('form-tipo').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData.entries());
    
    const res = await fetch(`${API_BASE}/api/component-types`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    log(await res.json());
    loadTypes();
});

// POST /api/components
document.getElementById('form-componente').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData.entries());
    payload.component_type_id = parseInt(payload.component_type_id);
    
    const res = await fetch(`${API_BASE}/api/components`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    log(await res.json());
    loadComponents();
});

// POST /api/components/<id>/specifications
document.getElementById('form-especificacion').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const id = formData.get('component_id');
    const payload = {
        attribute_name: formData.get('attribute_name'),
        attribute_value: formData.get('attribute_value')
    };
    
    const res = await fetch(`${API_BASE}/api/components/${id}/specifications`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    log(await res.json());
});

// DELETE /api/components/<id>
document.getElementById('form-delete').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const id = formData.get('delete_id');
    
    const res = await fetch(`${API_BASE}/api/components/${id}`, { method: 'DELETE' });
    if(res.ok) log({ mensaje: `Componente ${id} eliminado.` });
    loadComponents();
});

// Chequeo inicial
checkHealth();