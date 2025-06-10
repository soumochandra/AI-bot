import tkinter as tk
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia

# Initialize TTS engine with female voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_time():
    now = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The time is {now}")
    return f"🕒 {now}"

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        speak("Yes sir...")
        try:
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio).lower()
            print("🔎 Recognized:", command)
            return command
        except sr.WaitTimeoutError:
            speak("No input received.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("Network error.")
    return ""

def handle_command():
    command = listen_command()
    if not command:
        return
    if 'time' in command:
        update_output(get_time())
    elif 'wikipedia' in command:
        topic = command.replace('wikipedia', '').strip()
        try:
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
            update_output(f"📚 {result}")
        except:
            speak("Sorry, I couldn't find anything.")
            update_output("❌ Wikipedia lookup failed.")
    elif 'open' in command:
        site = command.replace('open', '').strip()
        url = f"https://{site}.com"
        webbrowser.open(url)
        speak(f"Opening {site}")
        update_output(f"🌐 Opening {url}")
    elif 'exit' in command or 'stop' in command:
        speak("Okay, I am closing. Goodbye sir!")
        root.quit()
    else:
        speak("Sorry, I can't do this right now.")
        update_output("❌ Command not recognized.")

def update_output(text):
    output_box.config(state='normal')
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state='disabled')

def animate_splash(count=0):
    dots = "." * (count % 4)
    splash_label.config(text=f"Loading your AI Assistant{dots}")
    splash.after(400, animate_splash, count + 1)

def show_main_app():
    splash.destroy()
    global root, output_box

    root = tk.Tk()
    root.title("Soumo's AI Assistant")
    root.geometry("500x600")
    root.configure(bg="#222831")

    title = tk.Label(root, text="Soumo's AI Assistant", font=("Helvetica", 20, "bold"), bg="#222831", fg="#00FFF5")
    title.pack(pady=10)

    output_box = tk.Text(root, height=8, width=50, bg="#393E46", fg="#EEEEEE", font=("Arial", 12))
    output_box.pack(pady=20)
    output_box.config(state='disabled')

    listen_btn = tk.Button(root, text="Start Talking", font=("Helvetica", 14), bg="#00ADB5", fg="white", command=handle_command)
    listen_btn.pack(pady=20)

    footer = tk.Label(root, text="Built by Soumo", bg="#222831", fg="#888")
    footer.pack(side="bottom", pady=10)

    root.after(800, lambda: speak("Hello sir, I am your AI Assistant. How can I help you today?"))
    root.mainloop()

# Splash screen
splash = tk.Tk()
splash.overrideredirect(True)
splash.geometry("400x300+500+200")
splash.configure(bg="#111")

splash_label = tk.Label(splash, text="Loading AI Assistant", font=("Helvetica", 16), bg="#111", fg="#00FFF5")
splash_label.pack(expand=True)

animate_splash()
splash.after(2000, show_main_app)
splash.mainloop()
