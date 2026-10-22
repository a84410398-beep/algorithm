from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS(Cross-Origin Resource Sharing) 설정

class FixedQueue:
    """리스트 기반 원형 큐 (Circular Queue) 클래스 (capacity=20)"""
    def __init__(self, capacity=20):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = 0
        self.count = 0

    def is_empty(self):
        """큐가 비어 있는지 검사"""
        return self.count == 0

    def is_full(self):
        """큐가 가득 찼는지 검사"""
        return self.count == self.capacity

    def size(self):
        """현재 데이터 개수 반환"""
        return self.count

    def push(self, value):
        """데이터 삽입 (Full인 경우 오류 메시지 반환)"""
        if self.is_full():
            return {"error": "오류: 큐가 가득 찼습니다 (Queue is full)"}
        self.queue[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity
        self.count += 1
        return {"success": True, "pushed": value, "count": self.count}

    def pop(self):
        """데이터 추출 (Empty인 경우 오류 메시지 반환)"""
        if self.is_empty():
            return {"error": "오류: 큐가 비어 있습니다 (Queue is empty)"}
        value = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return {"success": True, "popped": value, "count": self.count}

    def peek(self):
        """전면 데이터 확인 (Empty인 경우 오류 메시지 반환)"""
        if self.is_empty():
            return {"error": "오류: 큐가 비어 있습니다 (Queue is empty)"}
        return {"success": True, "peek": self.queue[self.front]}

    def clear(self):
        """큐 전체 삭제 및 초기화"""
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = 0
        self.count = 0
        return {"success": True, "message": "큐가 전체 삭제되었습니다 (Queue cleared)"}

    def find(self, value):
        """값의 index(위치) 및 개수 검색"""
        indices = []
        for i in range(self.count):
            idx = (self.front + i) % self.capacity
            if self.queue[idx] == value:
                indices.append(i)  # 큐 내부에서의 상대적 위치
        return {"success": True, "value": value, "indices": indices, "count": len(indices)}

    def contains(self, value):
        """값의 존재 여부 확인"""
        for i in range(self.count):
            idx = (self.front + i) % self.capacity
            if self.queue[idx] == value:
                return {"success": True, "exists": True}
        return {"success": True, "exists": False}

    def dump(self):
        """Front부터 Rear까지의 전체 데이터 및 상태 출력"""
        elements = []
        for i in range(self.count):
            idx = (self.front + i) % self.capacity
            elements.append(self.queue[idx])
        return {
            "success": True,
            "queue": elements,
            "raw_array": self.queue,
            "front": self.front,
            "rear": self.rear,
            "count": self.count,
            "capacity": self.capacity
        }

# 전역 큐 인스턴스 생성 (기본 용량 20)
q_instance = FixedQueue(capacity=20)

@app.route("/")
def home():
    """서버 동작 상태 페이지 (캡처용)"""
    dump_data = q_instance.dump()
    html_template = """
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
            ul { line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>구글 클라우드 런 백엔드 서버</h1>
            <p>서버 상태: <span class="status">Running (정상 동작 중)</span></p>
            <hr>
            <h3>현재 큐 상태 정보 (Queue Status)</h3>
            <ul>
                <li><strong>Capacity (용량):</strong> {{ capacity }}</li>
                <li><strong>Count (데이터 개수):</strong> {{ count }}</li>
                <li><strong>Front 위치:</strong> {{ front }}</li>
                <li><strong>Rear 위치:</strong> {{ rear }}</li>
                <li><strong>현재 큐 내용 (Front ~ Rear):</strong> {{ queue }}</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(
        html_template, 
        capacity=dump_data["capacity"], 
        count=dump_data["count"], 
        front=dump_data["front"], 
        rear=dump_data["rear"], 
        queue=dump_data["queue"]
    )

@app.route("/api/init", methods=["POST"])
def api_init():
    data = request.json or {}
    capacity = data.get("capacity", 20)
    global q_instance
    q_instance = FixedQueue(capacity=capacity)
    return jsonify({"success": True, "message": f"Queue initialized with capacity {capacity}"})

@app.route("/api/push", methods=["POST"])
def api_push():
    val = request.json.get("value")
    return jsonify(q_instance.push(val))

@app.route("/api/pop", methods=["POST"])
def api_pop():
    return jsonify(q_instance.pop())

@app.route("/api/peek", methods=["GET"])
def api_peek():
    return jsonify(q_instance.peek())

@app.route("/api/size", methods=["GET"])
def api_size():
    return jsonify({"success": True, "size": q_instance.size()})

@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify({
        "success": True,
        "is_full": q_instance.is_full(),
        "is_empty": q_instance.is_empty(),
        "size": q_instance.size(),
        "capacity": q_instance.capacity
    })

@app.route("/api/clear", methods=["POST"])
def api_clear():
    return jsonify(q_instance.clear())

@app.route("/api/find", methods=["GET"])
def api_find():
    val = int(request.args.get("value", 0))
    return jsonify(q_instance.find(val))

@app.route("/api/contains", methods=["GET"])
def api_contains():
    val = int(request.args.get("value", 0))
    return jsonify(q_instance.contains(val))

@app.route("/api/dump", methods=["GET"])
def api_dump():
    return jsonify(q_instance.dump())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
