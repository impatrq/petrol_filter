import RPi.GPIO as GPIO
import time
from telegram import 



SOLENOIDVALVES = [33,37,29]

PUMPDELAY = 26     
VALVEDELAY = 10

#Gpios del ultrasonico

TRIG = 23
ECHO = 24

#Gpios de los transistores

PETROLVALVE = 12 # pin 32 
WATERVALVE = 26 # pin 37
WATERPUMP = 13 # pin 33
BOOLSENSOR = 18 # pin 12

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



try:
    
        def distance_sensor():

            print ("Medición de distancia en progreso")

            while True:
                GPIO.output(TRIG, GPIO.LOW)
                print ("Esperando a que el sensor se estabilice")
                time.sleep(2)
                GPIO.output(TRIG, GPIO.HIGH)
                time.sleep(0.000001)
                GPIO.output(TRIG, GPIO.LOW)

                print ("Iniciando eco")
                while True:
                    pulso_inicio = time.time()
                    if GPIO.input(ECHO) == GPIO.HIGH:
                        break

                while True:
                    pulso_fin = time.time()
                    if GPIO.input(ECHO) == GPIO.LOW:
                        break
                duracion = pulso_fin - pulso_inicio
                distancia = (34300 * duracion) / 2
                print ("Distancia: %.2f cm") % distancia
            
                quotient = distancia / 45 #la distancia actual dividida por los cm que equivalen al 100% del bidón aunque sea de 50cm se dejan unos 15cm libres como margen de error y teniendo en cuenta el movimiento de la boya en el agua
                percent = quotient * 100
                print("el contenedor se encuentra en un", percent,"%", "de carga")  

    
                if distancia == 45:             
                        GPIO.output(WATERPUMP, False) #se activa la bomba
                        time.sleep(PUMPDELAY)
                elif distancia == 15:
                        GPIO.output(WATERPUMP, True) #se apaga la bomba
                        time.sleep(PUMPDELAY)
                
                if GPIO.input(18): #al detectar el voltaje en alto:
                        
                        GPIO.output(WATERVALVE, False) #se abre la electrovalvula de vaciado
                        time.sleep(VALVEDELAY) #tiempo de decantacion
                        GPIO.output(PETROLVALVE, True) #se cierra la elcrtovalvula de reserva
                
                else:  #al detectar el votaje en bajo:
                        
                        GPIO.output(WATERVALVE, True) #se cierra la electrovalvula de vaciado
                        GPIO.output(PETROLVALVE, False) #se abre la electrovalvula de reserva
                        time.sleep(VALVEDELAY) 
                        

finally:
    GPIO.cleanup()
