import time
import Adafruit_DHT #Libreria deprecata, clonata e installata da https://github.com/adafruit/Adafruit_Python_DHT

DELAY_SECONDS=10 # Apetta 10 secondi 

DHT_SENSOR=Adafruit_DHT.DHT11 #Tipo di sensore DHT11
DHT_PIN=4 #Pin indica il GPIO

if __name__ == "__main__":
    print("Lettura in corso... ")

    while True:
        try:
            # Stampa i valori letti
            humidity, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            print("Temp: {0:0.1f} °C    Humidity: {1:0.1f} % ".format(temp, humidity))
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(5.0) #Aspetta 5.0 secondi in caso di errore
            continue
        time.sleep(DELAY_SECONDS)
