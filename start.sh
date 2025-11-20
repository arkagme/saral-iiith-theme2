#!/bin/bash

echo "🚀 Starting AI PowerPoint Customization Engine..."
echo ""

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your GEMINI_API_KEY"
    exit 1
fi

source venv/bin/activate

echo "🔧 Starting backend server..."
python backend/app.py &
BACKEND_PID=$!

sleep 3

echo "🎨 Starting frontend dev server..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Servers started successfully!"
echo ""
echo "📍 Backend API: http://localhost:5000"
echo "📍 Frontend UI: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
