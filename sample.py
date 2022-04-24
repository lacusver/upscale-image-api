import requests
from PIL import Image
import base64
from io import BytesIO


url = 'http://127.0.0.1:5000/upscale'

img_path = "test_imgs/cat.jpg" # enter path to your image

my_img = {'image': open(img_path, 'rb')}
r = requests.post(url, files=my_img)
dict_data = r.json()
img = dict_data["img"]
img = base64.b64decode(img) 
img = BytesIO(img) 
img = Image.open(img) 
img.save("result.png")