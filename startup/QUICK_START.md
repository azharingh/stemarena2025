# 🚀 QUICK START GUIDE - STEM ARENA

## Step 1: Install Dependencies

Open Command Prompt or PowerShell and run:

```bash
cd "backend lessons"
pip install flask flask-cors python-jose[cryptography] bcrypt requests
```

## Step 2: Start the Backend

In the same terminal:

```bash
python main.py
```

You should see:
```
 * Running on http://0.0.0.0:8000
 * Debug mode: on
```

## Step 3: Start the Frontend

Open a NEW terminal window and run:

```bash
cd startup
python -m http.server 5500
```

You should see:
```
Serving HTTP on :: port 5500 (http://[::]:5500/) ...
```

## Step 4: Access the Website

Open your browser and go to:
**http://localhost:5500/pj.html**

## Troubleshooting

### If you get "Module not found" errors:
- Make sure you're in the `backend lessons` directory
- Run: `pip install flask flask-cors python-jose[cryptography] bcrypt requests`

### If you get "Port already in use" errors:
- Close other applications using ports 8000 or 5500
- Or kill the processes using those ports

### If the website doesn't load:
- Make sure both servers are running
- Check that you're using `http://localhost:5500/pj.html` (not `file://`)
- Try refreshing the page

### If the backend won't start:
- Check that Python is installed: `python --version`
- Make sure all dependencies are installed
- Check the console for error messages

## Quick Test

To test if everything is working:

1. Backend test: Visit http://127.0.0.1:8000
   - Should show: `{"message": "STEM ARENA Backend is running!", "status": "ok"}`

2. Frontend test: Visit http://localhost:5500/pj.html
   - Should show the STEM ARENA interface

## Need Help?

If you're still having issues:
1. Check the console output for error messages
2. Make sure both servers are running
3. Try restarting both servers
4. Check that ports 8000 and 5500 are available 