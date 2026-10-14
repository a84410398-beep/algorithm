from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# CORS 설정: 모든 도메인 및 GAS에서의 요청 허용
CORS(app, resources={r"/*": {"origins": "*"}})

# 전역 해시 테이블 저장소 (예시용 메모리 딕셔너리 구조)
# key: 해시 값(버킷), value: 저장된 데이터 리스트 또는 딕셔너리
HASH_TABLE_SIZE = 5
hash_table = {i: [] for i in range(HASH_TABLE_SIZE)}

def get_hash_key(key_str):
    """
    문자열 키를 받아 정수형 해시 값(버킷 인덱스)을 반환하는 해시 함수
    예: 문자들의 아스키 코드 합을 테이블 크기로 나눈 나머지
    """
    ascii_sum = sum(ord(char) for char in str(key_str))
    return ascii_sum % HASH_TABLE_SIZE

@app.route('/init', methods=['POST'])
def init_table():
    """1. init: 해시 테이블 초기화"""
    global hash_table
    hash_table = {i: [] for i in range(HASH_TABLE_SIZE)}
    return jsonify({"status": "success", "message": "해시 테이블이 초기화되었습니다.", "table": hash_table})

@app.route('/hash_value', methods=['POST'])
def hash_value():
    """2. hash_value: 주어진 키의 해시 값 계산 과정 반환"""
    data = request.json or {}
    key = data.get('key', '')
    if not key:
        return jsonify({"error": "키(key)가 제공되지 않았습니다."}), 400
    
    h_val = get_hash_key(key)
    return jsonify({
        "key": key,
        "hash_value": h_val,
        "formula": f"ASCII sum of '{key}' % {HASH_TABLE_SIZE} = {h_val}",
        "complexity": "O(1)"
    })

@app.route('/search', methods=['POST'])
def search():
    """3. search: 해시 테이블에서 데이터 검색"""
    data = request.json or {}
    key = data.get('key', '')
    if not key:
        return jsonify({"error": "검색할 키가 없습니다."}), 400
    
    h_val = get_hash_key(key)
    bucket = hash_table[h_val]
    
    found = False
    found_item = None
    steps = [f"1. 키 '{key}'의 해시값 계산 -> 버킷 [{h_val}] 도출"]
    
    for item in bucket:
        steps.append(f"2. 버킷 [{h_val}] 탐색 중 항목 확인: {item}")
        if item['key'] == key:
            found = True
            found_item = item['value']
            steps.append(f"3. 일치하는 키 발견! 값: {found_item}")
            break
            
    if not found:
        steps.append(f"3. 버킷 내에 키 '{key}'가 존재하지 않습니다.")

    return jsonify({
        "found": found,
        "key": key,
        "bucket": h_val,
        "value": found_item,
        "steps": steps,
        "complexity": "Best: O(1), Worst: O(N)"
    })

@app.route('/add', methods=['POST'])
def add():
    """4. add: 해시 테이블에 데이터 추가"""
    data = request.json or {}
    key = data.get('key', '')
    val = data.get('value', '')
    if not key:
        return jsonify({"error": "추가할 키가 없습니다."}), 400
        
    h_val = get_hash_key(key)
    bucket = hash_table[h_val]
    
    # 이미 존재하는지 확인 후 업데이트 또는 추가
    steps = [f"1. 키 '{key}'의 해시값 계산 -> 버킷 [{h_val}] 지정"]
    updated = False
    for item in bucket:
        if item['key'] == key:
            item['value'] = val
            updated = True
            steps.append(f"2. 기존 키 '{key}'가 존재하므로 값을 '{val}'(으)로 갱신함")
            break
            
    if not updated:
        bucket.append({"key": key, "value": val})
        steps.append(f"2. 버킷 [{h_val}]에 새 항목 {{'{key}': '{val}'}} 추가 완료")

    return jsonify({
        "status": "success",
        "bucket": h_val,
        "steps": steps,
        "table": hash_table,
        "complexity": "O(1) (평균)"
    })

@app.route('/remove', methods=['POST'])
def remove():
    """5. remove: 해시 테이블에서 데이터 삭제"""
    data = request.json or {}
    key = data.get('key', '')
    if not key:
        return jsonify({"error": "삭제할 키가 없습니다."}), 400
        
    h_val = get_hash_key(key)
    bucket = hash_table[h_val]
    
    steps = [f"1. 키 '{key}'의 해시값 계산 -> 버킷 [{h_val}] 접근"]
    removed = False
    for item in bucket[:]:
        if item['key'] == key:
            bucket.remove(item)
            removed = True
            steps.append(f"2. 버킷 [{h_val}]에서 키 '{key}' 항목 삭제 완료")
            break
            
    if not removed:
        steps.append(f"2. 삭제할 키 '{key}'를 찾지 못했습니다.")

    return jsonify({
        "status": "success",
        "removed": removed,
        "bucket": h_val,
        "steps": steps,
        "table": hash_table,
        "complexity": "O(1) (평균)"
    })

@app.route('/dump', methods=['POST', 'GET'])
def dump():
    """6. dump: 전체 해시 테이블 상태 출력"""
    return jsonify({
        "table": hash_table,
        "size": HASH_TABLE_SIZE,
        "steps": ["전체 해시 버킷 상태를 덤프(Dump) 하였습니다."],
        "complexity": "O(N)"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
