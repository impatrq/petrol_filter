import RPi.GPIO as GPIO
import time
import os


distancia = 0.0

PUMPDELAY = 26
VALVEDELAY = 10

# Gpios del ultrasonico
TRIG = 23
ECHO = 24

# Gpios de los transistores
PETROLVALVE = 12  # pin 32
WATERVALVE = 26  # pin 37
WATERPUMP = 13  # pin 33
BOOLSENSOR = 18  # pin 12

GPIO.setmode(GPIO.BCM)

# salida y entrada del ultrasonico

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# entrada del sensor logico

GPIO.setup(BOOLSENSOR, GPIO.IN)

# salida del transistor bomba de agua

GPIO.setup(WATERPUMP, GPIO.OUT)
GPIO.output(WATERPUMP, True)

# salida del transistor de la electrovalvula de escape

GPIO.setup(WATERVALVE, GPIO.OUT)
GPIO.output(WATERVALVE, True)

# salida del transistor de la electrovalvula de reserva

GPIO.setup(PETROLVALVE, GPIO.OUT)
GPIO.output(PETROLVALVE, True)


for x in range(5):
    print("Medicion de distancias en progreso")

    GPIO.setup(TRIG, GPIO.OUT)  # Set pin as GPIO out
    GPIO.setup(ECHO, GPIO.IN)  # Set pin as GPIO in

    while True:

        GPIO.output(TRIG, False)  # Set TRIG as LOW
        print("esperando a que el sensor se adapte")
        valor_anterior = distancia + 0.0

        time.sleep(2)  # Delay of 2 seconds

        GPIO.output(TRIG, True)  # Set TRIG as HIGH
        time.sleep(0.00001)  # Delay of 0.00001 seconds
        GPIO.output(TRIG, False)  # Set TRIG as LOW

        while GPIO.input(ECHO) == 0:  # Check if Echo is LOW
            pulse_start = time.time()  # Time of the last  LOW pulse

        while GPIO.input(ECHO) == 1:  # Check whether Echo is HIGH
            pulse_end = time.time()  # Time of the last HIGH pulse

        pulse_duration = pulse_end - pulse_start  # pulse duration to a variable

        distancia = (34300 * pulse_duration) / 2
        print("Distancia: %.2f cm" % distancia)
        time.sleep(2)

        if distancia == 45:
            GPIO.output(WATERPUMP, False)  # se activa la bomba
            time.sleep(PUMPDELAY)
        elif distancia == 15:
            GPIO.output(WATERPUMP, True)  # se apaga la bomba
            time.sleep(PUMPDELAY)

        if GPIO.input(18):  # al detectar el voltaje en alto:

            print("voltaje alto")
            # se abre la electrovalvula de vaciado
            GPIO.output(WATERVALVE, False)
            time.sleep(VALVEDELAY)  # tiempo de decantacion
            # se cierra la elcrtovalvula de reserva
            GPIO.output(PETROLVALVE, True)

        else:  # al detectar el votaje en bajo:

            print("voltaje bajo")
            # se cierra la electrovalvula de vaciado
            GPIO.output(WATERVALVE, True)
            if valor_anterior != 0:
                rest = (distancia - valor_anterior)
            else:
                rest = 0
            time.sleep(3)
            print("el petroleo esta en un ", valor_anterior, "%")
            time.sleep(1)
            # se abre la electrovalvula de reserva
            GPIO.output(PETROLVALVE, False)
            if rest == 50:
                GPIO.output(PETROLVALVE, True)
                #print("procesos finalizado!")
