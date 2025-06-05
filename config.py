class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 限制图片最大为 10MB
    PROMPT_HISTORY_FILE = 'prompts/history.json'
    DEFAULT_PROMPT = "详细描述这张图片的内容，包括主要对象、场景、颜色、风格等细节"