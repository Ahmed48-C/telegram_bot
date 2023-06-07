import qrcode
from io import BytesIO

def text_to_qrcode(text):
    try:
        img = qrcode.make(text)

        # Convert image to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
    except:
        return "Failed to generate qrcode, try again later."