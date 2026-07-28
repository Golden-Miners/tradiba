from tradiba.hermes.multimodal.embeddings.platform import UnifiedEmbeddingPlatform

def test_embeddings():
    up = UnifiedEmbeddingPlatform()
    up.store_embedding("doc_1", up.embed_text("text"))
    up.store_embedding("img_1", up.embed_image(b"img"))
    
    assert len(up.similarity_search([0.1, 0.2, 0.3], top_k=5)) == 2
