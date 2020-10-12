from network import LoRa
import machine
import socket
import binascii
import struct
import config
import time
import uos

# Esta prueba simula un nodo LoRaWAN que envía un mensaje cada 6 horas para
# extrapolar la información que envía un nodo diariamente.

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915, adr=False)
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
    for channel in range(0, 3):
        lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# Configuracion del socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)
s.setblocking(True)

# Generación de mensaje random de 10 bytes y espera de 10 segundos por generación
# de los sensores del mensaje
msg = uos.urandom(12)
time.sleep(30)

try:
    s.send(msg)
    lora.nvram_save()
except OSError:
    pass
machine.deepsleep(21570000) # 6 horas
