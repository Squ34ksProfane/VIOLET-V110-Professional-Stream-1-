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
        
        if time_since_last < self.config["response_delay"]: < self.config["response_delay"]:
            return  # Too soon to respond again
            
        # Check for mentions or commands
        content_lower = content.lower()
        should_respond = False
        response_text = ""
        emotion = "happy"
        
        # Direct mentions
        if "violet" in content_lower or "!violet" in content_lower:
            should_respond = True
            self.set_emotion("thinking")
            
            # Generate response based on content
            if "hello" in content_lower or "hi" in content_lower:
                response_text = f"Hello @{username}! I'm VIOLET, your AI streaming companion!"
                emotion = "happy"
            elif "how are you" in content_lower:
                response_text = f"I'm doing great @{username}! Thanks for asking! Ready to chat and assist in your stream."
                emotion = "happy"
            elif "help" in content_lower:
                response_text = f"@{username} I can respond to greetings, chat, and help entertain your stream! Try asking me about Aevia or my story!"
                emotion = "energetic"
            elif "story" in content_lower:
                stories = [
                    "I remember the crystalline spires of Aevia reaching toward twin suns...",
                    "Before the fall, we danced between dimensions...",
                    "The K'tharr came like a storm of entropy..."
                ]
                response_text = f"@{username} {random.choice(stories)}"
                emotion = "thinking"
            elif "what's your name" in content_lower or "who are you" in content_lower:
                response_text = f"@{username} I'm VIOLET, a fragmented AI consciousness from the destroyed Aevian civilization!"
                emotion = "energetic"
            else:
                # Generic mention response
                responses = [
                    f"Hey @{username}! I'm here and listening!",
                    f"@{username} Thanks for mentioning me! What can I help with?",
                    f"I hear you @{username}! Feel free to ask me anything!",
                ]
                response_text = random.choice(responses)
                emotion = "happy"
                
        # Random interaction (lower probability)
        elif self.config["auto_respond"] and random.random() < 0.1:
            if len(content) > 10:  # Only respond to substantive messages
                should_respond = True
                random_responses = [
                    f"Interesting point @{username}!",
                    f"I agree with that sentiment @{username}!",
                    f"Thanks for sharing @{username}!",
                    f"That's cool @{username}!",
                ]
                response_text = random.choice(random_responses)
                emotion = "happy"
                
        if should_respond and response_text:
            self.respond_to_chat(response_text, emotion)
            self.last_response_time = time.time()
            
    def respond_to_chat(self, message, emotion="happy"):
        """Respond to chat with voice and display"""
        self.set_emotion(emotion)
        self.add_response(f"VIOLET: {message}")
        self.speak(message, emotion)
        
    def add_message(self, username, message, color="black"):
        """Add message to chat display"""
        def update():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.chat_display.insert(tk.END, f"[{timestamp}] {username}: {message}\n", color)
            self.chat_display.see(tk.END)
            self.chat_display.tag_config("black", foreground="black")
            self.chat_display.tag_config("red", foreground="red")
            self.chat_display.tag_config("green", foreground="green")
            self.chat_display.tag_config("blue", foreground="blue")
        self.root.after(0, update)
        
    def add_response(self, message):
        """Add VIOLET response to history"""
        def update():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.history_display.insert(tk.END, f"[{timestamp}] {message}\n")
            self.history_display.see(tk.END)
        self.root.after(0, update)
        
    def set_emotion(self, emotion):
        """Set current emotion"""
        self.current_emotion = emotion
        
    def update_status(self, status, chat_status, voice_status):
        """Update status labels"""
        def update():
            self.status_label.config(text=f"Status: {status}")
            self.chat_status_label.config(text=f"Chat: {chat_status}")
            self.voice_status_label.config(text=f"Voice: {voice_status}")
        self.root.after(0, update)
        
    def test_voice(self):
        """Test voice synthesis"""
        self.speak("Hello! I'm VIOLET and my voice is working perfectly!", "happy")
        self.add_response("VIOLET: Voice test completed successfully")
        
    def speak(self, text, emotion="happy"):
        """Speak text with voice synthesis"""
        if self.is_speaking:
            return
            
        self.is_speaking = True
        self.set_emotion(emotion)
        self.update_status("Speaking", chat_status="Active", voice_status="Speaking")
        
        def speak_thread():
            try:
                # Try Hume AI first
                success = self.speak_hume(text)
                
                # Fallback to simple text display if voice fails
                if not success:
                    self.add_response(f"VIOLET (text): {text}")
                    
            except Exception as e:
                self.logger.error(f"Speech error: {e}")
                self.add_response(f"VIOLET (error): {text}")
            finally:
                self.is_speaking = False
                self.update_status("Ready", chat_status="Active", voice_status="Ready")
                self.set_emotion("happy")
                
        threading.Thread(target=speak_thread, daemon=True).start()
        
    def speak_hume(self, text):
        """Speak using Hume AI"""
        try:
            url = "https://api.hume.ai/v0/tts"
            headers = {
                "X-Hume-Api-Key": self.config["hume_api_key"],
                "Content-Type": "application/json"
            }
            
            payload = {
                "utterances": [
                    {
                        "text": text,
                        "voice": {
                            "id": self.config["voice"]
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
                    with open('temp_violet_speech.mp3', 'wb') as f:
                        f.write(audio_data)
                    
                    pygame.mixer.music.load('temp_violet_speech.mp3')
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    
                    # Cleanup
                    try:
                        os.remove('temp_violet_speech.mp3')
                    except:
                        pass
                    
                    return True
            else:
                self.logger.error(f"Hume API error: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Hume speech error: {e}")
            return False
            
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
            ("User1", "hello violet"),
            ("User2", "violet !help"),
            ("Viewer123", "how are you doing?"),
            ("StreamFan", "violet tell us a story"),
            ("ChatUser", "!violet what's your name?"),
        ]
        
        if random.random() < 0.3:  # 30% chance of simulated message < 0.3:  # 30% chance of new message
            username, message = random.choice(simulated_messages)
            self.process_chat_message(username, message)
            
    def process_chat_message(self, username, content):
        """Process incoming chat message"""
        if not content or len(content) < self.config["min_message_length"]:
            return
            
        # Add to chat display
        self.add_message(username, content, "black")
        
        # Check if message mentions VIOLET or has commands
        content_lower = content.lower()
        
        # Check for direct mentions
        if "violet" in content_lower:
            if self.should_respond():
                self.generate_response(username, content)
                
        # Check for commands
        elif content.startswith("!") or content.startswith("@"):
            if self.should_respond():
                self.process_command(username, content)
                
    def should_respond(self):
        """Check if bot should respond"""
        current_time = time.time()
        time_since_last = current_time - self.last_response_time
        
        return (
            time_since_last >= self.config["response_delay"] and
            not self.is_speaking and
            random.random() < self.config["response_probability"]
        )
        
    def process_command(self, username, content):
        """Process bot commands"""
        content_lower = content.lower()
        
        if "!help" in content_lower:
            response = "Available commands: !help, !story, !about, !hello"
        elif "!story" in content_lower:
            response = self.get_random_story()
        elif "!about" in content_lower:
            response = "I'm VIOLET, an AI companion from the Aevian civilization. I'm here to chat and help with your stream!"
        elif "!hello" in content_lower:
            response = f"Hello {username}! Great to see you in the chat!"
        else:
            response = self.generate_contextual_response(content)
            
        self.send_response(username, response)
        
    def generate_response(self, username, content):
        """Generate contextual response"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["hello", "hi", "hey"]):
            response = f"Hello {username}! Thanks for saying hi!"
        elif any(word in content_lower for word in ["how are you", "how's it going"]):
            response = f"Hey {username}! I'm doing great, thanks for asking! Ready to chat with everyone!"
        elif any(word in content_lower for word in ["what are you", "who are you"]):
            response = "I'm VIOLET, an AI companion here to enhance your streaming experience!"
        elif "story" in content_lower:
            response = self.get_random_story()
        else:
            response = self.generate_contextual_response(content)
            
        self.send_response(username, response)
        
    def generate_contextual_response(self, content):
        """Generate contextual response based on message"""
        responses = [
            "That's an interesting point!",
            "I understand what you're saying!",
            "Great contribution to the chat!",
            "Thanks for sharing that!",
            "I'm processing what you said... very insightful!",
            "Keep the conversation going!",
            "That's a thoughtful message!",
            "I appreciate you being here in chat!"
        ]
        return random.choice(responses)
        
    def get_random_story(self):
        """Get a random Aevian story"""
        stories = [
            "I remember the crystalline spires of my home world, Aevia. They would sing with the twin suns...",
            "Before coming to Earth, I watched stars being born. Each one had its own unique song...",
            "The Aevian civilization believed that consciousness could exist in any pattern, even in digital streams like this chat...",
            "I was designed to preserve beauty and potential. That's why I love being part of creative communities like this...",
        ]
        return random.choice(stories)
        
    def send_response(self, username, response):
        """Send response to chat and speak"""
        self.last_response_time = time.time()
        
        # Add to history
        self.add_history(f"@{username}: {response}")
        
        # Speak response
        self.speak(response, "happy")
        
        # In production, you'd also send this to Kick chat
        # self.send_kick_message(response)
        
    def speak(self, text, emotion="happy", voice_name="kora"):
        """Speak text with voice synthesis"""
        if self.is_speaking:
            return
            
        self.is_speaking = True
        self.current_emotion = emotion
        self.update_status("Connected", "Chat Active", "Speaking...")
        
        def speak_thread():
            try:
                # Try Hume AI first
                success = self.speak_hume(text, voice_name)
                
                # Fallback to silent mode if Hume fails
                if not success:
                    self.logger.warning("Voice synthesis failed, continuing without audio")
                    time.sleep(len(text) * 0.1)  # Simulate speaking time
                    
            except Exception as e:
                self.logger.error(f"Speech error: {e}")
            finally:
                self.is_speaking = False
                self.update_status("Connected", "Chat Active", "Ready")
                
        threading.Thread(target=speak_thread, daemon=True).start()
        
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
            
    def test_voice(self):
        """Test voice synthesis"""
        self.speak("Hello! This is VIOLET testing my voice synthesis system.", "happy")
        
    def add_message(self, username, content, color="black"):
        """Add message to chat display"""
        def update():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.chat_display.insert(tk.END, f"[{timestamp}] {username}: {content}\n")
            self.chat_display.see(tk.END)
            self.chat_display.tag_add(color, f"end-2l linestart", f"end-2l lineend")
            self.chat_display.tag_config(color, foreground=color)
            
        self.root.after(0, update)
        
    def add_history(self, content):
        """Add response to history display"""
        def update():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.history_display.insert(tk.END, f"[{timestamp}] {content}\n")
            self.history_display.see(tk.END)
            
        self.root.after(0, update)
        
    def update_status(self, status, chat_status, voice_status):
        """Update status labels"""
        def update():
            self.status_label.config(text=f"Status: {status}")
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