import hashlib
import math
import time

from flask import Blueprint, jsonify, request
from sqlalchemy import text
from werkzeug.exceptions import BadRequest, NotFound

from .extensions import db
from .models import ComponentType, HardwareComponent, Specification


api_bp = Blueprint("api", __name__)


def obtener_json():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        raise BadRequest("Debes enviar datos válidos en formato JSON.")

    return datos


def validar_campos(datos, campos_obligatorios):
    faltantes = []

    for campo in campos_obligatorios:
        if campo not in datos or datos[campo] in (None, ""):
            faltantes.append(campo)

    if faltantes:
        raise BadRequest(
            "Faltan campos obligatorios: " + ", ".join(faltantes)
        )


@api_bp.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "servicio": "API de Inventario y Benchmarks de Hardware",
        "version": "1.0",
        "estado": "funcionando",
        "endpoints": {
            "salud": "/health",
            "tipos": "/api/component-types",
            "componentes": "/api/components",
            "benchmark_cpu": "/api/benchmarks/cpu?iterations=250000"
        }
    })


@api_bp.route("/health", methods=["GET"])
def health():
    try:
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "ok",
            "database": "connected"
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "status": "degraded",
            "database": "disconnected"
        }), 503


@api_bp.route("/api/component-types", methods=["GET"])
def obtener_tipos():
    tipos = ComponentType.query.order_by(ComponentType.id).all()

    return jsonify({
        "cantidad": len(tipos),
        "tipos": [tipo.to_dict() for tipo in tipos]
    })


@api_bp.route("/api/component-types", methods=["POST"])
def crear_tipo():
    datos = obtener_json()
    validar_campos(datos, ["name"])

    nuevo_tipo = ComponentType(
        name=str(datos["name"]).strip(),
        description=datos.get("description")
    )

    db.session.add(nuevo_tipo)
    db.session.commit()

    return jsonify({
        "mensaje": "Tipo de componente creado correctamente",
        "tipo": nuevo_tipo.to_dict()
    }), 201


@api_bp.route("/api/components", methods=["GET"])
def obtener_componentes():
    fabricante = request.args.get("manufacturer")
    tipo = request.args.get("type")

    consulta = HardwareComponent.query.join(ComponentType)

    if fabricante:
        consulta = consulta.filter(
            HardwareComponent.manufacturer.ilike(f"%{fabricante}%")
        )

    if tipo:
        consulta = consulta.filter(
            ComponentType.name.ilike(f"%{tipo}%")
        )

    componentes = consulta.order_by(HardwareComponent.id).all()

    return jsonify({
        "cantidad": len(componentes),
        "componentes": [
            componente.to_dict()
            for componente in componentes
        ]
    })


@api_bp.route("/api/components/<int:component_id>", methods=["GET"])
def obtener_componente(component_id):
    componente = db.session.get(
        HardwareComponent,
        component_id
    )

    if componente is None:
        raise NotFound("El componente solicitado no existe.")

    return jsonify(componente.to_dict())


@api_bp.route("/api/components", methods=["POST"])
def crear_componente():
    datos = obtener_json()

    validar_campos(
        datos,
        [
            "name",
            "manufacturer",
            "model",
            "component_type_id"
        ]
    )

    tipo = db.session.get(
        ComponentType,
        datos["component_type_id"]
    )

    if tipo is None:
        raise BadRequest("El tipo de componente no existe.")

    nuevo_componente = HardwareComponent(
        name=str(datos["name"]).strip(),
        manufacturer=str(datos["manufacturer"]).strip(),
        model=str(datos["model"]).strip(),
        power_consumption_w=datos.get("power_consumption_w"),
        release_year=datos.get("release_year"),
        component_type=tipo
    )

    especificaciones = datos.get("specifications", [])

    if not isinstance(especificaciones, list):
        raise BadRequest(
            "El campo specifications debe ser una lista."
        )

    for dato_especificacion in especificaciones:
        validar_campos(
            dato_especificacion,
            ["attribute_name", "attribute_value"]
        )

        nueva_especificacion = Specification(
            attribute_name=str(
                dato_especificacion["attribute_name"]
            ).strip(),
            attribute_value=str(
                dato_especificacion["attribute_value"]
            ).strip(),
            unit=dato_especificacion.get("unit")
        )

        nuevo_componente.specifications.append(
            nueva_especificacion
        )

    db.session.add(nuevo_componente)
    db.session.commit()

    return jsonify({
        "mensaje": "Componente creado correctamente",
        "componente": nuevo_componente.to_dict()
    }), 201


