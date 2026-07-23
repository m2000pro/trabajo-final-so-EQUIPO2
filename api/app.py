from flask import Flask, jsonify, request

app = Flask(__name__)

# Nuestro "pequeño catálogo" en memoria (Cumple con manejo de datos)
inventario_procesadores = [
    {"id": 1, "modelo": "AMD Ryzen 5 8600G", "nucleos": 6, "tdp_w": 65, "graficos_integrados": "Radeon 760M"}
]

inventario_graficas = []

# Endpoint GET: Consultar detalles de un procesador (Cumple con Read)
@app.route('/api/hardware/procesadores', methods=['GET'])
def get_procesadores():
    return jsonify({"procesadores_registrados": inventario_procesadores})

# Endpoint POST: Registrar una nueva tarjeta gráfica (Cumple con Create / POST)
@app.route('/api/hardware/graficas', methods=['POST'])
def add_grafica():
    nuevo_dato = request.get_json()
    
    # Validación básica
    if not nuevo_dato:
        return jsonify({"error": "Faltan datos en formato JSON"}), 400
    
    # Simulamos la creación de un ID en la base de datos
    nuevo_id = len(inventario_graficas) + 1
    nuevo_dato['id'] = nuevo_id
    
    # Agregamos el dato al catálogo
    inventario_graficas.append(nuevo_dato)
    
    return jsonify({
        "mensaje": "Gráfica registrada exitosamente", 
        "datos_guardados": nuevo_dato
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)