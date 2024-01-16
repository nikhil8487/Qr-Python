import cv2
import webbrowser
import numpy as np
import datetime
import threading
import sys
import time  
# Set the maintenance command
maintenance_command = "monthly_maintenance"
def maintenance_timer():
    # Set the maintenance interval (e.g., 1 month)
    maintenance_interval = datetime.timedelta(minutes=44640)
    maintenance_start_time = datetime.datetime.now()
    while True:
        current_time = datetime.datetime.now()
        # Check if it's time for maintenance
        if current_time - maintenance_start_time >= maintenance_interval:
            print("Maintenance not performed on time. Exiting...")
            sys.exit(1)
        # Sleep for a short interval before checking again
        time.sleep(10)
# Start the maintenance timer in a separate thread
maintenance_thread = threading.Thread(target=maintenance_timer, daemon=True)
maintenance_thread.start()
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
            # Check if the scanned QR code is the maintenance command
            if qr_code_data == maintenance_command:
                print("Monthly maintenance performed. Exiting...")
                sys.exit(0)
        break
    resized_img = cv2.resize(img, None, fx=zoom_level, fy=zoom_level)
    cv2.imshow("QR Code Scanner", resized_img)
    if cv2.waitKey(1) == ord("q"):
        break
log_file.close()
webbrowser.open(str(qr_code_data))
cap.release()
cv2.destroyAllWindows()