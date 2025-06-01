
import datetime
import os.path
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QIntValidator, QColor
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QWidget, QPushButton, QHBoxLayout, QLabel, \
    QLineEdit, QComboBox, QTableWidgetItem, QHeaderView, QFrame, QSizePolicy, QStackedLayout, QMessageBox, \
    QGraphicsDropShadowEffect

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
        self.categories = [
            "Groceries", "Utilities", "Rent", "Transportation", "Gas",
            "Dining Out", "Health", "Insurance", "Clothing", "Entertainment",
            "Subscriptions", "Phone", "Internet", "Education", "Gifts",
            "Travel", "Household Supplies", "Pets", "Childcare", "Savings",
            "Debt Payments", "Personal Care", "Fitness", "Miscellaneous"
        ]
        self.int_validator = QIntValidator(-2147483648, 2147483647)
        self.int_day_validator = QIntValidator(1, 31)
        self.int_month_validator = QIntValidator(1, 12)
        self.int_year_validator = QIntValidator(1, 8888)
        self.is_asc = True

        # Geometry
        self.window_width = int(self.monitor.width() * 0.5)
        self.window_height = int(self.monitor.height() * 0.85)

        # Layout
        self.v_box_main = QVBoxLayout() # The main layout, level 0
        self.h_box_upper = QHBoxLayout()
        self.v_box_upper_1 = QVBoxLayout()
        self.v_box_upper_2 = QVBoxLayout()
        self.v_box_upper_3 = QVBoxLayout()
        self.v_box_upper_4 = QVBoxLayout()
        self.h_box_date = QHBoxLayout()
        self.h_box_price = QHBoxLayout()
        self.h_box_filter_main = QHBoxLayout()
        self.h_box_filter_2 = QHBoxLayout()
        self.stack_filter_changing = QStackedLayout()
        self.filter_page_id = QWidget()
        self.filter_page_category = QWidget()
        self.filter_page_price = QWidget()
        self.filter_page_date = QWidget()
        self.h_box_filter_changing_id = QHBoxLayout()
        self.h_box_filter_changing_category = QHBoxLayout()
        self.h_box_filter_changing_price = QHBoxLayout()
        self.h_box_filter_changing_date = QHBoxLayout()
        self.separator_1 = QFrame()
        self.separator_2 = QFrame()
        self.stack_filter_changing_qwidget = QWidget()
        self.h_box_buttons = QHBoxLayout()
        self.v_box_buttons_1 = QVBoxLayout()
        self.v_box_buttons_2 = QVBoxLayout()

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
        self.filter_button = QPushButton("Filter results")
        self.clear_filters_button = QPushButton("Clear all filters")

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
        self.sum_label = QLabel("")

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
        self.filter_line_edit_id_from = QLineEdit()
        self.filter_line_edit_id_to = QLineEdit()
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
        self.separator_1.setFrameShape(QFrame.HLine)
        self.separator_1.setFrameShadow(QFrame.Sunken)
        self.separator_1.setLineWidth(2)
        self.separator_2.setFrameShape(QFrame.HLine)
        self.separator_2.setFrameShadow(QFrame.Sunken)
        self.separator_2.setLineWidth(2)
            # Level 4
        self.v_box_buttons_1.addWidget(self.delete_selected_button)
        self.v_box_buttons_1.addWidget(self.delete_all_button)
        self.v_box_buttons_2.addWidget(self.refresh_button)
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
        self.h_box_filter_changing_id.addWidget(self.filter_line_edit_id_from)
        self.h_box_filter_changing_id.addWidget(self.filter_line_edit_id_to)
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
            # Level 3
        self.h_box_buttons.addLayout(self.v_box_buttons_1)
        self.h_box_buttons.addLayout(self.v_box_buttons_2)
        self.stack_filter_changing_qwidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.v_box_upper_1.addWidget(self.description_label)
        self.v_box_upper_1.addWidget(self.category_label)
        self.v_box_upper_1.addWidget(self.price_label)
        self.v_box_upper_1.addWidget(self.date_label)
        self.v_box_upper_2.addWidget(self.description_line_edit)
        self.v_box_upper_2.addWidget(self.category_combo_box, alignment = Qt.AlignLeft)
        self.v_box_upper_2.addLayout(self.h_box_price)
        self.v_box_upper_2.addLayout(self.h_box_date)
        self.v_box_upper_3.addWidget(self.add_button)
        self.v_box_upper_3.addLayout(self.h_box_buttons)
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
        self.stack_filter_changing_qwidget.setLayout(self.stack_filter_changing)
            # Level 2
        self.h_box_upper.addLayout(self.v_box_upper_1)
        self.h_box_upper.addLayout(self.v_box_upper_2)
        self.h_box_upper.addLayout(self.v_box_upper_3)
        #self.h_box_upper.addLayout(self.v_box_upper_4)
        self.h_box_filter_main.addWidget(self.filter_label)
        self.h_box_filter_main.addWidget(self.filter_by_combo_box)
        self.h_box_filter_main.addWidget(self.stack_filter_changing_qwidget)
        self.h_box_filter_main.addWidget(self.filter_button)
        self.h_box_filter_2.addWidget(self.clear_filters_button)
            # Level 1
        self.v_box_main.addLayout(self.h_box_upper)
        self.v_box_main.addWidget(self.separator_1)
        self.v_box_main.addLayout(self.h_box_filter_main)
        self.v_box_main.addLayout(self.h_box_filter_2)
        self.v_box_main.addWidget(self.separator_2)
        self.v_box_main.addWidget(self.expenses_table)
        self.v_box_main.addWidget(self.sum_label, alignment = Qt.AlignRight)
        self.central_widget.setLayout(self.v_box_main)

        # Event handling
        self.add_button.clicked.connect(self.add_entry)
        self.delete_selected_button.clicked.connect(self.delete_selected)
        self.delete_all_button.clicked.connect(self.delete_all)
        self.refresh_button.clicked.connect(self.refresh)
        self.filter_by_combo_box.currentIndexChanged.connect(self.change_filter)
        self.filter_button.clicked.connect(self.filter_selected)
        self.clear_filters_button.clicked.connect(self.refresh)
        #self.expenses_table.horizontalHeader().sectionClicked.connect(self.order_table)

        # Buttons, labels and other
        self.filter_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setWindowTitle("Simple expense manager by Peter Szepesi")
        self.year_line_edit.setText(str(self.today_date.year))
        self.month_line_edit.setText(str(f"{self.today_date.month:02}"))
        self.day_line_edit.setText(str(f"{self.today_date.day:02}"))
        self.price_decimal_line_edit.setText("00")
        self.filter_price_from.setPlaceholderText("Price FROM")
        self.filter_price_to.setPlaceholderText("Price TO")
        self.filter_date_day_from.setText("01")
        self.filter_date_month_from.setText(f"{self.today_date.month:02}")
        self.filter_date_year_from.setText(f"{self.today_date.year}")
        self.filter_date_day_to.setText(f"{self.today_date.day:02}")
        self.filter_date_month_to.setText(f"{self.today_date.month:02}")
        self.filter_date_year_to.setText(f"{self.today_date.year}")
        self.category_combo_box.addItems(self.categories)
        self.filter_category_combo_box.addItems(self.categories)
        self.expenses_table.setColumnCount(5)
        self.expenses_table.setHorizontalHeaderLabels(["ID", "Description", "Category", "Price", "Date"])
        self.expenses_table.verticalHeader().setVisible(False)
        self.fill_table()
        self.expenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.filter_by_combo_box.addItems(["ID", "Category", "Price", "Date"])
        self.filter_line_edit_id_from.setPlaceholderText("Id FROM")
        self.filter_line_edit_id_to.setPlaceholderText("Id TO")
        self.expenses_table.setSortingEnabled(True)
            # Setting line edit validators
        self.filter_line_edit_id_from.setValidator(self.int_validator)
        self.filter_line_edit_id_to.setValidator(self.int_validator)
        self.day_line_edit.setValidator(self.int_day_validator)
        self.month_line_edit.setValidator(self.int_month_validator)
        self.year_line_edit.setValidator(self.int_year_validator)
        self.price_line_edit.setValidator(self.int_validator)
        self.price_decimal_line_edit.setValidator(self.int_validator)
        self.filter_date_day_from.setValidator(self.int_day_validator)
        self.filter_date_month_from.setValidator(self.int_month_validator)
        self.filter_date_year_from.setValidator(self.int_year_validator)
        self.filter_date_day_to.setValidator(self.int_day_validator)
        self.filter_date_month_to.setValidator(self.int_month_validator)
        self.filter_date_year_to.setValidator(self.int_year_validator)
        self.filter_line_edit_id_from.setValidator(self.int_validator)
        self.filter_line_edit_id_to.setValidator(self.int_validator)

        # Object names for QSS styling
        self.sum_label.setObjectName("sumLabel")

        # Styling
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black
        self.shadow.setOffset(3, 3)
        self.sum_label.setGraphicsEffect(self.shadow)
            # Setting the stylesheet
        self.setStyleSheet("""
            
            MainWindow{
                background-color: rgb(235, 235, 255);
            }
            
            QLabel#sumLabel{
                font-size: 25px;
                font-family: Segoe UI;
                background-color: white;
                padding: 10px;
                border-radius: 10px;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(255, 255, 255),  /* Top of gradient */
                    stop:1 rgb(235, 235, 235)   /* Bottom of gradient */
                );
                border: 1px solid rgb(214, 214, 214);
                font-weight: bold;
                color: rgb(111, 111, 111);
            }
        
        """)

    def center_window(self):
        window_width = self.width()
        window_height = self.height()
        monitor_width = self.monitor.width()
        monitor_height = self.monitor.height()
        window_x = int((monitor_width - window_width) / 2)
        window_y = int((monitor_height - window_height) / 2)
        self.setGeometry(window_x, window_y, window_width, window_height)

    # Event handling ******************************************************************
    def add_entry(self):

        try:
            create_table(self.cursor, self.table_name)
            description = self.description_line_edit.text()
            category = self.category_combo_box.currentText()
            price = float(f"{self.price_line_edit.text()}.{self.price_decimal_line_edit.text()}")
            price = round(price, 2)
            day = int(self.day_line_edit.text())
            month = int(self.month_line_edit.text())
            year = int(self.year_line_edit.text())
            date = f"{year}-{month:02}-{day:02}"
            if not self.is_valid_date(date):
                self.print_warning_message("Invalid date", "Please enter a valid date!")
                return
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

    def filter_selected(self):
        index = self.stack_filter_changing.currentIndex()
        if index == 0:
            try:
                id_from = int(self.filter_line_edit_id_from.text())
                id_to = int(self.filter_line_edit_id_to.text())
                if not id_from or not id_to:
                    self.print_warning_message("Empty field", "Please fill the values!")
                rows = search_based_on_condition(
                    self.cursor, self.table_name, f"id >= {id_from} and id <= {id_to}"
                )
                self.fill_table_selected(rows)
            except Exception as e:
                self.write_log(f"def filter_selected : {e}")
                self.print_warning_message("Empty", "No results to show, please enter a valid input!")

        elif index == 1:
            try:
                category = self.filter_category_combo_box.currentText()
                rows = search_based_on_condition(
                    self.cursor, self.table_name, f"category = '{category}'"
                )
                self.fill_table_selected(rows)
            except Exception as e:
                self.write_log(f"def filter_selected : {e}")
                self.print_warning_message("Invalid input", f"Something went wrong, (error : {e})")
        elif index == 2:
            try:
                price_from = float(self.filter_price_from.text())
                price_to = float(self.filter_price_to.text())
                if not price_from or not price_to:
                    self.print_warning_message("Empty field", "Please fill the values!")
                rows = search_based_on_condition(
                    self.cursor, self.table_name,
                    f"price >= {price_from} and price <= {price_to}"
                )
                self.fill_table_selected(rows)
            except Exception as e:
                self.print_warning_message("Empty", "No results to show, please enter a valid input!")
                self.write_log(f"def filter_selected : exception : {e}")
        elif index == 3:
            try:
                day_from = int(self.filter_date_day_from.text())
                month_from = int(self.filter_date_month_from.text())
                year_from = int(self.filter_date_year_from.text())
                day_to = int(self.filter_date_day_to.text())
                month_to = int(self.filter_date_month_to.text())
                year_to = int(self.filter_date_year_to.text())
                date_from_validation = f"{year_from}-{month_from:02}-{day_from:02}"
                date_to_validation = f"{year_to}-{month_to:02}-{day_to:02}"
                date_from = f"'{year_from}-{month_from:02}-{day_from:02}'"
                date_to = f"'{year_to}-{month_to:02}-{day_to:02}'"
                if not self.is_valid_date(date_from_validation) or not self.is_valid_date(date_to_validation):
                    self.print_warning_message("Invalid date", "Please enter a valid date")
                    return

                rows = search_based_on_condition(
                    self.cursor, self.table_name,
                    f"date >= {date_from} and date <= {date_to}"
                )
                self.fill_table_selected(rows)
            except Exception as e:
                self.print_warning_message("Empty", "No results to show, please enter a valid input!")
                self.write_log(f"def filter_selected : exception : {e}")

    def fill_table(self):
        try:
            create_table(self.cursor, self.table_name)
            rows = show_all(self.cursor, self.table_name)
            if rows:
                self.expenses_table.setRowCount(len(rows))
                for row_index in range(0, len(rows)):
                    row = rows[row_index]
                    for column_index in range(0, len(row)):
                        column = row[column_index]

                        if column_index == 0:
                            cell = QTableWidgetItem()
                            cell.setData(Qt.EditRole, int(column))
                            cell.setText(f"{int(column)}")
                        elif column_index == 3:
                            cell = QTableWidgetItem()
                            cell.setData(Qt.EditRole, float(column))
                            cell.setText(f"{float(column):.2f}")
                        else:
                            cell = QTableWidgetItem(str(column))

                        self.expenses_table.setItem(row_index, column_index, cell)

            else:
                self.expenses_table.setRowCount(0)
        except Exception as e:
            self.write_log(f"def fill_table : something went wrong during filling the table : {e}")

        self.count_prices()

    def fill_table_selected(self, rows):
        try:
            if rows:
                self.expenses_table.setRowCount(len(rows))
                for row_index in range(0, len(rows)):
                    row = rows[row_index]
                    for column_index in range(0, len(row)):
                        column = row[column_index]
                        if column_index == 0:
                            cell = QTableWidgetItem()
                            cell.setData(Qt.EditRole, int(column))
                            cell.setText(f"{int(column)}")
                        elif column_index == 3:
                            cell = QTableWidgetItem()
                            cell.setData(Qt.EditRole, float(column))
                            cell.setText(f"{float(column):.2f}")
                        else:
                            cell = QTableWidgetItem(str(column))

                        self.expenses_table.setItem(row_index, column_index, cell)
            else:
                self.expenses_table.setRowCount(0)
                self.print_warning_message("Empty", "No results to show!")
        except Exception as e:
            self.write_log(f"def fill_table_selected : something went wrong during filling the table : {e}")

        self.count_prices()

    def order_table(self, index):
        # self.expenses_table.horizontalHeader().sectionClicked.connect(self.order_table) - automatically passes
        # the column index
        column = self.expenses_table.horizontalHeaderItem(index).text().lower()
        if self.is_asc:
            rows = order_by(self.cursor, self.table_name, column, "ASC")
            self.is_asc = False
        else:
            rows = order_by(self.cursor, self.table_name, column, "DESC")
            self.is_asc = True

        self.fill_table_selected(rows)

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

    # Print warning
    def print_warning_message(self, title, text):
        try:
            QMessageBox.warning(self, title, text)
        except Exception as e:
            self.write_log(f"def print_warning_message exception : {e}")

    # Date validator
    def is_valid_date(self, date):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # Showing the sum of prices
    def count_prices(self):
        sum: float = 0
        for i in range(0, self.expenses_table.rowCount()):
            cell = self.expenses_table.item(i, 3).text()
            sum += float(cell)
        self.sum_label.setText(f"Total : {sum}")