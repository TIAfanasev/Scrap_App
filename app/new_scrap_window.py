from PyQt5 import Qt, QtGui
from PyQt5.QtCore import Qt as Qtt

from app import styles
from app.db_requests import check_scrapname_unique, create_new_scrap


class ScrapCreator(Qt.QDialog):

    def __init__(self, u_id, parent=None):
        super().__init__(parent)

        self.u_id = u_id
        self.setGeometry(800, 350, 300, 300)
        self.setWindowTitle('Создание')
        self.label = Qt.QLabel('Новое наименование')

        self.setWindowIcon(QtGui.QIcon("icons/Icon.png"))
        self.label.setStyleSheet("color:black; font: bold 20pt 'Arial';")
        self.label.setAlignment(Qtt.AlignCenter)

        self.name_label = Qt.QLabel('Наименование:')
        self.name_label.setFont(styles.font)
        self.name = Qt.QLineEdit()
        self.name.setFont(styles.font)
        self.name.setPlaceholderText('Пример: Лом меди')

        self.price_label = Qt.QLabel('Цена:')
        self.price_label.setFont(styles.font)
        self.price = Qt.QLineEdit()
        self.price.setFont(styles.font)
        self.price.setPlaceholderText('Пример: 41.5')

        self.per_nds_label = Qt.QLabel('% НДС:')
        self.per_nds_label.setFont(styles.font)
        self.per_nds = Qt.QLineEdit()
        self.per_nds.setFont(styles.font)
        self.per_nds.setPlaceholderText('Пример: 2.2')

        self.save_btn = Qt.QPushButton('Сохранить и выйти')

        v_layout = Qt.QVBoxLayout(self)
        v_layout.addWidget(self.name_label)
        v_layout.addWidget(self.name)
        v_layout.addWidget(self.price_label)
        v_layout.addWidget(self.price)
        v_layout.addWidget(self.per_nds_label)
        v_layout.addWidget(self.per_nds)
        v_layout.addWidget(self.save_btn)

        self.save_btn.clicked.connect(self.save_new_scrap_and_exit)

    def save_new_scrap_and_exit(self):
        try:
            name = self.name.text()
            val_price = float(self.price.text())
            val_per_nds = float(self.per_nds.text())
        except Exception as e:
            Qt.QMessageBox.critical(self, 'Ошибка!', 'Ошибка в цене или %НДС!')
        else:
            if check_scrapname_unique(name):
                create_new_scrap(name, val_price, val_per_nds, self.u_id)
                self.accept()
            else:
                Qt.QMessageBox.critical(self, 'Ошибка!', 'Такое наименование уже существует!')
