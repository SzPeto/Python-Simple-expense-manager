from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QTextEdit


class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("About expense manager app")
        self.setMinimumSize(800, 600)

        v_box_layout = QVBoxLayout()

        text = QTextEdit()
        text.setReadOnly(True)

        about_text = ("""
            <h2>📊 Simple expense manager app created by Peter Szepesi, Slovakia</h2><br>
            <p>&nbsp;• You can sort by any column by simply clicking the column name, clicking multiple times<br>
               &nbsp;&nbsp;&nbsp;&nbsp;changes the order, either ascending or descending<br>
               &nbsp;• For editing any values, double-click any cell, than after fixing the value, press enter to<br>
               &nbsp;&nbsp;&nbsp;&nbsp;to save the new value<br><br> 
            If you encounter any issues related to this app, please report them via : szpeto12@gmail.com<br>
            and if you could, please include the log file, which is located in the same directory,<br>
            where your .exe file is located, under Log\\log.txt.<br><br>
            If you like my app and you feel that way, you can support me in my work,<br>
            I would be really grateful and appreciate any amount of donation.<br>
            You can do it via support me button, or IBAN account transfer,<br>
            IBAN account number : SK90 0900 0000 0051 2726 1825<br><br>
            Thank you very much!<br>
            Peter</p>
        """)

        text.setHtml(about_text)
        v_box_layout.addWidget(text)
        self.setLayout(v_box_layout)

        self.setStyleSheet("""
            QTextEdit{
                font-family: Segoe UI;
                font-size: 18px;
            }
        """)
