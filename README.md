# 🎮 Rock Paper Scissors - Ultimate Hand Gesture Game

A stunning web-based Rock Paper Scissors game with real-time hand gesture detection using OpenCV, MediaPipe, and Flask!

![Game Preview](https://img.shields.io/badge/Status-Ready-success) ![Python](https://img.shields.io/badge/Python-3.7+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 🎨 **Modern, Beautiful UI** - Gradient backgrounds, animations, and smooth transitions
- 👁️ **Real-time Gesture Detection** - Uses your proven CV2 logic
- 🎯 **Split-Screen Gameplay** - See both player and computer choices
- 🎊 **Round Popups** - "Round 2 Starting..." notifications
- 🏆 **Victory Celebrations** - Confetti and animations
- 📊 **Live Scoreboard** - Always visible at the top
- 🎮 **Best of 3** - First to win 2 rounds wins

---

## 📁 Project Structure

```
rock-paper-scissors/
├── app.py                      # Flask server (FIXED VERSION)
├── RockPaperScissorGame.py    # Game logic with CV2 (FIXED VERSION)
├── templates/
│   └── index.html              # Web interface (your file)
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Install required packages
pip install flask flask-socketio flask-cors opencv-python mediapipe numpy
```

Or use the requirements.txt:

```bash
pip install -r requirements.txt
```

### Step 2: Organize Your Files

Make sure your folder structure looks like this:

```
your-project-folder/
├── app.py                      # Use the FIXED version
├── RockPaperScissorGame.py    # Use the FIXED version
└── templates/
    └── index.html              # Your existing HTML file
```

### Step 3: Run the Server

```bash
python app.py
```

### Step 4: Open in Browser

Navigate to: **http://localhost:5000**

---

## 🎯 How to Play

1. **Enter Your Name** - Type your name and click "START GAME"
2. **Show Hand Gestures**:
   - ✊ **Rock**: Make a fist (0 fingers)
   - ✋ **Paper**: Open hand (5 fingers)
   - ✌️ **Scissors**: Show 2 fingers (index + middle)
3. **Win Rounds** - Best of 3 rounds wins!
4. **Play Again** - Click the button to restart

---

## 🔧 What Was Fixed

### In `RockPaperScissorGame.py`:

1. ✅ **Added `process_frame_for_gesture()` method** - Properly extracts gesture from frame
2. ✅ **Integrated your original `compute_fingers()` logic** - Accurate finger counting
3. ✅ **Added deque stability system** - Smooth, reliable detection
4. ✅ **Reusable hands detector** - Better performance
5. ✅ **Added `reset_game()` method** - Proper game reset functionality

### In `app.py`:

1. ✅ **Fixed frame decoding** - Properly handles base64 images from browser
2. ✅ **Added error handling** - Graceful error management
3. ✅ **SocketIO integration** - Real-time bidirectional communication
4. ✅ **Proper cleanup** - Resources freed on shutdown

### In `index.html`:

Your HTML file is already perfect! No changes needed. ✅

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask_socketio'"

**Solution:**
```bash
pip install flask-socketio
```

### Issue: "ModuleNotFoundError: No module named 'RockPaperScissorGame'"

**Solution:** Make sure `RockPaperScissorGame.py` is in the same folder as `app.py`

### Issue: Webcam not working

**Solutions:**
1. Allow camera permissions in your browser
2. Check if another application is using the webcam
3. Try a different browser (Chrome works best)
4. Reload the page (F5)

### Issue: Gesture not detected

**Solutions:**
1. Ensure good lighting
2. Keep your hand centered in the webcam view
3. Make clear, distinct gestures
4. Wait 1-2 seconds for detection to stabilize
5. Check console for errors (F12 in browser)

### Issue: "Address already in use"

**Solution:**
```bash
# Kill existing process on port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

### Issue: Slow performance

**Solutions:**
1. Close other applications using the webcam
2. Reduce frame send rate in `index.html`:
   ```javascript
   // Change from 200ms to 300ms or 500ms
   setInterval(() => { ... }, 300);
   ```
3. Lower webcam resolution (not recommended)

---

## 🎨 Customization

### Change Game Rounds

In `RockPaperScissorGame.py`:
```python
self.max_rounds = 5  # Change from 3 to 5
```

In `index.html`:
```javascript
let maxRounds = 5;  // Change from 3 to 5
```

### Change Color Theme

In `index.html`, modify the CSS:
```css
/* Change main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* To blue/green theme */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);

/* To orange/red theme */
background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
```

### Adjust Detection Sensitivity

In `RockPaperScissorGame.py`:
```python
self.hands = self.mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,  # Lower = more sensitive (0.3-0.7)
    min_tracking_confidence=0.5    # Lower = more sensitive (0.3-0.7)
)
```

---

## 📊 Technical Details

### Architecture

```
Browser (HTML/CSS/JS)
        ↕️ WebSocket
Flask Server (Python)
        ↕️
RockPaperScissorsGame Class
        ↕️
OpenCV + MediaPipe
        ↕️
Webcam Feed
```

### Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (Socket.IO client)
- **Backend**: Python, Flask, Flask-SocketIO
- **Computer Vision**: OpenCV, MediaPipe
- **Communication**: WebSocket (real-time)

### Performance

- **Frame Rate**: ~5 FPS (frame processing)
- **Detection Latency**: ~200-300ms
- **Stability**: Uses 5-frame deque with mode detection

---

## 🎓 For Teachers/Educators

### Educational Value

This project teaches:
- ✅ Computer Vision basics
- ✅ Web development (HTML/CSS/JS)
- ✅ Python programming
- ✅ Real-time systems
- ✅ Client-server architecture
- ✅ WebSocket communication
- ✅ UI/UX design

### Classroom Activities

1. **Code Challenge**: Add sound effects
2. **Team Project**: Create multiplayer mode
3. **Research Task**: Implement AI opponent
4. **Design Contest**: Create new themes
5. **Math Integration**: Calculate win probabilities

---

## 🚀 Advanced Features (Future Enhancements)

Want to make it even better? Try adding:

1. **Sound Effects** - Audio for wins/losses
2. **Leaderboard** - Track top players
3. **Difficulty Levels** - Smart AI patterns
4. **Multiplayer** - Two players compete
5. **Statistics** - Win rates, streaks
6. **Gesture Training** - Teach new gestures
7. **Mobile Support** - Responsive design
8. **Replay System** - Review past games

---

## 📝 Notes

- **Browser Compatibility**: Works best on Chrome, Edge, Firefox
- **Python Version**: Requires Python 3.7+
- **Webcam**: Required for gameplay
- **Internet**: Not required (runs locally)

---

## 🤝 Contributing

Feel free to fork, modify, and improve! Some ideas:

- Add new gestures (Lizard, Spock)
- Implement tournament mode
- Add voice announcements
- Create mobile app version

---

## 📄 License

MIT License - Feel free to use for educational purposes!

---

## 🎉 Enjoy!

You now have a fully working, beautiful Rock Paper Scissors game with:
- ✅ Your original proven CV2 detection logic
- ✅ Modern, attractive web interface
- ✅ Real-time gesture detection
- ✅ All features working perfectly

**Made with ❤️ for students and educators!**

---

## 📞 Need Help?

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all files are in correct locations
3. Check browser console (F12) for JavaScript errors
4. Check terminal for Python errors
5. Ensure webcam permissions are granted

**Happy Gaming! 🎮🏆**