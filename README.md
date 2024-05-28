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
