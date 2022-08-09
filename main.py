#programa central main.py
import sys
import traceback
import threading
from time import sleep, time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importar RPi.GPIO! Usando el comando 'sudo' para correr el script")
import cloud4rpi
from config import C4R_TOKEN, C4R_HOST
from config import GPIO_PUMP
from config import MIN_DISTANCE, MAX_DISTANCE, STOP_PUMP_DISTANCE, DISTANCE_DELTA
from config import SENSOR_ERROR, NO_WATER_ERROR
import rpi
from messages import calc_status, calc_alert
from logger import log_debug, log_error, log_info, log_error1
from notifications import notify_in_background, log_debug, log_error, log_info, log_error1, log_error2

# tiempo en intervalos

DIAG_SENDING_INTERVAL = 60  # segundos
DATA_SENDING_INTERVAL = 300 # segundos
DEBUG_LOG_INTERVAL = 10     # segundos

MIN_SEND_INTERVAL = 0.5  # segundos
POLL_INTERVAL = 0.1  # milisegundos

# control del relé para la bomba de agua

START_PUMP = 1
STOP_PUMP = 0
PUMP_BOUNCE_TIME = 50   # milisegundos
PUMP_STOP_TIMEOUT = 5   # segundos

prev_distance = -9999
last_sending_time = -1
emergency_stop_time = None
pump_on = False
pump_disabled = False
disable_alerts = False

#funcion que avisa si hubo alguna varicion en el nivel del agua

def water_level_changed(prev, current):
    return abs(prev - current) > DISTANCE_DELTA


def update_distance(distance):
    global prev_distance
    prev_distance = distance

#calculo del porcentaje de agua 

def calc_water_level_percent(distance):
    d = distance if distance else 0
    value = (MAX_DISTANCE - d) / (MAX_DISTANCE - MIN_DISTANCE) * 100
    return max(0, round(value))

#funcion de encendido y apagado de la bomba de agua
def is_pump_on():
    global pump_on
    return pump_on


def is_pump_enabled(): 
    return not pump_disabled


def pump_relay_handle(pin):
    global pump_on
    pump_on = GPIO.input(GPIO_PUMP)
    log_debug("El relé de la bomba acambiado a: %d" % pump_on)

#funcion apara el control de la bomba de agua
def toggle_pump(value):
    if pump_disabled:
        return        
    if is_pump_on() != value:
        log_debug("[x] %s" % ('INICIO' if value else 'PARADA'))
    GPIO.setup(GPIO_PUMP, GPIO.OUT)
    GPIO.output(GPIO_PUMP, value)  # Start/Stop pouring 


def set_emergency_stop_time(now, is_pouring):
    global emergency_stop_time
    emergency_stop_time = now + PUMP_STOP_TIMEOUT if is_pouring else None


def check_water_source_empty(now):
    return emergency_stop_time and now > emergency_stop_time

#se depositan los datos que se van a enviar a la nube

def send(cloud, variables, dist, error_code=0, force=False):
    pump_on = is_pump_on()
    percent = calc_water_level_percent(dist)
    variables['Distancia']['value'] = dist
    variables['Nivel de agua']['value'] = percent
    variables['Relé de bomba']['value'] = pump_on
    variables['Statatus']['value'] = calc_status(error_code, percent, pump_on)

    current = time()
    global last_sending_time
    if force or current - last_sending_time > MIN_SEND_INTERVAL:
        readings = cloud.read_data()
        cloud.publish_data(readings)
        last_sending_time = current

