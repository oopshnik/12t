import os
import requests
import shutil
import psutil
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout,
    QHBoxLayout, QMessageBox, QFrame, QFileDialog, QProgressBar, QDialog, QCheckBox
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import webbrowser
from update_check import isUpToDate

class DownloadThread(QThread):
    update_info = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    install_finished = pyqtSignal(bool, str)
    gd_input = str()
    geode_version = False

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.update_info.emit('Downloading the latest MegaCrack release...')
            response = requests.get('https://api.github.com/repos/qwix456/vzlomkaa/releases/latest')
            if response.status_code != 200:
                raise Exception('Failed to fetch release information. Check your internet connection.')
            release_data = response.json()

            assets_url = release_data.get('assets_url')
            if not assets_url:
                raise Exception('Invalid release data format. No assets_url found.')

            self.update_info.emit('Fetching download links...')
            assets_response = requests.get(assets_url)
            if assets_response.status_code != 200:
                raise Exception('Failed to fetch assets information.')

            assets_data = assets_response.json()

            if installer.geode_checkbox.isChecked():
                download_urls = {
                    'absolllute.megahack.geode': None,
                    'qwix456.megahack_crack_patcher.geode': None,
                }

                geode_mods_path = os.path.join(self.gd_input, 'geode', 'mods')
                if not os.path.exists(geode_mods_path):
                    os.makedirs(geode_mods_path)
            else:
                download_urls = {
                    'hackpro.dll': None,
                    'hackproldr.dll': None,
                    'nigapro.dll': None,
                    'XINPUT1_4.dll': None,
                }

            for asset in assets_data:
                asset_name = asset.get('name')
                if asset_name in download_urls:
                    download_urls[asset_name] = asset.get('browser_download_url')
        
            missing_files = [name for name, url in download_urls.items() if url is None]
            if missing_files:
                raise Exception(f'Missing download URLs for: {", ".join(missing_files)}')

            temp_dir = os.getenv('TEMP')

            for file_name, download_url in download_urls.items():
                self.update_info.emit(f'Downloading {file_name}...')
                temp_file_path = os.path.join(temp_dir, file_name)
                self.download_file(download_url, temp_file_path)

                if installer.geode_checkbox.isChecked():
                    dest_file_path = os.path.join(geode_mods_path, file_name)
                else:
                    dest_file_path = os.path.join(self.gd_input, file_name)

                self.update_info.emit(f'Installing {file_name}...')
                shutil.copy(temp_file_path, dest_file_path)
                time.sleep(0.5)

            self.update_progress.emit(100)
            self.update_info.emit('Successfully installed')
            self.install_finished.emit(True, 'MegaCrack successfully installed')
        except Exception as e:
            self.install_finished.emit(False, str(e))

    def download_file(self, url, dest):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        downloaded_size = 0

        with open(dest, 'wb') as file:
            for data in response.iter_content(block_size):
                downloaded_size += len(data)
                file.write(data)
                self.update_progress.emit(int((downloaded_size / total_size) * 100))

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Installation Progress")
        self.setGeometry(600, 300, 400, 150)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.label_info = QLabel("Initializing...", self)
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_info)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def update_info(self, text):
        self.label_info.setText(text)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

class Installer(QWidget):
    def __init__(self): 
        super().__init__() #privet )
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #4E4E4E;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4E4E4E;
            }
            QLineEdit {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #4E4E4E;
                border-radius: 5px;
            }
        """)
        self.setup_ui()

        if not isUpToDate(__file__, "https://raw.githubusercontent.com/username/repo/myProgram.py"):
            self.show_update_dialog()

    def setup_ui(self):
        self.setGeometry(400, 150, 800, 400)
        self.setWindowTitle('MegaCrack Installer')
        self.setWindowIcon(QIcon("icon.png"))

        font = QFont("Cascadia Code", 13)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        icon_label = QLabel()
        pixmap = QPixmap("icon.png").scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio)
        icon_label.setPixmap(pixmap)
        left_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

        credits_label = QLabel("Crack by @qwix456\nApp by @oopshnik\n \n \n Close Geometry Dash before opening app\nAlso press tab to open menu", self)
        credits_label.setFont(font)
        credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(credits_label)

        gd_modding_btn = QPushButton("PatchTeam Telegram")
        gd_modding_btn.setFont(font)
        gd_modding_btn.clicked.connect(lambda: self.open_link('https://t.me/patchteam1337'))
        left_layout.addWidget(gd_modding_btn)

        left_layout.addStretch(1)
 
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.VLine)
        frame.setFrameShadow(QFrame.Shadow.Sunken)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("MegaCrack Installer (v8)")
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(title)

        path_layout = QHBoxLayout()
        
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Path to GD (only folder)")
        self.path_input.setFont(font)
        path_layout.addWidget(self.path_input)

        browse_btn = QPushButton('...')
        browse_btn.setFixedWidth(30)
        browse_btn.clicked.connect(self.open_folder_dialog)
        path_layout.addWidget(browse_btn)

        right_layout.addLayout(path_layout)
        
        detect_path_btn = QPushButton('Detect Path')
        detect_path_btn.setFont(font)
        detect_path_btn.clicked.connect(self.detect_path)
        right_layout.addWidget(detect_path_btn)

        button_layout = QHBoxLayout()

        install_btn = QPushButton('Install')
        install_btn.setFont(font)
        install_btn.clicked.connect(self.start_install)
        button_layout.addWidget(install_btn)

        exit_btn = QPushButton('Exit')
        exit_btn.setFont(font)
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)

        right_layout.addLayout(button_layout)

        self.geode_checkbox = QCheckBox("Geode Version")
        self.geode_checkbox.setFont(font)
        right_layout.addWidget(self.geode_checkbox)

        main_layout.addLayout(left_layout)
        main_layout.addWidget(frame)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_input.setText(folder)
    
    def start_install(self):
        self.progress_dialog = ProgressDialog()
        self.progress_dialog.show()

        self.download_thread = DownloadThread()
        self.download_thread.gd_input = self.path_input.text()
        self.download_thread.geode_version = self.geode_checkbox.isChecked()
        self.download_thread.update_info.connect(self.progress_dialog.update_info)
        self.download_thread.update_progress.connect(self.progress_dialog.update_progress)
        self.download_thread.install_finished.connect(self.install_finished)
        self.download_thread.start()

    def detect_path(self):
        for process in psutil.process_iter(['name']):
            if process.info['name'] == 'GeometryDash.exe':
                self.path_input.setText(os.path.dirname(process.exe()))
                return
        QMessageBox.warning(self, "Warning", "Geometry Dash is not running.")

    def install_finished(self, success, message):
        self.progress_dialog.close()
        QMessageBox.information(self, "Installation Complete" if success else "Installation Failed", message)
        
    def open_link(self, url):
        webbrowser.open(url)

    def show_update_dialog(self):
        reply = QMessageBox.question(
        self,
        "Update Available",
        "A new version of the MegaCrack Installer is available. Would you like to download it?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )

        if reply == QMessageBox.StandardButton.Yes:
            webbrowser.open("https://t.me/")

if __name__ == '__main__':
    app = QApplication([])
    installer = Installer()
    installer.show()
    app.exec()
