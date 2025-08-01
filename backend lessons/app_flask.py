from flask import Flask, request, jsonify
from flask_cors import CORS
from database_sqlite import user_collection
from utilis import hash_password, verify_password, create_access_token
from ai_service import AIService
from datetime import datetime
import json
import random
import time

app = Flask(__name__)
CORS(app)

# Initialize AI service
ai_service = AIService()

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

# Store active competitions and waiting players
waiting_players = {}
active_competitions = {}

def calculate_age(birthday: str):
    birth_date = datetime.strptime(birthday, "%Y-%m-%d")
    today = datetime.utcnow()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

@app.route("/")
def read_root():
    return jsonify({"message": "STEM ARENA Backend is running!", "status": "ok"})

@app.route("/signup", methods=["POST"])
def signup():
    try:
        user_data = request.get_json()
        
        # Check if user already exists
        if user_collection.find_user_by_email(user_data["email"]):
            return jsonify({"detail": "Email already registered"}), 400
        if user_collection.find_user_by_username(user_data["username"]):
            return jsonify({"detail": "Username already taken"}), 400
        
        # Hash password
        user_data["password"] = hash_password(user_data["password"])
        
        # Insert user
        user_id = user_collection.insert_user(user_data)
        
        return jsonify({
            "id": str(user_id),
            "email": user_data["email"],
            "username": user_data["username"],
            "age": calculate_age(user_data["birthday"]),
            "location": user_data["location"],
            "grade": user_data["grade"],
            "level": user_data.get("level", 1),
            "gems": user_data.get("gems", 1000),
            "victories": user_data.get("victories", 0),
            "dominationRate": user_data.get("dominationRate", 0),
            "rank": user_data.get("rank", 0),
            "killStreak": user_data.get("killStreak", 0),
            "profileIcon": user_data.get("profileIcon", "🚀"),
            "firstName": user_data["firstName"],
            "lastName": user_data["lastName"],
            "birthday": user_data["birthday"]
        })
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        form_data = request.form
        
        # Try to find user by username first, then by email
        db_user = user_collection.find_user_by_username(form_data["username"])
        if not db_user:
            db_user = user_collection.find_user_by_email(form_data["username"])

        if not db_user or not verify_password(form_data["password"], db_user["password"]):
            return jsonify({"detail": "Invalid credentials"}), 401
        
        access_token = create_access_token(data={"sub": str(db_user["id"])})
        return jsonify({
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(db_user["id"]),
                "email": db_user["email"],
                "username": db_user["username"]
            }
        })
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/user/<username>")
def get_user_by_username(username):
    try:
        db_user = user_collection.find_user_by_username(username)
        if not db_user:
            return jsonify({"detail": "User not found"}), 404
        
        age = calculate_age(db_user["birthday"])
        return jsonify({
            "id": str(db_user["id"]),
            "email": db_user["email"],
            "username": db_user["username"],
            "age": age,
            "location": db_user["location"],
            "grade": db_user["grade"],
            "level": db_user.get("level", 1),
            "gems": db_user.get("gems", 1000),
            "victories": db_user.get("victories", 0),
            "dominationRate": db_user.get("dominationRate", 0),
            "rank": db_user.get("rank", 0),
            "killStreak": db_user.get("killStreak", 0),
            "profileIcon": db_user.get("profileIcon", "🚀"),
            "firstName": db_user.get("firstName", ""),
            "lastName": db_user.get("lastName", ""),
            "birthday": db_user["birthday"]
        })
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

