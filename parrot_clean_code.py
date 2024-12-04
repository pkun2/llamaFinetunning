import json
import subprocess
import ast
from datasets import load_dataset

def is_valid_python_code(code):
    """
    주어진 코드가 Python 문법적으로 유효한지 확인.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def process_code(code):
    # Black 및 기타 도구 실행
    with open('temp.py', 'w') as temp_file:
        temp_file.write(code)

    subprocess.run(['black', 'temp.py'])
    subprocess.run(['isort', 'temp.py'])
    subprocess.run(['autoflake', '--in-place', '--remove-unused-variables', '--remove-all-unused-imports', 'temp.py'])

    with open('temp.py', 'r') as temp_file:
        return temp_file.read()

# 데이터셋 로드
ds = load_dataset("codeparrot/codeparrot-clean", split="train")  # train 데이터만 로드

# 출력 파일 설정
output_file = 'parrot_updated_dataset.json'

with open(output_file, 'w', encoding='utf-8') as result_file:
    result_file.write("[\n")  # JSON 배열 시작

    for idx, data in enumerate(ds):  # 스트리밍 방식으로 데이터 순회
        try:
            code = data['content']  # 원본 코드 추출
            
            # 코드가 문법적으로 유효한지 확인
            if not is_valid_python_code(code):
                print(f"문법 오류로 건너뜀 (index={idx})")
                continue
            
            cleaned_code = process_code(code)  # 코드 포맷팅

            result_data = {
                "code": code,
                "cleaned_code": cleaned_code,
            }
            json.dump(result_data, result_file, indent=4, ensure_ascii=False)
            
            # 마지막 항목이 아닌 경우 쉼표 추가
            if idx < len(ds) - 1:
                result_file.write(",\n")
        except Exception as e:
            print(f"코드 처리 중 오류 발생: {e}")
            continue

    result_file.write("\n]\n")  # JSON 배열 종료

print(f"데이터셋이 '{output_file}'에 저장되었습니다.")
