import easyocr
from core.config import OCR_LANG, OCR_GPU

class LicensePlateReader:
    def __init__(self):
        # Initialize EasyOCR Reader
        self.reader = easyocr.Reader(OCR_LANG, gpu=OCR_GPU)

    def read_plate(self, crop):
        """
        Extract text from an image crop containing the license plate.
        Returns: (plate_text, confidence)
        """
        ocr_results = self.reader.readtext(crop)
        plate_text = ""
        plate_conf = 0.0
        
        if ocr_results:
            # take highest confidence text result
            plate_text = ocr_results[0][1]
            plate_conf = float(ocr_results[0][2])
            
        return plate_text, plate_conf
