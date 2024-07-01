import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QFrame, QScrollArea, QGridLayout, QHeaderView,
                             QFileDialog, QDialog, QComboBox, QTableView, QSizePolicy, QAbstractItemView,
                             QLayout, QListWidget, QDesktopWidget)

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class AuthorizationWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.main_color = '#FADFAD'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Авторизация')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(f'background-color: {self.main_color};')
        self.center_window()

        layout = QVBoxLayout()

        login_layout = QHBoxLayout()
        login_label = QLabel('Логин:')
        login_label.setStyleSheet('font-size: 20px; background-color: white;')
        login_layout.addWidget(login_label)

        self.login_entry = QLineEdit()
        self.login_entry.setStyleSheet(
            'font-size: 20px; background-color: white;')
        login_layout.addWidget(self.login_entry)

        layout.addLayout(login_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel('Пароль:')
        password_label.setStyleSheet(
            'font-size: 20px; background-color: white;')
        password_layout.addWidget(password_label)

        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet(
            'font-size: 20px; background-color: white;')
        password_layout.addWidget(self.password_entry)

        layout.addLayout(password_layout)

        self.login_button = QPushButton('Войти')
        self.login_button.setStyleSheet(
            'font-size: 20px; background-color: white;')
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        login = self.login_entry.text()
        password = self.password_entry.text()

        user, role = self.db.verification_of_authorization(login, password)
        if user is not None:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet('background-color: white; color: black;')
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Успех')
            msg_box.setText('Успешный вход')
            msg_box.exec_()

            if role == 0:
                self.main_admin_window = MainAdmin(self.db, self.main_color)
                self.main_admin_window.show()
                self.close()
            elif role in [1, 2, 3]:
                self.close()
        else:
            msg_box = QMessageBox(self)
            msg_box.setStyleSheet('background-color: white; color: black;')
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle('Ошибка')
            msg_box.setText('Неверный логин или пароль')
            msg_box.exec_()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)


