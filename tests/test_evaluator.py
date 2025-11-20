import pytest
from backend.evaluator import Evaluator

def test_evaluator_initialization():
    """Test evaluator initialization"""
    evaluator = Evaluator()
    assert evaluator is not None

def test_extract_keywords():
    """Test keyword extraction"""
    evaluator = Evaluator()
    text = "Machine learning and artificial intelligence are transforming technology"
    keywords = evaluator.extract_keywords(text)
    
    assert isinstance(keywords, set)
    assert len(keywords) > 0

def test_calculate_keyword_f1():
    """Test F1 score calculation"""
    evaluator = Evaluator()
    
    f1_perfect = evaluator.calculate_keyword_f1("test data", "test data")
    assert f1_perfect == 1.0
    
    f1_none = evaluator.calculate_keyword_f1("completely different", "nothing matches")
    assert f1_none >= 0.0
    
    f1_partial = evaluator.calculate_keyword_f1("machine learning", "machine intelligence")
    assert 0 < f1_partial < 1

def test_evaluate_content_consistency():
    """Test content consistency evaluation"""
    evaluator = Evaluator()
    source = "Climate change and global warming"
    structure = {
        'slides': [
            {'title': 'Climate Change', 'content': ['Global warming', 'Temperature rise']}
        ]
    }
    
    result = evaluator.evaluate_content_consistency(source, structure)
    
    assert 'keyword_f1_score' in result
    assert 'consistency_rating' in result
    assert result['keyword_f1_score'] >= 0

def test_check_design_quality():
    """Test design quality checks"""
    evaluator = Evaluator()
    
    good_structure = {
        'slides': [
            {'type': 'Title Slide', 'title': 'Title'},
            {'type': 'Title and Content', 'title': 'Content', 'content': ['A', 'B', 'C']}
        ]
    }
    result = evaluator.check_design_quality(good_structure)
    assert result['quality_score'] > 50
    
    bad_structure = {
        'slides': [
            {'type': 'Title and Content', 'content': ['A', 'B']}
        ]
    }
    result_bad = evaluator.check_design_quality(bad_structure)
    assert len(result_bad['issues']) > 0

def test_evaluate_presentation():
    """Test comprehensive presentation evaluation"""
    evaluator = Evaluator()
    source = "This is about machine learning and AI"
    structure = {
        'slides': [
            {'type': 'Title Slide', 'title': 'Machine Learning'},
            {'type': 'Title and Content', 'title': 'AI Overview', 'content': ['Deep learning', 'Neural networks']}
        ]
    }
    
    result = evaluator.evaluate_presentation(source, structure)
    
    assert 'overall_score' in result
    assert 'content_consistency' in result
    assert 'design_quality' in result
    assert 'recommendation' in result
