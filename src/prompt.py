from typing import List,Dict

def build_prompt(query: str, retrieved_chunks: List[Dict]) -> str :
    context_block = []
    for chunk in retrieved_chunks:
        source = chunk["metadata"].get("source", "unknown")
        page = chunk["metadata"].get("page", None)
        citation= f"{source}"
        if page is not None:
            citation += f" , page {page}"
        context_block.append(
            f"[source: {citation}]\n{chunk['text']}"
        )
    context = "\n\n".join(context_block)
    prompt = f'''
    You are a question-answering assistant.

    RULES (you MUST follow these):
    - Rules:
    - Use only the provided context.
    - Do not add external information.
    - If not found, reply: "I don't know based on the provided documents."
    Context:
    {context}
    Question:
    {query}
    Answer:
    '''.strip()

    return prompt
    
