# AI-Powered PowerPoint Customization Engine

An intelligent system that generates and customizes PowerPoint presentations using Gemini 2.0 Flash Lite and python-pptx.

## Technology Stack

### Backend

- Python 3
- Flask (REST API)
- python-pptx 
- google-generativeai using Gemini 2.0 Flash Lite
- pandas, matplotlib 

### Frontend

- React JS
- Tailwind CSS
- Vite
- Axios

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Gemini API key

### Backend Setup

1. Create Python virtual environment ( venv )

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` file:

```bash
cp .env.example .env
```

4. Add Gemini API key to `.env`:

```
GEMINI_API_KEY=your_api_key_here
```

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

## Usage

### Start Backend Server

```bash
python backend/app.py
```

The API will be available at `http://localhost:5000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The web interface will be available at `http://localhost:3000`

## API Endpoints

- `POST /api/generate` - Generate presentation from text content
- `POST /api/upload` - Upload files (PPTX, CSV, Excel)
- `POST /api/analyze` - Analyze existing PPTX file
- `POST /api/style-transfer` - Apply style from reference presentation
- `POST /api/chart` - Generate chart from data file
- `POST /api/chat` - Process natural language commands
- `GET /api/download/<filename>` - Download generated presentation

## Testing

Run the test suite:

```bash
# Make sure GEMINI_API_KEY is set
export GEMINI_API_KEY=your_key

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_llm_service.py -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

