from ultralytics import YOLO
from PIL import Image


# Load a pretrained YOLO model (recommended for training)
model = YOLO("/Users/Admin/Downloads/Test CV/phat_hien_bien_so_xe.pt")

results = model("/Users/Admin/Downloads/Test CV/test7.png")

for r in results:
    print(r.boxes)
    im_array = r.plot()
    im = Image.fromarray(im_array[..., ::-1])
    im.show()
    im.save('results_test.png')