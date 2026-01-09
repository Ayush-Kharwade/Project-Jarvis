import os
import subprocess
import requests
import json
import time
import vosk
import sounddevice as sd
import queue
import pvporcupine
import struct
import numpy as np

# --- Configuration ---
PICOVOICE_ACCESS_KEY = "YOUR_ACCESS_KEY_HERE"
HARDWARE_RATE = 48000
APP_RATE = 16000
DOWNSAMPLE_RATIO = int(HARDWARE_RATE / APP_RATE)
WAKE_WORD = "computer"
VOSK_MODEL_PATH = "vosk-model-small-en-us-0.15"
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "tinyllama"
DEVICE_ID = None

# --- Functions (speak, get_llm_response) ---
def speak(text_to_speak):
    print(f"Speaking: {text_to_speak}")
    wav_file = "response.wav"
    subprocess.run(['pico2wave', '-w', wav_file, text_to_speak], stderr=subprocess.DEVNULL)
    subprocess.run(['aplay', wav_file], stderr=subprocess.DEVNULL)
    print("Finished speaking.")

def get_llm_response(prompt):
    print(f"Sending prompt to {OLLAMA_MODEL}: {prompt}")
    try:
        payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        llm_answer = response_data.get("response", "I am not sure how to answer.").strip()
    except requests.exceptions.RequestException as e:
        llm_answer = "Sorry, I could not connect to the language model."
        print(f"Error connecting to Ollama: {e}")
    return ll_answer

# --- Speech-to-Text Function (Simpler) ---
def transcribe_audio(audio_data_resampled):
    """Takes a block of audio data and transcribes it using Vosk."""
    print("Processing command...")
    vosk_model = vosk.Model(VOSK_MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(vosk_model, APP_RATE)
    
    recognizer.AcceptWaveform(audio_data_resampled.tobytes())
    result = json.loads(recognizer.Result())
    heard_text = result.get('text', '')
    
    print(f"Heard: {heard_text}")
    return heard_text

# --- Main Program Loop (Corrected Architecture) ---
def main():
    porcupine = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(access_key=PICOVOICE_ACCESS_KEY, keywords=[WAKE_WORD])
        
        audio_stream = sd.RawInputStream(
            device=DEVICE_ID,
            samplerate=HARDWARE_RATE,
            blocksize=porcupine.frame_length * DOWNSAMPLE_RATIO,
            channels=1,
            dtype='int16',
        )
        audio_stream.start()
        print(f"System ready. Listening for the wake word '{WAKE_WORD}'...")
        speak("System ready.")

        while True:
            pcm_high_rate = audio_stream.read(porcupine.frame_length * DOWNSAMPLE_RATIO)[0]
            pcm_high_rate_np = np.frombuffer(pcm_high_rate, dtype=np.int16)
            pcm_low_rate_np = pcm_high_rate_np[::DOWNSAMPLE_RATIO]
            
            keyword_index = porcupine.process(pcm_low_rate_np.tolist())
            
            if keyword_index >= 0:
                print(f"Wake word '{WAKE_WORD}' detected!")
                speak("Listening.")
                
                # --- NEW: Capture command from the SAME stream ---
                command_frames = []
                # Calculate how many frames to capture for 5 seconds of audio
                num_frames_to_capture = int((HARDWARE_RATE / (porcupine.frame_length * DOWNSAMPLE_RATIO)) * 5)
                
                print("Recording command for 5 seconds...")
                for _ in range(num_frames_to_capture):
                    command_frames.append(audio_stream.read(porcupine.frame_length * DOWNSAMPLE_RATIO)[0])
                
                # Combine the captured frames into a single block of audio data
                command_audio_data = np.frombuffer(b''.join(command_frames), dtype=np.int16)
                
                # Resample the command audio for Vosk
                command_audio_resampled = command_audio_data[::DOWNSAMPLE_RATIO]
                
                # Transcribe the command
                command = transcribe_audio(command_audio_resampled)
                
                if command:
                    ai_response = get_llm_response(command)
                    speak(ai_response)
                else:
                    speak("I did not catch that.")
                print(f"Returning to listen for wake word '{WAKE_WORD}'...")

    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    main()