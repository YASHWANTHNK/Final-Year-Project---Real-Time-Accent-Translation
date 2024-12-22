import os
import threading
import tkinter as tk
from tkinter import ttk
import pyaudio
import speech_recognition as sr
from gtts import gTTS
from deep_translator import GoogleTranslator
import time
import subprocess

language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
}

input_language = "en"
output_language = "kn"
selected_device_index = None

def capture_audio_from_device(duration=10):
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=selected_device_index,
            frames_per_buffer=CHUNK,
        )

        r = sr.Recognizer()
        r.energy_threshold = 200
        r.dynamic_energy_threshold = False

        update_text(input_box, "Listening for 10 seconds...")

        frames = []
        start_time = time.time()

        while time.time() - start_time < duration:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                print(f"Audio capture error: {e}")

        audio_data = sr.AudioData(b''.join(frames), RATE, 2)
        return audio_data

    except Exception as e:
        print(f"Failed to open audio device: {e}")
        return None

def play_audio_and_wait():
    try:
        process = subprocess.Popen(["start", "translated_audio.mp3"], shell=True)
        process.wait()
    except Exception as e:
        print(f"Error while playing audio: {e}")
    finally:
        if os.path.exists("translated_audio.mp3"):
            os.remove("translated_audio.mp3")

def process_translation():
    r = sr.Recognizer()

    try:
        audio_data = capture_audio_from_device(duration=10)

        if audio_data:
            update_text(input_box, "Processing the audio...")

            try:
                update_text(input_box, f"Entering translator {audio_data}")
                recognized_text = r.recognize_google(audio_data, language=input_language)
                update_text(input_box, f"Recognized: {recognized_text}")

                translated_text = GoogleTranslator(source=input_language, target=output_language).translate(recognized_text)
                update_text(output_box, f"Translated: {translated_text}")

                tts = gTTS(translated_text, lang=output_language)
                tts.save("translated_audio.mp3")

                play_audio_and_wait()

            except sr.UnknownValueError:
                update_text(input_box, "Could not understand the audio.")
            except sr.RequestError as e:
                update_text(input_box, f"Google Speech API error: {e}")
            except Exception as e:
                print(f"Translation error: {e}")
        else:
            update_text(input_box, "No audio captured.")

    except Exception as e:
        print(f"Processing error: {e}")

def update_text(widget, text):
    widget.insert(tk.END, f"{text}\n")
    widget.see(tk.END)

def start_translation():
    threading.Thread(target=process_translation, daemon=True).start()

def stop_translation():
    root.quit()

def set_languages():
    global input_language, output_language
    input_language = language_codes[input_lang_dropdown.get()]
    output_language = language_codes[output_lang_dropdown.get()]
    update_text(input_box, f"Input language set to {input_lang_dropdown.get()}")
    update_text(output_box, f"Output language set to {output_lang_dropdown.get()}")

def set_audio_device():
    global selected_device_index
    selected_device_index = device_list.index(device_dropdown.get())
    update_text(input_box, f"Selected audio device: {device_dropdown.get()}")

root = tk.Tk()
root.title("Audio Translator")
root.geometry("800x600")

input_lang_label = tk.Label(root, text="Select Input Language:")
input_lang_label.pack()

input_lang_dropdown = ttk.Combobox(root, values=list(language_codes.keys()), state="readonly")
input_lang_dropdown.set("English")
input_lang_dropdown.pack()

output_lang_label = tk.Label(root, text="Select Output Language:")
output_lang_label.pack()

output_lang_dropdown = ttk.Combobox(root, values=list(language_codes.keys()), state="readonly")
output_lang_dropdown.set("Kannada")
output_lang_dropdown.pack()

set_lang_button = tk.Button(root, text="Set Languages", command=set_languages)
set_lang_button.pack()

device_list = sr.Microphone.list_microphone_names()
virtual_audio_device = "CABLE In 16 Ch (VB-Audio Virtual Cable)"

device_dropdown = ttk.Combobox(root, values=device_list, state="readonly")

input_box_label = tk.Label(root, text="Recognized Text:")
input_box_label.pack()

input_box = tk.Text(root, height=10, width=80)
input_box.pack()

output_box_label = tk.Label(root, text="Translated Text:")
output_box_label.pack()

output_box = tk.Text(root, height=10, width=80)
output_box.pack()

if virtual_audio_device in device_list:
    device_dropdown.set(virtual_audio_device)
    device_dropdown.pack()

    set_device_button = tk.Button(root, text="Set Device", command=set_audio_device)
    set_device_button.pack()

    update_text(input_box, f"Selected audio device: {virtual_audio_device}")
else:
    update_text(input_box, "VB-Audio Virtual Cable not found.")

start_button = tk.Button(root, text="Start Translation", command=start_translation, bg="green", fg="white")
start_button.pack(side=tk.LEFT, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop Translation", command=stop_translation, bg="red", fg="white")
stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()