## Stampa orario e valori di temperatura e umidità ad intervalli regolari sullo schermo

import Adafruit_DHT  # Libreria deprecata, clonata e installata da https://github.com/adafruit/Adafruit_Python_DHT
from time import strftime, sleep
from tm1637 import TM1637
import RPi.GPIO as GPIO  # Importa il modulo GPIO per pulire i pin

# Sensore DHT
DHT_SENSOR = Adafruit_DHT.DHT11  # Tipo di sensore DHT11
DHT_PIN = 4  # Pin indica il GPIO

# Definisci i pin del display
CLK_PIN = 1  # Sostituisci con il GPIO corretto
DIO_PIN = 0  # Sostituisci con il GPIO corretto

# Configura i pin GPIO
GPIO.setmode(GPIO.BCM)  # Usa la numerazione BCM
GPIO.setup(DHT_PIN, GPIO.IN)  # Imposta il pin del sensore DHT come INPUT
GPIO.setup(CLK_PIN, GPIO.OUT)  # Imposta il pin CLK del display come OUTPUT
GPIO.setup(DIO_PIN, GPIO.OUT)  # Imposta il pin DIO del display come OUTPUT

# Inizializza il display del modulo TM1637
display = TM1637(CLK_PIN, DIO_PIN)
display.brightness(4)  # Imposta la luminosità (valori tra 0 e 7)

# Definisci il tempo di attesa tra le letture
DELAY_SECONDS = 4  # 4 secondi 

while True:
    try:
        # Ottieni l'ora e i minuti
        ora = int(strftime("%H"))  # Ottieni le ore in formato HH
        minuti = int(strftime("%M"))  # Ottieni i minuti in formato MM

        # Ottieni i valori di temperatura e umidità
        humidity, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        # Invia l'ora al display
        display.numbers(ora, minuti)  # Visualizza l'ora
        sleep(DELAY_SECONDS)  

        # Invia la temperatura al display
        display.temperature(int(temp))  # Visualizza la temperatura
        sleep(DELAY_SECONDS)  

        # Invia l'umidità al display
        display.number(int(humidity))  # Visualizza l'umidità
        display.write([0b00111110, 0b01010000])  # Visualizza Ur prima del valore
        sleep(DELAY_SECONDS)  
          
    except RuntimeError as error:
        print(error.args[0])
        sleep(5.0)  # Aspetta 5 secondi in caso di errore 
        continue
