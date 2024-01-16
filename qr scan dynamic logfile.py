import cv2
import webbrowser
import numpy as np
import datetime
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
zoom_level = 1.0
log_file = open("scanned_qr_log.txt", "a")
while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        qr_code_data = data
        if bbox is not None and len(bbox) > 0:
            qr_size = np.amax(bbox[0, 2:])
            zoom_level = max(-100.0, 100.0 / qr_size)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"Scanned QR Code: {qr_code_data}, Date/Time: {current_time}\n")
            log_file.flush()
        break
    resized_img = cv2.resize(img, None, fx=zoom_level, fy=zoom_level)
    cv2.imshow("QR Code Scanner", resized_img)
    if cv2.waitKey(1) == ord("q"):
        break
log_file.close()
webbrowser.open(str(qr_code_data))
cap.release()
cv2.destroyAllWindows()
