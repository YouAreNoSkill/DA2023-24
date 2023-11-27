from selenium import webdriver
import cv2
import numpy as np
import base64
import time
from PIL import Image
from selenium.common.exceptions import WebDriverException
from ftplib import FTP

# Neue URL der Webseite
url = "file:///C:/Users/Maxig/Desktop/website-neu.html"
output_file = '800x480.bmp'

def png_to_monochrome_bitmap(input_file, output_file, output_size=(800, 480)):
    # Laden des PNG Bildes
    image = Image.open(input_file)
    
    # PNG Bild in Graustufen umwandeln
    grayscale_image = image.convert('L')
    
    # Umwandeln der Graustufen in 1/0 also schwarz oder weiss
    monochrome_bitmap = grayscale_image.point(lambda x: 0 if x < 128 else 255, '1')
    
    # Zuschneiden auf die gewuenschte Groesse (800x480)
    monochrome_bitmap = monochrome_bitmap.resize(output_size)
    
    # Speichern
    monochrome_bitmap.save(output_file)

# Funktion zum Hochladen der BMP-Datei auf den FTP-Server
def upload_to_ftp(server, username, password, file_path, remote_directory):
    try:
        with FTP(server) as ftp:
            ftp.login(user=username, passwd=password)
            ftp.cwd(remote_directory)
            with open(file_path, 'rb') as local_file:
                ftp.storbinary('STOR ' + output_file, local_file)
        print(f"Die Datei {file_path} wurde erfolgreich auf den FTP-Server hochgeladen.")
    except Exception as e:
        print(f"Fehler beim Hochladen der Datei auf den FTP-Server: {str(e)}")

# Hauptprogramm
while True:
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        # Die Webseite oeffnen
        driver.get(url)

        # Sicherstellen, dass die Seite vollstaendig geladen ist
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        driver.implicitly_wait(10)

        # Einen Screenshot der Webseite aufnehmen
        screenshot = driver.get_screenshot_as_base64()

        # Den Screenshot in ein OpenCV-Bild umwandeln
        image = cv2.imdecode(
            np.frombuffer(base64.b64decode(screenshot), np.uint8),
            cv2.IMREAD_COLOR
        )

        # Das Bild speichern
        cv2.imwrite("webpage_screenshot.png", image)

        # Den Webbrowser schliessen
        driver.quit()

        # .png in bmp 2 Farben monochrombitmap umwandeln und auf 800x480 zuschneiden
        input_file = 'webpage_screenshot.png'
        png_to_monochrome_bitmap(input_file, output_file)

        # Hochladen der BMP-Datei auf den FTP-Server
        ftp_server = 'raspberrypi.local'
        ftp_username = 'pi'
        ftp_password = 'Schoren1.2.3'
        remote_directory = '/home/pi/e-Paper/RaspberryPi_JetsonNano/c/pic'

        upload_to_ftp(ftp_server, ftp_username, ftp_password, output_file, remote_directory)

        # Warte 10 Sekunden vor der naechsten Iteration
        #time.sleep(1)
    except WebDriverException:
        print("Fehler beim Oeffnen der Webseite. Warte 10 Sekunden und versuche erneut.")
