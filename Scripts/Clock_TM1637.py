from time import strftime, sleep
from tm1637 import TM1637

# Definisci i pin del display
CLK_PIN = 1  # Sostituisci con il GPIO corretto
DIO_PIN = 0  # Sostituisci con il GPIO corretto

# Inizializza il display
display = TM1637(CLK_PIN, DIO_PIN)

# Imposta la luminosità (valori tra 0 e 7)
display.brightness(4)

while True:
    # Ottieni l'ora attuale
    ora = int(strftime("%H"))  # Ottieni le ore in formato HH
    minuti = int(strftime("%M"))  # Ottieni i minuti in formato MM

    # Invia l'ora al display
    display.numbers(ora, minuti)  # Visualizza l'ora
    sleep(15)  # Aggiorna ogni 15 secondi
