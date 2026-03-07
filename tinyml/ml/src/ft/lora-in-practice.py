# 导入模型和 tokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-2-7b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 生成 lora_model
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=8,                # 低秩近似的 rank
    lora_alpha=16,      # 缩放因子
    lora_dropout=0.1,   # dropout（正则化）
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM",
)

lora_model = get_peft_model(model, lora_config)

# 训练
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./lora_finetuned",
    learning_rate=2e-4,
    num_train_epochs=3,
    per_device_train_batch_size=8,
)

trainer = Trainer(
    model=lora_model,
    args=training_args,
    train_dataset=my_dataset,
)

trainer.train()

# 保存微调后的模型
lora_model.save_pretrained("./my_lora_adapter")