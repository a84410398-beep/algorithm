# 파이썬 공식 경량 이미지 사용
FROM python:3.11-slim

# 로그가 바로 출력되도록 설정
ENV PYTHONUNBUFFERED=True

# 작업 폴더
WORKDIR /app

# 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run이 지정하는 PORT(기본 8080)로 실행
# --workers 1 : 큐가 메모리에 저장되므로 워커를 1개로 고정 (여러 개면 큐가 나뉨)
# --threads 8 : 동시 요청은 스레드로 처리
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