class MainAdmin(QMainWindow):
    def __init__(self, db, color):
        super().__init__()
        self.db = db
        self.main_color = color
        self.init_ui()
        self.showMaximized()

    def message_errore(self, error):
        message = QMessageBox()
        # Установка белого фона
        message.setStyleSheet("background-color: white;")
        message.setText(error)

        # Центрирование окна сообщения
        qr = message.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        message.move(qr.topLeft())

        message.exec_()

    def init_ui(self):
        self.setWindowTitle('Администратор')
        self.setStyleSheet(f'background-color: {self.main_color};')
        self.setGeometry(100, 100, 1200, 800)

        menu_layout = QVBoxLayout()

        main_frame = QFrame(self)
        main_frame.setStyleSheet('background-color: Orange;')
        main_frame.setFixedHeight(70)

        button_layout = QHBoxLayout()

        self.button_users = QPushButton('Пользователи')
        self.button_users.setStyleSheet(
            'font-size: 24px; background-color: Purple;')
        self.button_users.setFixedHeight(50)
        self.button_users.clicked.connect(self.click_button_user)
        button_layout.addWidget(self.button_users)

        self.button_group = QPushButton('Группы')
        self.button_group.setStyleSheet(
            'font-size: 24px; background-color: Purple;')
        self.button_group.setFixedHeight(50)
        self.button_group.clicked.connect(self.click_button_group)
        button_layout.addWidget(self.button_group)

        self.button_test = QPushButton('Тесты')
        self.button_test.setStyleSheet(
            'font-size: 24px; background-color: Purple;')
        self.button_test.setFixedHeight(50)
        button_layout.addWidget(self.button_test)

        main_frame.setLayout(button_layout)
        menu_layout.addWidget(main_frame)

        self.work_area_layout = QVBoxLayout()

        self.frame_table = QFrame(self)
        self.frame_table.setStyleSheet('background-color: Black;')

        self.table_layout = QVBoxLayout(self.frame_table)
        self.table_layout.setAlignment(Qt.AlignTop)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.frame_table)
        self.work_area_layout.addWidget(scroll_area)

        main_layout = QVBoxLayout()
        main_layout.addLayout(menu_layout)
        main_layout.addLayout(self.work_area_layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def click_button_user(self):
        try:
            if hasattr(self, 'dop_frame') and self.dop_frame is not None:
                self.dop_frame.deleteLater()
                self.dop_frame = None

            self.clear_table_layout()

            self.dop_frame = QFrame(self)
            self.dop_frame.setStyleSheet('background-color: Green;')
            self.dop_frame.setFixedHeight(60)
            self.work_area_layout.insertWidget(0, self.dop_frame)

            button_layout = QHBoxLayout(self.dop_frame)

            button_executives = QPushButton('Администраторы')
            button_executives.setStyleSheet(
                'font-size: 24px; color: yellow; background-color: lime;')
            button_executives.clicked.connect(self.create_table_admin)
            button_layout.addWidget(button_executives)

            button_curators = QPushButton('Кураторы')
            button_curators.setStyleSheet(
                'font-size: 24px; color: yellow; background-color: lime;')
            button_curators.clicked.connect(self.create_table_curator)
            button_layout.addWidget(button_curators)

            button_teachers = QPushButton('Преподаватели')
            button_teachers.setStyleSheet(
                'font-size: 24px; color: yellow; background-color: lime;')
            button_teachers.clicked.connect(self.create_table_teacher)
            button_layout.addWidget(button_teachers)

            button_students = QPushButton('Ученики')
            button_students.setStyleSheet(
                'font-size: 24px; color: yellow; background-color: lime;')
            button_students.clicked.connect(self.create_table_student)
            button_layout.addWidget(button_students)

            self.dop_frame.setLayout(button_layout)
        except Exception as error:
            self.message_errore(error)

    def setup_table_filter(self, table):

        class CustomFilterProxyModel(QSortFilterProxyModel):
            def filterAcceptsRow(self, source_row, source_parent):
                model = self.sourceModel()
                for column in [1, 2, 4]:
                    index = model.index(source_row, column, source_parent)
                    if self.filterRegExp().indexIn(str(model.data(index))) >= 0:
                        return True
                return False

        proxy_model = CustomFilterProxyModel()
        proxy_model.setSourceModel(table.model())
        proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        table.setModel(proxy_model)
        table.setSortingEnabled(True)   # Включить сортировку

        s_layout = QHBoxLayout()

        search_label = QLabel("Поиск: ")
        search_label.setStyleSheet('background-color: White; font-size: 18px;')
        s_layout.addWidget(search_label)

        filter_line_edit = QLineEdit()
        filter_line_edit.setStyleSheet(
            'background-color: White; font-size: 18px;')
        filter_line_edit.textChanged.connect(
            lambda text: proxy_model.setFilterFixedString(text))
        s_layout.addWidget(filter_line_edit)

        self.table_layout.addLayout(s_layout)

    def create_table_admin(self):
        self.clear_table_layout()

        label = QLabel("Таблица администраторов")
        label.setStyleSheet(
            'background-color: White; color: Purple; font-size: 24px;')
        label.setAlignment(Qt.AlignCenter)
        self.table_layout.addWidget(label)

        self.model_admin = QStandardItemModel(self.frame_table)
        self.model_admin.setColumnCount(4)
        self.table_admin = QTableView(self.frame_table)
        self.table_admin.setModel(self.model_admin)
        self.table_admin.setStyleSheet(
            'background-color: White; font-size: 15px;')
        self.model_admin.setHorizontalHeaderLabels(
            ["ID", "Имя", "Логин", "Пароль"])

        self.setup_table_filter(self.table_admin)

        header = self.table_admin.horizontalHeader()
        header.setStyleSheet('font-size: 18px;')
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.db.populate_treeview(self.model_admin, 0)
        self.table_admin.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_layout.addWidget(self.table_admin)

        self.table_admin.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_admin.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.add_table_buttons(0, self.table_admin)

    def create_table_curator(self):
        self.clear_table_layout()

        label = QLabel("Таблица кураторов")
        label.setStyleSheet(
            'background-color: White; color: Purple; font-size: 24px;')
        label.setAlignment(Qt.AlignCenter)
        self.table_layout.addWidget(label)

        self.model_curator = QStandardItemModel(self.frame_table)
        self.model_curator.setColumnCount(3)
        self.table_curator = QTableView(self.frame_table)
        self.table_curator.setModel(self.model_curator)
        self.table_curator.setStyleSheet(
            'background-color: White; font-size: 15px;')
        self.model_curator.setHorizontalHeaderLabels(["ID", "Имя", "Логин"])

        self.setup_table_filter(self.table_curator)

        header = self.table_curator.horizontalHeader()
        header.setStyleSheet('font-size: 18px;')
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.db.populate_treeview(self.model_curator, 1)
        self.table_curator.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_layout.addWidget(self.table_curator)

        self.table_curator.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_curator.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.add_table_buttons(1, self.table_curator)

    def create_table_teacher(self):
        self.clear_table_layout()

        label = QLabel("Таблица преподавателей")
        label.setStyleSheet(
            'background-color: White; color: Purple; font-size: 24px;')
        label.setAlignment(Qt.AlignCenter)
        self.table_layout.addWidget(label)

        self.model_teacher = QStandardItemModel(self.frame_table)
        self.model_teacher.setColumnCount(3)
        self.table_teacher = QTableView(self.frame_table)
        self.table_teacher.setModel(self.model_teacher)
        self.table_teacher.setStyleSheet(
            'background-color: White; font-size: 15px;')
        self.model_teacher.setHorizontalHeaderLabels(["ID", "Имя", "Логин"])

        self.setup_table_filter(self.table_teacher)

        header = self.table_teacher.horizontalHeader()
        header.setStyleSheet('font-size: 18px;')
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.db.populate_treeview(self.model_teacher, 2)
        self.table_teacher.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_layout.addWidget(self.table_teacher)

        self.table_teacher.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_teacher.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.add_table_buttons(2, self.table_teacher)

    def create_table_student(self):
        self.clear_table_layout()

        label = QLabel("Таблица учащихся")
        label.setStyleSheet(
            'background-color: White; color: Purple; font-size: 24px;')
        label.setAlignment(Qt.AlignCenter)
        self.table_layout.addWidget(label)

        self.model_student = QStandardItemModel(self.frame_table)
        self.model_student.setColumnCount(4)
        self.table_student = QTableView(self.frame_table)
        self.table_student.setModel(self.model_student)
        self.table_student.setStyleSheet(
            'background-color: White; font-size: 15px;')
        self.model_student.setHorizontalHeaderLabels(
            ["ID", "Имя", "Логин", "Филиал"])

        self.setup_table_filter(self.table_student)

        header = self.table_student.horizontalHeader()
        header.setStyleSheet('font-size: 18px;')
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.db.populate_treeview(self.model_student, 3)
        self.table_student.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_layout.addWidget(self.table_student)

        self.table_student.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_student.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.add_table_buttons(3, self.table_student)

    def add_table_buttons(self, role, table):
        button_layout = QHBoxLayout()

        button_add = QPushButton('Добавить пользователя')
        button_add.setStyleSheet('color: black; background-color: white;')

        if role != 3:
            button_add.clicked.connect(lambda: self.add_user(role, table))
        else:
            button_add.clicked.connect(lambda: self.add_student(table))

        button_layout.addWidget(button_add)

        button_edit = QPushButton('Редактировать пользователя')
        button_edit.setStyleSheet('color: black; background-color: white;')
        if role != 3:
            button_edit.clicked.connect(lambda: self.edit_user(role, table))
        else:
            button_edit.clicked.connect(lambda: self.edit_student(table))

        button_layout.addWidget(button_edit)

        button_delete = QPushButton('Удалить выбранного пользователя')
        button_delete.setStyleSheet('color: black; background-color: white;')
        button_delete.clicked.connect(lambda: self.delete_user(role, table))
        button_layout.addWidget(button_delete)

        button_export = QPushButton('Импортировать пользователей')
        button_export.setStyleSheet('color: black; background-color: white;')
        button_export.clicked.connect(lambda: self.export_user(role, table))
        button_layout.addWidget(button_export)

        self.table_layout.addLayout(button_layout)

    def add_user(self, role, table):
        try:
            self.user_dialog = UserDialog(self, role, table, self.db)
            self.user_dialog.show()
        except Exception as error:
            self.message_errore(str(error))

    def delete_user(self, role, table):
        try:
            user_id, login = self.get_selected_user(table)
            self.db.delete_user(user_id, role, table)
        except Exception as error:
            self.message_errore(str(error))

    def edit_user(self, role, table):
        try:
            user_id, login = self.get_selected_user(table)
            self.user_dialog = EditUserDialog(
                self, role, table, self.db, user_id, login)
            self.user_dialog.show()
        except Exception as error:
            self.message_errore(str(error))

    def export_user(self, role, table):
        try:
            file_dialog = QFileDialog()
            file_dialog.setNameFilters(
                ["CSV files (*.csv)", "All files (*.*)"])
            file_dialog.selectNameFilter("CSV files (*.csv)")

            if file_dialog.exec_():
                file_path = file_dialog.selectedFiles()[0]
                if file_path:
                    self.db.import_users(file_path, role, table)
        except Exception as error:
            self.message_errore(str(error))

    def add_student(self, table):
        try:
            self.student_dialog = StudentDialog(self, table, self.db)
            self.student_dialog.show()
        except Exception as error:
            self.message_errore(str(error))

    def edit_student(self, table):
        try:
            user_id, login = self.get_selected_user(table)
            self.user_dialog_student = EditStudentDialog(
                self, table, self.db, user_id, login)
            self.user_dialog_student.show()
        except Exception as error:
            self.message_errore(str(error))

    def edit_student(self, table):
        user_id, login = self.get_selected_user(table)
        self.user_dialog_student = EditStudentDialog(
            self, table, self.db, user_id, login)
        self.user_dialog_student.show()

    def get_selected_user(self, table):
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        selected_rows = table.selectionModel().selectedIndexes()
        if selected_rows:
            row = selected_rows[0].row()
            model = table.model()
            user_id = model.data(model.index(row, 0))
            login = model.data(model.index(row, 2))
            return user_id, login

    def clear_table_layout(self):
        for i in reversed(range(self.table_layout.count())):
            item = self.table_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    layout_item = self.table_layout.takeAt(i)
                    if layout_item:
                        if isinstance(layout_item, QLayout):
                            if layout_item is not None:
                                while layout_item.count():
                                    item = layout_item.takeAt(0)
                                    if item.widget():
                                        item.widget().deleteLater()
                                    elif item.layout():
                                        self.clear_table_layout(item.layout())

    def add_group(self):
        self.group_dialog = GroupAddDialog(self.db, self.model_group)
        self.group_dialog.show()

    def edit_group(self):
        selected_group = self.get_selected_group()
        if selected_group:
            group_id, groupname, curator_id = selected_group
            if group_id != 0:
                self.group_edit_dialog = GroupEditDialog(
                    group_id, groupname, curator_id, self.db, self.model_group)
                self.group_edit_dialog.show()

    def get_selected_group(self):
        selected_indexes = self.table_group.selectionModel().selectedIndexes()

        if selected_indexes:
            row = selected_indexes[0].row()
            model = self.table_group.model()

            group_id = model.data(model.index(row, 0))
            groupname = model.data(model.index(row, 1))

            curator_id = self.db.get_curator_id_for_group(group_id)

            if curator_id is None:
                QMessageBox.warning(
                    self, 'Предупреждение', 'Не удалось получить ID куратора для выбранной группы.')

                return 0, 0, 0

            return group_id, groupname, curator_id
        else:
            QMessageBox.warning(
                self, 'Предупреждение', 'Пожалуйста, выберите группу.')
            return 0, 0, 0

    def delete_group(self):
        group_id, _, _ = self.get_selected_group()

        if group_id != 0:
            self.db.delete_group(group_id, self.model_group)

    def click_button_group(self):
        if hasattr(self, 'dop_frame') and self.dop_frame is not None:
            self.dop_frame.deleteLater()
            self.dop_frame = None

        self.clear_table_layout()

        # Группы

        label_group = QLabel("Таблица группы")
        label_group.setStyleSheet(
            'background-color: White; color: Purple; font-size: 24px;')
        label_group.setAlignment(Qt.AlignCenter)

        self.model_group = QStandardItemModel(self.frame_table)
        self.model_group.setColumnCount(3)
        self.table_group = QTableView(self.frame_table)
        self.table_group.setModel(self.model_group)
        self.table_group.setStyleSheet(
            'background-color: White; font-size: 15px;')

        # int(self.frame_table.height() - label_group.height()/2 - margins.bottom() - margins.top())
        height = 450

        self.table_group.setFixedHeight(height)

        self.model_group.setHorizontalHeaderLabels(
            ["ID", "Название", "Описание"])

        header_group = self.table_group.horizontalHeader()
        header_group.setStyleSheet('font-size: 18px;')
        header_group.setSectionResizeMode(QHeaderView.Stretch)

        self.db.populate_treeview_group(self.model_group)

        self.table_group.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_group.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table_group.selectionModel().selectionChanged.connect(
            self.populate_teachers_students_teste)

        self.table_layout.addWidget(label_group)
        self.table_layout.addWidget(self.table_group)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        self.add_group_table_buttons()
        button_layout.addStretch()
        button_layout.setAlignment(Qt.AlignRight)

        self.table_layout.addWidget(button_container)

        # Преподаватель

        teacher_container = QWidget()
        teacher_layout = QVBoxLayout(teacher_container)
        teacher_layout.setContentsMargins(0, 0, 0, 0)

        label_teacher = QLabel("Таблица преподавателей")
        label_teacher.setStyleSheet(
            'background-color: White; color: Yellow; font-size: 24px;')
        label_teacher.setAlignment(Qt.AlignCenter)
        teacher_layout.addWidget(label_teacher)

        self.model_teacher = QStandardItemModel(self.frame_table)
        self.model_teacher.setColumnCount(3)
        self.table_teacher = QTableView(self.frame_table)
        self.table_teacher.setModel(self.model_teacher)
        self.table_teacher.setStyleSheet(
            'background-color: White; font-size: 15px;')
        self.model_teacher.setHorizontalHeaderLabels(["ID", "Имя", "Логин"])

        self.table_teacher.setFixedHeight(height)

        header_teacher = self.table_teacher.horizontalHeader()
        header_teacher.setStyleSheet('font-size: 18px;')
        header_teacher.setSectionResizeMode(QHeaderView.Stretch)

        self.table_teacher.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.table_teacher.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_teacher.setSelectionBehavior(QAbstractItemView.SelectRows)

        teacher_button_container = QWidget()
        teacher_button_layout = QHBoxLayout(teacher_button_container)

        add_teacher_button = QPushButton("Добавить")
        add_teacher_button.setStyleSheet('background-color: White;')
        add_teacher_button.clicked.connect(self.add_teacher_in_group)

        delete_teacher_button = QPushButton("Удалить")
        delete_teacher_button.setStyleSheet('background-color: White;')
        delete_teacher_button.clicked.connect(self.delete_teacher_in_group)

        teacher_button_layout.addWidget(add_teacher_button)
        teacher_button_layout.addWidget(delete_teacher_button)

        teacher_layout.addWidget(self.table_teacher)
        teacher_layout.addWidget(teacher_button_container)

        # Учащиеся

        student_container = QWidget()
        student_layout = QVBoxLayout(student_container)
        student_layout.setContentsMargins(0, 0, 0, 0)

        label_student = QLabel("Таблица учащихся")
        label_student.setStyleSheet(
            'background-color: White; color: #A5260A; font-size: 24px;')
        label_student.setAlignment(Qt.AlignCenter)
        student_layout.addWidget(label_student)

        self.model_student = QStandardItemModel(self.frame_table)
        self.model_student.setColumnCount(4)
        self.table_student = QTableView(self.frame_table)
        self.table_student.setModel(self.model_student)
        self.table_student.setStyleSheet(
            'background-color: White; font-size: 15px;')
        self.model_student.setHorizontalHeaderLabels(
            ["ID", "Имя", "Логин", "Пароль", "Филиал"])

        self.table_student.setFixedHeight(height)

        header_student = self.table_student.horizontalHeader()
        header_student.setStyleSheet('font-size: 18px;')
        header_student.setSectionResizeMode(QHeaderView.Stretch)

        self.table_student.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.table_student.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_student.setSelectionBehavior(QAbstractItemView.SelectRows)

        student_button_container = QWidget()
        student_button_layout = QHBoxLayout(student_button_container)

        add_student_button = QPushButton("Добавить")
        add_student_button.setStyleSheet('background-color: White;')
        add_student_button.clicked.connect(self.add_student_in_group)

        delete_student_button = QPushButton("Удалить")
        delete_student_button.setStyleSheet('background-color: White;')
        delete_student_button.clicked.connect(self.delete_student_in_group)

        student_button_layout.addWidget(add_student_button)
        student_button_layout.addWidget(delete_student_button)

        student_layout.addWidget(self.table_student)
        student_layout.addWidget(student_button_container)

        # Тесты

        test_container = QWidget()
        test_layout = QVBoxLayout(test_container)
        test_layout.setContentsMargins(0, 0, 0, 0)

        label_test = QLabel("Таблица тестов")
        label_test.setStyleSheet(
            'background-color: White; color: #A5260A; font-size: 24px;')
        label_test.setAlignment(Qt.AlignCenter)
        test_layout.addWidget(label_test)

        self.model_test = QStandardItemModel(self.frame_table)
        self.model_test.setColumnCount(4)
        self.table_test = QTableView(self.frame_table)
        self.table_test.setModel(self.model_test)
        self.table_test.setStyleSheet(
            'background-color: White; font-size: 15px;')
        self.model_test.setHorizontalHeaderLabels(
            ["ID", "Преподаватель", "Группа", "Название", "Попытки", "Общее время прохождения теста", "Дата добавления"])

        self.table_test.setFixedHeight(height)

        header_test = self.table_test.horizontalHeader()
        header_test.setStyleSheet('font-size: 18px;')
        header_test.setSectionResizeMode(QHeaderView.Stretch)

        self.table_test.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.table_test.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_test.setSelectionBehavior(QAbstractItemView.SelectRows)

        test_button_container = QWidget()
        test_button_layout = QHBoxLayout(test_button_container)

        add_test_button = QPushButton("Добавить")
        add_test_button.setStyleSheet('background-color: White;')
        add_test_button.clicked.connect(self.add_test_in_group)

        delete_test_button = QPushButton("Удалить")
        delete_test_button.setStyleSheet('background-color: White;')
        delete_test_button.clicked.connect(self.delete_test_in_group)

        test_button_layout.addWidget(add_test_button)
        test_button_layout.addWidget(delete_test_button)

        test_layout.addWidget(self.table_test)
        test_layout.addWidget(test_button_container)

        self.table_layout.addWidget(test_container)
        self.table_layout.addWidget(teacher_container)
        self.table_layout.addWidget(student_container)

        self.frame_table.setContentsMargins(0, 0, 0, 0)

        self.frame_table.adjustSize()
        self.frame_table.update()

    def add_group_table_buttons(self):
        button_layout = QHBoxLayout()

        button_add = QPushButton('Добавить группу')
        button_add.setStyleSheet('color: black; background-color: white;')
        button_add.clicked.connect(self.add_group)
        button_layout.addWidget(button_add)

        button_edit = QPushButton('Редактировать группу')
        button_edit.setStyleSheet('color: black; background-color: white;')
        button_edit.clicked.connect(self.edit_group)
        button_layout.addWidget(button_edit)

        button_delet = QPushButton('Улалить группу')
        button_delet.setStyleSheet('color: black; background-color: white;')
        button_delet.clicked.connect(self.delete_group)
        button_layout.addWidget(button_delet)

        self.table_layout.addLayout(button_layout)

    def on_group_selection_changed(self, table):
        indexes = table.selectionModel().selectedRows()
        if indexes:
            id = indexes[0].data()
            return id

    def populate_teachers_students_teste(self):
        self.model_teacher.removeRows(0, self.model_teacher.rowCount())
        self.model_student.removeRows(0, self.model_student.rowCount())
        self.model_test.removeRows(0, self.model_test.rowCount())

        group_id = self.on_group_selection_changed(self.table_group)

        self.db.get_data_teachers_students_test(
            self.model_teacher, group_id, 0)
        self.db.get_data_teachers_students_test(
            self.model_student, group_id, 1)
        self.db.get_data_teachers_students_test(self.model_test, group_id, 2)

    def add_student_in_group(self):
        group_id = self.on_group_selection_changed(self.table_group)

        self.add_in_group = AddStudentInGroup(
            group_id, self.db, self.model_student, 1)
        self.add_in_group.show()

    def add_teacher_in_group(self):
        group_id = self.on_group_selection_changed(self.table_group)

        self.add_in_group = AddTeatcherInGroup(
            group_id, self.db, self.model_teacher, 0)
        self.add_in_group.show()

    def delete_student_in_group(self):
        group_id = self.on_group_selection_changed(self.table_group)
        user_id = self.on_group_selection_changed(self.table_student)
        self.db.remove_from_group(group_id, user_id, self.model_student, 1)

    def delete_teacher_in_group(self):
        group_id = self.on_group_selection_changed(self.table_group)
        user_id = self.on_group_selection_changed(self.table_teacher)
        self.db.remove_from_group(group_id, user_id, self.model_teacher, 0)

    def add_test_in_group(self):
        try:
            self.test_dialog = TestDialog(self, self.table_test, self.db)
            self.test_dialog.show()
        except Exception as error:
            self.message_errore(str(error))

    def delete_test_in_group(self):
        selected_indexes = self.table_test.selectionModel().selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            model = self.table_test.model()

            id_test = model.data(model.index(row, 0))
            id_group = model.data(model.index(row, 2))

            self.db.delete_test_group(id_test, model, id_group)
        else:
            QMessageBox.warning(
                self, 'Предупреждение', 'Пожалуйста, выберите тест.')


class UserDialog(QDialog):
    def __init__(self, main_admin, role, table, db, parent=None):
        super().__init__(parent)
        self.main_admin = main_admin
        self.db = db

        self.setWindowTitle('Добавить пользователя')

        self.layout = QVBoxLayout(self)

        self.fullname_label = QLabel('ФИО')
        self.fullname_input = QLineEdit()
        self.layout.addWidget(self.fullname_label)
        self.layout.addWidget(self.fullname_input)

        self.login_label = QLabel('Логин')
        self.login_input = QLineEdit()
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_input)

        self.password_label = QLabel('Пароль')
        self.password_input = QLineEdit()
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        self.add_button = QPushButton('Добавить')
        self.add_button.clicked.connect(lambda: self.add_user(role, table))
        self.layout.addWidget(self.add_button)

    def add_user(self, role, table):
        fullname = self.fullname_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        model = table.model().sourceModel()

        self.db.add_user(fullname, login, password, role, model)

        self.close()


