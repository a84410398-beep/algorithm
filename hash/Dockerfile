# Python 공식 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run에서 요구하는 포트(8080) 개방
ENV PORT=8080

# Gunicorn을 사용하여 Flask 앱 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
