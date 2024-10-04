import pyautogui
import time

# Espera unos segundos antes de capturar la posición del mouse
print("Mueve el mouse al punto deseado en los próximos 5 segundos...")
time.sleep(5)  # Tiempo para que muevas el mouse al lugar adecuado

# Captura y muestra la posición actual del mouse
x, y = pyautogui.position()
print(f"Las coordenadas actuales del mouse son: X={x}, Y={y}")
