import json, os
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
    except Exception as e:
        print(f"prompt 保存失败: {e}")