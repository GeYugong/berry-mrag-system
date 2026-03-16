from visual_module.inference import _yolo_inference


class _Scalar:
    def __init__(self, v):
        self._v = v

    def item(self):
        return self._v


class _Vector:
    def __init__(self, vals):
        self._vals = vals

    def argmax(self):
        max_idx = max(range(len(self._vals)), key=lambda i: self._vals[i])
        return _Scalar(max_idx)

    def __getitem__(self, idx):
        return _Scalar(self._vals[idx])


class _Row:
    def __init__(self, vals):
        self._vals = vals

    def tolist(self):
        return self._vals


class _Matrix:
    def __init__(self, rows):
        self._rows = rows

    def __getitem__(self, idx):
        return _Row(self._rows[idx])


class _Boxes:
    def __init__(self, conf_vals, cls_vals, xyxy_vals):
        self.conf = _Vector(conf_vals)
        self.cls = _Vector(cls_vals)
        self.xyxy = _Matrix(xyxy_vals)

    def __len__(self):
        return len(self.conf._vals)


class _Result:
    def __init__(self, names, boxes):
        self.names = names
        self.boxes = boxes


class _DummyModel:
    def __init__(self, result):
        self._result = result

    def predict(self, **kwargs):
        return [self._result]


def test_non_business_label_falls_back_unknown(monkeypatch):
    result = _Result(
        names={0: "frisbee"},
        boxes=_Boxes([0.91], [0], [[10.0, 20.0, 30.0, 40.0]]),
    )
    monkeypatch.setattr(
        "visual_module.inference._get_model", lambda model_path: _DummyModel(result)
    )

    out = _yolo_inference(
        image_path="x.jpg",
        model_path="m.pt",
        device="cpu",
        conf=0.25,
        iou=0.45,
        business_conf=0.45,
    )
    assert out is not None
    assert out["pest_type"] == "unknown_leaf_issue"
    assert out["bbox"] == [0, 0, 0, 0]


def test_low_conf_business_label_falls_back_unknown(monkeypatch):
    result = _Result(
        names={0: "aphid"},
        boxes=_Boxes([0.31], [0], [[1.0, 2.0, 3.0, 4.0]]),
    )
    monkeypatch.setattr(
        "visual_module.inference._get_model", lambda model_path: _DummyModel(result)
    )

    out = _yolo_inference(
        image_path="x.jpg",
        model_path="m.pt",
        device="cpu",
        conf=0.25,
        iou=0.45,
        business_conf=0.45,
    )
    assert out is not None
    assert out["pest_type"] == "unknown_leaf_issue"


def test_business_label_and_conf_passes(monkeypatch):
    result = _Result(
        names={0: "powdery mildew"},
        boxes=_Boxes([0.87], [0], [[11.0, 22.0, 33.0, 44.0]]),
    )
    monkeypatch.setattr(
        "visual_module.inference._get_model", lambda model_path: _DummyModel(result)
    )

    out = _yolo_inference(
        image_path="x.jpg",
        model_path="m.pt",
        device="cpu",
        conf=0.25,
        iou=0.45,
        business_conf=0.45,
    )
    assert out is not None
    assert out["pest_type"] == "powdery_mildew"
    assert out["bbox"] == [11, 22, 33, 44]
