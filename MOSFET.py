import RPi.GPIO as GPIO
import time

#Gpios de los transistores
PETROLVALVE = 12
WATERVALVE = 26
WATERPUMP = 13
BOOLSENSOR = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(BOOLSENSOR, GPIO.IN)

GPIO.setup(WATERPUMP, GPIO.OUT)
GPIO.output(WATERPUMP, True)

GPIO.setup(WATERVALVE, GPIO.OUT)
GPIO.output(WATERVALVE, True)

GPIO.setup(PETROLVALVE, GPIO.OUT)
GPIO.output(PETROLVALVE, True)


for x in range (1):

        GPIO.output(WATERPUMP, False) #se activa la bomba
        print("Waterpump prendida")
	time.sleep(5)
        GPIO.output(WATERPUMP, True) #se apaga la bomba
	print("Waterpump apagada")  


while True:

        if GPIO.input(18): #al detectar el voltaje en alto
		print("Voltaje alto")
              	GPIO.output(WATERVALVE, False) #se abre la electrovalvula de vaciado
            	
        else: 	
		print("Voltaje bajo")
		GPIO.output(WATERVALVE, True) #se cierra la electrovalvula de vaciado
	        GPIO.output(PETROLVALVE, False)#se abre la electrovalvula de reserva
		time.sleep(5)
            	GPIO.output(PETROLVALVE, True)
