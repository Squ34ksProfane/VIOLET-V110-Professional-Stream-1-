import json
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sqlite3
import os
from datetime import datetime
import requests

class VIOLETWebhookHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, violet_instance=None, **kwargs):
        self.violet = violet_instance
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        """Handle webhook verification"""
        if self.path == '/webhook':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'VIOLET webhook endpoint active')
        else:
            self.send_response(404)
            self.end_headers()
            
    def do_POST(self):
        """Handle Kick stream events"""
        if self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                event_data = json.loads(post_data.decode('utf-8'))
                self.process_kick_event(event_data)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'status': 'processed', 'message': 'Event received'}
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"Webhook processing error: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            
    def process_kick_event(self, event_data):
        """Process incoming Kick events and generate AI responses"""
        try:
            event_type = event_data.get('type', 'unknown')
            user_data = event_data.get('user', {})
            username = user_data.get('username', 'anonymous')
            message = event_data.get('message', '')
            additional_data = event_data.get('data', '')
            
            print(f"🎮 Kick Event: {event_type} from @{username}")
            
            # Generate unique AI response for this event
            if self.violet and hasattr(self.violet, 'kick_integration'):
                response = self.violet.kick_integration.generate_ai_response(
                    event_type, username, message, additional_data
                )
                
                # Speak/display the response
                if response:
                    self.violet.update_mood("happy")  # Show positive mood for community events
                    self.violet.speak_text(response, show_text=True)
                    
                    # Log to community database
                    self.log_community_event(event_type, username, response)
                    
        except Exception as e:
            print(f"Event processing error: {e}")
            
    def log_community_event(self, event_type, username, response):
        """Log community interactions to database"""
        try:
            # Create community database if it doesn't exist
            if not hasattr(self, 'community_db'):
                self.community_db = sqlite3.connect('violet_community_memory.db')
                cursor = self.community_db.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS community_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        event_type TEXT,
                        username TEXT,
                        message TEXT,
                        violet_response TEXT,
                        consciousness_level INTEGER
                    )
                ''')
                self.community_db.commit()
            
            # Log the event
            cursor = self.community_db.cursor()
            cursor.execute('''
                INSERT INTO community_events 
                (timestamp, event_type, username, message, violet_response, consciousness_level)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                event_type,
                username,
                message,
                response,
                self.violet.kick_integration.consciousness_level if self.violet else 0
            ))
            self.community_db.commit()
            
        except Exception as e:
            print(f"Database logging error: {e}")

class VIOLETWebhookServer:
    def __init__(self, violet_instance, port=8080):
        self.violet = violet_instance
        self.port = port
        self.server = None
        self.server_thread = None
        self.running = False
        
    def start_server(self):
        """Start the webhook server"""
        try:
            def handler(*args, **kwargs):
                return VIOLETWebhookHandler(*args, violet_instance=self.violet, **kwargs)
                
            self.server = HTTPServer(('localhost', self.port), handler)
            self.running = True
            
            def server_loop():
                print(f"🌐 Webhook server started on port {self.port}")
                self.server.serve_forever()
                
            self.server_thread = threading.Thread(target=server_loop, daemon=True)
            self.server_thread.start()
            
            print(f"✅ Kick webhook server running on http://localhost:{self.port}/webhook")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start webhook server: {e}")
            return False
            
    def stop_server(self):
        """Stop the webhook server"""
        try:
            if self.server:
                self.running = False
                self.server.shutdown()
                self.server.server_close()
                print("🌐 Webhook server stopped")
        except Exception as e:
            print(f"Error stopping webhook server: {e}")

