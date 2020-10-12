from network import Sigfox
import machine
import socket
import time
import uos

# Esta prueba simula un nodo Sigfox que envía un mensaje cada 30 minutos de 10
# bytes aleatorio simulando la información de una serie de sensores

sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# Generación de mensaje random de 10 bytes y espera de 10 segundos por generación
# de los sensores del mensaje
msg = uos.urandom(10)
time.sleep(10)

try:
    s.send(msg)
except OSError:
    pass
machine.deepsleep(1790000) #30 minutos
