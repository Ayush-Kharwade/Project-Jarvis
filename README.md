JARVIS: Offline AI Voice Assistant (Project Swadeshi)
JARVIS is a fully offline, private AI voice assistant built for the Raspberry Pi 4. It was specifically designed and launched for the 79th Independence Day celebration to demonstrate the power of local AI and innovative robotics.

🚀 Key Features
100% Offline: No data leaves the device. Privacy is baked into the design at every level.

Local LLM: Powered by TinyLlama via the Ollama engine, allowing for natural language understanding without an internet connection.

Custom Intent Parser: Specialized logic to handle specific commands like playing the National Anthem and reciting hardware specifications.

Omni-Directional Movement: Controlled via an Arduino Mega and a Cytron motor driver. The Omni-wheels allow JARVIS to glide in any direction without turning.

High-Torque Actuators: A synchronized dual-arm system using 150kg and 25kg high-torque servo motors.

🛠️The Tech Stack
Component	                          Technology
Brain	                              Raspberry Pi 4 (8GB RAM)
Wake Word	                          Picovoice Porcupine ("Jarvis")
Speech-to-Text	                    Vosk (Small Indian English Model)
Intelligence	                      Ollama + TinyLlama
Text-to-Speech	                    PicoTTS (pico2wave)
Audio Playback	                    ALSA (aplay)
Motion Control	                    Arduino Mega + Cytron Motor Driver

📥 Installation & Setup
To replicate this implementation on Raspberry Pi OS (64-bit), follow these steps:

1. Install System Dependencies

sudo apt update
sudo apt install libttspico-utils alsa-utils -y

2. Setup Ollama (Local LLM Engine)

curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama

3. Install Python Libraries

pip install vosk sounddevice numpy pvporcupine requests

4. Prepare Models & Files

Download the Vosk Small English Model and extract it to the project folder as vosk-model-small-en-us-0.15.

Ensure your national_anthem.wav is saved in /home/shadow/.

Ensure bot_specs.txt contains the introductory script in the same directory as main.py.

🎮 Usage
Run the assistant with the following command:

python main.py
Special Voice Commands:

"Play the national anthem" — Triggers the instrumental version of Jana Gana Mana.

"Tell me about yourself / specifications" — Reads the hardware and software breakdown from bot_specs.txt.

🇮🇳 Credits & Acknowledgments
This project is the result of the collective effort, passion, and technical innovation of the ROBO-CLUB members.

We extend our deepest gratitude to our Faculty Coordinator, Dr. Priyanka Bagul Ma'am, for her constant support, mentorship, and for encouraging the students to push the boundaries of engineering.

Jai Hind!
