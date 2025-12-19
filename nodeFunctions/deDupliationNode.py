from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from stateAgent import DocuementAgentState

model = SentenceTransformer("all-MiniLM-L6-v2")

def deDupliationNode(state:DocuementAgentState) -> DocuementAgentState:
    issues = state.get("issues_found", {})
    if not issues:
        return []
    
    threshold = 0.85
    summaries = [i.issue_summary for i in issues]   
    embeddings = model.encode(summaries)

    keep = []
    used = set()

    for i in range(len(issues)):
        if i in used:
            continue

        keep.append(issues[i])

        for j in range(i + 1, len(issues)):
            if j in used:
                continue

            sim = cosine_similarity(
                [embeddings[i]], [embeddings[j]]
            )[0][0]

            if sim >= threshold:
                used.add(j)
    
    state["issues_found"] = keep
    return state
