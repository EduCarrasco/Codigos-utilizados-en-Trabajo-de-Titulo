from network import Sigfox
import socket
import struct
import machine
import uos

# Esta prueba simula un nodo Sigfox que envía un mensaje de presencia o no de un
# vehículo cada minuto. Para esto último genera una opción random 1 y 0 enviando
# un mensaje de un byte: 00 o 01

sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# Generación de mensaje 0 o 1 random
place = uos.urandom(1)
if place <= struct.pack("B", 128):
    msg = bytes([0])
else:
    msg = bytes([1])

try:
    s.send(msg)
except OSError:
    pass
machine.deepsleep(60000)
