from PIL import Image
import math

def img_token_calculate(img_stream):
    '''根据阿里云百炼平台给出的方法计算上传的图像的 token 数'''
    image = Image.open(img_stream)

    height = image.height
    width = image.width
    h_bar = round(height / 28) * 28
    w_bar = round(width / 28) * 28

    # 图像的Token下限：4个Token
    min_pixels = 28 * 28 * 4
    # 图像的Token上限：1280个Token
    max_pixels = 1280 * 28 * 28
        
    # 对图像进行缩放处理，调整像素的总数在范围[min_pixels,max_pixels]内
    if h_bar * w_bar > max_pixels:
        # 计算缩放因子beta，使得缩放后的图像总像素数不超过max_pixels
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = math.floor(height / beta / 28) * 28
        w_bar = math.floor(width / beta / 28) * 28
    elif h_bar * w_bar < min_pixels:
        # 计算缩放因子beta，使得缩放后的图像总像素数不低于min_pixels
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = math.ceil(height * beta / 28) * 28
        w_bar = math.ceil(width * beta / 28) * 28
    
    token_cnt = int((h_bar * w_bar) / (28 * 28)) + 2
    return token_cnt