from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

from backend.config import config
from backend.llm_service import LLMService
from backend.pptx_parser import PPTXParser
from backend.pptx_builder import PPTXBuilder
from backend.style_transfer import StyleTransfer
from backend.chart_generator import ChartGenerator
from backend.evaluator import Evaluator

app = Flask(__name__)
CORS(app)

llm_service = LLMService()
chart_generator = ChartGenerator()
evaluator = Evaluator()

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/generate', methods=['POST'])
def generate_presentation():
    """Generate presentation from text content"""
    try:
        data = request.json
        content = data.get('content', '')
        audience_type = data.get('audience_type', 'corporate')
        template_path = data.get('template_path')
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        structure = llm_service.generate_slide_structure(content, audience_type)
        
        visual_style = llm_service.infer_visual_tone(content, audience_type)
        
        if template_path and os.path.exists(template_path):
            builder = PPTXBuilder(template_path)
        else:
            default_template = os.path.join(
                config.TEMPLATE_FOLDER,
                config.AUDIENCE_TYPES[audience_type]['template']
            )
            if os.path.exists(default_template):
                builder = PPTXBuilder(default_template)
            else:
                builder = PPTXBuilder()
        
        builder.set_style(visual_style)
        
        builder.build_from_structure(structure)

        output_filename = f"presentation_{uuid.uuid4().hex[:8]}.pptx"
        output_path = os.path.join(config.OUTPUT_FOLDER, output_filename)
        builder.save(output_path)
        
        evaluation = evaluator.evaluate_presentation(content, structure)
        
        return jsonify({
            'success': True,
            'output_path': output_path,
            'filename': output_filename,
            'structure': structure,
            'visual_style': visual_style,
            'evaluation': evaluation
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a file (PPTX, template, or data file)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
        filepath = os.path.join(config.UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filepath': filepath,
            'filename': unique_filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_presentation():
    """Analyze an existing PPTX file"""
    try:
        data = request.json
        filepath = data.get('filepath')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Invalid file path'}), 400
        
        parser = PPTXParser(filepath)
        style_profile = parser.get_style_profile()
        slide_structure = parser.get_slide_structure()
        
        return jsonify({
            'success': True,
            'style_profile': style_profile,
            'slide_structure': slide_structure
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/style-transfer', methods=['POST'])
def apply_style_transfer():
    """Apply style from reference presentation to new content"""
    try:
        data = request.json
        reference_path = data.get('reference_path')
        content = data.get('content', '')
        audience_type = data.get('audience_type', 'corporate')
        
        if not reference_path or not os.path.exists(reference_path):
            return jsonify({'error': 'Invalid reference file path'}), 400
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        style_transfer = StyleTransfer(reference_path)
        extracted_style = style_transfer.extract_style()
        
        structure = llm_service.generate_slide_structure(content, audience_type)
        
        builder = PPTXBuilder(reference_path)
        style_transfer.apply_style_to_builder(builder)
        
        builder.build_from_structure(structure)
        
        output_filename = f"styled_presentation_{uuid.uuid4().hex[:8]}.pptx"
        output_path = os.path.join(config.OUTPUT_FOLDER, output_filename)
        builder.save(output_path)
        
        return jsonify({
            'success': True,
            'output_path': output_path,
            'filename': output_filename,
            'extracted_style': extracted_style,
            'structure': structure
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart', methods=['POST'])
def generate_chart():
    """Generate chart from data file"""
    try:
        data = request.json
        data_filepath = data.get('data_filepath')
        chart_type = data.get('chart_type')
        title = data.get('title', '')
        
        if not data_filepath or not os.path.exists(data_filepath):
            return jsonify({'error': 'Invalid data file path'}), 400
        
        result = chart_generator.generate_chart(data_filepath, chart_type, title)
        
        return jsonify({
            'success': True,
            'chart_info': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def process_chat_command():
    """Process natural language command to modify presentation"""
    try:
        data = request.json
        command = data.get('command', '')
        current_structure = data.get('current_structure', {})
        presentation_path = data.get('presentation_path')
        
        if not command:
            return jsonify({'error': 'Command is required'}), 400
        
        modification = llm_service.process_natural_language_command(command, current_structure)
        
        updated_structure = apply_modification(current_structure, modification)
        
        if presentation_path and os.path.exists(presentation_path):
            builder = PPTXBuilder(presentation_path)
            builder.build_from_structure(updated_structure)
            
            output_filename = f"modified_{uuid.uuid4().hex[:8]}.pptx"
            output_path = os.path.join(config.OUTPUT_FOLDER, output_filename)
            builder.save(output_path)
            
            return jsonify({
                'success': True,
                'modification': modification,
                'updated_structure': updated_structure,
                'output_path': output_path,
                'filename': output_filename
            })
        else:
            return jsonify({
                'success': True,
                'modification': modification,
                'updated_structure': updated_structure
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated presentation"""
    try:
        filepath = os.path.join(config.OUTPUT_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def apply_modification(structure: dict, modification: dict) -> dict:
    """Apply modification to presentation structure"""
    action = modification.get('action')
    params = modification.get('parameters', {})
    
    if action == 'add_slide':
        position = params.get('position', len(structure.get('slides', [])))
        slide = params.get('slide', {})
        structure.setdefault('slides', []).insert(position, slide)
    
    elif action == 'remove_slide':
        position = params.get('position', -1)
        if 0 <= position < len(structure.get('slides', [])):
            structure['slides'].pop(position)
    
    elif action == 'modify_slide':
        position = params.get('position', -1)
        changes = params.get('changes', {})
        if 0 <= position < len(structure.get('slides', [])):
            structure['slides'][position].update(changes)
    
    elif action == 'reorder_slides':
        from_idx = params.get('from', -1)
        to_idx = params.get('to', -1)
        slides = structure.get('slides', [])
        if 0 <= from_idx < len(slides) and 0 <= to_idx < len(slides):
            slide = slides.pop(from_idx)
            slides.insert(to_idx, slide)
    
    return structure

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=config.FLASK_PORT,
        debug=(config.FLASK_ENV == 'development')
    )
