# 파이썬 공식 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필수 라이브러리 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 구글 클라우드 런 포트(8080) 개방
EXPOSE 8080

# Gunicorn을 이용해 Flask 서버 구동
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
