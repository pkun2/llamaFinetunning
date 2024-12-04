import json

# 파일을 한 줄씩 읽어서 JSON 형식이 올바른지 확인
with open("alphaca_formatted_dataset.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        try:
            json.loads(line)  # 각 줄을 JSON으로 파싱
        except json.JSONDecodeError as e:
            print(f"Error in line {i}: {e}")
