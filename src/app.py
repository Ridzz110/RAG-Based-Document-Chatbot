import os
import shutil
import gradio as gr
from monitoring import format_metrics_markdown
from ingest import ingest_documents, chunk_documents
from embed import load_embedding_model, embed_document
from vector_store import save_index, create_faiss_index
from retrieve import retrieve_relevant_chunks
from prompt import build_prompt
from llm import generate_answer

UPLOAD_DIR = "data/docs"

def list_uploaded_docs():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        return "Uploaded Documents\n_No documents uploaded yet_"
    files = sorted(os.listdir(UPLOAD_DIR))
    if not files:
        return "Uploaded Documents\n_No documents uploaded yet_"
    md = "### 📂 Uploaded Documents\n"
    for f in files:
        md += f"- 📄 **{f}**\n"
    return md


# Initialization
embedding_model = load_embedding_model()


# Document Processing
def process_documents(files):
    if not files:
        return "No files uploaded."

    # Clear old documents
    shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for file in files:
        shutil.copy(file, UPLOAD_DIR)

    documents = ingest_documents(UPLOAD_DIR)
    chunks = chunk_documents(documents)
    embeddings_data = embed_document(chunks, embedding_model)
    index = create_faiss_index(embeddings_data["embeddings"])
    save_index(
        index, 
        {
            "texts": embeddings_data["texts"],
            "metadata": embeddings_data["metadatas"]
        }
    )
    return f"Processed {len(chunks)} document chunks successfully."


# Question Answering
def answer_question(query):
    if not query.strip():
        return "Please enter a question.", ""

    retrieved_chunks = retrieve_relevant_chunks(query, embedding_model, top_k=3)
    prompt = build_prompt(query, retrieved_chunks)
    print(prompt)
    answer = generate_answer(prompt)

    sources = []
    for chunk in retrieved_chunks:
        meta = chunk["metadata"]
        src = meta.get("source", "unknown")
        page = meta.get("page", None)
        sources.append(f"{src} (page {page})" if page else src)

    sources_text = "\n".join(set(sources))

    return answer, sources_text

def get_current_docs():
    docs = list_uploaded_docs()  # this function reads actual folder
    return docs

# Gradio UI
with gr.Blocks(title="Local RAG Document Assistant") as demo:
    gr.Markdown("## Offline RAG-Based Document Assistant")

    with gr.Tab("Upload Documents"):
        with gr.Column(scale=1):
            docs_list_md = gr.Markdown()  # empty at first

            demo.load(
                fn=get_current_docs,
                inputs=[],
                outputs=docs_list_md
            )
        with gr.Row():
            with gr.Column(scale=2):
                file_input = gr.File(
                    file_types=[".pdf", ".docx", ".txt"],
                    file_count="multiple",
                    label="Upload documents"
                )
                process_btn = gr.Button("Process Documents")
                
                process_output = gr.Textbox(label="Status")

                process_btn.click(
                    fn=process_documents,
                    inputs=file_input,
                    outputs=process_output
                ).then(
                    fn=list_uploaded_docs,
                    outputs=docs_list_md
                )

            

    with gr.Tab("Ask a Question"):
        query_input = gr.Textbox(label="Your Question", lines=3)
        ask_btn = gr.Button("Ask")
        answer_output = gr.Textbox(label="Answer", lines=6)
        sources_output = gr.Textbox(label="Sources", lines=2)

        ask_btn.click(
            fn=answer_question,
            inputs=query_input,
            outputs=[answer_output, sources_output]
        )

    with gr.Tab("System Metrics"):
        metrics_md = gr.Markdown()
        refresh_btn = gr.Button("Refresh Metrics")

        refresh_btn.click(
            fn=format_metrics_markdown,
            inputs=[],
            outputs=metrics_md
        )


if __name__ == "__main__":
    demo.launch(share=True)
