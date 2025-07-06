import os
from groq import Groq
from app.infra.config import settings
from app.shared.utils.common_functions import CommonFuntions

os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

client = Groq(api_key=settings.GROQ_API_KEY)

model_name = settings.MODEL_NAME  

def get_groq_chat_completion(messages, temperature=0.3, max_tokens=1000):
    try:
        CommonFuntions.write_log(f"Making GROQ API request with model: {model_name}")
        CommonFuntions.write_log(f"Temperature: {temperature}, Max tokens: {max_tokens}")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        response_content = response.choices[0].message.content.strip()
        CommonFuntions.write_log("Raw LLM Response received")
        CommonFuntions.write_log(f"Response length: {len(response_content)} characters")
        
        return response_content
        
    except Exception as e:
        CommonFuntions.write_error_log(f"GROQ API error: {str(e)}")
        raise e