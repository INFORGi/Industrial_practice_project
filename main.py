import sys
import database
import gui
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = database.DataBase()
    ui_app = gui.AuthorizationWindow(db)
    ui_app.show()
    sys.exit(app.exec_())