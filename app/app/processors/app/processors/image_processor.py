from PIL import Image
import pytesseract




def ocr_image(path: str) -> str:
img = Image.open(path)
text = pytesseract.image_to_string(img)
return text
