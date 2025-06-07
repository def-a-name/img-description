import json, os
from flask import jsonify
from datetime import datetime
from config import Config

def save_prompt_to_history(prompt):
    try:
        with open(Config.PROMPT_HISTORY_FILE, 'r+') as f:
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

def delete_prompt_record(timestamp):
    try:
        with open(Config.PROMPT_HISTORY_FILE, 'r+') as f:
            history = json.load(f)
            history = [item for item in history if item['timestamp'] != timestamp]
            f.seek(0)
            f.truncate()
            json.dump(history, f, indent=2, ensure_ascii=False)
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f"prompt 删除失败: {str(e)}"}), 500