import easyocr
from core.config import OCR_LANG, OCR_GPU

class LicensePlateReader:
    def __init__(self):
        self.reader = easyocr.Reader(OCR_LANG, gpu=OCR_GPU)

    def read_plate(self, img):
        if img is None or img.size == 0:
            return "", 0.0
        results = self.reader.readtext(img)
        if results:
            # results format: [([[x, y], ...], text, conf), ...]
            # return text and confidence of the first valid result
            return results[0][1], results[0][2]
        return "", 0.0