class StudentDialog(QDialog):
    def __init__(self, main_admin, table, db, parent=None):
        super().__init__(parent)
        self.main_admin = main_admin  # Сохраняем экземпляр MainAdmin
        self.db = db

        self.setWindowTitle('Добавить студента')

        self.layout = QVBoxLayout(self)

        self.fullname_label = QLabel('ФИО')
        self.fullname_input = QLineEdit()
        self.layout.addWidget(self.fullname_label)
        self.layout.addWidget(self.fullname_input)

        self.login_label = QLabel('Логин')
        self.login_input = QLineEdit()
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_input)

        self.password_label = QLabel('Пароль')
        self.password_input = QLineEdit()
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        self.branch_label = QLabel('Филиал')
        self.branch_combo = QComboBox()
        self.layout.addWidget(self.branch_label)
        self.layout.addWidget(self.branch_combo)

        self.branch_model = QStandardItemModel()

        branches = self.db.get_all_branches()
        for branch in branches:
            item = QStandardItem(branch[1])
            item.setData(branch[0])
            self.branch_model.appendRow(item)

        self.branch_combo.setModel(self.branch_model)

        self.add_button = QPushButton('Добавить')
        self.add_button.clicked.connect(lambda: self.add_user(3, table))
        self.layout.addWidget(self.add_button)

    def add_user(self, role, table):
        fullname = self.fullname_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        selected_index = self.branch_combo.currentIndex()
        selected_item = self.branch_model.item(selected_index)

        branch_id = selected_item.data()

        model = table.model().sourceModel()

        self.db.add_student(fullname, login, password, branch_id, model, role)

        self.close()


