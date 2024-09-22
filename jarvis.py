import speech_recognition as sr
import pyttsx3
import pyaudio
import requests
from datetime import datetime
import webbrowser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Initialisation du moteur vocal
engine = pyttsx3.init()
engine.setProperty('volume', 1.5)
engine.setProperty('rate',225)

API_key_meteo = "e5859cf005fb60a5e50a53233a95b79a"
city = "Lille"
base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key_meteo}&units=metric"
playlist = "https://www.youtube.com/watch?v=s3O1Xro7oAI"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Jarvis écoute...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="fr-FR")
        print(f"Tu as dit : {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Je n'ai pas compris, peux-tu répéter?")
        return None

def send_email(to_email, subject, message):
    from_email = "louannegauche@gmail.com"
    # a verifier
    password = "paulvaavoirunesacreesurprise1999"

    print("to : ", to_email, "subject =", subject, "message = ", message  )
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try: 
        server = smtplib.SMTP('64.233.187.109', 587)
        server.starttls()
        server.login(from_email,password)

        server.send_message(msg)
        server.quit()
        speak("Le message vient d'être envoyé")

    except Exception as e:
        speak("Une erreur s'est produite lors de l'envoi de l'e-mail : " + str(e))
        print(e)

def configuration():
    global city
    response = requests.get("https://ipinfo.io")
    data = response.json()
    city = data["city"]
    
def correction_erreur():
    global city
    speak("Vous m'avez signaler une erreur... Quels paramètres cela concerne t'il?")
    param = listen()
    if "ville" in param:
        speak("Ou sommes nous alors?")
        city = listen()
        speak(f"c'est noté, nous sommes à {city}")
    else:
        return

def search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Voici les résultats pour {query} sur Google.")

def get_localisation():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        city = data["city"]
        region = data["region"]
        country = data["country"]
        loc = data['loc']
        speak(f"Vous vous trouvez actuellement à {city}, {region}, {country}")
        speak(f"Voulez vous les coordonnées GPS?")
        rep = listen()
        if "oui" in rep:
            speak(f"Les coordonnées GPS sont {loc}")
    except Exception as e:
        speak(f"Je n'ai réussi à avoir notre localisation, erreur {str(e)}")

def get_weather(city):
    try: 
        response = requests.get(base_url)
        data = response.json()       
        if data["cod"] != "404": #error code
            weather = data["main"]
            temp = weather["temp"]
            desc = data["weather"][0]["description"]
            speak(f"La température à {city} est de {temp} degrés Celsius, avec {desc}")
        else:
            speak(f"Je n'ai pas pu trouver la météo pour {city}")
    except Exception as e:
        speak(f"Je n'ai pas pu récupérer les données météos. Erreur {str(e)}")

"""
TODO
def get_weather_in_a_place():
    try:
        speak("Vous voulez la météo dans quel endroit?")
        where = listen()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={where}&appid={API_key_meteo}&units=metric"
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] != "404": #error code
            weather = data["main"]
            temp = weather["temp"]
            desc = data["weather"][0]["description"]
            speak(f"La température à {city} est de {temp} degrés Celsius, avec {desc}")
        else:
            speak(f"Je n'ai pas pu trouver la météo pour {city}")
    except Exception as e:
        speak(f"Je n'ai pas pu récupérer les données météos. Erreur {str(e)}")
"""
def youtube(request):
    url = f"https://www.youtube.com/results?search_query={request}"
    webbrowser.open(url)
    speak(f"Voici les résultats pour {request} sur Youtube.")

def get_hour():
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M")  # Format 24h
        speak(f"Il est {current_time}")
    except Exception as e:
        speak(f"Je n'ai pas réussi à obtenir l'heure à {city}, Erreur {str(e)}")

def open_app(app_name):
    if "navigateur" in app_name or "Google" in app_name or "Bing" in app_name:
        webbrowser.open("https://www.google.com")
        speak("J'ouvre le navigateur")
    elif "notepad" in app_name:
        os.startfile("notepad.exe")
        speak("J'ouvre Notepad")
    elif "facebook" in app_name:
        webbrowser.open("https://www.facebook.com") 
        speak("J'ouvre Facebook.")
    elif "whatsapp" in app_name:
        webbrowser.open("https://web.whatsapp.com") 
        speak("J'ouvre WhatsApp.")
    elif "caméra" in app_name or "camera" in app_name:
        os.startfile("Microsoft.WindowsCamera:")  
        speak("J'ouvre la caméra.")
    elif "calculatrice" in app_name:
        os.startfile("calc.exe")
        speak("J'ouvre la calculatrice.")
    elif "mes fichiers" in app_name:
        os.startfile("explorer.exe")  
        speak("J'ouvre Mes fichiers.")
    elif "mail" in app_name:
        os.startfile("outlook.exe")  
        speak("J'ouvre l'application Mail.")
    elif "teams" in app_name:
        os.startfile("Teams.exe") 
        speak("J'ouvre Teams.")
    else:
        speak("Je ne trouve pas l'application demandée.")

# Fonction principale
def jarvis():
    while True:
        command = listen()
        if command:
            if "bonjour" in command or "salut" in command or "allo" in command:
                speak("Bonjour, comment puis-je t'aider aujourd'hui?")
            elif "qui es-tu" in command or "Comment t'appelles tu" in command: 
                speak("Je suis Jarvisse, un assistant virtuel. J'ai été crée par Sébastien Doyez, dans le but de l'aider dans ses tâches. ")
            elif "stop" in command:
                speak("Au revoir !")
                break
            elif "météo" in command:
                get_weather(city)
            elif "heure" in command:
                get_hour()
            elif "youtube" in command:
                speak("Que voulez vous rechercher sur youtube?")
                request = listen()
                youtube(request)
            elif "localisation" in command or "ou suis-je" in command:
                get_localisation()
            elif "erreur" in command:
                correction_erreur()
            elif "recherche" in command or "cherche sur google" in command:
                speak("Que souhaitez vous rechercher?")
                recherche = listen()
                search(recherche) 
            elif "application" in command or "logiciel" in command:
                speak("Quel application voulez vous ouvrir?")
                app = listen()
                open_app(app)
            elif "musique" in command:
                speak("Quels application voulez vous utilisez?")
                rep = listen()
                if "YouTube" in rep:
                    webbrowser.open(playlist)
                else:
                    continue
            elif "mail" in command:
                speak("Qui est le destinateur?")
                dest = listen()
                if dest == "maman":
                    speak("Nous allons envoyé un mail à maman")
                    email_dest = "fontaine.christine7777@gmail.com"
                else :
                    email_dest = None
                speak("Objet du mail?")
                object = listen()
                speak("Quel est le message?")
                msg = listen()
                send_email(dest,object, msg)
            else:
                speak("Je ne connais pas encore cette commande.")


# Lancement de Jarvis
if __name__ == "__main__":
    configuration()
    jarvis()
