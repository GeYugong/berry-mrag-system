from fastapi.testclient import TestClient

from backend.main import app
from rag_module import embedder


class _EmbeddingsApi:
    def create(self, **kwargs):
        raise RuntimeError("embedding api down")


class _DummyClient:
    def __init__(self):
        self.embeddings = _EmbeddingsApi()


def test_embed_text_fallback_on_api_error(monkeypatch):
    monkeypatch.setattr(embedder, "_get_client", lambda: _DummyClient())
    vec = embedder.embed_text("fallback-check", dim=32)
    assert len(vec) == 32
    assert isinstance(vec[0], float)


def test_diagnose_returns_200_when_embedding_api_fails(monkeypatch):
    monkeypatch.setattr(embedder, "_get_client", lambda: _DummyClient())
    monkeypatch.setattr(
        "backend.api_routes.run_inference",
        lambda *args, **kwargs: {
            "pest_type": "unknown_leaf_issue",
            "confidence": 0.35,
            "bbox": [0, 0, 0, 0],
        },
    )
    monkeypatch.setattr(
        "backend.api_routes.search",
        lambda *args, **kwargs: [
            {
                "id": "manual-001",
                "title": "草莓白粉病",
                "content": "防治建议",
                "score": 0.9,
            }
        ],
    )

    client = TestClient(app)
    resp = client.post(
        "/api/diagnose",
        json={
            "query": "草莓白粉怎么办",
            "image_path": "D:/0code/berry-mrag-system/data/raw/strawberry_powdery_mildew.jpg",
            "crop": "草莓",
            "disease_hint": "powdery_mildew",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["detection"]["pest_type"] == "unknown_leaf_issue"
    assert len(data["retrieved"]) >= 1
