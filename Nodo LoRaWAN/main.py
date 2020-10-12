from network import LoRa
import machine
import socket
import binascii
import struct
import config
import uos

# Esta prueba simula un nodo LoRaWAN que envía un mensaje de presencia o no de un
# vehículo cada minuto. Para esto último genera una opción random 1 y 0 enviando
# un mensaje de un byte: 00 o 01
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915)
lora.nvram_restore()

if not lora.has_joined():
    # Autenticación por ABP
    dev_addr = struct.unpack(">l", binascii.unhexlify('26011F2B'))[0]
    nwk_swkey = binascii.unhexlify('DDA72EF15716F45F9F83DA52D9379EAA')
    app_swkey = binascii.unhexlify('D76BE692998F3AFFB45C82C19289F42F')

    # Se eliminan todos los canales
    for channel in range(0, 72):
        lora.remove_channel(channel)

    # Se agregan los primeros 3 canales
    for channel in range(0, 8):
        lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# Configuracion del socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)
s.setblocking(True)

# Generación de mensaje 0 o 1 random
place = uos.urandom(1)
if place <= struct.pack("B", 128):
    msg = bytes([0])
else:
    msg = bytes([1])
try:
    s.send(msg)
    lora.nvram_save()
except OSError:
    pass
machine.deepsleep(60000)
