<div align="center"> <h3> <a href="https://github.com/Solrikk/QRVision/blob/main/README.md">영어</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_RU.md">러시아어</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_GE.md">독일어</a> | <a href="https://github.com/Solrikk/QRVision/blob/main/README_JP.md">일본어</a> | <a href="README_KR.md">⭐한국어⭐</a> | <a href="README_CN.md">중국어</a> </h3> </div>

-----------------

**`QRVision`** — 는 카메라를 사용해 이미지를 캡처하기 위해 프론트엔드가 사용자와 상호작용하고, 백엔드는 이 이미지를 처리하여 QR 코드의 데이터를 데이터베이스에 추출하려는 웹 서비스입니다.

## 주요 구성 요소

### _기술 스택:_

### _백엔드:_

- **`Python`**: 프로젝트의 주요 프로그래밍 언어.
- **`Flask`**: 웹 애플리케이션을 작성하기 위한 웹 프레임워크.
- **`OpenCV`**: 이미지 처리를 위한 컴퓨터 비전 라이브러리.
- **`pyzbar`**: QR 코드를 디코딩하기 위한 라이브러리.
- **`scikit-learn`**: 머신 러닝 라이브러리 (TF-IDF 데이터 처리를 위해 사용됨).
- **`numpy`**: 파이썬에서의 수치 계산을 위한 라이브러리.
- **`SQLAlchemy`**: 데이터베이스 작업을 위한 ORM.
- **`PostgreSQL`**: QR 코드 및 관련 데이터를 저장하기 위한 DBMS.

### _프론트엔드:_

- **`HTML`**: 웹 페이지를 작성하기 위한 마크업 언어.
- **`CSS`**: 웹 페이지의 스타일링을 위한 스타일시트 언어.
- **`JavaScript`**: 사용자가 상호작용하기 위한 언어 (카메라를 사용한 이미지 캡처 및 서버로 전송).

### _추가 종속성:_

- **`Poetry`**: 파이썬의 종속성 관리 및 가상 환경 생성을 위한 도구.
- **`pyright`**: 파이썬을 위한 정적 타입 검사기.
- **`ruff`**: 코드 품질 및 스타일 준수를 향상시키기 위한 린터.

### _배포:_

- **`Gunicorn`**: 프로덕션 환경에서 Flask 앱을 실행하기 위한 WSGI HTTP 서버.

### _파일 구조:_

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
├── models.py
```
