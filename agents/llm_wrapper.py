import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class LLM:
    def __init__(self, model='llama-3.3-70b-versatile'):
        self.model = model
        api_key = os.getenv('GROQ_KEY')
        
        self.client = Groq(api_key=api_key)
    def invoke(self, sys_prompt:str,user_prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": sys_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                response_format={"type": "json_object"},  # Forces JSON output
                temperature=0.1,  # Lower temperature = more deterministic
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# Singleton instance
llm = LLM()




