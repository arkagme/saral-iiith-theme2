import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for the PowerPoint Customization Engine"""
    
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-2.0-flash-lite'
    
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'pptx', 'potx', 'txt', 'md', 'csv', 'xlsx'}
    
    DEFAULT_FONT = 'Calibri'
    DEFAULT_FONT_SIZE = 18
    TITLE_FONT_SIZE = 44
    HEADING_FONT_SIZE = 32
    

    LLM_TEMPERATURE = 0.7
    LLM_MAX_TOKENS = 2048
    
    AUDIENCE_TYPES = {
        'academic': {
            'tone': 'formal, scholarly, detailed',
            'template': 'academic_template.pptx',
            'colors': ['#003366', '#0066CC', '#FFFFFF']
        },
        'corporate': {
            'tone': 'professional, concise, business-oriented',
            'template': 'corporate_template.pptx',
            'colors': ['#1F4788', '#4A90E2', '#FFFFFF']
        },
        'creative': {
            'tone': 'vibrant, engaging, dynamic',
            'template': 'default_template.pptx',
            'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1']
        },
        'minimalist': {
            'tone': 'clean, simple, focused',
            'template': 'default_template.pptx',
            'colors': ['#2C3E50', '#ECF0F1', '#FFFFFF']
        }
    }
    
    LAYOUT_TYPES = [
        'Title Slide',
        'Title and Content',
        'Section Header',
        'Two Content',
        'Comparison',
        'Title Only',
        'Blank',
        'Content with Caption',
        'Picture with Caption'
    ]

config = Config()
