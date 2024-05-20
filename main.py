from flask import Flask, request, jsonify, render_template
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import io
import cv2
import numpy as np
import base64
import csv

app = Flask(__name__)


def preprocess_image(image_np, attempt):
  if attempt == 0:
    return image_np
  elif attempt == 1:
    return cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
  elif attempt == 2:
    return cv2.GaussianBlur(image_np, (5, 5), 0)
  elif attempt == 3:
    return cv2.rotate(image_np, cv2.ROTATE_90_CLOCKWISE)
  elif attempt == 4:
    return cv2.rotate(image_np, cv2.ROTATE_180)
  elif attempt == 5:
    return cv2.rotate(image_np, cv2.ROTATE_90_COUNTERCLOCKWISE)
  return image_np


@app.route("/", methods=['GET'])
def read_root():
  return render_template('index.html')


@app.route("/scan-qr/", methods=['POST'])
def scan_qr():
  try:
    file = request.files['file']
    contents = file.read()
    image = Image.open(io.BytesIO(contents))

    # Convert image to OpenCV format
    image_np = np.array(image)

    attempts = 6
    decoded_objects = []

    for attempt in range(attempts):
      processed_image = preprocess_image(image_np, attempt)
      decoded_objects = decode(Image.fromarray(processed_image))

      if decoded_objects:
        break

    if decoded_objects:
      qr_data_list = []
      image_draw = ImageDraw.Draw(image)

      for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        qr_data_list.append(qr_data)

        points = obj.polygon
        if len(points) == 4:
          pts = np.array(points, dtype=np.int32)
          cv2.polylines(image_np, [pts],
                        isClosed=True,
                        color=(0, 255, 0),
                        thickness=2)

          text_position = (points[0].x, points[0].y - 10)
          image_draw.text(text_position, f"QR", fill=(255, 0, 0))

      marked_image = Image.fromarray(image_np)
      marked_image.save("marked_image.png")

      _, buffer = cv2.imencode('.png', image_np)
      encoded_image = io.BytesIO(buffer).getvalue()

      with open("qr_data.txt", "a") as file:
        for idx, qr_data in enumerate(qr_data_list):
          file.write(f"Data: {qr_data}\n")

      with open("qr_data.csv", "a", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for idx, qr_data in enumerate(qr_data_list):
          csvwriter.writerow([qr_data])

      encoded_image_b64 = base64.b64encode(encoded_image).decode('utf-8')

      return jsonify({
          "data": qr_data_list,
          "processed_image": encoded_image_b64
      })
    else:
      return jsonify({"data": "No QR code found."})
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
