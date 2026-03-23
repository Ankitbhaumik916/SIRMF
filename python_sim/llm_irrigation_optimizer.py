import argparse
import os

from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer


DEFAULT_ADAPTER_ID = "persadian/CropSeek-LLM"
DEFAULT_BASE_ID = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
DEFAULT_PROMPT = (
    "You are an irrigation optimization assistant.\n"
    "Given: crop=rice, area_acres=3.2, soil_moisture=31, temp_c=34, humidity=42, rainfall_mm=0, forecast='hot_dry_48h'\n"
    "Return strict JSON with keys: irrigate_now (bool), water_liters (number), priority_zones (array), reasoning (string)."
)


def load_model_and_tokenizer(adapter_id: str, base_id: str, device_map: str, hf_token: str | None = None):
    tokenizer = AutoTokenizer.from_pretrained(base_id, token=hf_token)
    model = AutoPeftModelForCausalLM.from_pretrained(
        adapter_id,
        base_model_name_or_path=base_id,
        torch_dtype="auto",
        device_map=device_map,
        token=hf_token,
    )
    return model, tokenizer


def generate_irrigation_json(model, tokenizer, prompt: str, max_new_tokens: int = 220) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = inputs.to(model.device)
    output = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    return tokenizer.decode(output[0], skip_special_tokens=True)


def parse_args():
    parser = argparse.ArgumentParser(description="Run CropSeek LLM irrigation optimization inference")
    parser.add_argument("--adapter-id", default=DEFAULT_ADAPTER_ID)
    parser.add_argument("--base-id", default=DEFAULT_BASE_ID)
    parser.add_argument("--device-map", default="auto")
    parser.add_argument("--max-new-tokens", type=int, default=220)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument(
        "--hf-token",
        default=None,
        help="Hugging Face token. If omitted, script uses HF_TOKEN or HUGGINGFACE_HUB_TOKEN env var.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    hf_token = args.hf_token or os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    model, tokenizer = load_model_and_tokenizer(args.adapter_id, args.base_id, args.device_map, hf_token)
    result = generate_irrigation_json(model, tokenizer, args.prompt, args.max_new_tokens)
    print(result)


if __name__ == "__main__":
    main()
