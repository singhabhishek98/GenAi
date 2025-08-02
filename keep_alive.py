import requests
import time
import threading
import os
from datetime import datetime

class KeepAlive:
    def __init__(self, url=None):
        # Default URL, can be overridden
        self.url = url or os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:8080')
        self.running = False
        self.thread = None
        
    def ping(self):
        """Send a ping request to keep the app alive"""
        try:
            response = requests.get(f"{self.url}/", timeout=10)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Ping successful - Status: {response.status_code}")
            return True
        except Exception as e:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Ping failed: {str(e)}")
            return False
    
    def start_ping_service(self, interval=840):  # 14 minutes (just under 15 min timeout)
        """Start the ping service in a separate thread"""
        if self.running:
            print("Ping service is already running!")
            return
            
        print(f"Starting ping service for {self.url} with {interval}s interval")
        self.running = True
        
        def ping_loop():
            while self.running:
                time.sleep(interval)  # Wait first, then ping
                if self.running:  # Check again in case it was stopped during sleep
                    self.ping()
        
        self.thread = threading.Thread(target=ping_loop, daemon=True)
        self.thread.start()
        print("Ping service started successfully!")
    
    def stop_ping_service(self):
        """Stop the ping service"""
        if self.running:
            self.running = False
            print("Ping service stopped!")
        else:
            print("Ping service was not running!")

# Global instance
ping_service = KeepAlive()

def start_keep_alive(url=None, interval=840):
    """
    Start the keep-alive service
    Args:
        url: The URL to ping (optional, will use environment or localhost)
        interval: Ping interval in seconds (default 14 minutes)
    """
    if url:
        ping_service.url = url
    ping_service.start_ping_service(interval)

def stop_keep_alive():
    """Stop the keep-alive service"""
    ping_service.stop_ping_service()

if __name__ == "__main__":
    # For testing purposes
    import sys
    
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
        ping_service.url = test_url
    
    print("Testing ping service...")
    ping_service.ping()
    
    print("Starting continuous ping service...")
    ping_service.start_ping_service(60)  # 1 minute for testing
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping ping service...")
        ping_service.stop_ping_service()
        print("Ping service stopped. Goodbye!")
