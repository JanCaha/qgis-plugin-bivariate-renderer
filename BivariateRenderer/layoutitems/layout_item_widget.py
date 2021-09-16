from PyQt5.QtWidgets import QFormLayout, QComboBox, QPushButton, QLineEdit, QVBoxLayout, QLabel

from qgis.core import (QgsLayoutItem,
                       QgsProject,
                       QgsVectorLayer,
                       QgsMapLayer,
                       QgsMapLayerType,
                       QgsLayoutItemPolyline,
                       QgsSymbol,
                       QgsTextFormat)

from qgis.gui import (QgsLayoutItemBaseWidget,
                      QgsLayoutItemPropertiesWidget,
                      QgsLayoutItemAbstractGuiMetadata,
                      QgsDoubleSpinBox,
                      QgsFontButton,
                      QgsSymbolButton)

from ..renderer.bivariate_renderer import BivariateRenderer
from ..text_constants import Texts, IDS
from ..utils import log
from .layout_item import BivariateRendererLayoutItem


class BivariateRendererLayoutItemWidget(QgsLayoutItemBaseWidget):

    pb_update_legend: QPushButton
    axis_x_name: QLineEdit
    axis_y_name: QLineEdit

    layout_item: BivariateRendererLayoutItem

    def __init__(self, parent, layout_object: QgsLayoutItem):

        super().__init__(parent, layout_object)

        self.layout_item = layout_object

        self.b_font = QgsFontButton()
        log(self.layout_item.get_font.pointSize())
        self.b_font.setTextFormat(QgsTextFormat.fromQFont(self.layout_item.get_font))
        self.b_font.changed.connect(self.pass_font_to_item)

        self.b_line_symbol = QgsSymbolButton(self, "Arrows")
        self.b_line_symbol.setSymbolType(QgsSymbol.Line)
        self.b_line_symbol.setMinimumWidth(50)

        self.layers = QgsProject.instance().mapLayers()

        usable_layers = []

        for layer_id in self.layers.keys():

            layer: QgsMapLayer = self.layers[layer_id]

            if layer.type() == QgsMapLayerType.VectorLayer:

                layer: QgsVectorLayer

                if layer.renderer().type() == Texts.bivariate_renderer_short_name:
                    usable_layers.append(layer.name())

        self.cb_layers = QComboBox()
        self.cb_layers.addItem("")
        self.cb_layers.addItems(usable_layers)
        self.cb_layers.currentIndexChanged.connect(self.update_layer_to_work_with)
        self.cb_layers.setCurrentIndex(0)

        if self.layout_item.linked_layer_name:
            self.cb_layers.setCurrentText(self.layout_item.linked_layer_name)

        self.pb_update_legend = QPushButton("Render Legend")
        self.pb_update_legend.pressed.connect(self.update_item)

        self.axis_x_name = QLineEdit()
        if self.layout_item.text_axis_x.text():
            self.axis_x_name.setText(self.layout_item.text_axis_x.text())
        self.axis_x_name.textChanged.connect(self.update_axis_x)
        self.axis_y_name = QLineEdit()
        if self.layout_item.text_axis_y.text():
            self.axis_y_name.setText(self.layout_item.text_axis_y.text())
        self.axis_y_name.textChanged.connect(self.update_axis_y)

        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(QLabel("Select layer to obtainthe renderer from"))
        self.form_layout.addWidget(self.cb_layers)
        self.form_layout.addWidget(QLabel("Update legend"))
        self.form_layout.addWidget(self.pb_update_legend)
        self.form_layout.addWidget(QLabel("Font"))
        self.form_layout.addWidget(self.b_font)
        self.form_layout.addWidget(QLabel("Arrow"))
        self.form_layout.addWidget(self.b_line_symbol)
        self.form_layout.addWidget(QLabel("Axis X name"))
        self.form_layout.addWidget(self.axis_x_name)
        self.form_layout.addWidget(QLabel("Axis Y name"))
        self.form_layout.addWidget(self.axis_y_name)
        # self.form_layout.addRow("Select layer to obtain\nthe renderer from:", self.cb_layers)
        # self.form_layout.addRow("Update legend:", self.pb_update_legend)
        # self.form_layout.addRow("Font:", self.b_font)
        # self.form_layout.addRow("Arrow:", self.b_line_symbol)
        # self.form_layout.addRow("Axis X name:", self.axis_x_name)
        # self.form_layout.addRow("Axis Y name:", self.axis_y_name)
        self.setLayout(self.form_layout)

    def pass_font_to_item(self):
        self.layout_item.set_font(self.b_font.textFormat().toQFont())

    def update_axis_x(self, text: str):
        self.layout_item.set_axis_x_name(text)

    def update_axis_y(self, text: str):
        self.layout_item.set_axis_y_name(text)

    def update_item(self):
        # if self.render:
        #     self.render.render_legend_to_temp()
        #     self.layout_item.setPicturePath(self.render.temp_folder_legend_file)

        # self.layout_item.build_element()
        pass

    def update_layer_to_work_with(self):

        if self.cb_layers.currentText() != "":

            for layer_id in self.layers.keys():

                layer: QgsVectorLayer = self.layers[layer_id]

                if layer.name() == self.cb_layers.currentText():

                    self.layout_item.set_linked_layer(layer)
                    break

    def type(self):
        return IDS.plot_item_bivariate_renderer_legend


class BivariateRendererLayoutItemGuiMetadata(QgsLayoutItemAbstractGuiMetadata):
    """
    Metadata for plot item GUI classes
    """

    def __init__(self):
        super().__init__(IDS.plot_item_bivariate_renderer_legend, Texts.plot_item_bivariate_renderer)

    def createItemWidget(self, item: QgsLayoutItem):  # pylint: disable=missing-docstring, no-self-use
        return BivariateRendererLayoutItemWidget(None, item)

