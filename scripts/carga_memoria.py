import time
import sys

print ("Iniciando prueba de estres de MEMORIA.... " )
print ("!ADVERTENCIA: No ejecutar en la PC fisica (Windows) " )
arreglo_memoria =   [ ]
try:
	while True:
		arreglo_memoria.append(' ' * 10**7 )
		time.sleep(0.1 )
except KeyboardInterrupt:
	print("\n Prueba de memoria detenida por el usuario. " )
	arreglo_memoria.clear()
	sys.exit(0)
except MemoryError:
	print("\n !Limite de memoria alcanzado¡ El sistema matara el proceso pronto " )

