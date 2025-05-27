# TODO - make the resource path function

import datetime
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QWidget, QPushButton, QHBoxLayout, QLabel, \
    QLineEdit, QComboBox, QTableWidgetItem, QHeaderView

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
        self.h_box_price = QHBoxLayout()

        # Database
        self.db_connection = create_connection(self.resource_path("Databases\\main.db"))
        self.table_name = "expenses"
        self.cursor = self.db_connection.cursor()
        create_table(self.cursor, self.table_name)

        # Buttons
        self.add_button = QPushButton("Add")
        self.delete_selected_button = QPushButton("Delete selected")
        self.delete_all_button = QPushButton("Delete all")

        # Labels
        self.description_label = QLabel("Description")
        self.price_label = QLabel("Price")
        self.category_label = QLabel("Category")
        self.date_label = QLabel("Date")
        self.price_decimal_label = QLabel(".")
        self.date_format_label = QLabel("YYYY - MM - DD")

        # Line edits and combo boxes
        self.description_line_edit = QLineEdit()
        self.price_line_edit = QLineEdit()
        self.price_decimal_line_edit = QLineEdit()
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
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.center_window()

        #Layout
        self.setCentralWidget(self.central_widget)
        self.h_box_date.addWidget(self.year_line_edit)
        self.h_box_date.addWidget(self.month_line_edit)
        self.h_box_date.addWidget(self.day_line_edit)
        self.h_box_date.addWidget(self.date_format_label)
        self.h_box_date.addStretch()
        self.h_box_price.addWidget(self.price_line_edit, alignment = Qt.AlignLeft)
        self.h_box_price.addWidget(self.price_decimal_label, alignment = Qt.AlignLeft)
        self.h_box_price.addWidget(self.price_decimal_line_edit, alignment = Qt.AlignLeft)
        self.h_box_price.addStretch()
        self.v_box_upper_left.addWidget(self.description_label)
        self.v_box_upper_left.addWidget(self.category_label)
        self.v_box_upper_left.addWidget(self.price_label)
        self.v_box_upper_left.addWidget(self.date_label)
        self.v_box_upper_middle.addWidget(self.description_line_edit)
        self.v_box_upper_middle.addWidget(self.category_combo_box, alignment = Qt.AlignLeft)
        self.v_box_upper_middle.addLayout(self.h_box_price)
        self.v_box_upper_middle.addLayout(self.h_box_date)
        self.v_box_upper_right.addWidget(self.add_button)
        self.v_box_upper_right.addWidget(self.delete_selected_button)
        self.v_box_upper_right.addWidget(self.delete_all_button)

        self.h_box_upper.addLayout(self.v_box_upper_left)
        self.h_box_upper.addLayout(self.v_box_upper_middle)
        self.h_box_upper.addLayout(self.v_box_upper_right)

        self.v_box_main.addLayout(self.h_box_upper)
        self.v_box_main.addWidget(self.expenses_table)
        self.central_widget.setLayout(self.v_box_main)

        # Event handling
        self.add_button.clicked.connect(self.add_entry)
        self.delete_selected_button.clicked.connect(self.delete_selected)
        self.delete_all_button.clicked.connect(self.delete_all)

        # Buttons, labels and other
        self.setWindowTitle("Simple expense manager by Peter Szepesi")
        self.year_line_edit.setText(str(self.today_date.year))
        self.month_line_edit.setText(str(f"{self.today_date.month:02}"))
        self.day_line_edit.setText(str(f"{self.today_date.day:02}"))
        self.price_decimal_line_edit.setText("00")
        self.category_combo_box.addItems([
            "Groceries", "Utilities", "Rent", "Transportation", "Gas",
            "Dining Out", "Health", "Insurance", "Clothing", "Entertainment",
            "Subscriptions", "Phone", "Internet", "Education", "Gifts",
            "Travel", "Household Supplies", "Pets", "Childcare", "Savings",
            "Debt Payments", "Personal Care", "Fitness", "Miscellaneous"
        ])
        self.expenses_table.setColumnCount(5)
        self.expenses_table.setHorizontalHeaderLabels(["ID", "Description", "Category", "Price", "Date"])
        self.expenses_table.verticalHeader().setVisible(False)
        self.fill_table()
        self.expenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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

        try:
            # TODO - Make exception handling, add month and day formatting - :02
            create_table(self.cursor, self.table_name)
            description = self.description_line_edit.text()
            category = self.category_combo_box.currentText()
            price = float(f"{self.price_line_edit.text()}.{self.price_decimal_line_edit.text()}")
            price = round(price, 2)
            date = f"{self.year_line_edit.text()}-{self.month_line_edit.text()}-{self.day_line_edit.text()}"

            insert_entry(self.cursor, self.table_name, description, category, price, date)
            self.db_connection.commit()
            self.fill_table()
        except Exception as e:
            print(f"Something went wrong during adding entry : {e}")

    def fill_table(self):
        try:
            rows = show_all(self.cursor, self.table_name)
            if rows:
                self.expenses_table.setRowCount(len(rows))
                for row_index in range(0, len(rows)):
                    row = rows[row_index]
                    for column_index in range(0, len(row)):
                        column = row[column_index]
                        cell = QTableWidgetItem(str(column))
                        self.expenses_table.setItem(row_index, column_index, cell)
            else:
                self.expenses_table.setRowCount(0)
        except Exception as e:
            print(f"Something went wrong during filling the table : {e}")

    def delete_selected(self):

        try:
            selected_column_data = self.expenses_table.selectedItems()
            if selected_column_data:
                for i in range(0, len(selected_column_data)):
                    selected_cell = selected_column_data[i]
                    row = selected_cell.row()
                    column = selected_cell.column()
                    selected_cell_id = self.expenses_table.item(row, 0).text()
                    if selected_cell_id.isdigit():
                        selected_cell_id = int(selected_cell_id)
                        delete_entry(self.cursor, self.table_name, "id", selected_cell_id)
            else:
                print("There is nothing selected")
        except Exception as e:
            print(f"Something went wrong deleting selected items : {e}")

        try:
            self.db_connection.commit()
            self.fill_table()
        except Exception as e:
            print(f"Something went wrong during filling the table : {e}")


    def delete_all(self):
        try:
            delete_table(self.cursor, self.table_name)
            self.db_connection.commit()
            self.fill_table()
        except Exception as e:
            print(f"Something went wrong deleting table : {e}")

    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path) # In case of exe return the absolute path
        else:
            return os.path.join(os.path.abspath("."), relative_path) # In case of IDE return the relative path