@api_bp.route(
    "/api/components/<int:component_id>",
    methods=["PUT"]
)
def actualizar_componente(component_id):
    componente = db.session.get(
        HardwareComponent,
        component_id
    )

    if componente is None:
        raise NotFound("El componente solicitado no existe.")

    datos = obtener_json()

    if "name" in datos:
        componente.name = str(datos["name"]).strip()

    if "manufacturer" in datos:
        componente.manufacturer = str(
            datos["manufacturer"]
        ).strip()

    if "model" in datos:
        componente.model = str(datos["model"]).strip()

    if "power_consumption_w" in datos:
        componente.power_consumption_w = datos[
            "power_consumption_w"
        ]

    if "release_year" in datos:
        componente.release_year = datos["release_year"]

    if "component_type_id" in datos:
        tipo = db.session.get(
            ComponentType,
            datos["component_type_id"]
        )

        if tipo is None:
            raise BadRequest(
                "El tipo de componente indicado no existe."
            )

        componente.component_type = tipo

    db.session.commit()

    return jsonify({
        "mensaje": "Componente actualizado correctamente",
        "componente": componente.to_dict()
    })


@api_bp.route(
    "/api/components/<int:component_id>",
    methods=["DELETE"]
)
def eliminar_componente(component_id):
    componente = db.session.get(
        HardwareComponent,
        component_id
    )

    if componente is None:
        raise NotFound("El componente solicitado no existe.")

    db.session.delete(componente)
    db.session.commit()

    return "", 204


@api_bp.route(
    "/api/components/<int:component_id>/specifications",
    methods=["POST"]
)
def agregar_especificacion(component_id):
    componente = db.session.get(
        HardwareComponent,
        component_id
    )

    if componente is None:
        raise NotFound("El componente solicitado no existe.")

    datos = obtener_json()

    validar_campos(
        datos,
        ["attribute_name", "attribute_value"]
    )

    especificacion = Specification(
        attribute_name=str(
            datos["attribute_name"]
        ).strip(),
        attribute_value=str(
            datos["attribute_value"]
        ).strip(),
        unit=datos.get("unit"),
        component=componente
    )

    db.session.add(especificacion)
    db.session.commit()

    return jsonify({
        "mensaje": "Especificación agregada correctamente",
        "especificacion": especificacion.to_dict()
    }), 201


@api_bp.route(
    "/api/components/<int:component_id>/specifications/"
    "<int:specification_id>",
    methods=["DELETE"]
)
def eliminar_especificacion(
    component_id,
    specification_id
):
    especificacion = Specification.query.filter_by(
        id=specification_id,
        component_id=component_id
    ).first()

    if especificacion is None:
        raise NotFound("La especificación no existe.")

    db.session.delete(especificacion)
    db.session.commit()

    return "", 204


@api_bp.route("/api/benchmarks/cpu", methods=["GET"])
def benchmark_cpu():
    iterations = request.args.get(
        "iterations",
        default=250000,
        type=int
    )

    if iterations < 1000 or iterations > 2000000:
        raise BadRequest(
            "iterations debe estar entre 1000 y 2000000."
        )

    inicio = time.perf_counter()
    checksum = 0

    for numero in range(1, iterations + 1):
        contenido = (
            f"{numero}-{math.sqrt(numero):.8f}"
        ).encode()

        resumen = hashlib.sha256(contenido).digest()

        checksum ^= int.from_bytes(
            resumen[:4],
            "big"
        )

    duracion_ms = round(
        (time.perf_counter() - inicio) * 1000,
        3
    )

    return jsonify({
        "iterations": iterations,
        "duration_ms": duracion_ms,
        "checksum": checksum
    })
