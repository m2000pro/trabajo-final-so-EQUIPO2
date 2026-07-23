# 1. Usar una imagen base de Python ligera (ideal para ahorrar recursos)
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de dependencias al contenedor
COPY requirements.txt .

# 4. Instalar Flask sin guardar archivos temporales (mantiene la imagen pequeña)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar tu código fuente (app.py) dentro del contenedor
COPY app.py .

# 6. Exponer el puerto 8080, tal como lo pide la guía del trabajo
EXPOSE 8080

# 7. El comando que se ejecutará al encender el contenedor
CMD ["python", "app.py"]