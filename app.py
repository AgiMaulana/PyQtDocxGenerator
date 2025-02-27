import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QTextEdit
)
from docxtpl import DocxTemplate

class DocxGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DOCX Generator")
        self.resize(600, 400)
        self.layout = QVBoxLayout()

        # Button to choose DOCX Template
        self.template_button = QPushButton("Choose DOCX Template")
        self.template_button.clicked.connect(self.choose_template)
        self.layout.addWidget(self.template_button)

        # Label for template path
        self.template_label = QLabel("No template selected.")
        self.layout.addWidget(self.template_label)

        # Text Area for JSON Context
        self.json_textarea = QTextEdit()
        self.json_textarea.setPlaceholderText("Paste JSON context here...")
        self.layout.addWidget(self.json_textarea)

        # Button to generate DOCX
        self.generate_button = QPushButton("Generate DOCX")
        self.generate_button.clicked.connect(self.generate_docx)
        self.layout.addWidget(self.generate_button)

        # Status message at the bottom
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)
        self.template_path = ""

    def choose_template(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DOCX Template", "", "Word Documents (*.docx)")
        if file_path:
            self.template_path = file_path
            self.template_label.setText(f"Template: {file_path}")

    def generate_docx(self):
        if not self.template_path:
            self.status_label.setText("⚠️ Please select a DOCX template!")
            return
        
        raw_json = self.json_textarea.toPlainText()
        try:
            context = json.loads(raw_json)
        except json.JSONDecodeError:
            self.status_label.setText("❌ Invalid JSON format!")
            return

        docx = DocxTemplate(self.template_path)
        docx.render(context)

        save_path, _ = QFileDialog.getSaveFileName(self, "Save DOCX", "", "Word Documents (*.docx)")
        if save_path:
            docx.save(save_path)
            self.status_label.setText(f"✅ Successfully saved: {save_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocxGenerator()
    window.show()
    sys.exit(app.exec())
