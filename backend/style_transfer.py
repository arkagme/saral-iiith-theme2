from backend.pptx_parser import PPTXParser
from backend.pptx_builder import PPTXBuilder
from typing import Dict, List
import os

class StyleTransfer:
    """Transfer style from one presentation to another"""
    
    def __init__(self, reference_pptx_path: str):
        """Initialize with reference presentation"""
        self.parser = PPTXParser(reference_pptx_path)
        self.style_profile = self.parser.get_style_profile()
    
    def extract_style(self) -> Dict:
        """Extract comprehensive style information"""
        return {
            'colors': self.style_profile['colors'],
            'fonts': self.style_profile['fonts'],
            'layouts': self.style_profile['layouts'],
            'primary_color': self.style_profile['colors'][0] if self.style_profile['colors'] else '#1F4788',
            'secondary_color': self.style_profile['colors'][1] if len(self.style_profile['colors']) > 1 else '#4A90E2',
            'accent_color': self.style_profile['colors'][2] if len(self.style_profile['colors']) > 2 else '#FFFFFF',
            'font_suggestion': self.style_profile['fonts'][0] if self.style_profile['fonts'] else 'Calibri'
        }
    
    def apply_style_to_builder(self, builder: PPTXBuilder):
        """Apply extracted style to a presentation builder"""
        style = self.extract_style()
        builder.set_style(style)
        return builder
    
    def get_color_palette(self) -> List[str]:
        """Get color palette from reference"""
        return self.style_profile['colors']
    
    def get_font_family(self) -> str:
        """Get primary font from reference"""
        fonts = self.style_profile['fonts']
        return fonts[0] if fonts else 'Calibri'
