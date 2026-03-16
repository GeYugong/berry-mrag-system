from rag_module import retriever


def test_search_filters_by_crop(monkeypatch):
    items = [
        {"id": "a", "title": "草莓白粉病", "content": "x", "crop": "草莓", "disease_en": "powdery_mildew"},
        {"id": "b", "title": "蓝莓蚜虫", "content": "y", "crop": "蓝莓", "disease_en": "aphid"},
    ]
    vectors = [[1.0, 0.0], [0.0, 1.0]]
    cache = retriever._IndexCache(items=items, vectors=vectors, signature="t", faiss_index=None)
    monkeypatch.setattr(retriever, "_ensure_index", lambda dim: cache)

    out = retriever.search([1.0, 0.0], top_k=3, crop="草莓")
    assert [x["id"] for x in out] == ["a"]


def test_search_filters_by_disease_hint(monkeypatch):
    items = [
        {"id": "a", "title": "草莓白粉病", "content": "x", "crop": "草莓", "disease_en": "powdery_mildew"},
        {"id": "b", "title": "蓝莓蚜虫", "content": "y", "crop": "蓝莓", "disease_en": "aphid"},
    ]
    vectors = [[1.0, 0.0], [0.0, 1.0]]
    cache = retriever._IndexCache(items=items, vectors=vectors, signature="t", faiss_index=None)
    monkeypatch.setattr(retriever, "_ensure_index", lambda dim: cache)

    out = retriever.search([1.0, 0.0], top_k=3, disease_hint="aphid")
    assert [x["id"] for x in out] == ["b"]
