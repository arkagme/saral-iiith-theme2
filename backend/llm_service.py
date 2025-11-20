import google.generativeai as genai
from typing import Dict, List, Optional
import json
import re
from backend.config import config

class LLMService:
    """Service for interacting with Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API"""
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
    
    def generate_slide_structure(self, content: str, audience_type: str = 'corporate') -> Dict:
        """Generate slide structure from content"""
        
        audience_info = config.AUDIENCE_TYPES.get(audience_type, config.AUDIENCE_TYPES['corporate'])
        
        prompt = f"""You are an expert presentation designer. Analyze the following content and create a structured presentation outline.

Content:
{content}

Audience Type: {audience_type}
Tone: {audience_info['tone']}

Generate a JSON structure with the following format:
{{
    "title": "Main presentation title",
    "slides": [
        {{
            "type": "Title Slide",
            "title": "Presentation Title",
            "subtitle": "Optional subtitle"
        }},
        {{
            "type": "Section Header",
            "title": "Section Title"
        }},
        {{
            "type": "Title and Content",
            "title": "Slide Title",
            "content": ["Bullet point 1", "Bullet point 2", "Bullet point 3"]
        }},
        {{
            "type": "Two Content",
            "title": "Comparison Title",
            "left_content": ["Point 1", "Point 2"],
            "right_content": ["Point A", "Point B"]
        }}
    ]
}}

Rules:
1. Start with a Title Slide
2. Use Section Headers to divide major topics
3. Keep bullet points concise (max 7 words each)
4. Limit to 5-7 bullets per slide
5. Use appropriate slide types (Title and Content, Two Content, Section Header)
6. End with a summary or conclusion slide if appropriate

Return ONLY the JSON structure, no additional text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
         
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            structure = json.loads(result_text)
            return structure
        except Exception as e:
            print(f"Error generating slide structure: {e}")
    
            return {
                "title": "Presentation",
                "slides": [
                    {
                        "type": "Title Slide",
                        "title": "Presentation",
                        "subtitle": "Generated from content"
                    },
                    {
                        "type": "Title and Content",
                        "title": "Overview",
                        "content": [content[:100] + "..."]
                    }
                ]
            }
    
    def infer_visual_tone(self, content: str, audience_type: str = 'corporate') -> Dict:
        """Infer visual tone and style from content"""
        
        prompt = f"""Analyze this content and suggest visual styling for a presentation.

Content:
{content}

Audience: {audience_type}

Provide a JSON response with:
{{
    "tone": "formal/vibrant/minimalist/academic/corporate",
    "primary_color": "#RRGGBB",
    "secondary_color": "#RRGGBB",
    "accent_color": "#RRGGBB",
    "font_suggestion": "Font name",
    "style_keywords": ["keyword1", "keyword2", "keyword3"]
}}

Return ONLY the JSON, no additional text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            return json.loads(result_text)
        except Exception as e:
            print(f"Error inferring visual tone: {e}")
            audience_info = config.AUDIENCE_TYPES.get(audience_type, config.AUDIENCE_TYPES['corporate'])
            return {
                "tone": audience_type,
                "primary_color": audience_info['colors'][0],
                "secondary_color": audience_info['colors'][1],
                "accent_color": audience_info['colors'][2] if len(audience_info['colors']) > 2 else "#FFFFFF",
                "font_suggestion": config.DEFAULT_FONT,
                "style_keywords": [audience_type, "professional"]
            }
    
    def generate_chart_caption(self, chart_data: Dict, chart_type: str) -> str:
        """Generate caption for a chart"""
        
        prompt = f"""Generate a concise, informative caption for this chart.

Chart Type: {chart_type}
Data Summary: {json.dumps(chart_data, indent=2)}

Provide a single sentence caption that describes the key insight or trend shown in the data.
Return ONLY the caption text, no additional formatting."""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip().strip('"\'')
        except Exception as e:
            print(f"Error generating chart caption: {e}")
            return f"{chart_type} visualization"
    
    def process_natural_language_command(self, command: str, current_structure: Dict) -> Dict:
        """Process natural language commands to modify presentation"""
        
        prompt = f"""You are a presentation editing assistant. Process this command and return the modification to make.

Current Presentation Structure:
{json.dumps(current_structure, indent=2)}

User Command: "{command}"

Analyze the command and return a JSON response with:
{{
    "action": "add_slide/remove_slide/modify_slide/reorder_slides/change_style",
    "parameters": {{
        // Action-specific parameters
        // For add_slide: {{"position": index, "slide": {{...slide object...}}}}
        // For remove_slide: {{"position": index}}
        // For modify_slide: {{"position": index, "changes": {{...}}}}
        // For reorder_slides: {{"from": index, "to": index}}
        // For change_style: {{"style": "academic/corporate/creative/minimalist"}}
    }},
    "explanation": "Brief explanation of what will be done"
}}

Return ONLY the JSON, no additional text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            return json.loads(result_text)
        except Exception as e:
            print(f"Error processing command: {e}")
            return {
                "action": "error",
                "parameters": {},
                "explanation": f"Could not process command: {str(e)}"
            }
    
    def generate_summary_slide(self, content: str) -> Dict:
        """Generate a summary slide from content"""
        
        prompt = f"""Create a summary slide for this presentation content.

Content:
{content}

Generate a JSON slide object:
{{
    "type": "Title and Content",
    "title": "Summary" or "Key Takeaways" or "Conclusion",
    "content": ["Key point 1", "Key point 2", "Key point 3", "Key point 4"]
}}

Limit to 4-5 key points. Make them concise and impactful.
Return ONLY the JSON, no additional text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            return json.loads(result_text)
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {
                "type": "Title and Content",
                "title": "Summary",
                "content": ["Key points from the presentation"]
            }
    
    def suggest_slide_reordering(self, slides: List[Dict]) -> List[int]:
        """Suggest optimal slide ordering"""
        
        prompt = f"""Analyze these slides and suggest the optimal order for narrative flow.

Slides:
{json.dumps(slides, indent=2)}

Return a JSON array of indices representing the optimal order.
For example, if the best order is slide 2, then 0, then 1, return: [2, 0, 1]

Consider:
1. Title slide should be first
2. Section headers should precede related content
3. Summary/conclusion should be last
4. Logical flow of topics

Return ONLY the JSON array, no additional text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            order = json.loads(result_text)
            # Validate the order
            if len(order) == len(slides) and set(order) == set(range(len(slides))):
                return order
            else:
                return list(range(len(slides)))
        except Exception as e:
            print(f"Error suggesting reordering: {e}")
            return list(range(len(slides)))
