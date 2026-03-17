import argparse
from pathlib import Path
from typing import Optional

from ultralytics import YOLO


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train/validate/export YOLOv8 model for berry disease detection."
    )
    parser.add_argument(
        "--data",
        type=str,
        default="data/processed/berry_yolo_data.yaml",
        help="YOLO dataset yaml path.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help="Pretrained model or checkpoint path.",
    )
    parser.add_argument("--imgsz", type=int, default=640, help="Image size.")
    parser.add_argument("--epochs", type=int, default=100, help="Training epochs.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument(
        "--device",
        type=str,
        default="0",
        help="Training device, e.g. 0 / 0,1 / cpu.",
    )
    parser.add_argument(
        "--project", type=str, default="runs/yolo", help="Output project directory."
    )
    parser.add_argument("--name", type=str, default="berry-disease", help="Run name.")
    parser.add_argument("--workers", type=int, default=8, help="Dataloader workers.")
    parser.add_argument(
        "--patience", type=int, default=30, help="Early stopping patience."
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility."
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume training from the last checkpoint.",
    )
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Cache images for faster training (uses more RAM).",
    )
    parser.add_argument(
        "--close-mosaic",
        type=int,
        default=10,
        help="Disable mosaic augmentation in final N epochs.",
    )
    parser.add_argument(
        "--no-val", action="store_true", help="Skip standalone validation after training."
    )
    parser.add_argument(
        "--export-format",
        type=str,
        default="onnx",
        choices=["none", "onnx", "torchscript", "openvino", "engine"],
        help="Export format after training. Use 'none' to skip export.",
    )
    parser.add_argument(
        "--export-half",
        action="store_true",
        help="Export half precision model when supported.",
    )
    parser.add_argument(
        "--export-dynamic",
        action="store_true",
        help="Enable dynamic shape when exporting.",
    )
    return parser


def _resolve_best_path(save_dir: Path) -> Optional[Path]:
    best = save_dir / "weights" / "best.pt"
    return best if best.exists() else None


def main() -> None:
    args = build_parser().parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset yaml not found: {data_path}. "
            "Create it first, e.g. data/processed/berry_yolo_data.yaml."
        )

    print(f"[YOLO] Start training with data={data_path} model={args.model}")
    model = YOLO(args.model)

    train_results = model.train(
        data=str(data_path),
        imgsz=args.imgsz,
        epochs=args.epochs,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        workers=args.workers,
        patience=args.patience,
        seed=args.seed,
        resume=args.resume,
        cache=args.cache,
        close_mosaic=args.close_mosaic,
    )

    save_dir = Path(str(train_results.save_dir))
    best_path = _resolve_best_path(save_dir)
    print(f"[YOLO] Train finished. save_dir={save_dir}")
    if best_path:
        print(f"[YOLO] Best checkpoint: {best_path}")
    else:
        print("[YOLO] best.pt not found. Check training output.")

    if not args.no_val and best_path:
        print("[YOLO] Start validation on best checkpoint...")
        best_model = YOLO(str(best_path))
        best_model.val(data=str(data_path), imgsz=args.imgsz, device=args.device)

    if args.export_format != "none" and best_path:
        print(f"[YOLO] Export best model to {args.export_format} ...")
        best_model = YOLO(str(best_path))
        best_model.export(
            format=args.export_format,
            imgsz=args.imgsz,
            half=args.export_half,
            dynamic=args.export_dynamic,
        )
    print("[YOLO] Done.")


if __name__ == "__main__":
    main()