def main():
    variables = {
        'Distancia': {
            'type': 'numeric',
        },
        'Status': {
            'type': 'string',
        },
        'Relé de bomba': {
            'type': 'bool',
            'value': False
        },
        'Nivel de agua': {
            'type': 'numeric',
        }
    }

    diagnostics = {
        'Bomba_conectada': is_pump_enabled,
        'IP_Address': rpi.ip_address,
        'Host': rpi.host_name,
        'CPU_Temp': rpi.cpu_temp,
        'OS': rpi.os_name,
        'Uptime': rpi.uptime_human
    }

    cloud = cloud4rpi.connect(C4R_TOKEN, C4R_HOST)
    cloud.declare(variables)
    cloud.declare_diag(diagnostics)
    cloud.publish_config()

    data_timer = 0
    diag_timer = 0
    log_timer = 0

    log_info("Setup GPIO...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PUMP, GPIO.IN)
    GPIO.add_event_detect(GPIO_PUMP, GPIO.BOTH, callback=pump_relay_handle, bouncetime=PUMP_BOUNCE_TIME) 
    toggle_pump(STOP_PUMP)

    try:
        log_debug('Iniciar...')
        while True:
            global disable_alerts

            distance = () # lee la distacia a la que esta el agua

            if distance is None:
                if not disable_alerts:
                    log_error(SENSOR_ERROR)
                #Al llamar a la funcion del script notifications la ejecuta si detecta 
                send(cloud, variables, distance, error_code=SENSOR_ERROR, force=True)
                disable_alerts = True

                if is_pump_on() and prev_distance < STOP_PUMP_DISTANCE + DISTANCE_DELTA:
                    log_error('[!] Emergencia se ha detenido la bomba. No hay señal desde el sensor de distancia')
                    toggle_pump(STOP_PUMP)

                continue

            now = time()
            should_log = now - log_timer > DEBUG_LOG_INTERVAL
            if should_log:
                #log_debug("Distancia = %.2f (cm)" % (distance))
                log_timer = now

            if distance <= STOP_PUMP_DISTANCE:  #la bomba deja de verter agua 
                toggle_pump(STOP_PUMP)
           
            if GPIO.event_detected(GPIO_PUMP):                
                is_pouring = is_pump_on()
                set_emergency_stop_time(now, is_pouring)
                log_debug('[!] Acción de la bomba detectada:  %s' % ('On' if is_pouring else 'Off'))
                send(cloud, variables, distance, force=True)

            global pump_disabled
            if check_water_source_empty(now):
                log_error1('[!] la bomba se encuentra obstruida') #este mensaje sale si alguna cosa se traba en el filtro de la bomba                 
                toggle_pump(STOP_PUMP)
                pump_disabled = True
                
                notify_in_background(calc_alert(NO_WATER_ERROR))
                send(cloud, variables, distance, error_code = NO_WATER_ERROR, force=True)

            if distance > MAX_DISTANCE * 2:  #esto indica que la distancia esta fuera del rango por lo que la bomba no debe empezar a verter es decir que esta muy por arriba el nivel del tanque
                log_error2('Distancia fuera de rango:  %.2f' % distance)
                continue

            if distance > MAX_DISTANCE: #empieza a funcionar la bomba porque se redujo el nivel 
                toggle_pump(START_PUMP)
            
            if water_level_changed(prev_distance, distance):
                log_debug("La distancia ha cambiado a: %.2f (cm)" % (distance))
                send(cloud, variables, distance)
                
                update_distance(distance)
                set_emergency_stop_time(now, is_pump_on())
                
                pump_disabled = False # para que se pueda volver a activar la bomba mas tarde

            if now - data_timer > DATA_SENDING_INTERVAL:
                send(cloud, variables, distance)
                data_timer = now

            if now - diag_timer > DIAG_SENDING_INTERVAL:
                cloud.publish_diag()
                diag_timer = now
            
            disable_alerts = False
            
            sleep(POLL_INTERVAL)

    except Exception as e:
        log_error('ERROR: %s' % e)
        traceback.print_exc()

    finally:
        log_debug('Apagando!')
        GPIO.remove_event_detect(GPIO_PUMP)
        GPIO.cleanup()
        sys.exit(0)


if __name__ == '__main__':
    main()
