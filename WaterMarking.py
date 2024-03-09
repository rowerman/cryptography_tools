from blind_watermark import WaterMark
from datetime import datetime
from PIL import Image

def embed_text(image_path, text):
    # 初始化嵌入器
    bwm1 = WaterMark(password_img=1, password_wm=1)
    # 获取待嵌入水印图片路径
    bwm1.read_img(image_path)
    # 获取待嵌入文字
    watermark = text
    # 读取
    bwm1.read_wm(watermark, mode='str')
    # 嵌入
    now = datetime.now()
    time_string = now.strftime("%Y%m%d_%H%M%S_")
    len_wm = len(bwm1.wm_bit)
    output_path = './output/embed_text/' + time_string + str(len_wm) + "_embedded.png"
    # output_path = './output/embedded.png'
    bwm1.embed(output_path)
    
    len_wm = len(bwm1.wm_bit)
    print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
    return len_wm, output_path
    
def get_text(image_path,len_wm):
    bwm1 = WaterMark(password_img=1, password_wm=1)
    wm_extract = bwm1.extract(image_path, wm_shape=len_wm, mode='str')
    print(wm_extract)
    
    
""" Image_path = './pictures/4.jpg'
Text = 'hello world'
len_wm, outputPath = embed_text(Image_path, Text)
get_text(outputPath, len_wm) """

def embed_img(img_path, wm_path):
    bwm1 = WaterMark(password_wm=1, password_img=1)
    # read original image
    bwm1.read_img(img_path)
    # read watermark
    bwm1.read_wm(wm_path)
    # embed
    now = datetime.now()
    time_string = now.strftime("%Y%m%d_%H%M%S_")
    img = Image.open(wm_path)
    width, height = img.size
    output_path = './output/embed_picture/' + time_string + str(width) + '_' + str(height) + "_embedded.png"      
    
    bwm1.embed(output_path)
    return output_path, width, height

def get_img(image_path, width, height):
    bwm1 = WaterMark(password_wm=1, password_img=1)
    # notice that wm_shape is necessary
    now = datetime.now()
    time_string = now.strftime("%Y%m%d_%H%M%S_")
    output_path = './output/solved_picture/' + time_string + str(width) + '_' + str(height) + "_embedded.png"   
    bwm1.extract(filename=image_path, wm_shape=(height, width), out_wm_name=output_path, )

""" img_path = './pictures/4.jpg'
wm_path = './pictures/watermark.png'
output_path, width, height = embed_img(img_path, wm_path)
get_img(output_path, width, height)
 """
