"""
VIOLET - AI Chat Bot for Kick.com
Fully integrated bot that connects directly to REAL Kick chat
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
        self.root.title("VIOLET - Kick Chat Bot (REAL CONNECTION)")
        self.root.geometry("800x600")
        
        # Bot state
        self.is_connected = False
        self.is_speaking = False
        self.last_response_time = 0
        self.chat_messages = []
        self.commands_history = []
        self.channel_data = None
        self.chatroom_id = None
        self.last_message_id = None
        
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
        
        self.channel_label = ttk.Label(status_frame, text="Channel: Unknown", font=("Arial", 10))
        self.channel_label.pack(anchor=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(status_frame)
        button_frame.pack(pady=10)
        
        self.connect_button = ttk.Button(button_frame, text="Connect to Kick", command=self.toggle_connection)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        self.test_voice_button = ttk.Button(button_frame, text="Test Voice", command=self.test_voice)
        self.test_voice_button.pack(side=tk.LEFT, padx=5)
        
        # Chat display
        chat_label = ttk.Label(main_frame, text="REAL Kick Chat Messages", font=("Arial", 10, "bold"))
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
                self.update_status("Connected to Kick", "Ready", "Ready", f"Channel: {self.username}")
            else:
                self.logger.error(f"Kick connection failed: {response.status_code}")
                self.update_status("Connection Failed", "Not Connected", "Error", "Channel: Unknown")
                
        except Exception as e:
            self.logger.error(f"Kick connection error: {e}")
            self.update_status("Connection Error", "Not Connected", "Error", "Channel: Unknown")
            
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
            
            # Get channel info
            self.get_channel_info()
            
            self.update_status("Connected", "Chat Active", "Ready", f"Channel: {self.username}")
            
            # Start chat monitoring thread
            self.chat_thread = threading.Thread(target=self.monitor_real_chat, daemon=True)
            self.chat_thread.start()
            
            self.add_message("SYSTEM", f"Connected to REAL chat for {self.username}", "green")
            self.speak("I'm connected to your REAL Kick chat and ready to respond!", "happy")
            
    def stop_chat_connection(self):
        """Stop chat connection"""
        if self.is_connected:
            self.is_connected = False
            self.connect_button.config(text="Connect to Kick")
            self.update_status("Disconnected", "Chat Inactive", "Ready", f"Channel: {self.username}")
            self.add_message("SYSTEM", f"Disconnected from REAL chat for {self.username}", "red")
            
    def get_channel_info(self):
        """Get channel information and chatroom ID"""
        try:
            headers = {
                'Authorization': f'Bearer {self.config["kick_oauth_token"]}',
                'Accept': 'application/json',
                'Client-ID': self.config["kick_client_id"]
            }
            
            # Get channel info
            response = requests.get(f'https://kick.com/api/v1/channels/{self.username}', headers=headers)
            
            if response.status_code == 200:
                self.channel_data = response.json()
                self.chatroom_id = self.channel_data.get('chatroom', {}).get('id')
                
                if self.chatroom_id:
                    self.logger.info(f"Chatroom ID: {self.chatroom_id}")
                    self.add_message("SYSTEM", f"Chatroom ID: {self.chatroom_id}", "blue")
                else:
                    self.logger.error("No chatroom ID found")
                    self.add_message("SYSTEM", "ERROR: No chatroom found - you may not be streaming", "red")
            else:
                self.logger.error(f"Channel API error: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Channel info error: {e}")
            
    def monitor_real_chat(self):
        """Monitor REAL Kick chat messages"""
        while self.is_connected:
            try:
                if self.chatroom_id:
                    self.get_real_chat_messages()
                    
                time.sleep(self.config["response_delay"])
                
            except Exception as e:
                self.logger.error(f"Chat monitoring error: {e}")
                time.sleep(5)
                
    def get_real_chat_messages(self):
        """Get REAL chat messages from Kick API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.config["kick_oauth_token"]}',
                'Accept': 'application/json',
                'Client-ID': self.config["kick_client_id"]
            }
            
            # Get chat messages from the chatroom
            url = f'https://kick.com/api/v1/channels/{self.username}/chat'
            
            params = {}
            if self.last_message_id:
                params['after'] = self.last_message_id
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                messages = data.get('data', [])
                
                # Process new messages
                for message in messages:
                    self.process_real_chat_message(message)
                    
            elif response.status_code == 403:
                self.add_message("SYSTEM", "ERROR: Cannot access chat - permissions issue", "red")
                
        except Exception as e:
            self.logger.error(f"Get chat messages error: {e}")
            
    def process_real_chat_message(self, message):
        """Process REAL chat message"""
        try:
            username = message.get('user', {}).get('username', 'Unknown')
            content = message.get('content', '').strip()
            message_id = message.get('id')
            
            if not content or len(content)