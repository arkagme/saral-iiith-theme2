import pytest
import os
from backend.llm_service import LLMService
from backend.pptx_builder import PPTXBuilder
from backend.evaluator import Evaluator

pytestmark = pytest.mark.skipif(
    not os.getenv('GEMINI_API_KEY'),
    reason="GEMINI_API_KEY not set"
)

def test_end_to_end_presentation_generation():
    """Test complete presentation generation pipeline"""

    llm_service = LLMService()
    builder = PPTXBuilder()
    evaluator = Evaluator()
    
    content = """
    Introduction to Machine Learning
    
    Machine learning is a subset of artificial intelligence that enables systems to learn from data.
    
    Key concepts include supervised learning, unsupervised learning, and reinforcement learning.
    
    Applications range from image recognition to natural language processing.
    """
    

    structure = llm_service.generate_slide_structure(content, 'academic')
    assert structure is not None
    assert 'slides' in structure
    

    style = llm_service.infer_visual_tone(content, 'academic')
    assert style is not None
    

    builder.set_style(style)
    builder.build_from_structure(structure)
    

    output_path = 'outputs/test_integration.pptx'
    builder.save(output_path)
    assert os.path.exists(output_path)
    

    evaluation = evaluator.evaluate_presentation(content, structure)
    assert evaluation['overall_score'] >= 0
    

    if os.path.exists(output_path):
        os.remove(output_path)

def test_style_transfer_workflow():
    """Test style transfer workflow"""

    
    llm_service = LLMService()
    content = "New content for styled presentation"
    
    structure = llm_service.generate_slide_structure(content, 'corporate')
    assert structure is not None

def test_chat_command_processing():
    """Test natural language command processing"""
    llm_service = LLMService()
    
    current_structure = {
        'title': 'Test Presentation',
        'slides': [
            {'type': 'Title Slide', 'title': 'Test'},
            {'type': 'Title and Content', 'title': 'Content', 'content': ['Point 1']}
        ]
    }
    
    command = "Add summary slide"
    modification = llm_service.process_natural_language_command(command, current_structure)
    
    assert 'action' in modification
    assert modification['action'] in ['add_slide', 'remove_slide', 'modify_slide', 'reorder_slides', 'change_style', 'error']
