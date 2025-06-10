class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = 'def-a-name'
    SECURITY_PASSWORD_SALT = 'name-a-def'
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_LOGIN_URL = '/security-login'
    SECURITY_REGISTERABLE = False
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = False
    SECURITY_USER_IDENTITY_ATTRIBUTES = [
        {
            'username': {
                'mapper': lambda x: x.strip().lower(),
                'case_insensitive': True
            }
        }
    ]
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jpe', 'tif', 'tiff', 'webp', 'bmp', 'heic'}
    MAX_IMAGE_SIZE = 10 * 1024 * 1024   # 限制图片最大为 10MB
    TOKEN_PIXEL_SIZE = 28               # 每个图像 token 为 28x28 像素 
    PROMPT_HISTORY_FILE = 'prompts/history.json'
    DEFAULT_PROMPT = \
'''
任务：描述图片的内容；
关注点：主要对象；周边场景的细节；整体风格以及可能传达的情感；
输出格式：markdown；
提示：如果无法辨认某些细节，请注明“无法判断”；
'''