from transformers import AutoTokenizer, AutoModelForCausalLM

# 모델 로드
model_path = "Mungert/Qwen2.5-VL-3B-Instruct-GGUF"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map='cpu')

# 모델 저장
save_dir = "./model"
tokenizer.save_pretrained(save_dir)
model.save_pretrained(save_dir)
