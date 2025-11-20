import pytest
from backend.pptx_builder import PPTXBuilder
from backend.evaluator import Evaluator
import os

def test_pptx_builder_initialization():
    """Test PPTX builder initialization"""
    builder = PPTXBuilder()
    assert builder.prs is not None

def test_add_title_slide():
    """Test adding title slide"""
    builder = PPTXBuilder()
    slide = builder.add_title_slide("Test Title", "Test Subtitle")
    assert slide is not None

def test_add_content_slide():
    """Test adding content slide"""
    builder = PPTXBuilder()
    content = ["Point 1", "Point 2", "Point 3"]
    slide = builder.add_content_slide("Test Content", content)
    assert slide is not None

def test_build_from_structure():
    """Test building presentation from structure"""
    builder = PPTXBuilder()
    structure = {
        'title': 'Test Presentation',
        'slides': [
            {
                'type': 'Title Slide',
                'title': 'Test Title',
                'subtitle': 'Test Subtitle'
            },
            {
                'type': 'Title and Content',
                'title': 'Slide 1',
                'content': ['Point 1', 'Point 2']
            }
        ]
    }
    
    builder.build_from_structure(structure)
    assert len(builder.prs.slides) == 2

def test_save_presentation():
    """Test saving presentation"""
    builder = PPTXBuilder()
    builder.add_title_slide("Test", "Test")
    
    output_path = 'outputs/test_presentation.pptx'
    result = builder.save(output_path)
    
    assert os.path.exists(result)
    os.remove(result)  # Cleanup

def test_evaluator_keyword_extraction():
    """Test keyword extraction"""
    evaluator = Evaluator()
    text = "This is a test about machine learning and artificial intelligence"
    keywords = evaluator.extract_keywords(text)
    
    assert 'machine' in keywords or 'learning' in keywords

def test_evaluator_f1_score():
    """Test F1 score calculation"""
    evaluator = Evaluator()
    source = "machine learning artificial intelligence"
    generated = "machine learning deep learning"
    
    f1 = evaluator.calculate_keyword_f1(source, generated)
    assert 0 <= f1 <= 1

def test_evaluate_content_consistency():
    """Test content consistency evaluation"""
    evaluator = Evaluator()
    source = "This presentation is about climate change and sustainability"
    structure = {
        'slides': [
            {
                'title': 'Climate Change',
                'content': ['Sustainability', 'Environmental impact']
            }
        ]
    }
    
    result = evaluator.evaluate_content_consistency(source, structure)
    assert 'keyword_f1_score' in result
    assert 'consistency_rating' in result

def test_check_design_quality():
    """Test design quality check"""
    evaluator = Evaluator()
    structure = {
        'slides': [
            {'type': 'Title Slide', 'title': 'Test'},
            {'type': 'Title and Content', 'title': 'Slide 1', 'content': ['A', 'B', 'C']}
        ]
    }
    
    result = evaluator.check_design_quality(structure)
    assert 'quality_score' in result
    assert 'issues' in result
    assert 'warnings' in result
