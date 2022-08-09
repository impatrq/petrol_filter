from logger import log_debug, log_error, log_info, log_error1, log_error2, notify_in_background

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

#Mensajes del bot

async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola {update.effective_user.first_name} si deseas visitar a nuestro equipo en instagram: https://instagram.com/petrol_filter2022?igshid=YmMyMTA2M2Y= ')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Bienvenido/a al bot de servicio técnico Petrol Filter en que puedo ayudarle? pulse /help para más info')
async def guide (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('• El primer paso a seguir es la conexión al microcomputador mediante ssh por medio de una aplicación como Putty o similar, asegúrese de introducir las credenciales otorgadas por el equipo, (vease /contact) si el microcomputador se encuentra conectado a la misma red que el dispositivo externo desde el cual intenta conectarse no debería presentar falla alguna. \n'
                                    '• Segundo paso: una vez hecho el ingreso correctamente al micro debe entrar a la ruta del archivo en la particion de arranque /home/pi/boot/Petrol Filter e inicie el programa dentro de este directorio con el comando python3 main.py. \n'
                                    '• En el tercer paso ya abierto el programa inciará el proceso, continúe con los siguientes subpasos: para usar el servicio utilizar los comandos make start|stop|status, para ver la salida desde la terminal el código make log. \n'
                                    '• Cuarto paso: conectarse a la interfaz grafica desarrolada en la nube de \n https://cloud4rpi.io/, con el ID del proyecto para visualizar los distintos niveles de agua y demás advertencias.\n'
                                    '• Quinto paso: Gracias por confiar en Petrol Filter, Aclaremos el mar :)')
async def parts (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Componenetes:'    '\n [Electrónicos]: \n'
                                                  ' ❖ Sensor ultrasonico jsn-sr04t \n'
                                                  ' ❖ Electroválvula 12V \n'
                                                  ' ❖ Raspberry pi zero W 1.1v \n'
                                                  ' ❖ Bomba para agua e hidrocarburos 12V \n'
                                                  ' ❖ Batería tipo alarma 12V \n'
                                                      '\n [Estructurales]: \n'
                                                  ' ❖ Caños de termofusión \n'
                                                  ' ❖ Bidón de dispenser de 20L \n'
                                                  ' ❖ Salvavidas circular \n')

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('mail de contacto: petrolfilter2022@gmail.com')                                                    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Comandos de ayuda: \n /guide: Guía de usuario del dispositivo \n /parts: Componentes utilizados en el proyecto \n /contact: Contacto al equipo de petrol filter \n /github Link al repositorio en la plataforma GitHub')
async def github(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('github link: https://github.com/impatrq/petrol_filter')

#Notificaciones

async def SENSOR_ERROR (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('[⚠] Error de distancia!')
async def log_error (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('[⚠] Emergencia se ha detenido la bomba. No hay señal desde el sensor de distancia')
async def log_error1 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('[⚠] La bomba se encuentra obstruida!')
async def log_error2 (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('[☠] ALERTA RIESGO DE DERRAME!')
async def notify_in_background (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('[⚠] Advertencia entrada de aire en la bomba')



app = ApplicationBuilder().token("5575352817:AAEyO5bsI3s4O1DJUu5xA0M0rjSeBT0ijUA").build()

#Declaración de las notificaciones

app.add_handler(CommandHandler("log_error", log_error))
app.add_handler(CommandHandler("log_error1", log_error1))
app.add_handler(CommandHandler("log_error2", log_error2))
app.add_handler(CommandHandler("SENSOR_ERROR", SENSOR_ERROR))
app.add_handler(CommandHandler("notify_in_background", notify_in_background))

#Declaración de los mensajes del bot

app.add_handler(CommandHandler("hola", hola))
app.add_handler(CommandHandler("guide", guide))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("parts", parts))
app.add_handler(CommandHandler("contact", contact))
app.add_handler(CommandHandler("github", github))
app.run_polling()
