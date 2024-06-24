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
        self.initUI()  # Initialize the user interface

    def initUI(self):
        # Set the window title and size
        self.setWindowTitle('Image Generator and Video Converter')
        self.setGeometry(100, 100, 800, 600)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create and add a label for prompt input
        self.promptLabel = QLabel('Enter Prompts:')
        layout.addWidget(self.promptLabel)

        # Create and add a text edit for entering prompts
        self.promptTextEdit = QTextEdit()
        layout.addWidget(self.promptTextEdit)

        # Create and add a label for image width input
        self.widthLabel = QLabel('Enter Image Width:')
        layout.addWidget(self.widthLabel)

        # Create and add a line edit for entering image width
        self.widthLineEdit = QLineEdit()
        layout.addWidget(self.widthLineEdit)

        # Create and add a label for image height input
        self.heightLabel = QLabel('Enter Image Height:')
        layout.addWidget(self.heightLabel)

        # Create and add a line edit for entering image height
        self.heightLineEdit = QLineEdit()
        layout.addWidget(self.heightLineEdit)

        # Create and add a button to generate images
        self.generateButton = QPushButton('Generate Images')
        self.generateButton.clicked.connect(self.generateImages)  # Connect button to the function
        layout.addWidget(self.generateButton)

        # Create and add a button to convert images to video
        self.convertButton = QPushButton('Convert Images to Video')
        self.convertButton.clicked.connect(self.convertToVideo)  # Connect button to the function
        layout.addWidget(self.convertButton)

        # Create and add a label for displaying status messages
        self.statusLabel = QLabel('')
        layout.addWidget(self.statusLabel)

        # Set the layout for the widget
        self.setLayout(layout)

    def generateImages(self):
        # Get the prompts from the text edit and split them by new line
        prompts = self.promptTextEdit.toPlainText().split('\n')

        # Try to parse width and height, show a warning message if parsing fails
        try:
            width = int(self.widthLineEdit.text())
            height = int(self.heightLineEdit.text())
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Width and height must be integers.')
            return

        # Define the output directory for images
        output_dir = os.path.expanduser('~/Pictures/Assets/')
        os.makedirs(output_dir, exist_ok=True)

        # Define the font path
        font_cwd = os.getcwd()
        font_locator = "arial.ttf"

        # Loop through each prompt to generate an image
        for i, prompt in enumerate(prompts):
            img = Image.new('RGB', (width, height), color=(0, 0, 0))  # Create a new black image
            d = ImageDraw.Draw(img)  # Create a drawing object

            font_size = 100  # Start with a large font size
            fnt = ImageFont.truetype(os.path.join(font_cwd, font_locator), font_size)  # Load the font
            wrapper = textwrap.TextWrapper(width=width // (font_size // 2))  # Create a text wrapper
            lines = wrapper.wrap(text=prompt)  # Wrap the text
            text_height = len(lines) * font_size  # Calculate the text height

            # Adjust font size to fit text within the image height
            while text_height > height:
                font_size -= 1
                fnt = ImageFont.truetype(os.path.join(font_cwd, font_locator), font_size)
                wrapper = textwrap.TextWrapper(width=width // (font_size // 2))
                lines = wrapper.wrap(text=prompt)
                text_height = len(lines) * font_size

            # Draw each line of text centered horizontally and vertically
            for line_num, line in enumerate(lines):
                text_width = d.textlength(line, font=fnt)
                x = (width - text_width) / 2
                y = (height - text_height) / 2 + line_num * font_size
                d.text((x, y), line, font=fnt, fill=(255, 255, 255))

            # Save the image
            img.save(os.path.expanduser(f'~/Pictures/Assets/prompt_{i + 1}.jpg'))

        # Update the status label
        self.statusLabel.setText("Images generated successfully!")

    def convertToVideo(self):
        # Get the current working directory and the path to the bash script
        cwd = os.getcwd()
        bash_script_path = "./video_converter_v2.sh"

        # Check if the bash script exists, then run it; otherwise, show a warning message
        if os.path.exists(bash_script_path):
            subprocess.run(["bash", os.path.join(cwd, bash_script_path)])
            self.statusLabel.setText("Video conversion complete!")
        else:
            QMessageBox.warning(self, 'File Error', 'video_converter_v2.sh not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageGenerator()  # Create an instance of the ImageGenerator class
    ex.show()  # Show the widget
    sys.exit(app.exec_())  # Execute the application
