import json
import ijson

# 입력 JSON 파일 경로와 출력 파일 경로 지정
input_file_path = "parrot_updated_dataset.json"
output_file_path = "alphca_formatted_dataset.jsonl"  # JSON Lines 형식으로 저장

# 스트리밍 방식으로 JSON 파일 처리
with open(input_file_path, "r", encoding="utf-8") as infile, open(output_file_path, "w", encoding="utf-8") as outfile:
    for item in ijson.items(infile, "item"):  # "item"은 JSON 배열의 각 항목을 순회
        instruction = "클린코드 문법에 따라 코드를 개선하십시오."
        input_text = item.get("code", "").strip()
        output_text = item.get("cleaned_code", "").strip()

        formatted_item = {
            "Instruction": instruction,
            "Input": input_text,
            "Output": output_text
        }

        outfile.write(json.dumps(formatted_item, ensure_ascii=False) + "\n")