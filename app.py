from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from post_generator import generate_post
from few_shot import FewShotPosts
from keep_alive import start_keep_alive
import os

app = Flask(__name__)
CORS(app)

# Initialize few shot posts to get tags
fs = FewShotPosts()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tags', methods=['GET'])
def get_tags():
    try:
        print("Loading tags...")
        tags = fs.get_tags()
        print(f"Tags loaded: {len(tags) if tags else 0} tags")
        print(f"First few tags: {tags[:5] if tags else 'None'}")
        return jsonify({'success': True, 'tags': tags})
    except Exception as e:
        print(f"Error loading tags: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_linkedin_post():
    try:
        data = request.json
        length = data.get('length')
        language = data.get('language')
        tag = data.get('tag')
        include_emojis = data.get('include_emojis', True)
        
        if not all([length, language, tag]):
            return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
        
        post = generate_post(length, language, tag, include_emojis)
        return jsonify({'success': True, 'post': post})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Start keep-alive service for free hosting platforms
if os.environ.get('RENDER_SERVICE_NAME') or os.environ.get('RAILWAY_ENVIRONMENT'):
    # Only start ping service on production hosting platforms
    import threading
    def start_ping_delayed():
        import time
        time.sleep(30)  # Wait 30 seconds for app to fully start
        render_url = os.environ.get('RENDER_EXTERNAL_URL')
        if render_url:
            start_keep_alive(render_url)
        else:
            start_keep_alive()
    
    threading.Thread(target=start_ping_delayed, daemon=True).start()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
