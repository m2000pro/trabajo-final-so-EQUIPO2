#!/bin/bash

echo "==================================================="
echo "       SCRIPT DE MONITOREO BÁSICO - ACTIVIDAD 10"
echo "==================================================="

echo -e "\n[1] Puertos abiertos y conexiones de red (ss -tulnp):"
# Requiere sudo para ver todos los procesos asociados a los puertos
sudo ss -tulnp

echo -e "\n[2] Estadísticas de Memoria Virtual (vmstat):"
# Toma 5 muestras con 1 segundo de intervalo
vmstat 1 5 

echo -e "\n[3] Rendimiento y Entrada/Salida de Discos (iostat):"
# Nota: Si falla, instala el paquete sysstat (sudo apt install sysstat)
iostat -x 1 5

echo -e "\n[4] Resumen de procesos (top):"
# Ejecuta top en modo batch (-b) para que imprima 1 sola iteración (-n 1) y no bloquee el script
top -b -n 1 | head -n 15

echo -e "\n==================================================="
echo "NOTA SOBRE HTOP:"
echo "El comando 'htop' es una interfaz completamente interactiva."
echo "Para observar los procesos en tiempo real con una interfaz gráfica en terminal,"
echo "por favor ejecuta 'htop' directamente en la línea de comandos."
echo "==================================================="
