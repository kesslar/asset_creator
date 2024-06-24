import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont
import textwrap

class ImageGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Generator and Video Converter')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.promptLabel = QLabel('Enter Prompts:')
        layout.addWidget(self.promptLabel)

        self.promptTextEdit = QTextEdit()
        layout.addWidget(self.promptTextEdit)

        self.widthLabel = QLabel('Enter Image Width:')
        layout.addWidget(self.widthLabel)

        self.widthLineEdit = QLineEdit()
        layout.addWidget(self.widthLineEdit)

        self.heightLabel = QLabel('Enter Image Height:')
        layout.addWidget(self.heightLabel)

        self.heightLineEdit = QLineEdit()
        layout.addWidget(self.heightLineEdit)

        self.generateButton = QPushButton('Generate Images')
        self.generateButton.clicked.connect(self.generateImages)
        layout.addWidget(self.generateButton)

        self.convertButton = QPushButton('Convert Images to Video')
        self.convertButton.clicked.connect(self.convertToVideo)
        layout.addWidget(self.convertButton)

        self.statusLabel = QLabel('')
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def generateImages(self):
        prompts = self.promptTextEdit.toPlainText().split('\n')
        try:
            width = int(self.widthLineEdit.text())
            height = int(self.heightLineEdit.text())
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Width and height must be integers.')
            return

        output_dir = os.path.expanduser('~/Pictures/Assets/')
        os.makedirs(output_dir, exist_ok=True)

        font_cwd = os.getcwd()
        font_locator = "arial.ttf"

        for i, prompt in enumerate(prompts):
            img = Image.new('RGB', (width, height), color=(0, 0, 0))
            d = ImageDraw.Draw(img)

            font_size = 100
            fnt = ImageFont.truetype(os.path.join(font_cwd, font_locator), font_size)
            wrapper = textwrap.TextWrapper(width=width // (font_size // 2))
            lines = wrapper.wrap(text=prompt)
            text_height = len(lines) * font_size

            while text_height > height:
                font_size -= 1
                fnt = ImageFont.truetype(os.path.join(font_cwd, font_locator), font_size)
                wrapper = textwrap.TextWrapper(width=width // (font_size // 2))
                lines = wrapper.wrap(text=prompt)
                text_height = len(lines) * font_size

            for line_num, line in enumerate(lines):
                text_width = d.textlength(line, font=fnt)
                x = (width - text_width) / 2
                y = (height - text_height) / 2 + line_num * font_size
                d.text((x, y), line, font=fnt, fill=(255, 255, 255))

            img.save(os.path.expanduser(f'~/Pictures/Assets/prompt_{i + 1}.jpg'))

        self.statusLabel.setText("Images generated successfully!")

    def convertToVideo(self):
        cwd = os.getcwd()
        bash_script_path = "./video_converter_v2.sh"

        if os.path.exists(bash_script_path):
            subprocess.run(["bash", os.path.join(cwd, bash_script_path)])
            self.statusLabel.setText("Video conversion complete!")
        else:
            QMessageBox.warning(self, 'File Error', 'video_converter_v2.sh not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageGenerator()
    ex.show()
    sys.exit(app.exec_())