# New 1vs1 Competition System
@app.route("/competition/join", methods=["POST"])
def join_competition():
    try:
        data = request.get_json()
        username = data.get("username")
        subject = data.get("subject", "math")
        difficulty = data.get("difficulty", "medium")
        
        # Remove player from any existing waiting list
        for key in list(waiting_players.keys()):
            if waiting_players[key]["username"] == username:
                del waiting_players[key]
        
        # Check if there's a waiting player for the same subject
        for key in list(waiting_players.keys()):
            if waiting_players[key]["subject"] == subject and waiting_players[key]["difficulty"] == difficulty:
                # Match found! Create competition
                opponent = waiting_players[key]
                del waiting_players[key]
                
                # Generate competition task
                task_data = ai_service.generate_task(subject, difficulty)
                
                competition_id = f"comp_{int(time.time())}_{random.randint(1000, 9999)}"
                active_competitions[competition_id] = {
                    "player1": username,
                    "player2": opponent["username"],
                    "subject": subject,
                    "difficulty": difficulty,
                    "task": task_data,
                    "start_time": time.time(),
                    "duration": 300,  # 5 minutes
                    "answers": {},
                    "status": "active"
                }
                
                return jsonify({
                    "status": "matched",
                    "competition_id": competition_id,
                    "opponent": opponent["username"],
                    "subject": subject,
                    "difficulty": difficulty,
                    "task": task_data
                })
        
        # No match found, add to waiting list
        waiting_id = f"wait_{int(time.time())}_{random.randint(1000, 9999)}"
        waiting_players[waiting_id] = {
            "username": username,
            "subject": subject,
            "difficulty": difficulty,
            "join_time": time.time()
        }
        
        return jsonify({
            "status": "waiting",
            "waiting_id": waiting_id,
            "subject": subject,
            "difficulty": difficulty
        })
        
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/competition/status/<competition_id>")
def get_competition_status(competition_id):
    try:
        if competition_id not in active_competitions:
            return jsonify({"detail": "Competition not found"}), 404
        
        competition = active_competitions[competition_id]
        elapsed_time = time.time() - competition["start_time"]
        remaining_time = max(0, competition["duration"] - elapsed_time)
        
        return jsonify({
            "status": competition["status"],
            "remaining_time": remaining_time,
            "answers": competition["answers"],
            "task": competition["task"]
        })
        
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/competition/submit-answer", methods=["POST"])
def submit_competition_answer():
    try:
        data = request.get_json()
        competition_id = data.get("competition_id")
        username = data.get("username")
        answer = data.get("answer")
        
        if competition_id not in active_competitions:
            return jsonify({"detail": "Competition not found"}), 404
        
        competition = active_competitions[competition_id]
        
        # Check if time is up
        elapsed_time = time.time() - competition["start_time"]
        if elapsed_time > competition["duration"]:
            competition["status"] = "timeout"
            return jsonify({"detail": "Time is up!"}), 400
        
        # Store answer
        competition["answers"][username] = {
            "answer": answer,
            "submit_time": time.time()
        }
        
        # Check if both players have answered
        if len(competition["answers"]) == 2:
            # Assess answers
            results = {}
            for player, answer_data in competition["answers"].items():
                assessment = ai_service.assess_answer(
                    competition["task"]["question"], 
                    answer_data["answer"]
                )
                results[player] = assessment
            
            # Determine winner
            player1_score = results[competition["player1"]]["score"]
            player2_score = results[competition["player2"]]["score"]
            
            if player1_score > player2_score:
                winner = competition["player1"]
                loser = competition["player2"]
            elif player2_score > player1_score:
                winner = competition["player2"]
                loser = competition["player1"]
            else:
                winner = "tie"
                loser = "tie"
            
            competition["status"] = "completed"
            competition["results"] = results
            competition["winner"] = winner
            
            return jsonify({
                "status": "completed",
                "results": results,
                "winner": winner,
                "competition_id": competition_id
            })
        
        return jsonify({
            "status": "answer_submitted",
            "remaining_players": 2 - len(competition["answers"])
        })
        
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/competition/available-subjects")
def get_available_subjects():
    return jsonify({
        "subjects": [
            {"id": "math", "name": "Mathematics", "icon": "📐"},
            {"id": "physics", "name": "Physics", "icon": "⚛️"},
            {"id": "chemistry", "name": "Chemistry", "icon": "🧪"},
            {"id": "biology", "name": "Biology", "icon": "🧬"},
            {"id": "cs", "name": "Computer Science", "icon": "💻"},
            {"id": "engineering", "name": "Engineering", "icon": "⚙️"}
        ],
        "difficulties": [
            {"id": "easy", "name": "Easy"},
            {"id": "medium", "name": "Medium"},
            {"id": "hard", "name": "Hard"}
        ]
    })

@app.route("/competition/waiting-players")
def get_waiting_players():
    return jsonify({
        "waiting_players": [
            {
                "username": player["username"],
                "subject": player["subject"],
                "difficulty": player["difficulty"],
                "waiting_time": int(time.time() - player["join_time"])
            }
            for player in waiting_players.values()
        ]
    })

# AI-Enhanced Competition endpoints
@app.route("/competition/task")
def get_competition_task():
    try:
        # Get subject from query parameter, default to math
        subject = request.args.get("subject", "math")
        difficulty = request.args.get("difficulty", "medium")
        
        # Generate AI task
        task_data = ai_service.generate_task(subject, difficulty)
        
        return jsonify(task_data)
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/competition/submit", methods=["POST"])
def submit_single_competition_answer():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        answer = data.get("answer")
        question = data.get("question", "")
        
        # AI assessment
        assessment = ai_service.assess_answer(question, answer)
        
        # Calculate gems earned based on score
        gems_earned = max(10, int(assessment["score"] / 10))
        
        return jsonify({
            "status": "assessed",
            "score": assessment["score"],
            "feedback": assessment["feedback"],
            "correct": assessment["correct"],
            "gems_earned": gems_earned,
            "ai_assessment": assessment["ai_assessment"]
        })
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

# New AI Chat endpoint
@app.route("/ai/chat", methods=["POST"])
def chat_with_ai():
    try:
        data = request.get_json()
        message = data.get("message", "")
        context = data.get("context", "")
        
        # Get AI response
        ai_response = ai_service.chat_with_ai(message, context)
        
        return jsonify({
            "response": ai_response,
            "ai_generated": True
        })
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

# AI Task Generation endpoint
@app.route("/ai/generate-task", methods=["POST"])
def generate_ai_task():
    try:
        data = request.get_json()
        subject = data.get("subject", "math")
        difficulty = data.get("difficulty", "medium")
        
        # Generate AI task
        task_data = ai_service.generate_task(subject, difficulty)
        
        return jsonify(task_data)
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 