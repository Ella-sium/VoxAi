import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
from youtube_search import YoutubeSearch
import webbrowser
import pyaudio
# from PIL import Image

# Initialiser la reconnaissance vocale et la synthèse vocale
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Fonction pour parler (synthèse vocale)
def speak(text):
    label.configure(text=text, text_color="yellow") 
    app.update()
    engine.say(text)
    engine.runAndWait()


# Fonction pour écouter et reconnaitre la voix
def recognizer_speach():
    label.configure(text="🎤 Parlez maintenant...", text_color="red")  # Affiche "Parlez maintenant..."
    app.update() 

    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        # print("Parlez maintenant")

        try:
            audio = recognizer.listen(source, timeout=6)
            label.configure(text="Analyse en cours...", text_color="white")
            app.update()
            command = recognizer.recognize_google(audio, language="fr-FR")
            label.configure(text=f"Vous avez dit : {command}", text_color="white")
            return command.lower()
        except sr.WaitTimeoutError:
            speak("Temps écoulé")
        except sr.UnknownValueError:
            speak("Je n'ai pas compris!")
            return ""
        except sr.RequestError:
            speak("Erreur de connexion")
            return ""


# Fonction pour exécuter des commandes vocales
def execute_command():
    command = recognizer_speach()

    if "joue" in command:
        song_name = command.replace("joue", "").strip()
        speak(f"Recherche de {song_name} sur Youtube.")

        # Recherche sur youtube
        results = YoutubeSearch(song_name, max_results=1).to_dict()
        if results:
            video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
            speak(f"Lecture de {results[0]['title']}")
            webbrowser.open(video_url)

        else:
            speak("Aucune vidéo trouvée.")
    elif "ouvre Youtube" in command:
        speak("Ouverture de Youtube.")
        webbrowser.open("https://www.youtube.com/")

    elif "ferme" in command:
        speak("Fermeture de l'application.")
        app.quit()
    else: 
        speak("Commande non reconnue.")


# Initialisation de l'application
# Paramétrer l'apparence de la fenetre 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Créé une instance de customtkinder

app = ctk.CTk()
app.title("Assitant Vocal|VoxAi")
app.geometry("600*600")

# Création du label
# Label d'instruction
label = ctk.CTkLabel(app, text="Cliquer pour lancer une commande", font=("Helvetica", 16))
label.pack(pady=30)

# Charger l'icône du microphone
# mic_icon = ctk.CTkImage(light_image=Image.open("micro.png"), size=(50, 50))


# Créé un micro pour enregistrer la commande vocal
micro = ctk.CTkButton(app, text="Ecouter", command=execute_command, font=("Helvetica", 14), height=50, width=200)
micro.pack(pady=20)

# font=("Helvetica", 14), height=50, width=200 image=mic_icon
# Bouton pour quitter la reconnaissance vocale
quitter_bouton = ctk.CTkButton(app, text="Quitter", command=execute_command, font=("Helvetica", 14), height=50, width=200, fg_color="red")
quitter_bouton.pack(pady=20)

app.mainloop()




