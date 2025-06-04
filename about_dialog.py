from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QTextEdit


class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("About expense manager app")
        self.setMinimumSize(600, 400)

        v_box_layout = QVBoxLayout()

        text = QTextEdit()
        text.setReadOnly(True)

        about_text = (
            "📊 Simple expense manager app created by Peter Szepesi, Slovakia\n\n"
            "If you like my app and you feel that way, you can support me in my work,\n"
            "I would be really grateful and appreciate any amount of donation.\n"
            "You can do it via support me button, or IBAN account transfer,\n"
            "IBAN account number : SK90 0900 0000 0051 2726 1825"
        )

        text.setPlainText(about_text)
        v_box_layout.addWidget(text)
        self.setLayout(v_box_layout)

        self.setStyleSheet("""
            QTextEdit{
                font-family: Segoe UI;
                font-size: 18px;
            }
        """)
