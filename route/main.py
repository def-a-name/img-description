from route import main_bp
from db.ops import *
from config import Config
from service.api import get_description_local, get_description_error
from service.api import get_description
from service.prompt import save_prompt_to_history
from datetime import datetime
from flask import render_template, Response, stream_with_context, request, jsonify
from werkzeug.utils import secure_filename
import base64, json

@main_bp.route('/')
def index():
    try:
        with open(Config.PROMPT_HISTORY_FILE, 'r') as f:
            prompt_history = json.load(f)
            prompt = prompt_history[-1].get('prompt')
    except:
        with open(Config.PROMPT_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        prompt_history = []
        prompt = Config.DEFAULT_PROMPT
    
    return render_template('index.html', 
                           default_prompt=prompt,
                           prompt_history=prompt_history)

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    time_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
    file = request.files.get('file')
    if not file or file.filename == '':
        return add_error_request(time_str, '没有选择文件')

    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in Config.ALLOWED_EXTENSIONS:
        return add_error_request(time_str, '不支持的文件类型')

    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > Config.MAX_IMAGE_SIZE:
        return add_error_request(time_str, '文件太大，请选择小于 10MB 的图片')

    img_base64 = base64.b64encode(file.read()).decode()
    return jsonify({
        'success': True,
        'upload_time': time_str,
        'filename': secure_filename(file.filename),
        'file_ext': ext,
        'img_base64': img_base64
    })

# @main_bp.route('/describe', methods=['POST'])
# def describe():
#     data = request.json
#     if not all(k in data for k in ['img_base64', 'file_ext', 'prompt', 'upload_time']):
#         return add_error_request(data.get('upload_time', ''), '缺少必要参数')
#     req = add_success_request(data['upload_time'])
    
#     try:
#         # res_data = get_description_error(data['img_base64'], data['file_ext'], data['prompt'])
#         # res_data = get_description_local(data['img_base64'], data['file_ext'], data['prompt'])
#         res_data = get_description(data['img_base64'], data['file_ext'], data['prompt'])
        
#         add_success_response(req.id, res_data['model'], res_data['description'])
#         return jsonify({
#             'success': True,
#             'description': res_data['description'],
#             'prompt_used': res_data['prompt_used']
#         })
#     except Exception as e:
#         add_error_response(req.id, str(e))
#         return jsonify({'error': str(e), 'description': 'API 异常，无效描述'}), 500
@main_bp.route('/describe', methods=['POST'])
def describe():
    data = request.json
    if not all(k in data for k in ['img_base64', 'file_ext', 'prompt', 'upload_time']):
        return add_error_request(data.get('upload_time', ''), '缺少必要参数')
    req = add_success_request(data['upload_time'])

    @stream_with_context
    def event_stream():
        try:
            # generator = get_description(data['img_base64'], data['file_ext'], data['prompt'])
            # generator = get_description_error(data['img_base64'], data['file_ext'], data['prompt'])
            generator = get_description_local(data['img_base64'], data['file_ext'], data['prompt'])

            model_name = next(generator)
            full_content = ""
            for chunk in generator:
                if chunk:
                    full_content += chunk[6:]  # 移除 'data: '
                    yield chunk
            add_success_response(req.id, model_name, full_content)
        except Exception as e:
            add_error_response(req.id, str(e))
            yield "data: [ERROR]API 异常，无效描述\n\n"

    return Response(event_stream(), content_type='text/event-stream')

@main_bp.route('/save-new-prompt', methods=['POST'])
def save_prompt():
    save_prompt_to_history(request.json['prompt'])
    return jsonify({'success': True})

@main_bp.route('/debug', methods=['GET'])
def debug():
    reqs, resps = get_debug_data()
    return render_template('debug.html', requests=reqs, responses=resps)