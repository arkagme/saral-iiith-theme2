from typing import Dict, List, Set
import re

class Evaluator:
    """Evaluate presentation quality and consistency"""
    
    def __init__(self):
        """Initialize evaluator"""
        pass
    
    def extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text"""
  
        text = re.sub(r'[^\w\s]', ' ', text.lower())

        words = [w for w in text.split() if len(w) > 3]
        return set(words)
    
    def calculate_keyword_f1(self, source_text: str, generated_text: str) -> float:
        """Calculate F1 score for keyword overlap"""
        source_keywords = self.extract_keywords(source_text)
        generated_keywords = self.extract_keywords(generated_text)
        
        if not source_keywords or not generated_keywords:
            return 0.0
        

        true_positives = len(source_keywords & generated_keywords)
        precision = true_positives / len(generated_keywords) if generated_keywords else 0
        recall = true_positives / len(source_keywords) if source_keywords else 0
        if precision + recall == 0:
            return 0.0
        
        f1 = 2 * (precision * recall) / (precision + recall)
        return f1
    
    def evaluate_content_consistency(self, source_content: str, 
                                    slide_structure: Dict) -> Dict:
        """Evaluate content consistency between source and generated slides"""

        generated_text = ""
        for slide in slide_structure.get('slides', []):
            generated_text += slide.get('title', '') + " "
            if 'content' in slide:
                generated_text += " ".join(slide['content']) + " "
            if 'left_content' in slide:
                generated_text += " ".join(slide['left_content']) + " "
            if 'right_content' in slide:
                generated_text += " ".join(slide['right_content']) + " "
        
        f1 = self.calculate_keyword_f1(source_content, generated_text)
        
        return {
            'keyword_f1_score': f1,
            'source_keywords': len(self.extract_keywords(source_content)),
            'generated_keywords': len(self.extract_keywords(generated_text)),
            'consistency_rating': 'High' if f1 > 0.7 else 'Medium' if f1 > 0.4 else 'Low'
        }
    
    def check_design_quality(self, slide_structure: Dict) -> Dict:
        """Check design quality metrics"""
        slides = slide_structure.get('slides', [])
        
        issues = []
        warnings = []
        
        if len(slides) < 3:
            warnings.append("Presentation has fewer than 3 slides")
        elif len(slides) > 20:
            warnings.append("Presentation has more than 20 slides - may be too long")
        
        if slides and slides[0].get('type') != 'Title Slide':
            issues.append("First slide should be a Title Slide")
        
        for idx, slide in enumerate(slides):
            if 'content' in slide:
                bullet_count = len(slide['content'])
                if bullet_count > 7:
                    warnings.append(f"Slide {idx + 1} has {bullet_count} bullets (recommended max: 7)")
            
            if not slide.get('title') and slide.get('type') != 'Title Slide':
                issues.append(f"Slide {idx + 1} is missing a title")
        
        quality_score = 100
        quality_score -= len(issues) * 10
        quality_score -= len(warnings) * 5
        quality_score = max(0, min(100, quality_score))
        
        return {
            'quality_score': quality_score,
            'issues': issues,
            'warnings': warnings,
            'slide_count': len(slides),
            'quality_rating': 'Excellent' if quality_score >= 90 else 
                            'Good' if quality_score >= 70 else 
                            'Fair' if quality_score >= 50 else 'Poor'
        }
    
    def evaluate_presentation(self, source_content: str, 
                            slide_structure: Dict) -> Dict:
        """Comprehensive presentation evaluation"""
        content_eval = self.evaluate_content_consistency(source_content, slide_structure)
        design_eval = self.check_design_quality(slide_structure)
        

        overall_score = (
            content_eval['keyword_f1_score'] * 50 +  
            design_eval['quality_score'] / 2  
        )
        
        return {
            'overall_score': overall_score,
            'content_consistency': content_eval,
            'design_quality': design_eval,
            'recommendation': self._get_recommendation(overall_score)
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on score"""
        if score >= 80:
            return "Excellent presentation quality. Ready to use."
        elif score >= 60:
            return "Good presentation. Minor improvements recommended."
        elif score >= 40:
            return "Fair presentation. Consider revising content or structure."
        else:
            return "Presentation needs significant improvement."
