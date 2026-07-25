# Diseño, implementación y diagnóstico de una plataforma Linux segura, observable y contenerizada para servicios modernos

Este repositorio contiene la documentación, configuración y código fuente del proyecto final para el curso de Sistemas Operativos Modernos. El objetivo principal es demostrar la administración de recursos, aislamiento de procesos, observabilidad y *hardening* en un entorno Linux.

# Integrantes:
-Pastor Benites Marcelo Andre
<br>
-Porras Anticona Axel Edinson
<br>
-Quiroz Utani Joaquin Enmanuel
<br>
-Selva Sánchez Miguel de Jesús
<br>
-Silva Valera Carlos Roque

---

## 1. Infraestructura y Sistema Operativo Base

El proyecto se despliega bajo una arquitectura híbrida, utilizando virtualización local para aislar los servicios del sistema anfitrión.

*   **Host Físico (Anfitrión):** Equipo con Windows, procesador AMD Ryzen 7 8700G y 15 GB de RAM utilizables.
*   **Máquina Virtual (Servidor):** Ubuntu Server 24.04 LTS (Instalación por defecto, sin proxy).
*   **Red:** Adaptador configurado en modo NAT/Puente, accesible mediante la IP local `192.168.18.88`.
*   **Almacenamiento:** 
    *   Volumen lógico (LVM) principal de 40 GB para el sistema operativo raíz (`/`).
    *   Disco virtual secundario de 5 GB montado específicamente en `/laboratorio` para el aislamiento de datos y cargas de trabajo.

---

## 2. Configuraciones de Seguridad (Hardening)

Se aplicaron principios de menor privilegio y reducción de la superficie de ataque en el servidor Ubuntu.

*   **Gestión de Usuarios y Elevación:** Se crearon los usuarios `operador` y `adminlinux`, evitando el uso directo de la cuenta `root`. La administración se delega a través del grupo `sudo`.
*   **Permisos Estructurales (Bit SGID):** Los usuarios fueron añadidos al grupo unificado `equipo_proyecto`. Se aplicó el permiso `2775` (Bit SGID) y un `chown` al directorio `/laboratorio`, forzando a que cualquier archivo creado herede automáticamente el grupo colaborativo sin necesidad de usar privilegios de superusuario.
*   **Control de Tráfico (UFW):** El Uncomplicated Firewall se encuentra activo con una política de denegación por defecto. Solo se permite el tráfico entrante a través de los puertos:
    *   `22/TCP` (SSH para administración remota).
    *   `80` / `8080` (API Contenerizada).
*   **Optimización de Servicios (systemd):** Se deshabilitaron servicios innecesarios para el entorno de laboratorio (como `ModemManager`, `multipathd`, `open-iscsi` y `lxd-installer`) reduciendo el consumo de memoria y vectores de vulnerabilidad.

---

## 3. Arquitectura del Backend y Contenedores

La plataforma utiliza Docker Compose v2 para orquestar una API RESTful que interactúa con una base de datos relacional, implementando aislamiento de recursos a nivel de kernel mediante `cgroups`.

### Servicio de Base de Datos (`db`)
*   **Motor:** PostgreSQL 16.
*   **Persistencia:** Utiliza un volumen de Docker (`postgres_data`) para garantizar la integridad de los datos.
*   **Límites de Recursos:** Restringido estricta y explícitamente a **512 MB de RAM** y **0.75 de CPU**.
*   **Disponibilidad:** Cuenta con un *healthcheck* para asegurar que el motor relacional esté operativo antes de desplegar la API.

### Servicio de API (`api`)
*   **Stack:** Python Flask servido a través de Gunicorn.
*   **Seguridad y Configuración:** Credenciales inyectadas mediante un archivo `.env` (ignorado en el control de versiones). Integración de `Flask-CORS` para el consumo desde clientes externos.
*   **Límites de Recursos:** Restringido a **256 MB de RAM**, **0.50 de CPU** y un límite de seguridad de máximo **100 PIDs** para prevenir ataques de denegación de servicio (fork bombs).
*   **Pruebas de Estrés:** Incluye un endpoint de benchmarking (`/api/benchmarks/cpu`) diseñado para saturar el procesamiento lógico y demostrar la efectividad de las restricciones de `cgroups`.

---

## 4. Cliente Visual (Frontend Local)

Para interactuar con la infraestructura, se desarrolló una aplicación secundaria que opera fuera del entorno virtualizado:

*   **Ejecución:** Corre localmente en el host físico de Windows (`127.0.0.1:5000`).
*   **Integración:** Proporciona un panel de control asíncrono (HTML/JS/CSS) que consume los 12 endpoints de la API expuesta en el servidor Ubuntu (`192.168.18.88`).
*   **Funciones:** Permite probar conectividad, registrar componentes relacionales y gatillar las pruebas de carga para visualizar el impacto en las métricas de observabilidad en tiempo real.

---

## 5. Estructura del Repositorio

El proyecto se organiza siguiendo una estructura modular para facilitar la auditoría y revisión de los entregables:

| Directorio / Archivo | Descripción |
| :--- | :--- |
| `api/` | Código fuente del backend (`app/`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`). |
| `frontend/` | Código del cliente web visual desplegado en el host anfitrión. |
| `configuracion/` | Scripts de texto que documentan las políticas exactas de firewall, permisos aplicados y servicios del sistema deshabilitados. |
| `evidencias/` | Capturas de pantalla que validan el uso de herramientas de observabilidad (`htop`, `docker stats`, consumo de memoria, logs). |
| `scripts/` | Archivos (`.py` / `.sh`) utilizados para ejecutar pruebas de carga controlada (CPU/RAM) y automatización de monitoreo. |
| `informe/` | Documento técnico final en formato PDF con el análisis de los resultados y conclusiones. |
| `README.md` | Presentación general de la arquitectura y la plataforma (este documento). |

---
*Desarrollado para la evaluación final del curso de Sistemas Operativos.*
