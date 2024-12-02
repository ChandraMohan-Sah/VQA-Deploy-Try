import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import os

# Load the tokenizer and model (paths may need adjusting based on your setup)
tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-base')

# Define checkpoint path
checkpoint_path = os.path.join(os.getcwd(), "vqa-deploy-trial", "final_checkpoint.pth")

# Function to load checkpoint
def load_checkpoint(model, file_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Loading checkpoint from {file_path}")
    checkpoint = torch.load(file_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    print(f"Checkpoint loaded successfully from {file_path}")
    model.to(device)

# Load checkpoint
load_checkpoint(model, checkpoint_path)
model.eval()

# Function to generate answers based on input questions
def ask_question(question, object_name=None, max_length=50):
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

    # Decode the generated answer
    answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)
    return answer