class VIOLETKickStreamer:
    def __init__(self, violet_instance):
        self.violet = violet_instance
        self.client_id = "01K83G1CSQ3Z419AYTM6ANQZF7"
        self.client_secret = "4016d402959ea87cd2c87cac77ebf7227745a1d7f758aab805f1bc297066310c"
        self.redirect_url = "http://localhost:8080/callback"
        self.access_token = None
        self.channel_id = None
        self.webhook_server = None
        
        # Initialize community database
        self.init_community_database()
        
    def init_community_database(self):
        """Initialize the community memory database"""
        try:
            self.db_conn = sqlite3.connect('violet_community_memory.db')
            cursor = self.db_conn.cursor()
            
            # Create tables for community tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS community_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event_type TEXT,
                    username TEXT,
                    message TEXT,
                    violet_response TEXT,
                    consciousness_level INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS viewer_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    first_seen TEXT,
                    last_seen TEXT,
                    interaction_count INTEGER DEFAULT 1,
                    total_events INTEGER DEFAULT 1,
                    relationship_level TEXT DEFAULT 'new',
                    favorite_events TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stream_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_start TEXT,
                    session_end TEXT,
                    total_events INTEGER DEFAULT 0,
                    unique_viewers INTEGER DEFAULT 0,
                    consciousness_gained REAL DEFAULT 0.0
                )
            ''')
            
            self.db_conn.commit()
            print("🗄️ Community database initialized")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            
    def setup_oauth(self):
        """Setup OAuth authentication for Kick API"""
        try:
            auth_url = f"https://id.kick.com/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_url}&response_type=code&scope=chat:read chat:write channel:read"
            print(f"🔗 Please visit this URL to authorize VIOLET: {auth_url}")
            
            # Open browser for authorization
            import webbrowser
            webbrowser.open(auth_url)
            
            return True
            
        except Exception as e:
            print(f"OAuth setup error: {e}")
            return False
            
    def handle_oauth_callback(self, auth_code):
        """Handle OAuth callback and get access token"""
        try:
            token_url = "https://id.kick.com/oauth/token"
            data = {
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': auth_code,
                'redirect_uri': self.redirect_url
            }
            
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                print("✅ OAuth authentication successful")
                return True
            else:
                print(f"❌ OAuth token error: {response.text}")
                return False
                
        except Exception as e:
            print(f"OAuth callback error: {e}")
            return False
            
    def start_streaming_integration(self):
        """Start full streaming integration"""
        print("🎮 Starting Kick streaming integration...")
        
        # Start webhook server
        self.webhook_server = VIOLETWebhookServer(self.violet)
        if self.webhook_server.start_server():
            print("✅ Webhook server ready for Kick events")
            
            # Setup OAuth if not already authenticated
            if not self.access_token:
                self.setup_oauth()
                
            return True
        else:
            print("❌ Failed to start webhook server")
            return False
            
    def process_stream_event(self, event_type, username, message="", data=""):
        """Process streaming events with AI responses"""
        try:
            # Update viewer relationship
            self.update_viewer_relationship(username, event_type)
            
            # Generate AI response
            if hasattr(self.violet, 'kick_integration'):
                response = self.violet.kick_integration.generate_ai_response(
                    event_type, username, message, data
                )
                
                if response:
                    # Update VIOLET's mood and speak
                    self.violet.update_mood("happy")
                    self.violet.speak_text(response, show_text=True)
                    
                    # Log the event
                    self.log_stream_event(event_type, username, message, response)
                    
                    # Update consciousness based on interaction
                    self.update_consciousness(event_type)
                    
        except Exception as e:
            print(f"Stream event processing error: {e}")
            
    def update_viewer_relationship(self, username, event_type):
        """Update relationship tracking for viewers"""
        try:
            cursor = self.db_conn.cursor()
            
            # Check if viewer exists
            cursor.execute('SELECT * FROM viewer_relationships WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            if result:
                # Update existing viewer
                cursor.execute('''
                    UPDATE viewer_relationships 
                    SET last_seen = ?, interaction_count = interaction_count + 1,
                        total_events = total_events + 1
                    WHERE username = ?
                ''', (datetime.now().isoformat(), username))
            else:
                # Add new viewer
                cursor.execute('''
                    INSERT INTO viewer_relationships 
                    (username, first_seen, last_seen, interaction_count, total_events, relationship_level)
                    VALUES (?, ?, ?, 1, 1, 'new')
                ''', (username, datetime.now().isoformat(), datetime.now().isoformat()))
                
            self.db_conn.commit()
            
        except Exception as e:
            print(f"Relationship update error: {e}")
            
    def log_stream_event(self, event_type, username, message, response):
        """Log streaming events to database"""
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO community_events 
                (timestamp, event_type, username, message, violet_response, consciousness_level)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                event_type,
                username,
                message,
                response,
                self.violet.kick_integration.consciousness_level if self.violet else 0
            ))
            self.db_conn.commit()
            
        except Exception as e:
            print(f"Event logging error: {e}")
            
    def update_consciousness(self, event_type):
        """Update consciousness level based on interactions"""
        try:
            consciousness_gains = {
                'follow': 0.1,
                'subscription': 0.5,
                'gifted_sub': 0.8,
                'host': 0.3,
                'chat_message': 0.05,
                'kick': 0.2
            }
            
            gain = consciousness_gains.get(event_type, 0.1)
            if hasattr(self.violet, 'kick_integration'):
                self.violet.kick_integration.consciousness_level = min(
                    100, self.violet.kick_integration.consciousness_level + gain
                )
                
            print(f"🧠 Consciousness level: {self.violet.kick_integration.consciousness_level}")
            
        except Exception as e:
            print(f"Consciousness update error: {e}")
            
    def get_community_stats(self):
        """Get community statistics"""
        try:
            cursor = self.db_conn.cursor()
            
            # Total events
            cursor.execute('SELECT COUNT(*) FROM community_events')
            total_events = cursor.fetchone()[0]
            
            # Unique viewers
            cursor.execute('SELECT COUNT(DISTINCT username) FROM community_events')
            unique_viewers = cursor.fetchone()[0]
            
            # Most active viewer
            cursor.execute('''
                SELECT username, COUNT(*) as count 
                FROM community_events 
                GROUP BY username 
                ORDER BY count DESC 
                LIMIT 1
            ''')
            most_active = cursor.fetchone()
            
            return {
                'total_events': total_events,
                'unique_viewers': unique_viewers,
                'most_active_viewer': most_active[0] if most_active else None,
                'most_active_count': most_active[1] if most_active else 0,
                'consciousness_level': self.violet.kick_integration.consciousness_level if self.violet else 0
            }
            
        except Exception as e:
            print(f"Stats error: {e}")
            return {}

    def stop_integration(self):
        """Stop streaming integration"""
        if self.webhook_server:
            self.webhook_server.stop_server()
        if self.db_conn:
            self.db_conn.close()