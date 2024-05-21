# Приложение "QRVision" - Техническая документация

## Описание

**`QRVision`** — представляет собой веб-сервис для сканирования QR-кодов, где фронтенд взаимодействует с оператором для захвата изображения через камеру, а бэкенд обрабатывает это изображение и пытается извлечь данные из QR-кодов в базу данных.

## Основные компоненты

### _Стек технологий:_

 ### _Backend:_

- **`Python`**: Основной язык программирования проекта.
- **`Flask`**: Веб-фреймворк для создания веб-приложений.
- **`OpenCV`**: Библиотека компьютерного зрения для обработки изображений.
- **`pyzbar`**: Библиотека для декодирования QR-кодов.
- **`scikit-learn`**: Библиотека машинного обучения (используется для обработки данных с TF-IDF).
- **`numpy`**: Библиотека для численных вычислений в Python.
 
 ### _Frontend:_

- **`HTML`**: Язык разметки для создания веб-страницы.
- **`CSS`**: Язык стилей для оформления веб-страницы.
- **`JavaScript`**: Для взаимодействия с пользователем (захват изображения с камеры и отправка на сервер).

  ### _Дополнительные зависимости:_

- **`Poetry`**: Инструмент для управления зависимостями и создания виртуальных окружений в Python.
- **`pyright`**: Статический анализатор типов для Python.
- **`ruff`**: Линтер для улучшения качества кода и соблюдения стиля.

### _Deployment:_

- **`Gunicorn`**: WSGI HTTP сервер для запуска Flask-приложения в производственной среде.

 ### _Файловая структура:_

```shell
/app
├── .replit
├── static
│   ├── script.js
│   └── styles.css
├── main.py
├── pyproject.toml
├── templates
│   └── index.html
├── ...
├── replit.nix
```

- **`main.py`**: Основной backend файл, содержаший Flask маршруты и логику обработки изображений и QR-кодов.
- **`templates/index.html`**: HTML-шаблон для главной страницы приложения.
- **`pyproject.toml`**: Файл конфигурации для управления зависимостями проекта и настройки релевации кода (Pyright и Ruff).
________

  - **OpenCV (Open Source Computer Vision Library)** — используется для различных задач, связанных с обработкой изображений и распознаванием QR-кодов. OpenCV является мощным инструментом для компьютерного зрения и обработки изображений с множеством функций и модулей:

### _Процесс сканирования QR-кодов:_

1. **Загрузка изображения**:
    - При нажатии на кнопку сканирования `JavaScript` захватывает изображение с камеры и отправляет его на сервер через `POST-запрос` .

2. **Получение изображения на сервере**: 
 - Flask получает изображение через эндпоинт `/scan-qr/`.
    - `main.py`: Серверный код получает изображение, используя Flask, и читает его содержимое.

3. **Предобработка изображения**: 
- С помощью **`OpenCV`** изображение преобразуется для улучшения видимости QR-кода.
    - В функции `preprocess_image` изображение может быть конвертировано в серый цвет, заблюрено, повёрнуто или подвергнуто адаптивному пороговому преобразованию.

4. **Декодирование QR-кода**: 
- Библиотека **`Pyzbar`** декодирует QR-коды на обработанном изображении.
    - `main.py`: Функция `decode` из Pyzbar пытается распознать QR-коды на каждом этапе предобработки изображения.

5. **Результат декодирования**: 
- Если QR-код был успешно распознан, данные из QR-кода сохраняются.
    - `main.py`: Считанные данные сохраняются в **`PostgreSQL`**

6. **Возврат результата на клиент**: 
- Результаты обработки, включая декодированные данные и обработанное изображение, возвращаются оператору.
   - Сервер кодирует обработанное изображение в Base64, чтобы вернуть его в формате JSON через Flask.
   - Оператору отображается результат на веб-странице.


### Сканирование QR-кода (`scan_qr`)


```python
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
  elif attempt == 6:
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
  elif attempt == 7:
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
  elif attempt == 8:
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 50, 150)
  elif attempt == 9:
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    dilated = cv2.dilate(gray, np.ones((3, 3), np.uint8), iterations=1)
    return cv2.erode(dilated, np.ones((3, 3), np.uint8), iterations=1)
  elif attempt == 10:
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
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

    image_np = np.array(image)

    attempts = 10
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
```