class EditUserDialog(QDialog):
    def __init__(self, main_admin, role, table, db, user_id, login, parent=None):
        super().__init__(parent)
        self.main_admin = main_admin
        self.db = db
        self.user_id = user_id

        self.setWindowTitle('Редактировать пользователя')

        user_info = self.db.get_user_info(user_id, login, int(role))

        self.layout = QVBoxLayout(self)

        self.fullname_label = QLabel('FullName')
        self.fullname_input = QLineEdit(user_info['name'])
        self.layout.addWidget(self.fullname_label)
        self.layout.addWidget(self.fullname_input)

        self.login_label = QLabel('Login')
        self.login_input = QLineEdit(user_info['login'])
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_input)

        self.password_label = QLabel('Password')
        self.password_input = QLineEdit(user_info['password'])
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        self.edit_button = QPushButton('Редактировать')
        self.edit_button.clicked.connect(lambda: self.edit_user(role, table))
        self.layout.addWidget(self.edit_button)

    def edit_user(self, role, table):
        fullname = self.fullname_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        model = table.model().sourceModel()

        self.db.edit_user(fullname, login, password, role, model, self.user_id)

        self.close()


class EditStudentDialog(QDialog):
    def __init__(self, main_admin, table, db, user_id, login, parent=None):
        super().__init__(parent)
        self.main_admin = main_admin  # Сохраняем экземпляр MainAdmin
        self.db = db
        self.user_id = user_id

        self.setWindowTitle('Редактировать студента')

        user_info = self.db.get_user_info(user_id, login, 3)

        self.layout = QVBoxLayout(self)

        self.fullname_label = QLabel('ФИО')
        self.fullname_input = QLineEdit(user_info['name'])
        self.layout.addWidget(self.fullname_label)
        self.layout.addWidget(self.fullname_input)

        self.login_label = QLabel('Логин')
        self.login_input = QLineEdit(user_info['login'])
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_input)

        self.password_label = QLabel('Пароль')
        self.password_input = QLineEdit(user_info['password'])
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        # Добавляем комбобокс для веток
        self.branch_label = QLabel('Филиал')
        self.branch_combo = QComboBox()
        self.layout.addWidget(self.branch_label)
        self.layout.addWidget(self.branch_combo)

        self.branch_model = QStandardItemModel()
        branches = self.db.get_all_branches()
        for branch in branches:
            # Используем имя ветки для отображения в комбобоксе
            item = QStandardItem(branch[1])
            item.setData(branch[0])  # Сохраняем ID ветки в модели
            self.branch_model.appendRow(item)

        # Устанавливаем модель для комбобокса
        self.branch_combo.setModel(self.branch_model)

        # Получаем ID ветки студента
        student_branch_id = user_info['branch']

        # Находим индекс этой ветки в модели
        for i in range(self.branch_model.rowCount()):
            item = self.branch_model.item(i)
            if item.data() == student_branch_id:
                student_branch_index = i
                break

        # Устанавливаем этот индекс как текущий для комбобокса
        self.branch_combo.setCurrentIndex(student_branch_index)

        self.edit_button = QPushButton('Редактировать')
        self.edit_button.clicked.connect(lambda: self.edit_user(3, table))
        self.layout.addWidget(self.edit_button)

    def edit_user(self, role, table):
        fullname = self.fullname_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        selected_index = self.branch_combo.currentIndex()
        selected_item = self.branch_model.item(selected_index)

        branch_id = selected_item.data()

        model = table.model().sourceModel()

        self.db.edit_student(fullname, login, password,
                             branch_id, model, self.user_id)

        self.close()


