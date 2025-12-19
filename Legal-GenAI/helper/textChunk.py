from typing import List


def chunk_text(text: str,max_chars: int = 1000,min_chars: int = 300) -> List[str]:
    """
    Chunk legal document text into coherent chunks.

    - Splits by paragraphs
    - Merges paragraphs until max_chars
    - Avoids tiny fragments
    """
    
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        # If adding paragraph exceeds max size, finalize current chunk
        if len(current_chunk) + len(para) > max_chars:
            if len(current_chunk) >= min_chars:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                # Force merge if chunk too small
                current_chunk += "\n\n" + para
        else:
            current_chunk += "\n\n" + para

    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
