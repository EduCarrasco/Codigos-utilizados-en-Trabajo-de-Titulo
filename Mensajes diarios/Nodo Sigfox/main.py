from network import Sigfox
import machine
import socket
import time
import uos

# Esta prueba simula un nodo Sigfox que envía un mensaje cada 6 horas para
# extrapolar el comportamiento de mensajes diarios.

sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# Generación de mensaje random de 10 bytes y espera de 10 segundos por generación
# de los sensores del mensaje
msg = uos.urandom(12)
time.sleep(15)

try:
    s.send(msg)
except OSError:
    pass
machine.deepsleep(21600000) #30 minutos
