import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def linear_search_trace(array, target):
    """
    선형검색 알고리즘을 수행하며, 각 단계(step)별 상태를 기록하는 함수
    
    :param array: 검색 대상 리스트 (List[int/str])
    :param target: 찾고자 하는 값 (int/str)
    :return: 단계별 진행 상황을 담은 리스트 (List[dict])
    """
    steps = []
    found_index = -1
    
    for idx, value in enumerate(array):
        # 현재 단계의 정보 저장
        is_match = (value == target)
        steps.append({
            "step": idx + 1,
            "currentIndex": idx,
            "currentValue": value,
            "target": target,
            "isMatch": is_match
        })
        
        # 값을 찾으면 검색 종료
        if is_match:
            found_index = idx
            break
            
    return steps, found_index

@app.route('/search', methods=['POST'])
def search():
    """
    선형검색 API 엔드포인트
    요청 본문(JSON): { "array": [10, 20, 30], "target": 20 }
    """
    try:
        data = request.get_json()
        if not data or 'array' not in data or 'target' not in data:
            return jsonify({"status": "error", "message": "유효하지 않은 요청 데이터입니다."}), 400

        array = data['array']
        target = data['target']

        # 선형검색 수행 및 트레이스 기록 생성
        steps, found_index = linear_search_trace(array, target)

        # 복잡도 정보
        complexity = {
            "time_best": "O(1)",
            "time_average": "O(N)",
            "time_worst": "O(N)",
            "space": "O(1)"
        }

        response = {
            "status": "success",
            "array": array,
            "target": target,
            "foundIndex": found_index,
            "totalSteps": len(steps),
            "steps": steps,
            "complexity": complexity
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Cloud Run은 PORT 환경 변수를 사용함
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
