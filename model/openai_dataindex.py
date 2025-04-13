import os
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import numpy as np
from model import read_chunked_html


def initialize_model():
    """Initialize and return the model and tokenizer"""
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return model, tokenizer


def get_embeddings(chunk_tuples, model, tokenizer, batch_size=32):
    """
    Generate embeddings for text chunks using GPU acceleration.
    Optimized to use MPS on Apple Silicon or CUDA if available.
    """
    # Extract just the text content from the tuples for embedding
    text_chunks = [chunk[1] for chunk in chunk_tuples]

    # Set up device for GPU acceleration
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using MPS (Apple Silicon) for acceleration")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        print("Using CUDA for acceleration")
    else:
        device = torch.device("cpu")
        print("GPU acceleration not available, using CPU")

    # Move model to GPU
    model = model.to(device)

    embeddings = []
    total_batches = (len(text_chunks) + batch_size - 1) // batch_size

    # Progress tracking
    last_percent_reported = -5

    for i in range(0, len(text_chunks), batch_size):
        batch_num = i // batch_size + 1
        current_percent = int((batch_num / total_batches) * 100)

        # Print progress every 5%
        if current_percent >= last_percent_reported + 5:
            last_percent_reported = current_percent
            print(f"Processing embeddings: {current_percent}% complete ({batch_num}/{total_batches} batches)")

        batch = text_chunks[i:i + batch_size]
        encoded_input = tokenizer(batch, padding=True, truncation=True, return_tensors='pt')

        # Move input tensors to GPU
        encoded_input = {k: v.to(device) for k, v in encoded_input.items()}

        with torch.no_grad():
            model_output = model(**encoded_input)

        # Move output back to CPU for numpy conversion
        embeddings.append(model_output.pooler_output.to(torch.float16).cpu().numpy())

    # Ensure we print 100% completion
    if last_percent_reported < 100:
        print(f"Processing embeddings: 100% complete ({total_batches}/{total_batches} batches)")

    return np.vstack(embeddings)


def create_faiss_index(embeddings, output_dir, index_name="faiss_index.index"):
    """Create and save a FAISS index"""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype='float32'))

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save FAISS index
    index_path = os.path.join(output_dir, index_name)
    faiss.write_index(index, index_path)
    print(f"Embeddings stored successfully in FAISS at {index_path}")

    return index, index_path


def build_knowledge_base(chunked_html_folder=os.getenv('CHUNKDATA_DIR'),
                         output_dir=os.getenv('HOME_DIR'),
                         index_name="faiss_index.index"):
    """Main function to orchestrate the knowledge base building process.
    Only builds the index if it doesn't already exist."""

    # Check if index already exists
    index_path = os.path.join(output_dir, index_name)
    if not os.path.exists(index_path):
        print(f"No existing index found at {index_path}. Building new index...")

        # 1. Load chunked HTML files using the read_chunked_html function
        all_chunks = read_chunked_html(chunked_html_folder)
        print(f"Loaded {len(all_chunks)} chunks.")

        # 2. Initialize the model and tokenizer
        model, tokenizer = initialize_model()

        # 3. Generate embeddings
        print(f"Generating embeddings for {len(all_chunks)} chunks...")
        embeddings = get_embeddings(all_chunks, model, tokenizer)
        print(f"Generated embeddings with shape: {embeddings.shape}")

        # 4. Create and save FAISS index
        index, index_path = create_faiss_index(embeddings, output_dir, index_name)

        return all_chunks, index, index_path
    else:
        print(f"FAISS index already exists at {index_path}.")
