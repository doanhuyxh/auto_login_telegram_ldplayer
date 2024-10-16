from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def ocr_image(image_path, lang='eng'):
    image = Image.open(image_path)    
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, lang=lang, config=custom_config)
    return text

# Tìm vị trí của 1 từ trong ảnh
def get_text_positions(text, image_path, lang='eng'):
    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    for i in range(len(data['text'])):
        if data['text'][i].strip() == text:
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            
            # Tính toán tọa độ trung tâm
            center_x = x + w // 2
            center_y = y + h // 2
            
            return center_x, center_y
    
    return None

# Kiểm tra tồn tại của 1 câu trong ảnh
def check_paragraph_on_image(text, image_path, lang='eng'):
    image = Image.open(image_path)
    data = pytesseract.image_to_string(image, lang=lang)
    if text in data:
        return True
    return False

# Tìm vị trí của 1 câu trong ảnh
def get_paragraph_positions(paragraph, image_path, lang='eng'):
    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)   
    words = paragraph.split()
    num_words = len(words)
    
    for i in range(len(data['text']) - num_words + 1):
        match = True
        for j in range(num_words):
            if words[j] not in data['text'][i + j]:
                match = False
                break
        if match:
            x = min(data['left'][i:i + num_words])
            y = min(data['top'][i:i + num_words])
            w = max(data['left'][i:i + num_words]) + max(data['width'][i:i + num_words]) - x
            h = max(data['top'][i:i + num_words]) + max(data['height'][i:i + num_words]) - y
            
            # Tính toán tọa độ trung tâm
            center_x = x + w // 2
            center_y = y + h // 2
            
            return center_x, center_y
    
    return None