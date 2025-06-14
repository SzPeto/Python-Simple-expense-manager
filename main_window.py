
import datetime
import os.path
import sys
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QIntValidator, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidget, QWidget, QPushButton, QHBoxLayout, QLabel, \
    QLineEdit, QComboBox, QTableWidgetItem, QHeaderView, QFrame, QSizePolicy, QStackedLayout, QMessageBox, \
    QGraphicsDropShadowEffect, QMenuBar, QMenu, QAction

from main_database import *
from about_dialog import AboutDialog


class MainWindow(QMainWindow):

    def __init__(self, main_instance):
        super().__init__()
        from Main import Main

        # Master
        self.central_widget = QWidget()
        self.monitor = QGuiApplication.primaryScreen().geometry()
        self.main_instance: Main = main_instance
        self.today_date = datetime.date.today()
        self.is_first_filter = True
        get_main_instance(self)
        self.log_file = self.create_file_dir("Log\\log.txt")
        self.write_log_init()
        self.today = datetime.datetime.today()
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
        self.icon_size = 40
        self.about_dialog = AboutDialog()

        # Geometry
        self.window_width = int(self.monitor.width() * 0.5)
        self.window_height = int(self.monitor.height() * 0.88)

        # Layout
        self.v_box_main = QVBoxLayout() # The main layout, level 0
        self.h_box_upper = QHBoxLayout()
        self.v_box_upper_1 = QVBoxLayout()
        self.v_box_upper_2 = QVBoxLayout()
        self.v_box_upper_3 = QVBoxLayout()
        self.h_box_date = QHBoxLayout()
        self.h_box_price = QHBoxLayout()
        self.h_box_filter_main = QHBoxLayout()
        self.h_box_filter_2 = QHBoxLayout()
        self.stack_filter_changing = QStackedLayout()
        self.filter_page_month = QWidget()
        self.filter_page_id = QWidget()
        self.filter_page_category = QWidget()
        self.filter_page_price = QWidget()
        self.filter_page_date = QWidget()
        self.h_box_filter_changing_month = QHBoxLayout()
        self.h_box_filter_changing_id = QHBoxLayout()
        self.h_box_filter_changing_category = QHBoxLayout()
        self.h_box_filter_changing_price = QHBoxLayout()
        self.h_box_filter_changing_date = QHBoxLayout()
        self.separator_1 = QFrame()
        self.separator_2 = QFrame()
        self.separator_3 = QFrame()
        self.stack_filter_changing_qwidget = QWidget()
        self.h_box_buttons = QHBoxLayout()
        self.h_box_add_title = QHBoxLayout()
        self.h_box_filter_title = QHBoxLayout()
        self.h_box_table_buttons = QHBoxLayout()
        self.h_box_sum = QHBoxLayout()

        # Database
        self.db_connection = create_connection("Databases\\main.db")
        self.table_name = "expenses"
        self.cursor = self.db_connection.cursor()
        create_table(self.cursor, self.table_name)

        # Menu
        self.menu_bar = QMenuBar()
        self.file_menu = QMenu("File")
        self.about_menu = QMenu("About")
        self.exit_action = QAction("Exit")
        self.about_action = QAction("About")
        self.read_me_action = QAction("Read me")

        # Buttons
        self.add_button = QPushButton("Add")
        self.delete_selected_button = QPushButton("Delete selected")
        self.delete_all_button = QPushButton("Delete all")
        self.refresh_button = QPushButton("Refresh")
        self.filter_button = QPushButton("Filter results")
        self.clear_filters_button = QPushButton("Clear all filters")
        self.support_me_button = QPushButton("Support me")

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
        self.add_label = QLabel("Add entry into table")
        self.filter_label = QLabel("Filter by : ")
        self.add_icon_label = QLabel()
        self.filter_icon_label = QLabel()
        self.sum_icon_label = QLabel()

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
        self.filter_month_year_combo_box = QComboBox()
        self.filter_month_month_combo_box = QComboBox()

        # Other
        self.expenses_table = QTableWidget()
        self.main_icon = QIcon(self.resource_path("icon.png"))
        self.add_icon = QIcon(self.resource_path("add.png"))
        self.filter_icon = QIcon(self.resource_path("filter.png"))
        self.sum_icon = QIcon(self.resource_path("sum.png"))
        self.add_icon_pixmap = self.add_icon.pixmap(self.icon_size, self.icon_size)
        self.filter_icon_pixmap = self.filter_icon.pixmap(self.icon_size, self.icon_size)
        self.sum_icon_pixmap = self.sum_icon.pixmap(self.icon_size, self.icon_size)
        self.write_log(f"Resource path : {self.resource_path("icon.png")}")
        self.write_log(f"Resource path : {self.resource_path("add.png")}")
        self.write_log(f"Resource path : {self.resource_path("filter.png")}")
            # After updating an entry, call the function fill_table if 1, filter if 2
        self.previous_operation = 0
        self.shadow_sum_label = QGraphicsDropShadowEffect()

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
        self.separator_3.setFrameShape(QFrame.HLine)
        self.separator_3.setFrameShadow(QFrame.Sunken)
        self.separator_3.setLineWidth(2)
            # Level 4
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
        self.h_box_filter_changing_month.addWidget(self.filter_month_year_combo_box)
        self.h_box_filter_changing_month.addWidget(self.filter_month_month_combo_box)
        self.h_box_filter_changing_id.addWidget(self.filter_line_edit_id_from)
        self.h_box_filter_changing_id.addWidget(self.filter_line_edit_id_to)
        self.h_box_filter_changing_category.addWidget(self.filter_category_combo_box)
        self.h_box_filter_changing_price.addWidget(self.filter_price_from)
        self.h_box_filter_changing_price.addWidget(self.filter_dash_label)
        self.h_box_filter_changing_price.addWidget(self.filter_price_to)
        self.h_box_filter_changing_date.addWidget(self.date_from_label)
        self.h_box_filter_changing_date.addWidget(self.filter_date_year_from)
        self.h_box_filter_changing_date.addWidget(self.filter_date_month_from)
        self.h_box_filter_changing_date.addWidget(self.filter_date_day_from)
        self.h_box_filter_changing_date.addStretch()
        self.h_box_filter_changing_date.addWidget(self.date_to_label)
        self.h_box_filter_changing_date.addWidget(self.filter_date_year_to)
        self.h_box_filter_changing_date.addWidget(self.filter_date_month_to)
        self.h_box_filter_changing_date.addWidget(self.filter_date_day_to)
            # Level 3
        self.stack_filter_changing_qwidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.v_box_upper_1.addWidget(self.description_label)
        self.v_box_upper_1.addWidget(self.category_label)
        self.v_box_upper_1.addWidget(self.price_label)
        self.v_box_upper_1.addWidget(self.date_label)
        self.v_box_upper_2.addWidget(self.description_line_edit)
        self.v_box_upper_2.addWidget(self.category_combo_box, alignment = Qt.AlignLeft)
        self.v_box_upper_2.addLayout(self.h_box_price)
        self.v_box_upper_2.addLayout(self.h_box_date)
        self.v_box_upper_3.addWidget(self.add_button, alignment = Qt.AlignTop)
                    # Wrapping the changing filter layouts into QWidgets
        self.filter_page_month.setLayout(self.h_box_filter_changing_month)
        self.filter_page_id.setLayout(self.h_box_filter_changing_id)
        self.filter_page_category.setLayout(self.h_box_filter_changing_category)
        self.filter_page_price.setLayout(self.h_box_filter_changing_price)
        self.filter_page_date.setLayout(self.h_box_filter_changing_date)
                    # Adding into stack layout
        self.stack_filter_changing.addWidget(self.filter_page_month)
        self.stack_filter_changing.addWidget(self.filter_page_id)
        self.stack_filter_changing.addWidget(self.filter_page_category)
        self.stack_filter_changing.addWidget(self.filter_page_price)
        self.stack_filter_changing.addWidget(self.filter_page_date)
        self.stack_filter_changing.setCurrentIndex(0)
        self.stack_filter_changing_qwidget.setLayout(self.stack_filter_changing) # Wrapping the stack into QWidget
            # Level 2
        self.h_box_upper.addLayout(self.v_box_upper_1)
        self.h_box_upper.addLayout(self.v_box_upper_2)
        self.h_box_upper.addLayout(self.v_box_upper_3)
        self.h_box_filter_main.addWidget(self.filter_label)
        self.h_box_filter_main.addWidget(self.filter_by_combo_box)
        self.h_box_filter_main.addWidget(self.stack_filter_changing_qwidget)
        self.h_box_filter_main.addWidget(self.filter_button)
        self.h_box_filter_2.addWidget(self.clear_filters_button)
        self.h_box_add_title.addWidget(self.add_icon_label, alignment = Qt.AlignLeft)
        #self.h_box_add_title.addWidget(self.add_label, alignment = Qt.AlignLeft)
        self.h_box_filter_title.addWidget(self.filter_icon_label, alignment = Qt.AlignLeft)
        #self.h_box_filter_title.addWidget(self.filter_label, alignment = Qt.AlignLeft)
        self.h_box_table_buttons.addWidget(self.delete_all_button)
        self.h_box_table_buttons.addWidget(self.delete_selected_button)
        self.h_box_table_buttons.addWidget(self.refresh_button)
        self.h_box_sum.addWidget(self.sum_icon_label, alignment = Qt.AlignLeft)
        self.h_box_sum.addWidget(self.support_me_button)
        self.h_box_sum.addWidget(self.sum_label, alignment = Qt.AlignRight)
            # Level 1
        self.v_box_main.addLayout(self.h_box_add_title)
        self.v_box_main.addLayout(self.h_box_upper)
        self.v_box_main.addWidget(self.separator_1)
        self.v_box_main.addLayout(self.h_box_filter_title)
        self.v_box_main.addLayout(self.h_box_filter_main)
        self.v_box_main.addLayout(self.h_box_filter_2)
        self.v_box_main.addWidget(self.separator_2)
        self.v_box_main.addWidget(self.expenses_table)
        self.v_box_main.addLayout(self.h_box_table_buttons)
        self.v_box_main.addWidget(self.separator_3)
        self.v_box_main.addLayout(self.h_box_sum)
        self.central_widget.setLayout(self.v_box_main)

        # Menu
        self.file_menu.addAction(self.exit_action)
        self.about_menu.addActions([self.about_action])
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.about_menu)
        self.setMenuBar(self.menu_bar)


        # Event handling
        self.add_button.clicked.connect(self.add_entry)
        self.delete_selected_button.clicked.connect(self.delete_selected)
        self.delete_all_button.clicked.connect(self.delete_all)
        self.refresh_button.clicked.connect(self.refresh)
        self.filter_by_combo_box.currentIndexChanged.connect(self.change_filter)
        self.filter_button.clicked.connect(self.filter_selected)
        self.filter_month_month_combo_box.currentIndexChanged.connect(self.filter_selected)
        self.clear_filters_button.clicked.connect(self.refresh)
        self.expenses_table.itemChanged.connect(self.update_selected)
        #self.expenses_table.horizontalHeader().sectionClicked.connect(self.order_table)
        self.support_me_button.clicked.connect(self.support_me)
        self.exit_action.triggered.connect(self.exit)
        self.about_action.triggered.connect(self.show_about)

        # Buttons, labels and other
        self.add_button.setMinimumWidth(240)
        self.add_icon_label.setMaximumWidth(50)
        self.filter_icon_label.setMaximumWidth(50)
        self.sum_icon_label.setMaximumWidth(50)
        self.support_me_button.setMaximumWidth(120)
        self.setWindowIcon(self.main_icon)
        self.filter_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setWindowTitle("Simple expense manager by Peter Szepesi")
        self.year_line_edit.setText(str(self.today_date.year))
        self.month_line_edit.setText(str(f"{self.today_date.month:02}"))
        self.day_line_edit.setText(str(f"{self.today_date.day:02}"))
        self.price_decimal_line_edit.setPlaceholderText("00")
        self.filter_price_from.setPlaceholderText("Price FROM")
        self.filter_price_to.setPlaceholderText("Price TO")
        self.filter_date_day_from.setText("01")
        self.add_icon_label.setPixmap(self.add_icon_pixmap)
        self.filter_icon_label.setPixmap(self.filter_icon_pixmap)
        self.sum_icon_label.setPixmap(self.sum_icon_pixmap)
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
        self.expenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.filter_by_combo_box.addItems(["Month", "ID", "Category", "Price", "Date"])
        self.filter_line_edit_id_from.setPlaceholderText("Id FROM")
        self.filter_line_edit_id_to.setPlaceholderText("Id TO")
        self.filter_month_year_combo_box.addItems(self.get_years())
        self.filter_month_year_combo_box.setCurrentIndex(len(self.filter_month_year_combo_box) - 1)
        self.filter_month_year_combo_box.setMaximumWidth(80)
        self.filter_month_month_combo_box.addItems([
            "All", "January", "February", "March", "April", "May", "June", "July", "August", "September",
            "October", "November", "December"
        ])
        self.filter_month_month_combo_box.setCurrentIndex(int(self.today.month) - 1)
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
        self.add_button.setObjectName("addButton")
        self.price_decimal_label.setObjectName("priceDecimalLabel")
        self.filter_month_month_combo_box.setObjectName("filterMonthMonthComboBox")
        self.v_box_upper_2.setObjectName("vBoxUpper2")

        # Styling
        self.shadow_sum_label.setBlurRadius(15)
        self.shadow_sum_label.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black
        self.shadow_sum_label.setOffset(3, 3)
        self.sum_label.setGraphicsEffect(self.shadow_sum_label)
        self.price_line_edit.setMaximumWidth(80)
        self.price_decimal_line_edit.setMaximumWidth(40)
        self.year_line_edit.setMaximumWidth(60)
        self.month_line_edit.setMaximumWidth(40)
        self.day_line_edit.setMaximumWidth(40)
            # Setting the stylesheet
        self.setStyleSheet("""
            
            MainWindow{
                background-color: rgb(235, 235, 255);
            }
            
            QLabel{
                font-family: Segoe UI;
                font-size: 16px;
            }
            
            QLabel#priceDecimalLabel{
                font-size: 20px;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(255, 255, 255),  /* Top of gradient */
                    stop:1 rgb(235, 235, 235)   /* Bottom of gradient */
                );
                color: rgb(51, 51, 51);
                border: 1px solid rgb(204, 204, 204);
                border-radius: 8px;
                padding: 6px 12px;
                font-family: Segoe UI;
                font-size: 16px;
            }
            
            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(245, 245, 245),  /* Top of gradient */
                    stop:1 rgb(225, 225, 225)   /* Bottom of gradient */
                );
            }
            
            QPushButton:pressed {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(230, 230, 230),  /* Top of gradient */
                    stop:1 rgb(210, 210, 210)   /* Bottom of gradient */
                );
                border: 1px inset rgb(144, 144, 144);
            }
            
            QPushButton#addButton{
                font-size: 25px;
                font-weight: bold;
                color: rgb(111, 111, 111);
            }
            
            QLineEdit {
                background-color: rgb(255, 255, 255);
                color: rgb(33, 33, 33);
                border: 1px solid rgb(204, 204, 204);
                border-radius: 6px;
                padding: 4px 8px;
                font-family: Segoe UI;
                font-size: 16px;
            }
            
            QLineEdit:focus {
                border: 1px solid rgb(100, 149, 237);
                background-color: rgb(250, 250, 250);
            }
            
            QComboBox {
                background-color: rgb(250, 250, 250);
                color: rgb(33, 33, 33);
                border: 1px solid rgb(204, 204, 204);
                border-radius: 6px;
                padding: 4px 8px;
                font-family: Segoe UI;
                font-size: 16px;
            }
            
            QComboBox:hover {
                border: 1px solid rgb(180, 180, 180);
            }
            
            QComboBox:focus {
                border: 1px solid rgb(100, 149, 237); /* Cornflower Blue */
                background-color: rgb(250, 250, 250);
            }
            
            QComboBox QAbstractItemView {
                background-color: rgb(255, 255, 255);
                border: 1px solid rgb(204, 204, 204);
                selection-background-color: rgb(230, 230, 230);
                selection-color: rgb(33, 33, 33);
            }
            
            QComboBox#filterMonthMonthComboBox{
                font-size: 23px;
                border: 2px solid rgb(204, 204, 204);
                background-color: rgb(240, 248, 255);
                
            }
            
            QLabel#sumLabel{
                font-size: 30px;
                font-family: Segoe UI;
                background-color: white;
                padding: 10px;
                border-radius: 4px;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(255, 255, 255),  /* Top of gradient */
                    stop:1 rgb(235, 235, 235)   /* Bottom of gradient */
                );
                border: 1px solid rgb(214, 214, 214);
                font-weight: bold;
                color: rgb(111, 111, 111);
            }
            
            QTableWidget {
                background-color: rgb(255, 255, 255);
                alternate-background-color: rgb(248, 248, 248);
                color: rgb(33, 33, 33);
                gridline-color: rgb(220, 220, 220);
                font-family: Segoe UI;
                font-size: 16px;
                border: 1px solid rgb(204, 204, 204);
                border-radius: 6px;
            }
        
            QHeaderView::section {
                background-color: rgb(245, 245, 245);
                color: rgb(80, 80, 80);
                padding: 6px;
                border: 1px solid rgb(204, 204, 204);
                font-weight: bold;
            }
        
            QTableWidget::item {
                padding: 6px;
                border: none;
            }
        
            QTableWidget::item:selected {
                background-color: rgb(220, 235, 252);
                color: rgb(0, 0, 0);
            }
        
        """)

        # Filling the table with all results
        self.fill_table()
        self.filter_month_month_combo_box.setCurrentIndex(0)

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
            self.description_line_edit.setText("")
            self.price_line_edit.setText("")
            self.price_decimal_line_edit.setText("")
            self.price_decimal_line_edit.setPlaceholderText("00")
        except Exception as e:
            self.write_log(f"Something went wrong during adding entry : {e}")

    def change_filter(self):
        filter_text = self.filter_by_combo_box.currentText().lower()
        if filter_text == "month":
            self.stack_filter_changing.setCurrentIndex(0)
        elif filter_text == "id":
            self.stack_filter_changing.setCurrentIndex(1)
        elif filter_text == "category":
            self.stack_filter_changing.setCurrentIndex(2)
        elif filter_text == "price":
            self.stack_filter_changing.setCurrentIndex(3)
        elif filter_text == "date":
            self.stack_filter_changing.setCurrentIndex(4)

    def filter_selected(self):
        index = self.stack_filter_changing.currentIndex()
        if index == 0:
            try:
                year = self.filter_month_year_combo_box.currentText()
                month = f"{int(self.filter_month_month_combo_box.currentIndex()):02}"
                if month == "00":
                    self.fill_table()
                else:
                    rows = search_based_on_condition(
                        self.cursor, self.table_name,
                        f"date >= '{year}-{month}-01' AND date <= '{year}-{month}-31'"
                    )
                    self.fill_table_selected(rows)
            except Exception as e:
                self.write_log(f"def filter_selected : {e}")
                self.print_warning_message("Empty", "No results to show, please enter a valid input!")
        elif index == 1:
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

        elif index == 2:
            try:
                category = self.filter_category_combo_box.currentText()
                rows = search_based_on_condition(
                    self.cursor, self.table_name, f"category = '{category}'"
                )
                self.fill_table_selected(rows)
            except Exception as e:
                self.write_log(f"def filter_selected : {e}")
                self.print_warning_message("Invalid input", f"Something went wrong, (error : {e})")
        elif index == 3:
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
        elif index == 4:
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
        self.previous_operation = 2

    def support_me(self):
        webbrowser.open("https://www.paypal.me/szpeto")

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
        reply = QMessageBox.question(
            self,
            "Are you sure?",
            "Are you sure you want to delete the selected entries?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
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
                    self.write_log("def delete_selected : There is nothing selected")
            except Exception as e:
                self.write_log(f"def delete_selected : something went wrong deleting selected items : {e}")

            try:
                self.db_connection.commit()
                self.fill_table()
            except Exception as e:
                self.write_log(f"def delete_selected : something went wrong during filling the table : {e}")

    def delete_all(self):
        reply = QMessageBox.question(
            self,
            "Are you sure?",
            "Are you sure you want to delete ALL entries?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                delete_table(self.cursor, self.table_name)
                self.db_connection.commit()
                self.fill_table()
            except Exception as e:
                self.write_log(f"Something went wrong deleting table : {e}")

    def refresh(self):
        self.fill_table()

    def update_selected(self):
        clicked_cell = self.expenses_table.selectedItems()[0]
        row = clicked_cell.row()
        column = clicked_cell.column()
        column_search = "id"
        keyword_search = self.expenses_table.item(row, 0).text()
        column_update = self.expenses_table.horizontalHeaderItem(column).text().lower()
        keyword_update = self.expenses_table.item(row, column).text()
        update_entry(self.cursor, self.table_name, column_search, keyword_search, column_update, keyword_update)
        print(column_search, keyword_search, column_update, keyword_update)
        self.db_connection.commit()
        if self.previous_operation == 1:
            self.fill_table()
        elif self.previous_operation == 2:
            self.filter_selected()

    def exit(self):
        sys.exit(0)

    def show_about(self):
        self.about_dialog.exec_()

    # Logging and printing warning messages ****************************************************************
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

    def print_warning_message(self, title, text):
        try:
            QMessageBox.warning(self, title, text)
        except Exception as e:
            self.write_log(f"def print_warning_message exception : {e}")

    # Filling the table ************************************************************************************
    def fill_table(self):
        self.expenses_table.blockSignals(True)
        try:
            create_table(self.cursor, self.table_name)
            rows = show_all(self.cursor, self.table_name)
            if rows:
                self.expenses_table.setRowCount(len(rows))
                for row_index in range(0, len(rows)):
                    row = rows[row_index]
                    for column_index in range(0, len(row)):
                        column = row[column_index]

                        # Column index 0 and 3 should be int and float for sorting purposes
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
            self.previous_operation = 1
        except Exception as e:
            self.write_log(f"def fill_table : something went wrong during filling the table : {e}")

        self.count_prices()
        self.expenses_table.blockSignals(False)

    def fill_table_selected(self, rows):
        self.expenses_table.blockSignals(True)
        try:
            if rows:
                self.expenses_table.setRowCount(len(rows))
                for row_index in range(0, len(rows)):
                    row = rows[row_index]
                    for column_index in range(0, len(row)):
                        column = row[column_index]

                        # Column index 0 and 3 should be int and float for sorting purposes
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
                if not self.is_first_filter:
                    self.print_warning_message("Empty", "No results to show!")
                if self.is_first_filter:
                    self.is_first_filter = False
        except Exception as e:
            self.write_log(f"def fill_table_selected : something went wrong during filling the table : {e}")

        self.count_prices()
        self.expenses_table.blockSignals(False)

    # Files and directories ********************************************************************************
    def create_file_dir(self, file_path):
        try:
            dir_name = os.path.dirname(file_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
        except Exception as e:
            print(f"Error during creating directory : {e}")

        return file_path

    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path) # In case of exe return the absolute path
        else:
            return os.path.join(os.path.abspath("."), relative_path) # In case of IDE return the relative path

    # Replacing widgets and layouts during runtime *********************************************************
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

    # Validators
    def is_valid_date(self, date):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # Other helper functions ******************************************************************************
    def get_years(self):
        years = []
        current_year = self.today.year
        length = int(current_year - 1990 + 1)
        for i in range(0, length):
            years.append(str(1990 + i))

        return years

    def count_prices(self):
        sum: float = 0
        for i in range(0, self.expenses_table.rowCount()):
            cell = self.expenses_table.item(i, 3).text()
            sum += float(cell)
        self.sum_label.setText(f"Total : {sum:.2f}")