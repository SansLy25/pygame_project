import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QComboBox,
    QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QFont


class LevelEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.grid_width = 18  # Ширина сетки
        self.grid_height = 10  # Высота сетки
        self.cell_size = 40  # Размер ячейки
        self.current_symbol = "."
        self.grid = [
            ["." for _ in range(self.grid_width)] for _ in range(self.grid_height)
        ]  # Инициализация сетки
        self.dragging = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.grid_widget = QWidget()
        self.grid_widget.setFixedSize(
            self.grid_width * self.cell_size, self.grid_height * self.cell_size
        )
        self.grid_widget.setMouseTracking(True)
        self.grid_widget.mousePressEvent = self.mousePressEvent
        self.grid_widget.mouseMoveEvent = self.mouseMoveEvent
        self.grid_widget.mouseReleaseEvent = self.mouseReleaseEvent
        self.grid_widget.paintEvent = self.paintEvent
        layout.addWidget(self.grid_widget)

        self.symbol_selector = QComboBox()
        self.symbol_selector.addItems(
            ["#", ".", "s", "h", "e", "b", "B", "t", "T", "S", "c", "p"]
        )
        self.symbol_selector.currentTextChanged.connect(self.set_symbol)
        self.current_symbol = "#"
        layout.addWidget(self.symbol_selector)

        save_button = QPushButton("Сохранить уровень")
        load_button = QPushButton("Загрузить уровень")
        save_button.clicked.connect(self.save_level)
        load_button.clicked.connect(self.load_level)
        layout.addWidget(save_button)
        layout.addWidget(load_button)

        self.setWindowTitle("Конструктор уровней")
        self.show()

    def set_symbol(self, symbol):
        self.current_symbol = symbol

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.update_cell(event.position().x(), event.position().y())

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.update_cell(event.position().x(), event.position().y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def update_cell(self, x, y):
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)
        if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
            self.grid[row][col] = self.current_symbol
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self.grid_widget)
        painter.setFont(QFont("Arial", 12))
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                painter.drawText(
                    col * self.cell_size + 15,
                    row * self.cell_size + 25,
                    self.grid[row][col],
                )
                painter.setPen(QColor(200, 200, 200))
                painter.drawRect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

    def save_level(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Сохранить уровень", "", "Text Files (*.txt)"
        )
        if filename:
            with open(filename, "w") as f:
                for row in self.grid:
                    f.write("".join(row) + "\n")

    def load_level(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Загрузить уровень", "", "Text Files (*.txt)"
        )
        if filename:
            with open(filename, "r") as f:
                lines = [list(line.rstrip()) for line in f.readlines()]

                for row in range(len(lines)):
                    for col in range(len(lines[0])):
                        self.grid[row][col] = lines[row][col]

        self.update()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = LevelEditor()
    sys.excepthook = except_hook
    sys.exit(app.exec())
