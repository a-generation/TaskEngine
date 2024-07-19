import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QAction, QMenuBar, QMenu, QInputDialog, QMessageBox, QTextBrowser, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import QTimer

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        self.setGeometry(100, 100, 300, 200)

        # Создаем макет
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Создаем виджет для текста с поддержкой гиперссылок
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setHtml(
            '<h2>TaskEngine</h2>'
            '<p>A-generation, 2024</p>'
            '<p>GitHub: <a href="https://github.com/a-generation/TaskEngine">https://github.com/a-generation/TaskEngine</a></p>'
        )

        layout.addWidget(self.text_browser)

        # Кнопка "OK"
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        layout.addWidget(self.button_box)

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Task Manager')
        self.setGeometry(100, 100, 800, 600)

        # Создаем основной виджет и устанавливаем его
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Создаем макет
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Создаем таблицу для отображения процессов
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Создаем меню
        self.menu_bar = self.menuBar()
        self.update_menu = self.menu_bar.addMenu('Update Interval')
        self.process_menu = self.menu_bar.addMenu('Processes')
        self.about_menu = self.menu_bar.addMenu('About')

        # Меню Update Interval
        self.update_1s_action = QAction('1 sec', self)
        self.update_3s_action = QAction('3 sec', self)
        self.update_5s_action = QAction('5 sec', self)
        self.no_update_action = QAction('No Update', self)

        self.update_1s_action.triggered.connect(lambda: self.set_update_interval(1000))
        self.update_3s_action.triggered.connect(lambda: self.set_update_interval(3000))
        self.update_5s_action.triggered.connect(lambda: self.set_update_interval(5000))
        self.no_update_action.triggered.connect(lambda: self.set_update_interval(0))

        self.update_menu.addAction(self.update_1s_action)
        self.update_menu.addAction(self.update_3s_action)
        self.update_menu.addAction(self.update_5s_action)
        self.update_menu.addAction(self.no_update_action)

        # Меню Processes
        self.stop_action = QAction('Stop Process', self)
        self.restart_action = QAction('Restart Process', self)
        self.create_task_action = QAction('Create Task', self)

        self.stop_action.triggered.connect(self.stop_process)
        self.restart_action.triggered.connect(self.restart_process)
        self.create_task_action.triggered.connect(self.create_task)

        self.process_menu.addAction(self.stop_action)
        self.process_menu.addAction(self.restart_action)
        self.process_menu.addAction(self.create_task_action)

        # Меню About
        self.about_action = QAction('About', self)
        self.about_action.triggered.connect(self.show_about_dialog)

        self.about_menu.addAction(self.about_action)

        # Настраиваем таймер для обновления данных
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_processes)
        self.update_interval = 0  # Default to no update
        self.update_processes()

    def update_processes(self):
        # Получаем список процессов и преобразуем его в список
        processes = list(psutil.process_iter(['pid', 'name', 'username']))

        # Устанавливаем количество строк и колонок
        self.table.setRowCount(len(processes))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['PID', 'Name', 'Username'])

        # Заполняем таблицу данными
        for row, proc in enumerate(processes):
            self.table.setItem(row, 0, QTableWidgetItem(str(proc.info['pid'])))
            self.table.setItem(row, 1, QTableWidgetItem(proc.info['name']))
            self.table.setItem(row, 2, QTableWidgetItem(proc.info['username']))

        # Настроим ширину столбцов
        self.table.resizeColumnsToContents()

        # Устанавливаем высоту строк
        self.table.setStyleSheet("QTableWidget::item { height: 20px; }")

        # Запускаем таймер с обновленным интервалом
        if self.update_interval > 0:
            self.timer.start(self.update_interval)

    def set_update_interval(self, interval):
        self.update_interval = interval
        if self.update_interval == 0:
            self.timer.stop()
        else:
            self.timer.start(self.update_interval)

    def stop_process(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            pid_item = self.table.item(selected_row, 0)
            if pid_item:
                pid = int(pid_item.text())
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()
                    QMessageBox.information(self, 'Success', f'Process {pid} terminated.')
                except psutil.NoSuchProcess:
                    QMessageBox.warning(self, 'Error', 'Process does not exist.')
                except Exception as e:
                    QMessageBox.warning(self, 'Error', f'Error terminating process: {e}')
        else:
            QMessageBox.warning(self, 'Error', 'No process selected.')

    def restart_process(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            pid_item = self.table.item(selected_row, 0)
            if pid_item:
                pid = int(pid_item.text())
                try:
                    proc = psutil.Process(pid)
                    # Attempt to restart process
                    proc.terminate()
                    proc.wait()
                    proc = psutil.Popen(proc.cmdline())
                    QMessageBox.information(self, 'Success', f'Process {pid} restarted.')
                except psutil.NoSuchProcess:
                    QMessageBox.warning(self, 'Error', 'Process does not exist.')
                except Exception as e:
                    QMessageBox.warning(self, 'Error', f'Error restarting process: {e}')
        else:
            QMessageBox.warning(self, 'Error', 'No process selected.')

    def create_task(self):
        command, ok = QInputDialog.getText(self, 'Create Task', 'Enter command to run:')
        if ok and command:
            try:
                proc = psutil.Popen(command, shell=True)
                QMessageBox.information(self, 'Success', f'Command "{command}" started.')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Error starting command: {e}')

    def show_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
