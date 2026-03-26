import Metashape
from PySide2 import QtWidgets, QtCore, QtGui
import json
import os

# --- WINDOW 1: Facies Configuration ---
class FaciesSetupWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facies Configuration")
        self.setFixedSize(450, 400)
        self.facies_data = {}

        self.layout = QtWidgets.QVBoxLayout()

        self.facies_list = QtWidgets.QListWidget()
        self.layout.addWidget(self.facies_list)

        form_layout = QtWidgets.QHBoxLayout()
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Facies name")
        form_layout.addWidget(self.name_input)

        self.color_button = QtWidgets.QPushButton("Pick color")
        self.color_button.clicked.connect(self.select_color)
        self.selected_color = QtGui.QColor(200, 200, 200)
        form_layout.addWidget(self.color_button)
        self.layout.addLayout(form_layout)

        # Botones: Añadir, Guardar, Cargar
        button_layout1 = QtWidgets.QHBoxLayout()

        self.add_button = QtWidgets.QPushButton("➕ Add facies")
        self.add_button.clicked.connect(self.add_facies)
        button_layout1.addWidget(self.add_button)

        self.save_button = QtWidgets.QPushButton("💾 Save")
        self.save_button.clicked.connect(self.save_facies)
        button_layout1.addWidget(self.save_button)

        self.load_button = QtWidgets.QPushButton("📂 Load")
        self.load_button.clicked.connect(self.load_facies)
        button_layout1.addWidget(self.load_button)

        self.layout.addLayout(button_layout1)

        # Botón para continuar
        button_layout2 = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("▶ Start interpretation")
        self.start_button.clicked.connect(self.accept)
        button_layout2.addWidget(self.start_button)

        self.layout.addLayout(button_layout2)
        self.setLayout(self.layout)

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.color_button.setStyleSheet("background-color: {}".format(color.name()))

    def add_facies(self):
        name = self.name_input.text().strip()
        if not name:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a facies name.")
            return
        rgb = self.selected_color.getRgb()[:3]
        self.facies_data[name] = rgb
        self.facies_list.addItem("{} - RGB{}".format(name, rgb))
        self.name_input.clear()

    def save_facies(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save facies configuration", "", "JSON Files (*.json)")[0]
        if path:
            with open(path, 'w') as f:
                json.dump(self.facies_data, f, indent=4)
            QtWidgets.QMessageBox.information(self, "Saved", "Facies saved to:\n{}".format(path))

    def load_facies(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Load facies configuration", "", "JSON Files (*.json)")[0]
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                self.facies_data = json.load(f)
            self.facies_list.clear()
            for name, rgb in self.facies_data.items():
                self.facies_list.addItem("{} - RGB{}".format(name, tuple(rgb)))
            QtWidgets.QMessageBox.information(self, "Loaded", "Facies loaded from:\n{}".format(path))

    def get_facies_dict(self):
        return self.facies_data


# --- WINDOW 2: Apply Facies to the 3D Model ---
class FaciesTool(QtWidgets.QWidget):
    def __init__(self, chunk, model, colores_facies):
        super().__init__()
        self.setWindowTitle("Apply facies to model")
        self.setFixedSize(300, 150)
        self.chunk = chunk
        self.model = model
        self.colores_facies = colores_facies
        self.facies_dict = {}

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Select a facies:")
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(colores_facies.keys())

        self.btn_apply = QtWidgets.QPushButton("Apply facies to selection")
        self.btn_apply.clicked.connect(self.asignar_facies)

        self.btn_close = QtWidgets.QPushButton("Close")
        self.btn_close.clicked.connect(self.close)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.btn_apply)
        layout.addWidget(self.btn_close)
        self.setLayout(layout)

    def asignar_facies(self):
        nombre_facies = self.combo.currentText()
        selected_vertices_indices = set()

        for face in self.model.faces:
            if face.selected:
                for v_index in face.vertices:
                    selected_vertices_indices.add(v_index)
                face.selected = False

        if not selected_vertices_indices:
            Metashape.app.messageBox("⚠️ No faces selected.")
            return

        self.facies_dict[nombre_facies] = self.facies_dict.get(nombre_facies, set()).union(selected_vertices_indices)

        color_actual = self.colores_facies[nombre_facies]
        for index in selected_vertices_indices:
            if 0 <= index < len(self.model.vertices):
                self.model.vertices[index].color = color_actual

        print("✔️ Facies '{}' applied to {} vertices.".format(nombre_facies, len(selected_vertices_indices)))
        print("🔄 View updated.")


# --- EJECUCIÓN DEL FLUJO COMPLETO ---
try:
    doc = Metashape.app.document
    chunk = doc.chunk

    if not chunk or not chunk.model:
        Metashape.app.messageBox("No model found in the active chunk.")
        exit()

    dlg = FaciesSetupWindow()
    if dlg.exec_() == QtWidgets.QDialog.Accepted:
        colores_facies = dlg.get_facies_dict()

        tool_window = FaciesTool(chunk, chunk.model, colores_facies)
        tool_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        tool_window.show()
    else:
        print("❌ Facies configuration cancelled by user.")

except Exception as e:
    Metashape.app.messageBox("Error: {}".format(e))
