# Приложение "QRVision" - Техническая документация

## Описание

**`QRVision`** — представляет собой веб-сервис для сканирования QR-кодов, где фронтенд взаимодействует с апператором для захвата изображения через камеру, а бэкенд обрабатывает это изображение и пытается извлечь данные из QR-кодов в базу данных.

## Основные компоненты

### Стек технологий

 ### Backend:
- **`Python`**: Основной язык программирования проекта.
- **`Flask`**: Веб-фреймворк для создания веб-приложений.
- **`Gunicorn`**: WSGI HTTP сервер для развертывания приложения Flask.
- **`OpenCV`**: Библиотека компьютерного зрения для обработки изображений.
- **`pyzbar`**: Библиотека для декодирования QR-кодов.
- **`scikit-learn`**: Библиотека машинного обучения (используется для обработки данных с TF-IDF).
- **`numpy`**: Библиотека для численных вычислений в Python.
  ### Frontend:
- **`HTML`**: Язык разметки для создания веб-страницы.
- **`CSS`**: Язык стилей для оформления веб-страницы.
- **`JavaScript`**: Для взаимодействия с пользователем (захват изображения с камеры и отправка на сервер).
  ### Дополнительные зависимости:
- **`Poetry`**: Инструмент для управления зависимостями и создания виртуальных окружений в Python.
- **`pyright`**: Статический анализатор типов для Python.
- **`ruff`**: Линтер для улучшения качества кода и соблюдения стиля.

### Deployment

- **`Gunicorn`**: WSGI HTTP сервер для запуска Flask-приложения в производственной среде.

 ### Файловая структура:

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

### Процесс сканирования QR-кодов:

1. **Загрузка изображения**:
    - При нажатии на кнопку сканирования `JavaScript` захватывает изображение с камеры и отправляет его на сервер через `POST-запрос` .

2. **Получение изображения на сервере**: Flask получает изображение через эндпоинт `/scan-qr/`.
    - `main.py`: Серверный код получает изображение, используя Flask, и читает его содержимое.

3. **Предобработка изображения**: С помощью **`OpenCV`** изображение преобразуется для улучшения видимости QR-кода.
    - В функции `preprocess_image` изображение может быть конвертировано в серый цвет, заблюрено, повёрнуто или подвергнуто адаптивному пороговому преобразованию.

4. **Декодирование QR-кода**: Библиотека **`Pyzbar`** декодирует QR-коды на обработанном изображении.
    - `main.py`: Функция `decode` из Pyzbar пытается распознать QR-коды на каждом этапе предобработки изображения.

5. **Результат декодирования**: Если QR-код был успешно распознан, данные из QR-кода сохраняются.
    - `main.py`: Считанные данные сохраняются в **`PostgreSQL`**

6. **Возврат результата на клиент**: Результаты обработки, включая декодированные данные и обработанное изображение, возвращаются оператору.
   - Сервер кодирует обработанное изображение в Base64, чтобы вернуть его в формате JSON через Flask.
   - Оператору отображается результат на веб-странице.


### Сканирование QR-кода (`scan_qr`)

Код маршрута:

```python
@app.route("/scan-qr", methods=['POST'])
def scan_qr():
    try:
        file = request.files['file']
        if file.mimetype not in ['image/jpeg', 'image/png']:
            return jsonify({"error": "Invalid file type. Only JPEG and PNG are supported."}), 400
        if file.content_length > 5 * 1024 * 1024:
            return jsonify({"error": "File size exceeds limit of 5MB"}), 400

        contents = file.read()
        try:
            image = Image.open(io.BytesIO(contents))
        except Exception as e:
            return jsonify({"error": f"Error opening image: {str(e)}"}), 500

        image_np = np.array(image)
        attempts = 7
        decoded_objects = []

        for attempt in range(attempts):
            try:
                processed_image = preprocess_image(image_np, attempt)
                decoded_objects = decode(Image.fromarray(processed_image))
            except Exception as e:
                app.logger.error(f"Error during decoding attempt {attempt}: {str(e)}")
                continue
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
                    cv2.polylines(image_np, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
                    text_position = (points[0].x, points[0].y - 10)
                    image_draw.text(text_position, f"QR", fill=(255, 0, 0))

            marked_image = Image.fromarray(image_np)
            _, buffer = cv2.imencode('.png', np.array(marked_image))
            encoded_image = io.BytesIO(buffer).getvalue()

            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(qr_data_list)
            tfidf_scores = X.toarray()

            with open("qr_data.txt", "a") as txt_file:
                for idx, qr_data in enumerate(qr_data_list):
                    txt_file.write(f"Data: {qr_data}, TF-IDF Scores: {tfidf_scores[idx]}\n")

            with open("qr_data.csv", "a", newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                for idx, qr_data in enumerate(qr_data_list):
                    csvwriter.writerow([qr_data] + tfidf_scores[idx].tolist())

            encoded_image_b64 = base64.b64encode(encoded_image).decode('utf-8')
            return jsonify({
                "data": qr_data_list,
                "processed_image": encoded_image_b64
            })
        else:
            return jsonify({"error": "No QR code found."}), 404
    except Exception as e:
        app.logger.error(f"Error in /scan-qr route: {str(e)}")
        return jsonify({"error": str(e)}), 500
```
