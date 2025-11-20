import pytest
from backend.llm_service import LLMService
import os


pytestmark = pytest.mark.skipif(
    not os.getenv('GEMINI_API_KEY'),
    reason="GEMINI_API_KEY not set"
)

def test_llm_service_initialization():
    """Test LLM service can be initialized"""
    service = LLMService()
    assert service.model is not None

def test_generate_slide_structure():
    """Test slide structure generation"""
    service = LLMService()
    content = "This is a test presentation about AI and machine learning."
    
    structure = service.generate_slide_structure(content, 'corporate')
    
    assert 'title' in structure
    assert 'slides' in structure
    assert len(structure['slides']) > 0

def test_infer_visual_tone():
    """Test visual tone inference"""
    service = LLMService()
    content = "Academic research on quantum computing"
    
    style = service.infer_visual_tone(content, 'academic')
    
    assert 'tone' in style
    assert 'primary_color' in style
    assert 'font_suggestion' in style

def test_generate_summary_slide():
    """Test summary slide generation"""
    service = LLMService()
    content = "Key points about climate change and sustainability"
    
    summary = service.generate_summary_slide(content)
    
    assert 'type' in summary
    assert 'title' in summary
    assert 'content' in summary

def test_process_natural_language_command():
    """Test natural language command processing"""
    service = LLMService()
    command = "Add summary slide for conclusion"
    current_structure = {
        'title': 'Test',
        'slides': [
            {'type': 'Title Slide', 'title': 'Test'}
        ]
    }
    
    modification = service.process_natural_language_command(command, current_structure)
    
    assert 'action' in modification
    assert 'parameters' in modification
    assert 'explanation' in modification
