import cv2

for i in range(4):
    cap = cv2.VideoCapture(2)
    if cap.isOpened():
        print(f"Device /dev/video{1} açıldı!")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Frame alınamadı")
                break
            cv2.imshow(f"Camera {i}", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"Device /dev/video{i} açılamadı")