class GroupAddDialog(QDialog):
    def __init__(self, db, model, parent=None):
        super().__init__(parent)
        self.db = db
        self.model = model

        self.setWindowTitle('Добавить группу')

        self.layout = QVBoxLayout(self)

        self.groupname_label = QLabel('Название группы')
        self.groupname_input = QLineEdit()
        self.layout.addWidget(self.groupname_label)
        self.layout.addWidget(self.groupname_input)

        self.curator_label = QLabel('Куратор')
        self.curator_combobox = QComboBox()
        self.setup_combobox()
        self.layout.addWidget(self.curator_label)
        self.layout.addWidget(self.curator_combobox)

        self.add_button = QPushButton('Добавить')
        self.add_button.clicked.connect(self.add_group)
        self.layout.addWidget(self.add_button)

    def setup_combobox(self):
        curators = self.db.get_all_curators()

        for curator_id, fullname in curators:
            self.curator_combobox.addItem(fullname, userData=curator_id)

    def add_group(self):
        group_name = self.groupname_input.text()
        curator_id = self.curator_combobox.currentData()

        if self.db.add_group(group_name, curator_id, self.model):
            self.close()
        else:
            QMessageBox.critical(
                self, "Ошибка", "Ошибка при добавлении группы в базу данных.")


class GroupEditDialog(QDialog):
    def __init__(self, group_id, groupname, curator_id, db, model, parent=None):
        super().__init__(parent)
        self.group_id = group_id
        self.db = db
        self.model = model

        self.setWindowTitle('Редактировать группу')

        self.layout = QVBoxLayout(self)

        self.groupname_label = QLabel('Название группы')
        self.groupname_input = QLineEdit(groupname)
        self.layout.addWidget(self.groupname_label)
        self.layout.addWidget(self.groupname_input)

        self.curator_label = QLabel('Куратор')
        self.curator_combobox = QComboBox()

        self.setup_combobox(curator_id)
        self.layout.addWidget(self.curator_label)
        self.layout.addWidget(self.curator_combobox)

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(self.save_group)
        self.layout.addWidget(self.save_button)

    def setup_combobox(self, selected_curator_id):
        curators = self.db.get_all_curators()

        for curator_id, fullname in curators:
            self.curator_combobox.addItem(fullname, userData=curator_id)

            if curator_id == selected_curator_id:
                self.curator_combobox.setCurrentIndex(
                    self.curator_combobox.findData(curator_id))

    def save_group(self):
        groupname = self.groupname_input.text()
        curator_id = self.curator_combobox.currentData()

        self.db.update_group(self.group_id, groupname, curator_id, self.model)

        self.close()


