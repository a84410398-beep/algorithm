# 경량화된 파이썬 베이스 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# Cloud Run 포트 환경변수 설정 (기본값 8080)
ENV PORT 8080

# Production용 WSGI 서버인 Gunicorn으로 실행 (main.py의 app 객체 실행)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
