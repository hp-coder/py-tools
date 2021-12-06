import pytesseract
import requests as req
from PIL import Image
from io import BytesIO







if __name__ == '__main__':
    resp = req.get("http://www.78gk.com/tel/130/MTg1MjAyMDY2NTI=")
    text = pytesseract.image_to_string(Image.open(BytesIO(resp.content)),lang="eng")
    print(text)