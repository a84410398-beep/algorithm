# =====================================================================
# 고정 길이 큐 (Fixed-Size Circular Queue) 서버 - 구글 클라우드 런 (Python Flask)
# ---------------------------------------------------------------------
# 서버 기능:
#  1) 초기화(init)  2) push / pop  3) 현재 데이터 개수(size)
#  4) 상태 검사(full, empty)  5) 전면(Front) 데이터 확인(peek)
#  6) 큐 전체 데이터 삭제(clear)  7) 값의 index 검색(find)
#  8) 값의 개수(count)  9) 값의 존재 여부 검사(contains)
#  10) Front부터 Rear까지 출력(dump)
# =====================================================================
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS(Cross-Origin Resource Sharing) 설정: 다른 도메인에서의 요청 허용


class FixedQueue:
    """리스트 기반 원형 큐 (Circular Queue) 클래스

    - queue    : 고정 크기 리스트 (capacity 칸)
    - front    : 맨 앞 데이터의 위치 (pop / peek 할 위치)
    - rear     : 다음 데이터가 들어갈 위치 (push 할 위치)
    - count    : 현재 들어있는 데이터 개수
    - 인덱스 이동은 (index + 1) % capacity → 끝에 도달하면 0으로 돌아감 (원형)
    """

    def __init__(self, capacity=20):
        """1) 초기화: 크기 capacity의 빈 큐 생성 - O(N)"""
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = 0
        self.count = 0

    def is_empty(self):
        """4) 상태 검사: 비어 있으면 True - O(1)"""
        return self.count == 0

    def is_full(self):
        """4) 상태 검사: 가득 찼으면 True - O(1)"""
        return self.count == self.capacity

    def size(self):
        """3) 현재 데이터 개수 반환 - O(1)"""
        return self.count

    def push(self, value):
        """2) 데이터 삽입 (rear 위치에 저장) - O(1)"""
        if self.is_full():
            return {"success": False, "error": "오류: 큐가 가득 찼습니다 (Queue is full)"}
        self.queue[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity  # rear를 원형으로 한 칸 이동
        self.count += 1
        return {"success": True, "pushed": value, "count": self.count}

    def pop(self):
        """2) 데이터 추출 (front 위치에서 꺼냄) - O(1)"""
        if self.is_empty():
            return {"success": False, "error": "오류: 큐가 비어 있습니다 (Queue is empty)"}
        value = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity  # front를 원형으로 한 칸 이동
        self.count -= 1
        return {"success": True, "popped": value, "count": self.count}

    def peek(self):
        """5) 전면(Front) 데이터 확인 (꺼내지 않음) - O(1)"""
        if self.is_empty():
            return {"success": False, "error": "오류: 큐가 비어 있습니다 (Queue is empty)"}
        return {"success": True, "peek": self.queue[self.front]}

    def clear(self):
        """6) 큐 전체 데이터 삭제 - O(N)"""
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = 0
        self.count = 0
        return {"success": True, "message": "큐 전체 데이터가 삭제되었습니다 (Queue cleared)"}

    def find(self, value):
        """7) 값의 index 검색 + 8) 값의 개수 - O(N)
        index는 front 기준 상대 위치 (0부터 시작)"""
        indices = []
        for i in range(self.count):
            idx = (self.front + i) % self.capacity  # front부터 i번째 실제 위치
            if self.queue[idx] == value:
                indices.append(i)
        return {"success": True, "value": value, "indices": indices, "count": len(indices)}

    def contains(self, value):
        """9) 값의 존재 여부 검사 - O(N)"""
        for i in range(self.count):
            idx = (self.front + i) % self.capacity
            if self.queue[idx] == value:
                return {"success": True, "value": value, "exists": True}
        return {"success": True, "value": value, "exists": False}

    def dump(self):
        """10) Front부터 Rear까지 출력 - O(N)"""
        elements = []
        for i in range(self.count):
            idx = (self.front + i) % self.capacity
            elements.append(self.queue[idx])
        return {
            "success": True,
            "queue": elements,          # front → rear 순서의 데이터
            "raw_array": self.queue,    # 실제 내부 배열 (시각화용)
            "front": self.front,
            "rear": self.rear,
            "count": self.count,
            "capacity": self.capacity,
        }


# 전역 큐 인스턴스 (메모리에 저장 → 배포 시 --max-instances 1 필수)
q_instance = FixedQueue(capacity=20)


# ---------------------------------------------------------------------
# 서버 동작 상태 페이지 (캡처용)
# ---------------------------------------------------------------------
@app.route("/")
def home():
    d = q_instance.dump()
    html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <title>고정 길이 큐 서버 상태</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6f9; color: #333; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        .status { font-weight: bold; color: #27ae60; }
        ul { line-height: 1.8; }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>구글 클라우드 런 - 고정 길이 큐 서버</h1>
        <p>서버 상태: <span class="status">Running (정상 동작 중)</span></p>
        <hr>
        <h3>현재 큐 상태 (Queue Status)</h3>
        <ul>
          <li><b>Capacity (용량):</b> {{ capacity }}</li>
          <li><b>Count (데이터 개수):</b> {{ count }}</li>
          <li><b>Full / Empty:</b> {{ full }} / {{ empty }}</li>
          <li><b>Front 위치:</b> {{ front }}</li>
          <li><b>Rear 위치:</b> {{ rear }}</li>
          <li><b>현재 큐 내용 (Front ~ Rear):</b> {{ queue }}</li>
        </ul>
        <h3>API 목록</h3>
        <ul>
          <li>POST /api/init, /api/push, /api/pop, /api/clear</li>
          <li>GET /api/size, /api/status, /api/peek, /api/find, /api/contains, /api/dump</li>
        </ul>
      </div>
    </body>
    </html>
    """
    return render_template_string(
        html,
        capacity=d["capacity"], count=d["count"],
        full=q_instance.is_full(), empty=q_instance.is_empty(),
        front=d["front"], rear=d["rear"], queue=d["queue"],
    )


# ---------------------------------------------------------------------
# REST API (모든 응답은 JSON)
# ---------------------------------------------------------------------
@app.route("/api/init", methods=["POST"])
def api_init():
    """1) 초기화"""
    global q_instance
    data = request.get_json(silent=True) or {}
    capacity = int(data.get("capacity", 20))
    q_instance = FixedQueue(capacity=capacity)
    return jsonify({"success": True, "message": f"큐 초기화 완료 (capacity={capacity})", "capacity": capacity})


@app.route("/api/push", methods=["POST"])
def api_push():
    """2) push"""
    data = request.get_json(silent=True) or {}
    if "value" not in data:
        return jsonify({"success": False, "error": "value 값이 필요합니다"})
    return jsonify(q_instance.push(int(data["value"])))


@app.route("/api/pop", methods=["POST"])
def api_pop():
    """2) pop"""
    return jsonify(q_instance.pop())


@app.route("/api/size", methods=["GET"])
def api_size():
    """3) 현재 데이터 개수"""
    return jsonify({"success": True, "size": q_instance.size(), "capacity": q_instance.capacity})


@app.route("/api/status", methods=["GET"])
def api_status():
    """4) 상태 검사 (full, empty)"""
    return jsonify({
        "success": True,
        "is_full": q_instance.is_full(),
        "is_empty": q_instance.is_empty(),
        "size": q_instance.size(),
        "capacity": q_instance.capacity,
    })


@app.route("/api/peek", methods=["GET"])
def api_peek():
    """5) 전면 데이터 확인"""
    return jsonify(q_instance.peek())


@app.route("/api/clear", methods=["POST"])
def api_clear():
    """6) 큐 전체 데이터 삭제"""
    return jsonify(q_instance.clear())


@app.route("/api/find", methods=["GET"])
def api_find():
    """7) 값의 index 검색 + 8) 값의 개수"""
    val = int(request.args.get("value", 0))
    return jsonify(q_instance.find(val))


@app.route("/api/contains", methods=["GET"])
def api_contains():
    """9) 값의 존재 여부 검사"""
    val = int(request.args.get("value", 0))
    return jsonify(q_instance.contains(val))


@app.route("/api/dump", methods=["GET"])
def api_dump():
    """10) Front부터 Rear까지 출력"""
    return jsonify(q_instance.dump())


if __name__ == "__main__":
    # 로컬 테스트용 (Cloud Run에서는 gunicorn이 실행)
    app.run(host="0.0.0.0", port=8080)
