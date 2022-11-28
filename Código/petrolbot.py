import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime     # Paquete instalado de fabrica

name = 'petrol'

# Voz del asistente
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)


# Contestaciones del asistente
def talk(text):
    engine.say(text)
    engine.runAndWait()


# Reconocimiento de voz
listener = sr.Recognizer()

def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)  # Escucha al microfono
            rec = listener.recognize_google(voice)
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')     # Elimina el nombre del comando dicho, para que no moleste a la hora de ejecutar acciones
            print(rec)
    except:
        talk("No te escucho")
    return rec

# Acciones del asistente
def run():
    rec = listen()
    if 'mail' in rec:
        talk("en la consola se encuentra el correo")
        print("petrolfilter2022@gmail.com")
    elif 'hour' in rec:
        hora = datetime.datetime.now().strftime('%H:%M')
        talk("Son las " + hora)
    if 'help' in rec:
        talk("en la consola se encuentran todos los comandos")
        print('Comandos: \n /guide: Guía de usuario del dispositivo \n /parts: Componentes utilizados en el proyecto \n /contact: Contacto al equipo de petrol filter \n /github Link al repositorio en la plataforma GitHub')
    if 'github' in rec:
        talk("en la consola se encuentra nuestro github")
        print("https://github.com/impatrq/petrol_filter")
    if 'parts' in rec:
        talk("Petrol Filter utiliza un sensor ultrasonico, una electrovalvula, una raspberry pi zero, una bomba de gasoil, una bateria, y estructurales, caños de termofusion, un bidon y un salvavidas")
        print('Componenetes:'    '\n [Electrónicos]: \n'
                                                  ' ❖ Sensor ultrasonico jsn-sr04t \n'
                                                  ' ❖ Electroválvula 12V \n'
                                                  ' ❖ Raspberry pi zero W 1.1v \n'
                                                  ' ❖ Bomba de gasoil 12V \n'
                                                  ' ❖ Batería tipo alarma 12V \n'
                                                      '\n [Estructurales]: \n'
                                                  ' ❖ Caños de termofusión \n'
                                                  ' ❖ Bidón de dispenser de 20L \n'
                                                  ' ❖ Salvavidas circular \n')
    if 'for us' in rec:
        talk("fede cornudo")
    else:
        talk("Vuelve a intentarlo")     # Si el comando dicho no aparece en "def run()" te dira "Vuelve a intentarlo"

while True:
    run()
