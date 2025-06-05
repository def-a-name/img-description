from route import main_bp
from db import db
from config import Config
from db.models import UserRequest, AiResponse
from service.api import get_test_description
from service.prompt import save_prompt_to_history
from datetime import datetime
from flask import render_template, request, jsonify
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
        return _error_request('没有选择文件', time_str)

    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in Config.ALLOWED_EXTENSIONS:
        return _error_request('不支持的文件类型', time_str)

    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > Config.MAX_IMAGE_SIZE:
        return _error_request('文件太大，请选择小于 10MB 的图片', time_str)

    img_base64 = base64.b64encode(file.read()).decode()
    return jsonify({
        'success': True,
        'upload_time': time_str,
        'filename': secure_filename(file.filename),
        'file_ext': ext,
        'img_base64': img_base64
    })

def _error_request(msg, time):
    req = UserRequest(upload_time=time, request_time='', status_code=400, error_message=msg)
    db.session.add(req)
    db.session.commit()
    return jsonify({'error': msg}), 400

@main_bp.route('/describe', methods=['POST'])
def describe():
    now = datetime.now().strftime('%Y%m%d %H:%M:%S')
    data = request.json
    if not all(k in data for k in ['img_base64', 'file_ext', 'prompt', 'upload_time']):
        return _error_request('缺少必要参数', data.get('upload_time', ''))

    req = UserRequest(upload_time=data['upload_time'], 
                      request_time=now, 
                      status_code=200, 
                      error_message='')
    db.session.add(req)
    db.session.commit()

    try:
        res_data = get_test_description(data['img_base64'], data['file_ext'], data['prompt'])
        res_time = datetime.now().strftime('%Y%m%d %H:%M:%S')
        res = AiResponse(
            request_id=req.id,
            respond_time=res_time,
            model=res_data['model'],
            description=res_data['description'],
            status_code=200,
            error_message=''
        )
        db.session.add(res)
        db.session.commit()

        return jsonify({
            'success': True,
            'description': res.description,
            'prompt_used': res_data['prompt_used']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/save-new-prompt', methods=['POST'])
def save_prompt():
    save_prompt_to_history(request.json['prompt'])
    return jsonify({'success': True})

@main_bp.route('/debug', methods=['GET'])
def debug():
    reqs = UserRequest.query.order_by(UserRequest.id.desc()).all()
    resps = AiResponse.query.order_by(AiResponse.id.desc()).all()
    return render_template('debug.html', requests=reqs, responses=resps)