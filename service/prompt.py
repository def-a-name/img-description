import json
from flask import jsonify
from datetime import datetime
from config import Config

def get_prompt_filename(user_id):
    filename = Config.PROMPT_HISTORY_FILE
    if not filename.endswith('.json'):
        raise ValueError("prompt 历史文件必须是 json 格式")
    
    return f"{filename[:-5]}_{user_id}.json"

def save_prompt_to_history(uid, prompt):
    try:
        with open(get_prompt_filename(uid), 'r+') as f:
            history = json.load(f)
            history.append({
                'prompt': prompt,
                'timestamp': datetime.now().strftime('%Y%m%d %H:%M:%S')
            })
            f.seek(0)
            json.dump(history, f, indent=2, ensure_ascii=False)
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f"prompt 保存失败: {str(e)}"}), 500

def delete_prompt_record(uid, timestamp):
    try:
        with open(get_prompt_filename(uid), 'r+') as f:
            history = json.load(f)
            history = [item for item in history if item['timestamp'] != timestamp]
            f.seek(0)
            f.truncate()
            json.dump(history, f, indent=2, ensure_ascii=False)
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f"prompt 删除失败: {str(e)}"}), 500