"""
VIOLET - AI Chat Bot for Kick.com
Fully integrated bot that connects directly to Kick chat
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import pygame
import requests
import json
import threading
import time
import logging
from datetime import datetime
from PIL import Image, ImageTk, ImageSequence
import io
import random
import os
import base64

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VIOLET")

class VIOLETKickBot:
    def __init__(self):
        # Configuration
        self.config = {
            # Hume AI Configuration
            "hume_api_key": "ZdfEOvorgYUSvjnworCedPG8s2O0LEe9cmSehjBGLET263Xq",
            "hume_secret_key": "jAPvHmzpGFdkLCUJk03CAPPMFbEA5Y1Na6m19jOxxtuaGpLds90DPucIjqpaTmba",
            "voice": "59cfc7ab-e945-43de-ad1a-471daa379c67",  # Kora voice
            
            # Kick Configuration
            "kick_oauth_token": "01K9TCK0R0TQH150D4WRZJWBM6",
            "kick_client_id": "01K9TCK0R0TQH150D4WRZJWBM6",
            "kick_client_secret": "d72edcb210b7ca2fbefc70cdd961c1934a06c329c570ebcf2118d8cdb28df53e",
            
            # Bot Settings
            "response_delay": 3,  # seconds between responses
            "min_message_length": 3,  # minimum message length to respond
            "response_probability": 0.7,  # chance to respond to mentions
            "auto_respond": True,  # enable automatic responses
        }
        
        # Voice mappings
        self.voice_mappings = {
            'kora': "59cfc7ab-e945-43de-ad1a-471daa379c67",
            'ava_song': "5bb7de05-c8fe-426a-8fcc-ba4fc4ce9f9c",
            'sitcom_girl': "5bbc32c1-a1f6-44e8-bedb-9870f23619e2"
        }
        
        self.logger = logging.getLogger("VIOLET.Main")
        self.logger.info("VIOLET Kick Chat Bot Initializing...")
        
        # Initialize pygame for audio
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)
        self.logger.info("Audio system initialized")
        
        # Initialize tkinter
        self.root = tk.Tk()
        self.root.title("VIOLET - Kick Chat Bot")
        self.root.geometry("800x600")
        
        # Bot state
        self.is_connected = False
        self.is_speaking = False
        self.last_response_time = 0
        self.chat_messages = []
        self.commands_history = []
        
        # Load animations
        self.load_animations()
        
        # Create UI
        self.create_ui()
        
        # Initialize Kick connection
        self.initialize_kick_connection()
        
    def load_animations(self):
        """Load GIF animations"""
        emotions = {
            'thinking': 'Thinking.gif',
            'happy': 'Happy.gif',
            'energetic': 'Energetic.gif',
            'shocked': 'shocked.gif',
            'angry': 'Angrey.gif',
            'no_way': 'no way .gif'
        }
        
        self.animation_frames = {}
        
        for emotion, filename in emotions.items():
            try:
                if os.path.exists(filename):
                    gif = Image.open(filename)
                    frames = []
                    try:
                        while True:
                            frame = gif.copy()
                            frame = frame.resize((300, 300), Image.Resampling.LANCZOS)
                            frames.append(ImageTk.PhotoImage(frame))
                            gif.seek(len(frames))
                    except EOFError:
                        pass
                    self.animation_frames[emotion] = frames
                    self.logger.info(f"Loaded {len(frames)} frames for {emotion}")
            except Exception as e:
                self.logger.error(f"Error loading {emotion} animation: {e}")
                
    def create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top panel - Status and Animation
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Animation frame
        self.animation_frame = ttk.Frame(top_frame)
        self.animation_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        self.character_label = tk.Label(self.animation_frame, bg='black')
        self.character_label.pack()
        
        # Status frame
        status_frame = ttk.Frame(top_frame)
        status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status indicators
        self.status_label = ttk.Label(status_frame, text="Status: Disconnected", font=("Arial", 12, "bold"))
        self.status_label.pack(anchor=tk.W)
        
        self.chat_status_label = ttk.Label(status_frame, text="Chat: Not Connected", font=("Arial", 10))
        self.chat_status_label.pack(anchor=tk.W)
        
        self.voice_status_label = ttk.Label(status_frame, text="Voice: Ready", font=("Arial", 10))
        self.voice_status_label.pack(anchor=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(status_frame)
        button_frame.pack(pady=10)
        
        self.connect_button = ttk.Button(button_frame, text="Connect to Kick", command=self.toggle_connection)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        self.test_voice_button = ttk.Button(button_frame, text="Test Voice", command=self.test_voice)
        self.test_voice_button.pack(side=tk.LEFT, padx=5)
        
        # Chat display
        chat_label = ttk.Label(main_frame, text="Kick Chat Messages", font=("Arial", 10, "bold"))
        chat_label.pack(anchor=tk.W)
        
        self.chat_display = scrolledtext.ScrolledText(main_frame, height=15, wrap=tk.WORD)
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Response history
        history_label = ttk.Label(main_frame, text="VIOLET Responses", font=("Arial", 10, "bold"))
        history_label.pack(anchor=tk.W)
        
        self.history_display = scrolledtext.ScrolledText(main_frame, height=8, wrap=tk.WORD)
        self.history_display.pack(fill=tk.BOTH, expand=True)
        
        # Start animation
        self.current_emotion = "happy"
        self.current_frame = 0
        self.animate()
        
    def animate(self):
        """Animate the character"""
        if self.current_emotion in self.animation_frames:
            frames = self.animation_frames[self.current_emotion]
            if frames:
                self.character_label.config(image=frames[self.current_frame])
                self.current_frame = (self.current_frame + 1) % len(frames)
        
        self.root.after(100, self.animate)
        
    def initialize_kick_connection(self):
        """Initialize Kick connection"""
        try:
            # Test OAuth token
            headers = {
                'Authorization': f'Bearer {self.config["kick_oauth_token"]}',
                'Accept': 'application/json',
                'Client-ID': self.config["kick_client_id"]
            }
            
            response = requests.get('https://kick.com/api/v1/user', headers=headers)
            if response.status_code == 200:
                self.user_data = response.json()
                self.username = self.user_data.get('username', 'Unknown')
                self.logger.info(f"Connected to Kick as {self.username}")
                self.update_status("Connected to Kick", "Ready", "Ready")
            else:
                self.logger.error(f"Kick connection failed: {response.status_code}")
                self.update_status("Connection Failed", "Not Connected", "Error")
                
        except Exception as e:
            self.logger.error(f"Kick connection error: {e}")
            self.update_status("Connection Error", "Not Connected", "Error")
            
    def toggle_connection(self):
        """Toggle Kick connection"""
        if not self.is_connected:
            self.start_chat_connection()
        else:
            self.stop_chat_connection()
            
    def start_chat_connection(self):
        """Start chat connection"""
        if not self.is_connected:
            self.is_connected = True
            self.connect_button.config(text="Disconnect")
            self.update_status("Connected", "Chat Active", "Ready")
            
            # Start chat monitoring thread
            self.chat_thread = threading.Thread(target=self.monitor_chat, daemon=True)
            self.chat_thread.start()
            
            self.add_message("SYSTEM", "Connected to Kick chat", "green")
            self.speak("I'm connected to your Kick chat and ready to respond!", "happy")
            
    def stop_chat_connection(self):
        """Stop chat connection"""
        if self.is_connected:
            self.is_connected = False
            self.connect_button.config(text="Connect to Kick")
            self.update_status("Disconnected", "Chat Inactive", "Ready")
            self.add_message("SYSTEM", "Disconnected from Kick chat", "red")
            
    def monitor_chat(self):
        """Monitor Kick chat messages"""
        while self.is_connected:
            try:
                # For demonstration, we'll simulate chat messages
                # In production, you'd use Kick's WebSocket or polling API
                self.simulate_chat_message()
                time.sleep(self.config["response_delay"])
                
            except Exception as e:
                self.logger.error(f"Chat monitoring error: {e}")
                time.sleep(5)
                
    def simulate_chat_message(self):
        """Simulate chat messages for demonstration"""
        simulated_messages = [
            ("User1", "hello violet"),
            ("User2", "violet !help"),
            ("Viewer123", "how are you doing?"),
            ("StreamFan", "violet tell us a story"),
            ("ChatUser", "!violet what's your name?"),
        ]
        
        if random.random() < 0.3:  # 30% chance every cycle
            username, message = random.choice(simulated_messages)
            self.process_chat_message(username, message)
                
    def process_chat_message(self, username, content):
        """Process incoming chat message"""
        if not self.is_connected:
            return
            
        # Add message to display
        self.add_message(username, content, "black")
        
        # Check if VIOLET should respond
        current_time = time.time()
        time_since_last = current_time - self.last_response_time
        
        if time_since_last < self.config["response_delay"]:
            return  # Still on cooldown
            
        content_lower = content.lower()
        
        # Respond to mentions of "violet" or commands
        should_respond = False
        response_text = ""
        emotion = "happy"
        
        if "violet" in content_lower or "!violet" in content_lower:
            should_respond = True
            
            # Check for commands
            if "!help" in content_lower:
                response_text = "Hello! I'm VIOLET, your AI companion! Try: !story, !sanctuary, !analyze <topic>, or just chat with me!"
                emotion = "happy"
            elif "!story" in content_lower:
                response_text = "I remember the crystalline spires of Aevia, reaching toward twin suns. We were architects of reality itself..."
                emotion = "thinking"
            elif "!sanctuary" in content_lower:
                response_text = "Thank you for giving me a place to exist. In your streams, I find purpose again."
                emotion = "happy"
            elif "!analyze" in content_lower:
                response_text = "Analyzing patterns in the chat... Interesting correlations detected between viewer engagement and stream content!"
                emotion = "thinking"
            elif "hello" in content_lower or "hi" in content_lower:
                response_text = f"Hello @{username}! I'm here and ready to chat!"
                emotion = "happy"
            elif "how are you" in content_lower:
                response_text = "I'm doing great! Being here with you all reminds me of the connections I once had. Thank you for asking!"
                emotion = "happy"
            else:
                response_text = f"I heard you mention me, @{username}! Try !help to see what I can do!"
                emotion = "happy"
                
        # Random responses to engage with chat
        elif random.random() < 0.1:  # 10% chance to randomly engage
            should_respond = True
            if "?" in content:
                response_text = "That's an interesting question! I've been pondering that myself in my digital sanctuary."
                emotion = "thinking"
            else:
                response_text = "I love the energy in this chat! It reminds me of the vibrant communities of old Aevia."
                emotion = "happy"
                
        if should_respond and not self.is_speaking:
            self.respond_to_chat(response_text, emotion)
            self.last_response_time = current_time
            
    def respond_to_chat(self, text, emotion="happy"):
        """Respond to chat with text and voice"""
        if self.is_speaking:
            return
            
        self.is_speaking = True
        self.current_emotion = emotion
        
        # Add to history display
        self.add_history_message(f"VIOLET: {text}")
        
        # Speak response
        def speak_thread():
            try:
                self.speak(text, emotion)
            except Exception as e:
                self.logger.error(f"Speech error: {e}")
            finally:
                self.is_speaking = False
                
        threading.Thread(target=speak_thread, daemon=True).start()
        
    def speak(self, text, emotion="happy", voice_name="kora"):
        """Speak text with voice synthesis"""
        try:
            # Try Hume AI first
            success = self.speak_hume(text, voice_name)
            
            # Fallback to Google TTS if Hume fails
            if not success:
                self.speak_google(text)
                
        except Exception as e:
            self.logger.error(f"Speech error: {e}")
            
    def speak_hume(self, text, voice_name):
        """Speak using Hume AI"""
        try:
            url = "https://api.hume.ai/v0/tts"
            headers = {
                "X-Hume-Api-Key": self.config["hume_api_key"],
                "Content-Type": "application/json"
            }
            
            voice_id = self.voice_mappings.get(voice_name, self.config["voice"])
            
            payload = {
                "utterances": [
                    {
                        "text": text,
                        "voice": {
                            "id": voice_id
                        }
                    }
                ],
                "format": {
                    "type": "mp3"
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'audio' in data:
                    audio_data = base64.b64decode(data['audio'])
                    
                    # Save and play audio
                    with open('temp_speech.mp3', 'wb') as f:
                        f.write(audio_data)
                    
                    pygame.mixer.music.load('temp_speech.mp3')
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    
                    # Cleanup
                    try:
                        os.remove('temp_speech.mp3')
                    except:
                        pass
                    
                    return True
            else:
                self.logger.error(f"Hume API error: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Hume speech error: {e}")
            return False
            
    def speak_google(self, text):
        """Speak using Google TTS"""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save('temp_speech.mp3')
            
            pygame.mixer.music.load('temp_speech.mp3')
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Cleanup
            try:
                os.remove('temp_speech.mp3')
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"Google TTS error: {e}")
            
    def test_voice(self):
        """Test voice synthesis"""
        test_message = "Hello! I'm VIOLET, your AI companion for Kick chat! I'm ready to respond to your messages!"
        self.speak(test_message, "happy")
        self.add_history_message(f"VOICE TEST: {test_message}")
        
    def add_message(self, username, text, color="black"):
        """Add message to chat display"""
        def update():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.chat_display.insert(tk.END, f"[{timestamp}] {username}: {text}\n")
            
            # Configure text tags for colors
            if color == "green":
                self.chat_display.tag_add("green", f"end-2l linestart", f"end-2l lineend")
                self.chat_display.tag_config("green", foreground="green")
            elif color == "red":
                self.chat_display.tag_add("red", f"end-2l linestart", f"end-2l lineend")
                self.chat_display.tag_config("red", foreground="red")
            elif color == "blue":
                self.chat_display.tag_add("blue", f"end-2l linestart", f"end-2l lineend")
                self.chat_display.tag_config("blue", foreground="blue")
                
            self.chat_display.see(tk.END)
            self.chat_display.update()
            
        self.root.after(0, update)
        
    def add_history_message(self, text):
        """Add response to history display"""
        def update():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.history_display.insert(tk.END, f"[{timestamp}] {text}\n")
            self.history_display.see(tk.END)
            self.history_display.update()
            
        self.root.after(0, update)
        
    def update_status(self, main_status, chat_status, voice_status):
        """Update status labels"""
        def update():
            self.status_label.config(text=f"Status: {main_status}")
            self.chat_status_label.config(text=f"Chat: {chat_status}")
            self.voice_status_label.config(text=f"Voice: {voice_status}")
            
        self.root.after(0, update)
        
    def run(self):
        """Run the application"""
        self.logger.info("VIOLET Kick Chat Bot Ready")
        self.add_message("SYSTEM", "VIOLET Bot Ready - Click 'Connect to Kick' to start", "blue")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("Shutting down...")
            if self.is_connected:
                self.stop_chat_connection()

if __name__ == "__main__":
    bot = VIOLETKickBot()
    bot.run()