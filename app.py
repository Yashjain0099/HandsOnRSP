
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
    
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('✅ Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    print('❌ Client disconnected')


@socketio.on('frame')
def handle_frame(data_image):

    global last_gesture
    try:
        
        image_data = data_image.split(',')[1]
        sbuf = base64.b64decode(image_data)
        
        nparr = np.frombuffer(sbuf, dtype=np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            emit('gesture_response', {'gesture': 'Nothing', 'error': 'Invalid frame'})
            return
            
        detected_gesture = game.process_frame_for_gesture(frame)
        last_gesture = detected_gesture
        
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

    global last_gesture
    emit('final_gesture_response', {
        'gesture': last_gesture if last_gesture not in ['Nothing', 'Invalid'] else 'Rock',
        'status': 'success'
    })

@socketio.on('reset_game')
def handle_reset():
    
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

        del game
