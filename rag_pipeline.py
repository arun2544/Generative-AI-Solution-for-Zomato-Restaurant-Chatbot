# File: src/rag_pipeline.py
from typing import List, Dict
import os
from groq import Groq

class RAGSystem:
    def __init__(self, vector_db, system_prompt):
        self.vector_db = vector_db
        self.system_prompt = system_prompt
        
    def format_context(self, results: List[Dict]) -> str:
        """Format retrieved results for LLM context"""
        context = "Available restaurant information:\n"
        for res in results:
            context += (
                f"Name: {res['names']}\n"
                f"Rating: {res['ratings']}\n"
                f"Price: {res['price for one']}\n"
                f"Cuisine: {res['cuisine']}\n"
                f"Location: {res['location']}\n\n"
            )
        return context
    
    def generate_response(self, query: str) -> str:
        """End-to-end RAG pipeline"""
        # 1. Retrieve relevant context
        results = self.vector_db.search(query)
        
        # 2. Format for LLM
        context = self.format_context(results)
        prompt = f"{self.system_prompt}\n\nQuery: {query}\n\n{context}"
        
        # 3. Simulated LLM call (replace with actual API call)
        response = self._mock_llm_call("context:\n\n"+ context + "Now answer the following based on the context:" + query)
        
        return response
    
    def _mock_llm_call(self, query: str) -> str:
        client = Groq(
            api_key="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",  # This is the default and can be omitted
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content":self.system_prompt,
                },
                {
                    "role": "user",
                    "content": query,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
