from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from abc import ABC, abstractmethod
from typing import List
import requests
from utils import load_config

class BaseModelService(ABC):
    @abstractmethod
    def generate_response(self, messages: List[dict], max_tokens: int) -> str:
        pass
    
class QwenModelServiceLocal(BaseModelService):
    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct", lora_weights_path: str = None):
        """
        :param model_name: Name of base model which will be used.
        :param lora_weights_path: Path to LoRA weights (if None, loads base model).
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        base_model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype="auto", device_map="auto"
        )
        if lora_weights_path:
            self.model = PeftModel.from_pretrained(base_model, lora_weights_path)
        else:
            self.model = base_model

    def generate_response(self, messages: List[dict], max_tokens: int = 512) -> str:
        """
        :param messages: List of messages in the following format: [{"role": "system", "content": ...}, {"role": "user", "content": ...}]
        :param max_tokens: Max number of tokens which model can generate in an answer.
        :returns: Generated text that is the response to the input messages.
        """
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(**model_inputs, max_new_tokens=max_tokens)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

class QwenModelServiceRemote(BaseModelService):
    def __init__(self, api_url: str):
        self.api_url = api_url

    def generate_response(self, messages: List[dict], max_tokens: int = 512) -> str:
        payload = {
            "messages": messages,
            "max_tokens": max_tokens
        }

        response = requests.post(f"{self.api_url}/generate", json=payload)

        if response.status_code == 200:
            return response.json().get("response")
        else:
            raise Exception(f"Ошибка при запросе: {response.status_code}, {response.text}")

qwen_model_base = QwenModelServiceLocal() 
qwen_model_lora = QwenModelServiceLocal(lora_weights_path="olisval/qavito_model")