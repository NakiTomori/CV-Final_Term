from ultralytics import YOLO
import cv2
from PIL import Image

import util
from util import read_license_plate, write_csv


results = {}

# load models
model_path = 'phat_hien_bien_so_xe.pt'
license_plate_detector = YOLO(model_path)

# read and load image
img_path = 'test9.jpg'
img = cv2.imread(img_path)

# detect license plates
license_plates = license_plate_detector(img)
for license_plate in license_plates:
    for i in license_plate.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = i

for license_plate in license_plates:
    if license_plate.boxes.data.tolist() != []:
        # crop license plate
        license_plate_crop = img[int(y1):int(y2), int(x1): int(x2), :]

        # process license plate
        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
        _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

        # read license plate number
        license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
        if license_plate_text is not None:
            results = {'license_plate': {'bbox': [x1, y1, x2, y2],
                                        'text': license_plate_text,
                                        'bbox_score': score,
                                        'text_score': license_plate_text_score}}
            print("License plate text: ", license_plate_text)
            print("License plate text score: ",license_plate_text_score)
            # #write results
            # write_csv(results, './test.csv')
    else:
        print("No license plate detected")
