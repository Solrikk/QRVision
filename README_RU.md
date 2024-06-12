<p align="center">
  <img src="https://github.com/Solrikk/QRVision/blob/main/assets/photo/scanner.png" alt="Логотип" width="300">
</p>

<div align="center"> <h3> <a href="https://github.com/Solrikk/QRVision/blob/main/README.md">Английский</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_RU.md">⭐Русский⭐</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_GE.md">Немецкий</a> | <a href="https:///Solrikk/QRVision/blob/main/README_JP.md">Японский</a> | <a href="README_KR.md">Корейский</a> | <a href="README_CN.md">Китайский</a> </h3> </div>

-----------------

**`QRVision`** — это веб-сервис для сканирования QR-кодов, где фронтенд взаимодействует с оператором для захвата изображения через камеру, а бекенд обрабатывает это изображение и пытается извлечь данные из QR-кодов в базу данных.

## ⚠️ Начало работы с QRVision: ⚠️
Этот раздел предназначен для того, чтобы познакомить вас с основами работы с проектом "QRVision". Давайте пройдем через детали пошагово:

1. Python 3.10: Убедитесь, что у вас установлена версия Python 3.10. Вы можете скачать её с официального сайта Python.
2. Node.js: Убедитесь, что у вас установлен Node.js для управления зависимостями фронтенда. Скачайте его с сайта Node.js.
3. Poetry: Установите Poetry для управления зависимостями Python. Вы можете установить его, выполнив следующую команду:

**_Настройка бекенда:_**

```Shell Script
curl -sSL https://install.python-poetry.org | python3 -
```
## Настройка бекенда
1. Клонируйте репозиторий:

```Shell Script
git clone https://github.com/Solrikk/QRVision.git
cd QRVision
```
2. Установите зависимости Python:

```Shell Script
poetry install
```

**_Настройка фронтенда:_**

1. Перейдите в директорию static:
```Shell Script
cd static
```

2. Установите зависимости Node.js (если есть, иначе пропустите):
```Shell Script
npm install
```
3. Запустите фронтенд (если нужно, иначе пропустите):
Здесь нет специальных команд для запуска фронтенд файлов, поскольку Flask обслуживает статические файлы. Убедитесь, что Flask запущен для обслуживания фронтенда.

**_Запуск приложения:_**
1. Доступ к приложению:
Откройте ваш веб-браузер и перейдите по адресу http://127.0.0.1:5000. Вы должны увидеть основное интерфейс приложения.
2. Использование QR-сканера:
-  Разрешите доступ к вашей веб-камере, когда будет предложено.
-  Разместите QR-код в пределах видимости вашей веб-камеры.
-  Нажмите кнопку "Сканировать QR-код".
-  Захваченное изображение будет отправлено на сервер для обработки.

<img src="https://github.com/Solrikk/QRVision/blob/main/assets/photo/1fbf8bf5b.jpg" width="65%" /> 

Дополнительные заметки
- Коды доступа для администратора и оператора:
 -  Используйте код **1111** для доступа к интерфейсу оператора.
 -  Используйте код **2222** для доступа к интерфейсу администратора.
 -  Эти коды могут быть изменены в файле access.js при необходимости.

<img src="https://github.com/Solrikk/QRVision/blob/main/assets/photo/560bce24.jpg" width="65%" /> 

## Функции ⚙️

### _Технологический стек:_

### _Бекенд:_

- **`Python`**: Основной язык программирования, используемый для реализации серверной части проекта.
- **`Flask`**: Легковесный, но мощный веб-фреймворк для создания и развертывания веб-приложений. Flask предоставляет все необходимые инструменты и библиотеки для создания серверных функций и основан на принципе расширяемости.
- **`OpenCV`**: Библиотека компьютерного зрения, используемая для обработки изображений. Мы используем её для выполнения различных операций преобразования изображений, помогающих улучшить распознавание QR-кодов, включая фильтрацию шумов и коррекцию искажений.
- **`pyzbar`**: Специализированная библиотека для декодирования QR-кодов. Она обеспечивает точное и быстрое считывание информации с QR-кодов, что имеет критически важное значение.
- **`scikit-learn`**: Одна из ведущих библиотек машинного обучения, используемая для универсальной обработки данных. В нашем проекте, она используется для анализа текста с помощью алгоритма TF-IDF (Term Frequency-Inverse Document Frequency), который позволяет эффективно анализировать и классифицировать текстовые данные.
- **`numpy`**: Высокопроизводительная библиотека для численных вычислений, работающая с многомерными массивами и матрицами. Она предоставляет множество математических функций, делая её незаменимой для обработки данных и выполнения сложных расчетов.

### _Фронтенд:_

- **`HTML`**: Язык разметки, используемый для создания структуры веб-страницы. С его помощью можно определить различные элементы страницы, такие как заголовки, абзацы, формы и кнопки.
- **`CSS`**: Язык таблиц стилей, используемый для стилизации элементов HTML. С его помощью можно задать цвет, шрифты, размеры, отступы и другие визуальные характеристики элементов веб-страницы.
- **`JavaScript`**: Язык программирования, используемый для добавления интерактивности на веб-страницу. В этом проекте он необходим для управления взаимодействием с оператором, например, для захвата изображения с камеры и отправки его на сервер.

