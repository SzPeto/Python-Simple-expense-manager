
import datetime
import os.path
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QWidget, QPushButton, QHBoxLayout, QLabel, \
    QLineEdit, QComboBox, QTableWidgetItem, QHeaderView, QFrame, QSizePolicy, QStackedLayout

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
        get_main_instance(self)
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_file = self.create_file_dir("Log\\log.txt")
        self.write_log_init()

        # Geometry
        self.window_width = int(self.monitor.width() * 0.5)
        self.window_height = int(self.monitor.height() * 0.85)

        # Layout
        self.v_box_main = QVBoxLayout()
        self.h_box_upper = QHBoxLayout()
        self.v_box_upper_1 = QVBoxLayout()
        self.v_box_upper_2 = QVBoxLayout()
        self.v_box_upper_3 = QVBoxLayout()
        self.v_box_upper_4 = QVBoxLayout()
        self.h_box_date = QHBoxLayout()
        self.h_box_price = QHBoxLayout()
        self.h_box_filter_main = QHBoxLayout()
        self.stack_filter_changing = QStackedLayout()
        self.filter_page_id = QWidget()
        self.filter_page_category = QWidget()
        self.filter_page_price = QWidget()
        self.filter_page_date = QWidget()
        self.h_box_filter_changing_id = QHBoxLayout()
        self.h_box_filter_changing_category = QHBoxLayout()
        self.h_box_filter_changing_price = QHBoxLayout()
        self.h_box_filter_changing_date = QHBoxLayout()
        self.separator = QFrame()

        # Database
        self.db_connection = create_connection(self.resource_path("Databases\\main.db"))
        self.table_name = "expenses"
        self.cursor = self.db_connection.cursor()
        create_table(self.cursor, self.table_name)

        # Buttons
        self.add_button = QPushButton("Add")
        self.delete_selected_button = QPushButton("Delete selected")
        self.delete_all_button = QPushButton("Delete all")
        self.refresh_button = QPushButton("Refresh")
        self.filter_button = QPushButton("Filter")

        # Labels
        self.description_label = QLabel("Description")
        self.price_label = QLabel("Price")
        self.category_label = QLabel("Category")
        self.date_label = QLabel("Date")
        self.price_decimal_label = QLabel(".")
        self.date_format_label = QLabel("YYYY - MM - DD")
        self.filter_label = QLabel("Filter by : ")
        self.filter_dash_label = QLabel("-")
        self.date_from_label = QLabel("Date FROM:")
        self.date_to_label = QLabel("Date TO:")

        # Line edits and combo boxes
        self.description_line_edit = QLineEdit()
        self.price_line_edit = QLineEdit()
        self.price_decimal_line_edit = QLineEdit()
        self.category_combo_box = QComboBox()
        self.year_line_edit = QLineEdit()
        self.month_line_edit = QLineEdit()
        self.day_line_edit = QLineEdit()
        self.filter_by_combo_box = QComboBox()
        self.filter_category_combo_box = QComboBox()
        self.filter_line_edit_id = QLineEdit()
        self.filter_price_from = QLineEdit()
        self.filter_price_to = QLineEdit()
        self.filter_date_day_from = QLineEdit()
        self.filter_date_month_from = QLineEdit()
        self.filter_date_year_from = QLineEdit()
        self.filter_date_day_to = QLineEdit()
        self.filter_date_month_to = QLineEdit()
        self.filter_date_year_to = QLineEdit()

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
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(2)
            # Wrapping the changing filter layouts into QWidgets
        self.filter_page_id.setLayout(self.h_box_filter_changing_id)
        self.filter_page_category.setLayout(self.h_box_filter_changing_category)
        self.filter_page_price.setLayout(self.h_box_filter_changing_price)
        self.filter_page_date.setLayout(self.h_box_filter_changing_date)
            # Adding into stack layout
        self.stack_filter_changing.addWidget(self.filter_page_id)
        self.stack_filter_changing.addWidget(self.filter_page_category)
        self.stack_filter_changing.addWidget(self.filter_page_price)
        self.stack_filter_changing.addWidget(self.filter_page_date)
        self.stack_filter_changing.setCurrentIndex(1)
            #
        self.h_box_date.addWidget(self.year_line_edit)
        self.h_box_date.addWidget(self.month_line_edit)
        self.h_box_date.addWidget(self.day_line_edit)
        self.h_box_date.addWidget(self.date_format_label)
        self.h_box_date.addStretch()
        self.h_box_price.addWidget(self.price_line_edit, alignment = Qt.AlignLeft)
        self.h_box_price.addWidget(self.price_decimal_label, alignment = Qt.AlignLeft)
        self.h_box_price.addWidget(self.price_decimal_line_edit, alignment = Qt.AlignLeft)
        self.h_box_price.addStretch()
            # Constructing the changing filter hbox
        self.h_box_filter_changing_id.addWidget(self.filter_line_edit_id)
        self.h_box_filter_changing_category.addWidget(self.filter_category_combo_box)
        self.h_box_filter_changing_price.addWidget(self.filter_price_from)
        self.h_box_filter_changing_price.addWidget(self.filter_dash_label)
        self.h_box_filter_changing_price.addWidget(self.filter_price_to)
        self.h_box_filter_changing_date.addWidget(self.date_from_label)
        self.h_box_filter_changing_date.addWidget(self.filter_date_day_from)
        self.h_box_filter_changing_date.addWidget(self.filter_date_month_from)
        self.h_box_filter_changing_date.addWidget(self.filter_date_year_from)
        self.h_box_filter_changing_date.addStretch()
        self.h_box_filter_changing_date.addWidget(self.date_to_label)
        self.h_box_filter_changing_date.addWidget(self.filter_date_day_to)
        self.h_box_filter_changing_date.addWidget(self.filter_date_month_to)
        self.h_box_filter_changing_date.addWidget(self.filter_date_year_to)

        self.h_box_filter_main.addWidget(self.filter_label)
        self.h_box_filter_main.addWidget(self.filter_by_combo_box)
        self.h_box_filter_main.addLayout(self.stack_filter_changing)
        self.h_box_filter_main.addWidget(self.filter_button)
        self.v_box_upper_1.addWidget(self.description_label)
        self.v_box_upper_1.addWidget(self.category_label)
        self.v_box_upper_1.addWidget(self.price_label)
        self.v_box_upper_1.addWidget(self.date_label)
        self.v_box_upper_2.addWidget(self.description_line_edit)
        self.v_box_upper_2.addWidget(self.category_combo_box, alignment = Qt.AlignLeft)
        self.v_box_upper_2.addLayout(self.h_box_price)
        self.v_box_upper_2.addLayout(self.h_box_date)
        self.v_box_upper_3.addWidget(self.add_button)
        self.v_box_upper_3.addWidget(self.delete_selected_button)
        self.v_box_upper_3.addWidget(self.delete_all_button)
        self.v_box_upper_4.addWidget(self.refresh_button)

        self.h_box_upper.addLayout(self.v_box_upper_1)
        self.h_box_upper.addLayout(self.v_box_upper_2)
        self.h_box_upper.addLayout(self.v_box_upper_3)
        self.h_box_upper.addLayout(self.v_box_upper_4)

        self.v_box_main.addLayout(self.h_box_upper)
        self.v_box_main.addWidget(self.separator)
        self.v_box_main.addLayout(self.h_box_filter_main)
        self.v_box_main.addWidget(self.expenses_table)
        self.central_widget.setLayout(self.v_box_main)

        # Event handling
        self.add_button.clicked.connect(self.add_entry)
        self.delete_selected_button.clicked.connect(self.delete_selected)
        self.delete_all_button.clicked.connect(self.delete_all)
        self.refresh_button.clicked.connect(self.refresh)
        self.filter_by_combo_box.currentIndexChanged.connect(self.change_filter)

        # Buttons, labels and other
        self.filter_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setWindowTitle("Simple expense manager by Peter Szepesi")
        self.year_line_edit.setText(str(self.today_date.year))
        self.month_line_edit.setText(str(f"{self.today_date.month:02}"))
        self.day_line_edit.setText(str(f"{self.today_date.day:02}"))
        self.price_decimal_line_edit.setText("00")
        self.filter_price_from.setPlaceholderText("Price FROM")
        self.filter_price_to.setPlaceholderText("Price TO")
        self.filter_date_day_from.setPlaceholderText("DD")
        self.filter_date_month_from.setPlaceholderText("MM")
        self.filter_date_year_from.setPlaceholderText("YYYY")
        self.filter_date_day_to.setPlaceholderText("DD")
        self.filter_date_month_to.setPlaceholderText("MM")
        self.filter_date_year_to.setPlaceholderText("YYYY")
        self.category_combo_box.addItems([
            "Groceries", "Utilities", "Rent", "Transportation", "Gas",
            "Dining Out", "Health", "Insurance", "Clothing", "Entertainment",
            "Subscriptions", "Phone", "Internet", "Education", "Gifts",
            "Travel", "Household Supplies", "Pets", "Childcare", "Savings",
            "Debt Payments", "Personal Care", "Fitness", "Miscellaneous"
        ])
        self.filter_category_combo_box.addItems([
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
        self.filter_by_combo_box.addItems(["ID", "Category", "Price", "Date"])
        self.filter_line_edit_id.setPlaceholderText("Enter ID")

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
            date = f"{self.year_line_edit.text()}-{int(self.month_line_edit.text()):02}-{int(self.day_line_edit.text()):02}"

            insert_entry(self.cursor, self.table_name, description, category, price, date)
            self.db_connection.commit()
            self.fill_table()
        except Exception as e:
            self.write_log(f"Something went wrong during adding entry : {e}")

    def change_filter(self):
        filter_text = self.filter_by_combo_box.currentText().lower()
        if filter_text == "id":
           self.stack_filter_changing.setCurrentIndex(0)
        elif filter_text == "category":
            self.stack_filter_changing.setCurrentIndex(1)
        elif filter_text == "price":
            self.stack_filter_changing.setCurrentIndex(2)
        elif filter_text == "date":
            self.stack_filter_changing.setCurrentIndex(3)

    def fill_table(self):
        try:
            self.write_log(f"Filling table")
            create_table(self.cursor, self.table_name)
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
            self.write_log(f"Something went wrong during filling the table : {e}")

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
                self.write_log("There is nothing selected")
        except Exception as e:
            self.write_log(f"Something went wrong deleting selected items : {e}")

        try:
            self.db_connection.commit()
            self.fill_table()
        except Exception as e:
            self.write_log(f"Something went wrong during filling the table : {e}")


    def delete_all(self):
        try:
            delete_table(self.cursor, self.table_name)
            self.db_connection.commit()
            self.fill_table()
        except Exception as e:
            self.write_log(f"Something went wrong deleting table : {e}")

    def refresh(self):
        self.fill_table()

    # Resource path
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path) # In case of exe return the absolute path
        else:
            return os.path.join(os.path.abspath("."), relative_path) # In case of IDE return the relative path

    def write_log_init(self):
        with open(self.log_file, "a", encoding = "utf-8") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            log_file.write("\n")
            log_file.write(f"{timestamp} *****************************************************************************")
            log_file.write("\n")

    def write_log(self, text):
        with open(self.log_file, "a", encoding = "utf-8") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S - ")
            log_file.write(f"{timestamp}{text}")
            log_file.write("\n")

    def create_file_dir(self, file_path):
        try:
            dir_name = os.path.dirname(file_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
        except Exception as e:
            print(f"Error during creating directory : {e}")

        return file_path

    # Replacing widgets and layouts during runtime
    def replace_widget(self, layout, index, new_widget):
        item = layout.itemAt(index)
        if item is None:
            self.write_log(f"There is no such widget at index : {index} in layout : {layout}")
            return

        old_widget = item.widget()
        if old_widget is not None:
            old_widget.setParent(None) # Remove old widget

        layout.insertWidget(index, new_widget, alignment = Qt.AlignLeft)

    def replace_layout(self, layout, index, new_layout):
        item = layout.itemAt(index)
        if item is None:
            self.write_log(f"There is no such layout at index : {index} in layout : {layout}")
            return

        old_layout = item.layout()
        if old_layout is not None:
            self.remove_layout(old_layout)
            layout.removeItem(item)

        layout.insertLayout(index, new_layout, alignment=Qt.AlignLeft)

    def remove_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.setParent(None)
            if child_layout is not None:
                self.remove_layout(child_layout)