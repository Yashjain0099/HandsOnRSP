"""
Flask Web Server for Rock Paper Scissors Game
Connects the beautiful HTML UI with your CV2 gesture detection logic
"""

import cv2
import base64
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from RockPaperScissorGame import RockPaperScissorsGame

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'rock-paper-scissors-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Create game instance
game = RockPaperScissorsGame()

# Store the last detected gesture during countdown
last_gesture = "Nothing"

print("=" * 70)
print("🎮 ROCK PAPER SCISSORS - Server Starting...")
print("=" * 70)
print("✅ Game instance created")
print("✅ MediaPipe initialized with your original logic")
print("=" * 70)


@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('✅ Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('❌ Client disconnected')


@socketio.on('frame')
def handle_frame(data_image):
    """
    Receive frame from browser, process it, and send back the detected gesture
    """
    global last_gesture
    try:
        # Decode the base64 image from the browser
        image_data = data_image.split(',')[1]
        sbuf = base64.b64decode(image_data)
        
        # Convert to numpy array
        nparr = np.frombuffer(sbuf, dtype=np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            emit('gesture_response', {'gesture': 'Nothing', 'error': 'Invalid frame'})
            return
        
        # Process the frame using YOUR original gesture detection logic
        detected_gesture = game.process_frame_for_gesture(frame)
        last_gesture = detected_gesture
        
        # Send the detected gesture back to the client
        emit('gesture_response', {
            'gesture': detected_gesture,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"❌ Error processing frame: {e}")
        emit('gesture_response', {
            'gesture': 'Nothing',
            'error': str(e)
        })


@socketio.on('get_final_gesture')
def handle_get_final_gesture():
    """Get the final gesture when countdown ends"""
    global last_gesture
    emit('final_gesture_response', {
        'gesture': last_gesture if last_gesture not in ['Nothing', 'Invalid'] else 'Rock',
        'status': 'success'
    })


@socketio.on('reset_game')
def handle_reset():
    """Reset the game state"""
    global last_gesture
    last_gesture = "Nothing"
    game.reset_game()
    emit('reset_response', {'status': 'success'})


if __name__ == '__main__':
    print("\n🌐 Starting Flask-SocketIO server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\n💡 Features:")
    print("   • Real-time hand gesture detection")
    print("   • Countdown timer for simultaneous reveal")
    print("   • Your original CV2 finger counting logic")
    print("   • Beautiful modern web interface")
    print("\n⌨️  Press Ctrl+C to stop the server")
    print("=" * 70)
    
    try:
        # Run the server
        socketio.run(
            app,
            host='0.0.0.0',
            port=5000,
            debug=True,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    finally:
        # Cleanup
        del game