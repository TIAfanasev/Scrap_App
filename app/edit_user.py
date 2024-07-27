from PyQt5 import Qt, QtWidgets, QtGui
from PyQt5.QtCore import Qt as Qtt
from hashlib import md5

import styles
from db_requests import get_user_info, check_unique_login, update_user, get_all_roles, create_user


class UserEditor(Qt.QDialog):

    def __init__(self, u_id=None, parent=None):
        super().__init__(parent)

        self.roles_list = get_all_roles()

        self.setGeometry(800, 350, 300, 300)
        if u_id:
            self.u_id = u_id
            self.setWindowTitle('Редактирование')
            self.label = Qt.QLabel('Редактирование пользователя')
            self.user, self.role = get_user_info(self.u_id)
        else:
            self.setWindowTitle('Создание')
            self.label = Qt.QLabel('Создание пользователя')

        self.setWindowIcon(QtGui.QIcon("icons/Icon.png"))
        self.label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.label.setAlignment(Qtt.AlignCenter)

        self.name_label = Qt.QLabel('ФИО:')
        self.name_label.setFont(styles.font)
        self.name = Qt.QLineEdit()
        self.name.setFont(styles.font)
        self.name.setPlaceholderText('Пример: Иванов Иван Иванович')

        self.login_label = Qt.QLabel('Логин:')
        self.login_label.setFont(styles.font)
        self.login = Qt.QLineEdit()
        self.login.setFont(styles.font)
        self.login.setPlaceholderText('Пример: user1')

        self.role_label = Qt.QLabel(f'Роль:')
        self.role_label.setFont(styles.font)
        self.role_combo = Qt.QComboBox()
        self.role_combo.setFont(styles.font)
        self.role_combo.addItems(self.roles_list)

        self.password = Qt.QLineEdit()
        self.password.setFont(styles.font)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.save_btn = Qt.QPushButton('Сохранить и выйти')

        if u_id:
            self.id_label = Qt.QLabel(f'ID: {self.user.id}')
            self.id_label.setFont(styles.font)

            self.name.setText(self.user.name)

            self.login.setText(self.user.login)
            self.role_combo.setCurrentText(self.role.role)

            self.password_label = Qt.QLabel('Изменить пароль:')
        else:
            self.password_label = Qt.QLabel('Задать пароль:')

        self.password_label.setFont(styles.font)

        v_layout = Qt.QVBoxLayout(self)
        if u_id:
            v_layout.addWidget(self.id_label)
        v_layout.addWidget(self.name_label)
        v_layout.addWidget(self.name)
        v_layout.addWidget(self.login_label)
        v_layout.addWidget(self.login)
        v_layout.addWidget(self.role_label)
        v_layout.addWidget(self.role_combo)
        v_layout.addWidget(self.password_label)
        v_layout.addWidget(self.password)
        v_layout.addWidget(self.save_btn)

        if u_id:
            self.save_btn.clicked.connect(self.save_updated_user_and_exit)
        else:
            self.save_btn.clicked.connect(self.save_new_user_and_exit)

    def save_updated_user_and_exit(self):
        if check_unique_login(str(self.login.text())) or self.user.login == str(self.login.text()):
            if self.password.text():
                password = self.password.text()
                for x in range(10):
                    password = md5(password.encode()).hexdigest()
                update_user(self.u_id, (self.name.text()), str(self.login.text()), str(self.role_combo.currentText()),
                            str(password))
            else:
                update_user(self.u_id, str(self.name.text()), str(self.login.text()),
                            str(self.role_combo.currentText()))
            self.accept()
        else:
            Qt.QMessageBox.critical(self, 'Ошибка!', 'Указанный логин уже существует!')

    def save_new_user_and_exit(self):
        if check_unique_login(str(self.login.text())) and self.login.text():
            if self.name.text():
                if self.password.text():
                    password = self.password.text()
                    for x in range(10):
                        password = md5(password.encode()).hexdigest()
                    create_user((self.name.text()), str(self.login.text()), str(password),
                                str(self.role_combo.currentText()))
                    self.accept()
                else:
                    Qt.QMessageBox.critical(self, 'Ошибка!', 'Задайте пароль!')
            else:
                Qt.QMessageBox.critical(self, 'Ошибка!', 'Введите имя!')
        else:
            Qt.QMessageBox.critical(self, 'Ошибка!', 'Указанный логин уже существует!')
