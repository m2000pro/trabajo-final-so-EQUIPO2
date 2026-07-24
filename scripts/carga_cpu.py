#!/usr/bin/env python3
import multiprocessing
import time
import sys

def estresar_nucleo():
    """Bucle infinito matemático para saturar el núcleo"""
    while True:
        _ = 9999 * 9999

if __name__ == '__main__':
    print("Iniciando prueba de estrés de CPU...")
    print("¡ADVERTENCIA: No ejecutar en la PC física (Windows)! Presiona Ctrl+C para detener.")
    
    # Detecta el número de núcleos asignados a la máquina (deberían ser 2 según tu configuración)
    nucleos = multiprocessing.cpu_count()
    procesos = []
    
    try:
        # Crea un proceso por cada núcleo disponible
        for i in range(nucleos):
            p = multiprocessing.Process(target=estresar_nucleo)
            procesos.append(p)
            p.start()
        
        # Mantiene el hilo principal vivo mientras los demás procesos trabajan
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nDeteniendo prueba de CPU...")
        for p in procesos:
            p.terminate()
            p.join()
        print("Prueba de CPU finalizada.")
        sys.exit(0)
