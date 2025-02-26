from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load the fine-tuned model and tokenizer
MODEL_PATH = "./model"  # Path to your fine-tuned model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

# Set the padding token if it doesn't exist
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Use EOS token as PAD token

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Query(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)  # Validate input length

@app.post("/predict/")
async def predict(query: Query):
    try:
        logger.info(f"Received question: {query.question}")
        
        # Tokenize the input query with EOS token
        bot_input_ids = tokenizer.encode(
            query.question + tokenizer.eos_token,
            return_tensors="pt"
        ).to(device)
        
        # Generate response with the same parameters as the notebook
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=100,  # Maximum length of the generated response
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,  # Prevent repetition of n-grams
            do_sample=True,  # Enable sampling
            top_k=10,  # Limit sampling to the top-k tokens
            top_p=0.7,  # Nucleus sampling
            temperature=0.8  # Control randomness
        )
        
        # Decode the generated response
        predicted_text = tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0],
            skip_special_tokens=True
        )
        
        logger.info(f"Generated response: {predicted_text}")
        return {"response": predicted_text}
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))