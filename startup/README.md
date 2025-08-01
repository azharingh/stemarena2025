# STEM ARENA - Educational Gaming Platform

A modern web-based educational platform for STEM subjects with AI-powered tutoring and competitive learning features.

## Features

- 🤖 **AI Tutor**: Get help with math, physics, chemistry, biology, computer science, and engineering
- 🏆 **Competitive Learning**: 1v1 competitions with real-time assessment
- 📚 **Multiple Subjects**: Math, Physics, Chemistry, Biology, Computer Science, Engineering
- 🎮 **Gamified Learning**: Earn gems, track victories, and climb rankings
- 💬 **Interactive Chat**: Real-time AI assistance for any STEM topic

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Install Dependencies**:
   ```bash
   # Run the installation script
   install_dependencies.bat
   # OR
   install_dependencies.ps1
   ```

2. **Start the Application**:
   ```bash
   # Run the startup script
   start.bat
   # OR
   start.ps1
   ```

3. **Access the Application**:
   - Backend API: http://127.0.0.1:8000
   - Frontend: http://localhost:5500/pj.html

## Manual Setup

If the scripts don't work, you can set up manually:

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd "backend lessons"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements_flask.txt
   ```

3. Run the backend server:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the startup directory:
   ```bash
   cd startup
   ```

2. Start a simple HTTP server:
   ```bash
   python -m http.server 5500
   ```

3. Open your browser and go to: http://localhost:5500/pj.html

## Testing

To verify everything is working:

1. Run the test script:
   ```bash
   cd "backend lessons"
   python test_backend.py
   ```

2. Check the backend is running:
   - Visit http://127.0.0.1:8000
   - You should see: `{"message": "STEM ARENA Backend is running!", "status": "ok"}`

## Troubleshooting

### Common Issues

1. **Port 8000 already in use**:
   - Close other applications using port 8000
   - Or change the port in `main.py`

2. **Port 5500 already in use**:
   - Close other applications using port 5500
   - Or use a different port for the frontend server

3. **Module not found errors**:
   - Make sure you've installed dependencies: `pip install -r requirements_flask.txt`
   - Check that you're in the correct directory

4. **Database errors**:
   - The database will be created automatically
   - Make sure you have write permissions in the `backend lessons` directory

5. **Frontend can't connect to backend**:
   - Ensure the backend is running on http://127.0.0.1:8000
   - Check that CORS is properly configured
   - Try refreshing the browser page

### Debug Mode

To run in debug mode with more detailed error messages:

```bash
cd "backend lessons"
python main.py
```

The backend will show detailed logs of all requests and any errors.

## API Endpoints

### Authentication
- `POST /signup` - Register a new user
- `POST /login` - Login user

### User Management
- `GET /user/<username>` - Get user profile

### AI Services
- `POST /ai/chat` - Chat with AI tutor
- `POST /ai/generate-task` - Generate AI task

### Competition
- `POST /competition/join` - Join competition
- `GET /competition/status/<id>` - Get competition status
- `POST /competition/submit-answer` - Submit answer
- `GET /competition/available-subjects` - Get available subjects

## File Structure

```
startup backend/
├── backend lessons/
│   ├── app_flask.py          # Main Flask application
│   ├── main.py               # Entry point
│   ├── database_sqlite.py    # Database operations
│   ├── ai_service.py         # AI service functions
│   ├── utilis.py             # Utility functions
│   ├── requirements_flask.txt # Python dependencies
│   └── test_backend.py       # Backend tests
└── startup/
    ├── pj.html               # Main application page
    ├── ai-chat.html          # AI chat interface
    ├── competition.html       # Competition interface
    ├── start.bat             # Windows startup script
    ├── start.ps1             # PowerShell startup script
    └── README.md             # This file
```

## Support

If you encounter any issues:

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure both backend and frontend servers are running
4. Check that the ports (8000 and 5500) are available

## License

This project is for educational purposes. 