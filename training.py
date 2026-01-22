from ultralytics import YOLO

def train_yolo_segmentation():
    # 1. Load the model
    # We use 'yolov8n-seg.pt' (nano) for speed,
    # but you can use 'yolov8s-seg.pt' or 'yolov8m-seg.pt' for better accuracy.
    model = YOLO('yolo11x-seg.pt')

    # 2. Train the model
    # Replace 'path/to/data.yaml' with the actual absolute path if this script
    # is not in the same folder as your yaml file.
    results = model.train(
        data='cubeds/data.yaml',     # Path to your config file
        task='segment',
        epochs=100,           # Number of training epochs
        imgsz=640,            # Input image size
        batch=8,             # Batch size (reduce if you run out of GPU memory)
        name='yolo11m', # Name of the output folder
        device=0              # Use 0 for GPU, 'cpu' if no GPU is available
    )

    print("Training complete. Results saved to 'runs/segment_yolov8_segmentation_rubiks'")

if __name__ == "__main__":
    train_yolo_segmentation()