class AddStudentInGroup(QDialog):
    def __init__(self, group_id, db, model, code, parent=None):
        super().__init__(parent)

        self.group_id = group_id
        self.db = db
        self.model = model
        self.code = code

        self.setWindowTitle('Добавить учащегося в группу')
        self.layout = QGridLayout(self)

        label1 = QLabel("Список учащихся")
        label1.setAlignment(Qt.AlignCenter)
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.select_item)
        self.db.fill_list(self.list_widget, self.code)

        label2 = QLabel("Добавляемые учащиеся")
        label2.setAlignment(Qt.AlignCenter)
        self.list_widget2 = QListWidget()
        self.list_widget2.itemClicked.connect(self.deselect_item)

        self.button = QPushButton("Добавить в группу")
        self.button.clicked.connect(self.adding_a_record)

        self.layout.addWidget(label1, 0, 0)
        self.layout.addWidget(self.list_widget, 1, 0)
        self.layout.addWidget(label2, 0, 1)
        self.layout.addWidget(self.list_widget2, 1, 1)
        self.layout.addWidget(self.button, 2, 0, 1, 2)

    def select_item(self, item):
        self.list_widget2.addItem(item.text())
        self.list_widget.takeItem(self.list_widget.row(item))

    def deselect_item(self, item):
        self.list_widget.addItem(item.text())
        self.list_widget2.takeItem(self.list_widget2.row(item))

    def adding_a_record(self):
        for i in range(self.list_widget2.count()):
            item_text = self.list_widget2.item(i).text()
            data = item_text.split(' / ')
            self.db.add_student_to_group(
                self.group_id, data[0], self.model, self.code)

        self.close()


