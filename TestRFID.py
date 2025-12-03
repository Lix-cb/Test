#!/usr/bin/env python3
"""
test_rfid_standalone.py
Script independiente para probar el lector RFID RC522 en Raspberry Pi

Uso:
    sudo python3 test_rfid_standalone.py

Presiona Ctrl+C para salir
"""

import sys
import time

print("="*60)
print("TEST RFID RC522 - Raspberry Pi")
print("="*60)

# Intentar importar la librería
try:
    from mfrc522 import SimpleMFRC522
    print("✓ Librería mfrc522 importada correctamente")
except ImportError as e:
    print("✗ ERROR: No se pudo importar mfrc522")
    print(f"  Detalle: {e}")
    print("\n📦 Instala la librería con:")
    print("  pip3 install mfrc522")
    sys.exit(1)

# Verificar que SPI esté habilitado
try:
    with open('/dev/spidev0.0', 'r'):
        print("✓ SPI está habilitado (/dev/spidev0. 0 existe)")
except FileNotFoundError:
    print("✗ ERROR: SPI no está habilitado")
    print("\n⚙️  Habilita SPI con:")
    print("  sudo raspi-config")
    print("  → Interface Options → SPI → Enable")
    print("  sudo reboot")
    sys.exit(1)
except PermissionError:
    print("⚠ WARNING: Sin permisos para acceder a SPI")
    print("  Ejecuta este script con sudo:")
    print("  sudo python3 test_rfid_standalone. py")
    sys.exit(1)

# Inicializar lector
try:
    reader = SimpleMFRC522()
    print("✓ Lector RFID inicializado correctamente")
except Exception as e:
    print(f"✗ ERROR inicializando el lector: {e}")
    sys.exit(1)

print("="*60)
print("🔍 ESPERANDO TARJETAS RFID...")
print("="*60)
print("Acerca una tarjeta al lector RC522")
print("Presiona Ctrl+C para salir\n")

# Contador de lecturas
contador = 0

try:
    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Esperando tarjeta.. .", end='\r')
            
            # Leer tarjeta (bloqueante - espera hasta que detecte una)
            id, text = reader.read()
            
            contador += 1
            
            # Limpiar línea y mostrar resultado
            print(" " * 80, end='\r')  # Limpiar línea
            print("\n" + "─"*60)
            print(f"✅ TARJETA DETECTADA #{contador}")
            print("─"*60)
            print(f"📇 ID (numérico): {id}")
            print(f"📇 ID (string):   {str(id)}")
            print(f"📝 Texto en tarjeta: '{text. strip() if text else '(vacío)'}'")
            print("─"*60)
            print("Esperando siguiente tarjeta.. .\n")
            
            # Pequeña pausa para evitar lecturas duplicadas
            time.sleep(1)
            
        except KeyboardInterrupt:
            raise  # Propagar para salir limpiamente
        except Exception as e:
            print(f"\n⚠ Error en lectura: {e}")
            print("Reintentando en 2 segundos...")
            time. sleep(2)

except KeyboardInterrupt:
    print("\n\n" + "="*60)
    print(f"✓ Test finalizado - Total de lecturas: {contador}")
    print("="*60)
    sys.exit(0)
