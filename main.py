from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import subprocess
import re

class Dpsht(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        spwn_ver = subprocess.check_output(['spwn', 'version']).decode()
        dpsht_ver = "v0.1.0-dev"
        
        ver_match = re.compile("v[0-9]+[.][0-9]+[.][0-9]+")
        if ver_match.match(spwn_ver) == None:
            spwn_ver = "N/A"

        build_group = QGroupBox("Build")
        build = QVBoxLayout()
        build_type = QComboBox()
        build_type.addItem("Script")
        build_type.addItem("Documentation")
        build.addWidget(build_type)
        build.addWidget(QPushButton("Build"))
        build_group.setLayout(build)

        build_options_group = QGroupBox("Build Options")
        build_options = QVBoxLayout()
        build_options.addWidget(QCheckBox('Console Output'))
        build_options.addWidget(QCheckBox('No Level'))
        build_options.addWidget(QCheckBox('No Optimize'))
        self.level_name = QCheckBox('Level Name', self)
        self.level_name.stateChanged.connect(self.level_name_change)
        build_options.addWidget(self.level_name)
        self.level_name_data = QLineEdit()
        self.level_name_data.setDisabled(True)
        build_options.addWidget(self.level_name_data)
        build_options.addWidget(QCheckBox('Live Editor'))
        self.save_file = QCheckBox('Save File')
        self.save_file.stateChanged.connect(self.save_file_change)
        build_options.addWidget(self.save_file)
        self.save_file_data = QLineEdit()
        self.save_file_data.setDisabled(True)
        build_options.addWidget(self.save_file_data)
        self.include_path = QCheckBox('Include Path')
        self.include_path.stateChanged.connect(self.include_path_change)
        build_options.addWidget(self.include_path)
        self.include_path_data = QLineEdit()
        self.include_path_data.setDisabled(True)
        build_options.addWidget(self.include_path_data)
        build_options_group.setLayout(build_options)

        logo_label = QLabel()
        logo = QPixmap('logo.png')
        logo_label.setPixmap(logo)
        logo_label.setScaledContents(True)

        file_group = QGroupBox("Location Select")
        file = QHBoxLayout()
        file.addWidget(QLabel("Location:"))
        file.addWidget(QLineEdit())
        file.addWidget(QPushButton('Browse'))
        file_group.setLayout(file)

        about_group = QGroupBox("About")
        about = QVBoxLayout()
        about.addWidget(QLabel(f"SPWN Version: {spwn_ver}\nDPSHT Version: {dpsht_ver}"))
        about_group.setLayout(about)

        main = QVBoxLayout()
        main.addWidget(logo_label)
        main.addWidget(file_group)
        main.addWidget(build_options_group)
        main.addWidget(build_group)
        main.addWidget(about_group)

        self.setLayout(main)
        self.setWindowTitle(f'DPSHT {dpsht_ver}')
        self.setFixedWidth(400)
        self.setFixedHeight(700)
        self.show()

    def level_name_change(self, state):
        if state == Qt.Checked:
            self.level_name_data.setDisabled(False)
        else:
            self.level_name_data.clear()
            self.level_name_data.setDisabled(True)
    
    def save_file_change(self, state):
        if state == Qt.Checked:
            self.save_file_data.setDisabled(False)
        else:
            self.save_file_data.clear()
            self.save_file_data.setDisabled(True)

    def include_path_change(self, state):
        if state == Qt.Checked:
            self.include_path_data.setDisabled(False)
        else:
            self.include_path_data.clear()
            self.include_path_data.setDisabled(True)

def main():
    app = QApplication(sys.argv)
    dpsht = Dpsht()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()