import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import cv2
import easyocr
import pytesseract

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Recognition App")
        self.setGeometry(100, 100, 640, 480)

        self.central_widget = QLabel()
        self.central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.central_widget)

        self.btn_select_image = QPushButton("Select Image")
        self.btn_select_image.clicked.connect(self.select_image)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.central_widget)
        self.layout.addWidget(self.btn_select_image)

        self.image_path = ""

        self.reader = easyocr.Reader(['en'])

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_name:
            self.image_path = file_name
            self.process_image()

    def process_image(self):
        if self.image_path:
            image = cv2.imread(self.image_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            result = self.reader.readtext(gray_image)

            recognized_text = ""
            for detection in result:
                recognized_text += detection[1] + "\n"

            tesseract_text = pytesseract.image_to_string(gray_image)

            final_text = f"Text recognized by EasyOCR:\n{recognized_text}\nText recognized by Tesseract OCR:\n{tesseract_text}"

            pixmap = QPixmap(self.image_path)
            self.central_widget.setPixmap(pixmap)
            self.central_widget.setText(final_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
