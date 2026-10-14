import hashlib
import time
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/compute-hash", methods=["POST"])
def compute_hash():
  """클라이언트로부터 데이터를 받아 해시 알고리즘을 수행하고

  단계별 결과 및 복잡도 정보를 반환하는 API 엔드포인트
  """
  start_time = time.time()

  # 클라이언트 요청 데이터 파싱
  req_data = request.get_json() or {}
  input_text = req_data.get("text", "Default Input Data")

  steps = []
  current_data = input_text.encode("utf-8")

  # 단계 1: 데이터 패딩 (Padding) 과정 시뮬레이션
  padded_data = current_data + b"\x80"
  steps.append({
      "step": 1,
      "name": "데이터 패딩 (Padding)",
      "data": padded_data.hex(),
      "description": (
          "입력 데이터에 비트 '1'과 패딩 비트를 추가하여 블록 크기에 맞춤"
      ),
  })

  # 단계 2: 초기 해시값 설정 (Initial Hash Values)
  h_val = "6a09e667"  # SHA-256 초기값 중 일부 예시
  steps.append({
      "step": 2,
      "name": "초기 해시값 설정",
      "data": h_val,
      "description": "해시 연산을 시작하기 위한 표준 초기 상수(IV) 로드",
  })

  # 단계 3: 해시 압축 함수 / 라운드 연산 수행 (Hashing Round)
  # 여기서는 시연을 위해 hashlib을 이용해 단계별 해시 축약 과정을 시뮬레이션
  hasher = hashlib.sha256()
  hasher.update(current_data)
  final_hash = hasher.hexdigest()

  steps.append({
      "step": 3,
      "name": "압축 함수 및 최종 해시 생성",
      "data": final_hash,
      "description": "비트 연산 및 모듈러 연산을 거쳐 최종 256비트 해시값 생성 완료",
  })

  # 연산 시간 측정 (복잡도 분석용)
  execution_time = (time.time() - start_time) * 1000  # 밀리초(ms)

  # 서버 응답 데이터 구성
  response = {
      "status": "success",
      "server_status": "정상 작동 중 (Running)",
      "input": input_text,
      "final_hash": final_hash,
      "steps": steps,
      "complexity": {
          "time_complexity": "O(N) - 입력 데이터 길이에 비례",
          "space_complexity": "O(1) - 고정된 메모리 버퍼 사용",
          "execution_time_ms": round(execution_time, 2),
      },
  }

  return jsonify(response)


if __name__ == "__main__":
  # 클라우드 런 환경에서는 포트 8080을 기본으로 사용
  app.run(host="0.0.0.0", port=8080)
