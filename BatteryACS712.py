from scipy.signal import lfilter
import matplotlib.pyplot as plt
import numpy as np
import serial
import time

# Toma de N datos de calibración y obtención de una recta en base a ella.
arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1.0)

N = 200
x = 0

print('Toma de %i datos para calibracion' %N)
with arduino:
    i = 0
    while i < N:
        try:
            line = arduino.readline()
            if not line:
                continue
            p = np.fromstring(line.decode('ascii', errors='replace'), sep=' ')
            try:
                x += float(p)
                i += 1
            except TypeError:
                print('Reintento con lectura %i' %i)
        except KeyboardInterrupt:
            print('Calibracion Interrumpida. Reintente...')
            break

a = float(x/N)
m = (1023-a)/13.5
n = -m*a

print('Calibracion lista con a = %f' %a)
print('m: ', m)
print('n: ', n)
input('ENTER para iniciar medicion')

# Cada dato es guardado en un archivo hasta que se indique su interrupción
f = open('Data', 'a')
with arduino:
    while True:
        try:
            line = arduino.readline()
            if not line:
                continue
            p = np.fromstring(line.decode('ascii', errors='replace'), sep=' ')
            try:
                f.write('\n'+str(p)+',')
            except TypeError:
                print("Reintento")
        except KeyboardInterrupt:
            break

f.close()
print('Realizado')
