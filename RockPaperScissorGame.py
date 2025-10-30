import cv2
import mediapipe as mp
import random
from collections import deque
import statistics as st
import numpy as np
import time


class RockPaperScissorsGame:
    def __init__(self):
        # Mediapipe setup
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        
        # Initialize hands detector (reusable instance)
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Game variables
        self.player_name = ""
        self.cpu_score = 0
        self.player_score = 0
        self.round_number = 0
        self.max_rounds = 3
        
        self.cpu_choice = "Nothing"
        self.player_choice = "Nothing"
        self.winner = "None"
        self.winner_colour = (0, 255, 0)
        self.hand_valid = False
        
        self.cpu_choices = ["Rock", "Paper", "Scissors"]
        self.display_values = ["Rock", "Invalid", "Scissors", "Invalid", "Invalid", "Paper"]
        self.de = deque(['Nothing'] * 5, maxlen=5)
        
        # Game states
        self.game_state = "NAME_INPUT"
        self.result_timer = 0
        self.countdown_timer = 0
        
        # Colors
        self.COLOR_PLAYER = (255, 100, 100)
        self.COLOR_CPU = (100, 100, 255)
        self.COLOR_WIN = (100, 255, 100)
        self.COLOR_LOSE = (100, 100, 255)
        self.COLOR_TIE = (255, 255, 100)
    
    def compute_fingers(self, hand_landmarks, count):
        """Count fingers being held up - YOUR ORIGINAL LOGIC"""
        # Index Finger
        if hand_landmarks[8][2] < hand_landmarks[6][2]:
            count += 1
        
        # Middle Finger
        if hand_landmarks[12][2] < hand_landmarks[10][2]:
            count += 1
        
        # Ring Finger
        if hand_landmarks[16][2] < hand_landmarks[14][2]:
            count += 1
        
        # Pinky Finger
        if hand_landmarks[20][2] < hand_landmarks[18][2]:
            count += 1
        
        # Thumb
        if hand_landmarks[4][3] == "Left" and hand_landmarks[4][1] > hand_landmarks[3][1]:
            count += 1
        elif hand_landmarks[4][3] == "Right" and hand_landmarks[4][1] < hand_landmarks[3][1]:
            count += 1
        
        return count
    
    def process_frame_for_gesture(self, frame):
        """
        Process a single frame to detect hand gesture.
        This method is called from the Flask app for real-time detection.
        Returns the detected gesture as a string.
        """
        # Process the frame
        frame.flags.writeable = False
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        frame.flags.writeable = True
        
        hand_landmarks = []
        isCounting = False
        count = 0
        player_choice = "Nothing"
        
        if results.multi_hand_landmarks:
            isCounting = True
            
            # Get hand landmarks
            handNumber = 0
            for hand in results.multi_hand_landmarks:
                # Determine if it's left or right hand
                if results.multi_handedness:
                    label = results.multi_handedness[handNumber].classification[0].label
                else:
                    label = "Right"  # Default
                
                # Convert landmarks to pixel coordinates
                imgH, imgW, imgC = frame.shape
                for id, landmark in enumerate(hand.landmark):
                    xPos, yPos = int(landmark.x * imgW), int(landmark.y * imgH)
                    hand_landmarks.append([id, xPos, yPos, label])
                
                # Count fingers using YOUR original logic
                count = self.compute_fingers(hand_landmarks, count)
                handNumber += 1
        
        # Determine player choice based on finger count
        if isCounting and count <= 5:
            player_choice = self.display_values[count]
        elif isCounting:
            player_choice = "Invalid"
        else:
            player_choice = "Nothing"
        
        # Add to deque for stability (YOUR original stability system)
        self.de.appendleft(player_choice)
        
        # Use mode for stable detection
        try:
            player_choice = st.mode(self.de)
        except st.StatisticsError:
            # If no mode can be determined, use the most recent choice
            player_choice = self.de[0] if self.de else "Nothing"
        
        return player_choice
    
    def calculate_winner(self, cpu_choice, player_choice):
        """Determines the winner of each round"""
        if player_choice == "Invalid":
            return "Invalid!"
        
        if player_choice == cpu_choice:
            return "Tie!"
        
        elif player_choice == "Rock" and cpu_choice == "Scissors":
            return "You win!"
        
        elif player_choice == "Rock" and cpu_choice == "Paper":
            return "CPU wins!"
        
        elif player_choice == "Scissors" and cpu_choice == "Rock":
            return "CPU wins!"
        
        elif player_choice == "Scissors" and cpu_choice == "Paper":
            return "You win!"
        
        elif player_choice == "Paper" and cpu_choice == "Rock":
            return "You win!"
        
        elif player_choice == "Paper" and cpu_choice == "Scissors":
            return "CPU wins!"
    
    def reset_game(self):
        """Reset game state for a new game"""
        self.player_score = 0
        self.cpu_score = 0
        self.round_number = 0
        self.cpu_choice = "Nothing"
        self.player_choice = "Nothing"
        self.winner = "None"
        self.hand_valid = False
        self.de = deque(['Nothing'] * 5, maxlen=5)
        self.game_state = "PLAYING"
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, 'hands'):
            self.hands.close()


if __name__ == "__main__":
    print("=" * 60)
    print("ROCK PAPER SCISSORS - Hand Gesture Game")
    print("=" * 60)
    print("\nThis file is meant to be imported by app.py")
    print("Run: python app.py")
    print("=" * 60)