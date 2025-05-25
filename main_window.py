import datetime

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QWidget, QPushButton, QHBoxLayout, QLabel, \
    QLineEdit, QComboBox

from main_database import *


class MainWindow(QMainWindow):

    def __init__(self, main_instance):
        super().__init__()
        from Main import Main

        # Master
        self.central_widget = QWidget()
        self.monitor = QGuiApplication.primaryScreen().geometry()
        self.main_instance: Main = main_instance
        self.today_date = datetime.date.today()

        # Geometry
        self.window_width = int(self.monitor.width() * 0.5)
        self.window_height = int(self.monitor.height() * 0.85)

        # Layout
        self.v_box_main = QVBoxLayout()
        self.h_box_upper = QHBoxLayout()
        self.v_box_upper_left = QVBoxLayout()
        self.v_box_upper_middle = QVBoxLayout()
        self.v_box_upper_right = QVBoxLayout()
        self.h_box_date = QHBoxLayout()

        # Database
        self.db_connection = create_connection("Databases\\main.db")
        self.table_name = "expenses"
        self.cursor = self.db_connection.cursor()
        create_table(self.cursor, self.table_name)

        # Buttons
        self.add_button = QPushButton("Add")

        # Labels
        self.description_label = QLabel("Description")
        self.price_label = QLabel("Price")
        self.category_label = QLabel("Category")
        self.date_label = QLabel("Date")

        # Line edits and combo boxes
        self.description_line_edit = QLineEdit()
        self.price_line_edit = QLineEdit()
        self.category_combo_box = QComboBox()
        self.year_line_edit = QLineEdit()
        self.month_line_edit = QLineEdit()
        self.day_line_edit = QLineEdit()

        # Other
        self.expenses_table = QTableWidget()

        # Method calls
        self.initUI()

    def initUI(self):

        # Geometry
        self.setMinimumWidth(self.window_width)
        self.setMinimumHeight(self.window_height)
        self.center_window()

        #Layout
        self.setCentralWidget(self.central_widget)
        self.h_box_date.addWidget(self.year_line_edit)
        self.h_box_date.addWidget(self.month_line_edit)
        self.h_box_date.addWidget(self.day_line_edit)
        self.v_box_upper_left.addWidget(self.description_label)
        self.v_box_upper_left.addWidget(self.category_label)
        self.v_box_upper_left.addWidget(self.price_label)
        self.v_box_upper_left.addWidget(self.date_label)
        self.v_box_upper_middle.addWidget(self.description_line_edit)
        self.v_box_upper_middle.addWidget(self.category_combo_box)
        self.v_box_upper_middle.addWidget(self.price_line_edit)
        self.v_box_upper_middle.addLayout(self.h_box_date)
        self.v_box_upper_right.addWidget(self.add_button)

        self.h_box_upper.addLayout(self.v_box_upper_left)
        self.h_box_upper.addLayout(self.v_box_upper_middle)
        self.h_box_upper.addLayout(self.v_box_upper_right)

        self.v_box_main.addLayout(self.h_box_upper)
        self.v_box_main.addWidget(self.expenses_table)
        self.central_widget.setLayout(self.v_box_main)

        # Event handling
        self.add_button.clicked.connect(self.add_entry)

        # Buttons, labels and other
        self.year_line_edit.setText(str(self.today_date.year))
        self.month_line_edit.setText(str(f"{self.today_date.month:02}"))
        self.day_line_edit.setText(str(f"{self.today_date.day:02}"))
        self.category_combo_box.addItems([
            "Groceries", "Utilities", "Rent", "Transportation", "Gas",
            "Dining Out", "Health", "Insurance", "Clothing", "Entertainment",
            "Subscriptions", "Phone", "Internet", "Education", "Gifts",
            "Travel", "Household Supplies", "Pets", "Childcare", "Savings",
            "Debt Payments", "Personal Care", "Fitness", "Miscellaneous"
        ])

    def center_window(self):
        window_width = self.width()
        window_height = self.height()
        monitor_width = self.monitor.width()
        monitor_height = self.monitor.height()
        window_x = int((monitor_width - window_width) / 2)
        window_y = int((monitor_height - window_height) / 2)
        self.setGeometry(window_x, window_y, window_width, window_height)

    # Event handling
    def add_entry(self):

        # TODO - Make exception handling

        description = self.description_line_edit.text()
        category = self.category_combo_box.currentText()
        price = float(self.price_line_edit.text())
        date = f"{self.year_line_edit.text()}-{self.month_line_edit.text()}-{self.day_line_edit.text()}"

        insert_entry(self.cursor, self.table_name, description, category, price, date)
        self.db_connection.commit()
        show_all(self.cursor, self.table_name)