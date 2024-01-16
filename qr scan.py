import cv2
import webbrowser
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        qr_code_data = data
        break
    cv2.imshow("QR Code Scanner", img)
    if cv2.waitKey(1) == ord("q"):
        break
webbrowser.open(str(qr_code_data))
cap.release()
cv2.destroyAllWindows()