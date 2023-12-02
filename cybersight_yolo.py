import cybersight_sample as cs
import yolo_inference 
import cv2

if __name__ == "__main__":
    args = cs.parse_cam_args()
    pipeline = cs.gstreamer_pipeline(args)
    cap = cs.open_stream(pipeline)
    if not cap.isOpened():
        print("Failed to open stream")
        exit()

    model = yolo_inference.get_torch_model(yolo_inference.yolo_model)  

    img_shape = cs.SENSOR_MODES[cs.SENSOR][args.sensor_mode].mode_values[:-1]+[3]
    annotator = yolo_inference.create_annotator(img_shape)

    try:
        cv2.namedWindow("Video stream", cv2.WINDOW_NORMAL)
        while cap.isOpened():
            ret, frame = cap.read()

            results = model(frame)
            yolo_inference.update_annotator_img(annotator, frame)
            yolo_inference.annotate_keypoints(annotator, results)
            frame = annotator.result()

            cv2.imshow("Video stream", frame)
            # if the 'q' key was pressed, break from the loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except cv2.error as e:
        print(e)
        if "Can't initialize GTK backend" in str(e):
            print("Unable to open window for showing stream preview. Is a display available?")