class AddTeatcherInGroup(QDialog):
    def __init__(self, group_id, db, model, code, parent=None):
        super().__init__(parent)

        self.group_id = group_id
        self.db = db
        self.model = model
        self.code = code

        self.setWindowTitle('Добавить преподавателя в группу')
        self.layout = QGridLayout(self)

        label1 = QLabel("Список преподавателей")
        label1.setAlignment(Qt.AlignCenter)
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.select_item)
        self.db.fill_list(self.list_widget, self.code)

        label2 = QLabel("Добавляемые преподаватели")
        label2.setAlignment(Qt.AlignCenter)
        self.list_widget2 = QListWidget()
        self.list_widget2.itemClicked.connect(self.deselect_item)

        self.button = QPushButton("Добавить в группу")
        self.button.clicked.connect(self.adding_a_record)

        self.layout.addWidget(label1, 0, 0)
        self.layout.addWidget(self.list_widget, 1, 0)
        self.layout.addWidget(label2, 0, 1)
        self.layout.addWidget(self.list_widget2, 1, 1)
        self.layout.addWidget(self.button, 2, 0, 1, 2)

    def select_item(self, item):
        self.list_widget2.addItem(item.text())
        self.list_widget.takeItem(self.list_widget.row(item))

    def deselect_item(self, item):
        self.list_widget.addItem(item.text())
        self.list_widget2.takeItem(self.list_widget2.row(item))

    def adding_a_record(self):
        for i in range(self.list_widget2.count()):
            item_text = self.list_widget2.item(i).text()
            data = item_text.split(' / ')
            self.db.add_student_to_group(
                self.group_id, data[0], self.model, self.code)

        self.close()


