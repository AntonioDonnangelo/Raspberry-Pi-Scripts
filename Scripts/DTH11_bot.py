import Adafruit_DHT  # Libreria deprecata, clonata da https://github.com/adafruit/Adafruit_Python_DHT
from tm1637 import TM1637
import RPi.GPIO as GPIO  # Modulo per gestire i pin GPIO
import telepot  # Libreria per Telegram
from telepot.loop import MessageLoop  # Gestione dei messaggi
from time import sleep, strftime

# Configura il token del bot Telegram
TOKEN = '8097530462:AAF01TEd3_rwn-3rigifDigLmf4Ur7kCQzM'
bot = telepot.Bot(TOKEN)

# Configurazione del sensore DHT
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Pin collegato al sensore DHT11

# Pin per il display TM1637
CLK_PIN = 1  # Pin GPIO per il clock
DIO_PIN = 0  # Pin GPIO per i dati

# Inizializzazione GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DHT_PIN, GPIO.IN)
GPIO.setup(CLK_PIN, GPIO.OUT)
GPIO.setup(DIO_PIN, GPIO.OUT)

# Inizializzazione del display TM1637
display = TM1637(CLK_PIN, DIO_PIN)
display.brightness(4)  # Luminosità del display (0-7)

# Funzione per leggere i dati dal sensore DHT11
def get_temp_humidity():
    humidity, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is None or temp is None:
        raise RuntimeError("Impossibile leggere i dati dal sensore")
    return temp, humidity

# Funzione per gestire i messaggi ricevuti dal bot Telegram
def handle_message(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].strip().lower()

    if command == '/temp':
        try:
            temp, humidity = get_temp_humidity()
            message = f"Temperatura: {temp:.1f}°C\nUmidità: {humidity:.1f}%"
        except RuntimeError as e:
            message = f"Errore: {str(e)}"
        bot.sendMessage(chat_id, message)
    else:
        bot.sendMessage(chat_id, "Comando non riconosciuto. Usa /temp per ottenere temperatura e umidità.")

# Funzione per aggiornare il display con l'ora, temperatura e umidità
def update_display(temp, humidity):
    # Mostra l'ora corrente
    ora = int(strftime("%H"))
    minuti = int(strftime("%M"))
    display.numbers(ora, minuti)
    sleep(3)  # Attendi prima di aggiornare la temperatura

    # Mostra la temperatura sul display
    display.temperature(int(temp))
    sleep(3)

    # Mostra l'umidità sul display
    display.number(int(humidity))
    display.write([0b00111110, 0b01010000])  # Icona personalizzata
    sleep(3)

# Funzione principale di esecuzione del loop
def main_loop():
    while True:
        try:
            temp, humidity = get_temp_humidity()
            update_display(temp, humidity)
        except RuntimeError as e:
            print(f"Errore: {e}")
            sleep(5)  # Attendi prima di riprovare

# Avvia il bot per gestire i messaggi
MessageLoop(bot, handle_message).run_as_thread()

# Messaggio di avvio
print("Bot attivo. Usa il comando /temp per ottenere la temperatura e umidità.")

# Esegui il loop principale
if __name__ == "__main__":
    main_loop()
