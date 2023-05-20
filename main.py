import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QMessageBox, QStatusBar, QProgressBar
from bs4 import BeautifulSoup
from googletrans import Translator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Translator")
        self.resize(400, 200)

        # Create main widget and layout
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)

        # Create file selection button
        self.file_button = QPushButton("Select HTML File", self.main_widget)
        self.file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.file_button)

        # Create language selection dropdown
        self.language_label = QLabel("Destination Language:", self.main_widget)
        self.layout.addWidget(self.language_label)

        self.language_dropdown = QComboBox(self.main_widget)
        self.language_dropdown.addItem("Hindi", "hi")
        self.language_dropdown.addItem("Spanish", "es")
        self.language_dropdown.addItem("French", "fr")
        # Add more language options as needed

        self.layout.addWidget(self.language_dropdown)

        # Create progress bar
        self.progress_bar = QProgressBar(self.main_widget)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        # Create translate button
        self.translate_button = QPushButton("Translate", self.main_widget)
        self.translate_button.clicked.connect(self.translate_html)
        self.layout.addWidget(self.translate_button)

        self.setCentralWidget(self.main_widget)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select HTML File", "", "HTML Files (*.html)")
        self.file_path = file_path

    def translate_html(self):
        try:
            # Load the HTML file
            with open(self.file_path, 'r') as f:
                html = f.read()

            # Parse the HTML and extract the text
            soup = BeautifulSoup(html, 'html.parser')
            for tag in soup.find_all():
                if tag.string:
                    # Translate the text to the selected language
                    translator = Translator()
                    translated_text = translator.translate(tag.string, dest=self.language_dropdown.currentData()).text

                    # Replace the original text with the translated text
                    tag.string.replace_with(translated_text)

            # Save the modified HTML to a file
            output_path, _ = QFileDialog.getSaveFileName(self, "Save Translated HTML", "", "HTML Files (*.html)")
            with open(output_path, 'w') as f:
                f.write(str(soup))

            QMessageBox.information(self, "Translation Complete", "The translated HTML has been saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