class TestDialog(QDialog):
    def __init__(self, main_admin, table, db, parent=None):
        super().__init__(parent)
        self.main_admin = main_admin  # Сохраняем экземпляр MainAdmin
        self.db = db

        self.setWindowTitle('Добавить тест')

        self.layout = QVBoxLayout(self)

        self.teacher_label = QLabel('Преподаватель')
        self.teacher_combo = QComboBox()
        self.teacher_model = QStandardItemModel()  # Инициализируем модель
        self.teacher_combo.setModel(self.teacher_model)
        self.layout.addWidget(self.teacher_label)
        self.layout.addWidget(self.teacher_combo)

        self.group_label = QLabel('Группа')
        self.group_combo = QComboBox()
        self.group_model = QStandardItemModel()  # Инициализируем модель
        self.group_combo.setModel(self.group_model)
        self.layout.addWidget(self.group_label)
        self.layout.addWidget(self.group_combo)

        # Заполните комбо-боксы данными из базы данных
        self.fill_combos()

        self.name_label = QLabel('Название')
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.attempts_label = QLabel('Попытки')
        self.attempts_input = QLineEdit()
        self.layout.addWidget(self.attempts_label)
        self.layout.addWidget(self.attempts_input)

        self.time_label = QLabel('Общее время прохождения теста')
        self.time_input = QLineEdit()
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.time_input)

        self.add_button = QPushButton('Добавить')
        self.add_button.clicked.connect(lambda: self.add_test(table))
        self.layout.addWidget(self.add_button)

    def fill_combos(self):
        teachers = self.db.get_all_teachers()
        for teacher in teachers:
            # Используйте индекс вместо ключа
            item = QStandardItem(str(teacher[1]))
            # Используйте Qt.UserRole для установки данных
            item.setData(teacher[0], Qt.UserRole)
            self.teacher_model.appendRow(item)
        if self.teacher_model.rowCount() > 0:
            self.teacher_combo.setCurrentIndex(
                0)  # Устанавливаем текущий индекс

        groups = self.db.get_all_groups()
        for group in groups:
            # Используйте индекс вместо ключа
            item = QStandardItem(str(group[1]))
            # Используйте Qt.UserRole для установки данных
            item.setData(group[0], Qt.UserRole)
            self.group_model.appendRow(item)
        if self.group_model.rowCount() > 0:
            self.group_combo.setCurrentIndex(0)  # Устанавливаем текущий индекс

    def add_test(self, table):
        selected_teacher_index = self.teacher_combo.currentIndex()
        selected_teacher_item = self.teacher_model.item(selected_teacher_index)
        teacher_id = selected_teacher_item.data(Qt.UserRole)

        selected_group_index = self.group_combo.currentIndex()
        selected_group_item = self.group_model.item(selected_group_index)
        group_id = selected_group_item.data(Qt.UserRole)

        name = self.name_input.text()
        attempts = self.attempts_input.text()
        time = self.time_input.text()

        model = table.model()

        self.db.add_test(teacher_id, group_id, name, attempts, time, model)

        self.close()
