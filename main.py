from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pathlib import Path
import sys
import subprocess
import re

class Dpsht(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        spwn_ver = subprocess.check_output(['spwn', 'version']).decode()
        dpsht_ver = "v0.1.0"
        
        ver_match = re.compile("v[0-9]+[.][0-9]+[.][0-9]+")
        if ver_match.match(spwn_ver) == None:
            spwn_ver = "N/A"

        build_group = QGroupBox("Build")
        build = QVBoxLayout()
        self.build_type = QComboBox()
        self.build_type.addItem("Script")
        self.build_type.addItem("Documentation")
        self.build_type.currentIndexChanged.connect(self.build_type_switch)
        build.addWidget(self.build_type)
        self.build_button = QPushButton("Build")
        self.build_button.clicked.connect(self.build_button_click)
        build.addWidget(self.build_button)
        build_group.setLayout(build)

        save_path = QHBoxLayout()
        self.save_file_data = QLineEdit()
        self.save_file_data.setDisabled(True)
        save_path.addWidget(self.save_file_data)
        self.save_browse = QPushButton("Browse")
        self.save_browse.setDisabled(True)
        self.save_browse.clicked.connect(self.browse_save_button_click)
        save_path.addWidget(self.save_browse)

        include_dir = QHBoxLayout()
        self.include_path_data = QLineEdit()
        self.include_path_data.setDisabled(True)
        include_dir.addWidget(self.include_path_data)
        self.include_browse = QPushButton("Browse")
        self.include_browse.setDisabled(True)
        self.include_browse.clicked.connect(self.browse_include_button_click)
        include_dir.addWidget(self.include_browse)

        self.build_options_group = QGroupBox("Build Options")
        build_options = QVBoxLayout()
        self.no_level = QCheckBox('No Level')
        build_options.addWidget(self.no_level)
        self.no_opti = QCheckBox('No Optimize')
        build_options.addWidget(self.no_opti)
        self.level_name = QCheckBox('Level Name', self)
        self.level_name.stateChanged.connect(self.level_name_change)
        build_options.addWidget(self.level_name)
        self.level_name_data = QLineEdit()
        self.level_name_data.setDisabled(True)
        build_options.addWidget(self.level_name_data)
        self.live = QCheckBox('Live Editor')
        build_options.addWidget(self.live)
        self.save_file = QCheckBox('Save File')
        self.save_file.stateChanged.connect(self.save_file_change)
        build_options.addWidget(self.save_file)
        build_options.addLayout(save_path)
        self.include_path = QCheckBox('Include Path')
        self.include_path.stateChanged.connect(self.include_path_change)
        build_options.addWidget(self.include_path)
        build_options.addLayout(include_dir)
        self.build_options_group.setLayout(build_options)

        logo_label = QLabel()
        logo = QPixmap('logo.png')
        logo_label.setPixmap(logo)
        logo_label.setScaledContents(True)

        file_group = QGroupBox("Location Select")
        file = QHBoxLayout()
        self.location_data = QLineEdit()
        file.addWidget(self.location_data)
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_button_click)
        file.addWidget(self.browse_button)
        file_group.setLayout(file)

        about_group = QGroupBox("About")
        about = QVBoxLayout()
        about.addWidget(QLabel(f"SPWN Version: {spwn_ver}\nDPSHT Version: {dpsht_ver}"))
        about_group.setLayout(about)

        main = QVBoxLayout()
        main.addWidget(logo_label)
        main.addWidget(file_group)
        main.addWidget(self.build_options_group)
        main.addWidget(build_group)
        main.addWidget(about_group)

        self.setLayout(main)
        self.setWindowTitle(f'DPSHT {dpsht_ver}')
        self.setWindowIcon(QIcon("logo.ico"))
        self.setFixedWidth(400)
        self.setFixedHeight(660)
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
            self.save_browse.setDisabled(False)
        else:
            self.save_file_data.clear()
            self.save_file_data.setDisabled(True)
            self.save_browse.setDisabled(True)

    def include_path_change(self, state):
        if state == Qt.Checked:
            self.include_path_data.setDisabled(False)
            self.include_browse.setDisabled(False)
        else:
            self.include_path_data.clear()
            self.include_path_data.setDisabled(True)
            self.include_browse.setDisabled(True)

    def build_button_click(self):
        no_level_flag = ''
        no_opti_flag = ''
        level_name_flag = ''
        level_name_flag_name = ''
        live_flag = ''
        save_flag = ''
        save_flag_location = ''
        include_flag = ''
        include_flag_location = ''
        if self.no_level.isChecked():
            no_level_flag = '-l'
        if self.no_opti.isChecked():
            no_opti_flag = '-o'
        if self.level_name.isChecked():
            level_name_flag = '-n'
            level_name_flag_name = self.level_name_data.text()
        if self.live.isChecked():
            live_flag = '-e'
        if self.save_file.isChecked():
            save_flag = '-s'
            save_flag_location = self.save_file_data.text()
        if self.include_path.isChecked():
            include_flag = '-i'
            include_flag_location = self.include_path_data.text()
        selection = self.build_type.currentText()
        output = QMessageBox()
        if selection == "Script":
            subcommand = 'b'
        elif selection == "Documentation":
            subcommand = 'doc'
        try:
            self.res = subprocess.check_output(['spwn', subcommand, self.location_data.text(), no_level_flag, no_opti_flag, level_name_flag, level_name_flag_name, live_flag, save_flag, save_flag_location, include_flag, include_flag_location])
            output.setWindowTitle("Result")
            output.setIcon(QMessageBox.Information)
            output.setText("Script built successfully.")
            output.exec()
        except subprocess.CalledProcessError:
            pass

    def browse_button_click(self):
        selection = self.build_type.currentText()
        if selection == "Script":
            browse = QFileDialog.getOpenFileName(self, 'Open script', str(Path.home()), "SPWN scripts (*.spwn)")
            self.location_data.setText(browse[0])
        elif selection == "Documentation":
            browse = QFileDialog.getExistingDirectory(self, 'Select library directory')
            self.location_data.setText(browse)

    def build_type_switch(self):
        self.location_data.clear()
        index = self.build_type.currentText()
        if index == "Script":
            self.build_options_group.setDisabled(False)
        elif index == "Documentation":
            self.build_options_group.setDisabled(True)

    def browse_save_button_click(self):
        browse = QFileDialog.getOpenFileName(self, 'Open save', str(Path.home()), "GD Save (*.dat)")
        self.save_file_data.setText(browse[0])

    def browse_include_button_click(self):
            browse = QFileDialog.getExistingDirectory(self, 'Select include directory')
            self.include_path_data.setText(browse)

def main():
    app = QApplication(sys.argv)
    dpsht = Dpsht()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()