### _Дополнительные зависимости:_

- **`Poetry`**: Инструмент для управления зависимостями и создания изолированных виртуальных сред в Python. Poetry упрощает установку и обновление пакетов, а также управление версиями, обеспечивая консистентность и воспроизводимость сред.
- **`pyright`**: Быстрый и мощный статический анализатор типов для Python, который помогает выявлять ошибки типов до выполнения кода, тем самым повышая надежность и качество программного обеспечения.
- **`ruff`**: Линтер, предназначенный для улучшения качества кода и поддержания стиля. Ruff помогает выявлять и исправлять стилистические ошибки, обеспечивая консистентность и чистоту кода в соответствии с установленными стандартами.

### _Развертывание:_

- **`Gunicorn`**: Высокопроизводительный WSGI HTTP сервер для запуска Flask приложений в производственной среде. Gunicorn обеспечивает масштабируемость и надежность вашего веб-приложения, позволяя ему обрабатывать большое количество одновременных запросов и обеспечивать стабильную работу сервиса.

### _File Structure:_

```shell
/app
├── .replit
├── static
│   ├── script.js
│   └── styles.css
├── main.py
├── pyproject.toml
├── templates
│   └── index.html
├── ...
├── replit.nix
├── models.py
```
_This project structure organizes code and resources logically, simplifying development and maintenance of the application._

- **`main.py`**: The main backend file containing Flask routes and logic for image and QR code processing.
- **`templates/index.html`**: An HTML template for the main page of the application.
- **`pyproject.toml`**: A configuration file for managing project dependencies and code linting settings (Pyright and Ruff).

___

- **OpenCV (Open Source Computer Vision Library)** — is used for performing various tasks related to image processing and QR code recognition. OpenCV is a powerful tool for computer vision and image processing, providing a wide range of functions and modules, including filtering, shape transformation, object recognition, and more. With its extensive capabilities, OpenCV enables efficient image processing to improve the quality of scanning and accuracy of QR code recognition.

_Example of OpenCV in action:_
<img src="https://pbs.twimg.com/media/C2iLN6iW8AEbk5D.jpg:large">

## _The QR Code Scanning Process:_

1. When the page loads, a script is initiated that requests access to the user's webcam:

```javascript
navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Ошибка доступа к камере: ", err);
    });
```

2. The video stream from the webcam is displayed inside a **`<video>`** element, allowing the user to check the correct angle and position of the QR code before scanning. This element is placed in the center of the page for user convenience.

3. The operator clicks the "Scan QR Code" button. This action captures the current image from the webcam and draws it onto a **`<canvas>`** element.

```javascript
captureBtn.addEventListener('click', () => {
    setTimeout(() => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.style.display = 'block';
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
```

4. After drawing the image onto the `<canvas>` element, it is converted to **`Blob format`** and sent to the server endpoint **`/scan-qr/`** using the **`Fetch API`**:
```javascript
    canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'capture.png');

        fetch('/scan-qr/', {
            method: 'POST',
            body: formData
        })
```
5. On the server, Flask processes this request at the **`/scan-qr/`** endpoint. The image is first read and converted into an object using **Pillow (PIL)**:

```python
file = request.files['file']
contents = file.read()
image = Image.open(io.BytesIO(contents))
image_np = np.array(image)
```

6. The server performs several preprocessing steps on the image to improve the quality for reading QR codes. Preprocessing is done using a function called **`preprocess_image`** in multiple attempts:

```python
attempts = 12
decoded_objects = []
for attempt in range(attempts):
    processed_image = preprocess_image(image_np, attempt)
    decoded_objects = decode(Image.fromarray(processed_image))
    if decoded_objects:
        break
```
7. The library **`pyzbar`** is used to recognize and decode QR codes from preprocessed images:

```python
if decoded_objects:
    qr_data_list = []
    image_draw = ImageDraw.Draw(image)
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        qr_data_list.append(qr_data)
```

8. The server creates markers on the original image to show the location of the QR codes using **`OpenCV`**:

```python
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            cv2.polylines(image_np, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            text_position = (points[0].x, points[0].y - 10)
            image_draw.text(text_position, f"QR", fill=(255, 0, 0))
```

<img src="https://link-akyoning.replit.app/files/photo_2024-05-28_14-18-24.jpg">

9. An **`alert`** is displayed on the client side with the QR code scanning results:

```javascript
.then((data) => {
        alert('Данные QR-кода: ' + data.data);
        canvas.style.display = 'none';
    })
    .catch(error => {
        console.error('Ошибка:', error);
        canvas.style.display = 'none';
    });
```

<img src="https://link-akyoning.replit.app/files/photo_2024-05-28_14-42-14.jpg">
