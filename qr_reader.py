import logging
import json
import cv2 as cv
import pyzbar.pyzbar as pyzbar

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class QRReader:
    QUIT_KEY = 'q'

    def __init__(self):
        self.cap:cv.VideoCapture = cv.VideoCapture(0)
        self.codes = {}

        if not self.cap.isOpened():
            logger.error("Cannot open camera")
            raise Exception("Could not open video capture")

    def read(self):
        while cv.waitKey(1) != ord(QRReader.QUIT_KEY):
            ret, frame = self.cap.read()

            if not ret:
                logger.info("Can't receive frame (stream end?). Exiting...")
                break
            cv.imshow('frame', cv.flip(frame, flipCode=1))
            self.detect_and_decode(frame)

        print(json.dumps(self.codes))
        self.cap.release()
        cv.destroyAllWindows()

    def detect_and_decode(self, frame):
        decoded = pyzbar.decode(frame)
        for obj in decoded:
            url = str(obj.data, "utf-8")
            if "http" not in url:
                continue
            if url not in self.codes:
                self.codes[url] = url
                logger.info(f"New code added. Total count: {len(self.codes)}. Code added: {url}")

