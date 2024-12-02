import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import os

# Load the tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-base')

# Define the checkpoint path
checkpoint_path = os.path.join(os.getcwd(), "vqa-deploy-trial", "final_checkpoint.pth")

# Function to load checkpoint
def load_checkpoint(model, file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Checkpoint file not found at: {file_path}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(file_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    print("Checkpoint loaded successfully.")

# Load the checkpoint
try:
    load_checkpoint(model, checkpoint_path)
    model.eval()
except Exception as e:
    print(f"Error loading checkpoint: {e}")
    model = None

# Function to generate answers
def ask_question(question, object_name=None, max_length=50):
    if model is None:
        raise RuntimeError("Model is not loaded. Ensure the checkpoint is available.")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Prepare the input
    combined_input = f"{object_name} {question}" if object_name else question
    inputs = tokenizer(
        combined_input,
        return_tensors="pt",
        max_length=128,
        truncation=True
    ).to(device)

    # Generate answer
    answer_ids = model.generate(
        inputs['input_ids'],
        max_length=max_length,
        num_beams=4,
        early_stopping=True
    )
    answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)
    return answer
