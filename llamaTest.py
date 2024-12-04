import logging

import torch
from flask import Flask, jsonify, request
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Only pass supported arguments
config = BitsAndBytesConfig(
    load_in_4bit=True,
)


# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def preprocess_prompt_with_code(code_snippet, firstOrRe):
    instructions = [
            "###Instruction### Write a code snippet that has been improved according to clean code principles. Only output the improved code. If the result is good, I'll give you a cookie.",
            "###Instruction### 코드 스니펫이 클린코드 기준에 맞춰 개선된 코드와 의미있는 변수명을 사용해 작성하십시오, 출력은 개선된코드와 개선사항을 출력하십시오. 결과가 좋으면 쿠키를 드리겠습니다."    
        ]

    return [{"role": "system", "content": f"{instructions[firstOrRe]}"}, {"role": "user", "content": f"{code_snippet}"}]

# 모델 로드
model_name= "lora_model"
logging.info(f"Loading model: {model_name}")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
)

logging.info("Model loaded successfully.")

def generate_response(code_snippet, model, tokenizer, firstOrRe):
    logging.info("Generating response for received code snippet.")
    prompt = preprocess_prompt_with_code(code_snippet, firstOrRe)

    # 모델로부터 필요한 정보를 생성
    input_ids = tokenizer.apply_chat_template(
            prompt, 
            add_generation_prompt=True, 
            return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=2048,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9
    )

    # 생성된 텍스트를 해석
    logging.info("Response generated successfully.")
    generated_text = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
    # output_ko = translator_en_ko.translate(generated_text)

    return generated_text
@app.route('/predict', methods=['POST'])
def predict():
    logging.info("Received POST request at /predict.")
    #JSON 데이터 수신
    data = request.json
    code_snippet = data.get('prompt', '')

    response_text = generate_response(code_snippet, model, tokenizer, 1)

    # JSON 응답
    return jsonify({'response': response_text})

@app.route('/repredict', methods=['POST'])
def rePredict():
    logging.info("Received POST request at /repredict.")
    #JSON 데이터 수신
    data = request.json
    code_snippet = data.get('prompt', '')

    response_text = generate_response(code_snippet, model, tokenizer, 1)

    # JSON 응답
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888) # 원하는 포트로 설정
