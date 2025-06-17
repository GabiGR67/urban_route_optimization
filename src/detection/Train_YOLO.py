from ultralytics import YOLO

def main():
    model = YOLO('yolov8m-seg.pt')

    model.train(
        data=r'C:\Users\Usuario\Desktop\urban_route_optimization\dataset\data.yaml',
        epochs=50,
        imgsz=640,
        batch=16,
        task='segment'
    )

    model.val()


if __name__ == '__main__':
    main()
