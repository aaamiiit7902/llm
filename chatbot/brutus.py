from langchain_community.llms import HuggingFacePipeline
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    CodeLlamaTokenizer,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)

# The model that you want to train from the Hugging Face hub
model_name = "maniacamit/codellama-finetunes-brutus"
use_4bit = True
bnb_4bit_compute_dtype = "float16"
bnb_4bit_quant_type = "nf4"
use_nested_quant = False
device_map = {"": 0} 

model_id = "/Users/amitkumar/Desktop/llm/codellama-finetunes-brutus/"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_use_double_quant=use_nested_quant,
)

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map=device_map
)
prompt = "What are some configurations that I can tweak Argus when using DynamoDB as backend database?"
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=200)
result = pipe(f"<s>[INST] {prompt} [/INST]")
print(result[0]['generated_text'])