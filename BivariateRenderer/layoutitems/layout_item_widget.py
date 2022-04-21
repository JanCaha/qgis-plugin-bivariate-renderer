from pathlib import Path

from qgis.PyQt.QtWidgets import (QComboBox, QPushButton, QVBoxLayout, QLabel, QCheckBox,
                                 QPlainTextEdit)

from qgis.PyQt.QtGui import QIcon

from qgis.core import (QgsLayoutItem, QgsProject, QgsVectorLayer, QgsMapLayer, QgsMapLayerType,
                       QgsSymbol)

from qgis.gui import (QgsLayoutItemBaseWidget, QgsLayoutItemAbstractGuiMetadata, QgsFontButton,
                      QgsSymbolButton, QgsCollapsibleGroupBoxBasic)

from ..text_constants import Texts, IDS
from ..utils import log, get_symbol_dict
from .layout_item import BivariateRendererLayoutItem


class BivariateRendererLayoutItemWidget(QgsLayoutItemBaseWidget):

    pb_update_legend: QPushButton
    axis_x_name: QPlainTextEdit
    axis_y_name: QPlainTextEdit
    rotate_legend: QCheckBox
    add_arrows: QCheckBox
    add_axes_values_text: QCheckBox
    rotate_direction: QComboBox

    layout_item: BivariateRendererLayoutItem

    def __init__(self, parent, layout_object: QgsLayoutItem):

        super().__init__(parent, layout_object)

        self.layout_item = layout_object

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

        self.form_layout = QVBoxLayout()

        self.form_layout.addWidget(QLabel("Select layer to obtain the renderer from"))
        self.form_layout.addWidget(self.cb_layers)

        self.form_layout.addWidget(self.widget_rotate())

        self.form_layout.addWidget(self.widget_arrow_axes())

        self.form_layout.addWidget(self.widget_text_axes())

        self.form_layout.addWidget(self.widget_text_ticks())

        self.form_layout.addWidget(self.widget_rotate_y_axis_texts())

        self.setLayout(self.form_layout)

    def widget_rotate_y_axis_texts(self) -> QgsCollapsibleGroupBoxBasic:

        cg_rotate = QgsCollapsibleGroupBoxBasic('Rotate Y Axis')
        cg_rotate_layout = QVBoxLayout()

        self.rotate_direction = QComboBox()
        self.rotate_direction.addItem("Counterclockwise")
        self.rotate_direction.addItem("Clockwise")
        self.rotate_direction.currentIndexChanged.connect(self.update_y_axis_rotation)
        self.rotate_direction.setCurrentIndex(0)

        if self.layout_item.y_axis_rotation == -90:
            self.rotate_direction.setCurrentIndex(1)
        else:
            self.rotate_direction.setCurrentIndex(0)

        cg_rotate_layout.addWidget(QLabel("Rotate Y axis in direction"))
        cg_rotate_layout.addWidget(self.rotate_direction)

        cg_rotate.setLayout(cg_rotate_layout)

        return cg_rotate

    def update_y_axis_rotation(self) -> None:

        value = self.rotate_direction.currentText()

        if value == "Counterclockwise":

            self.layout_item.set_y_axis_rotation(90)

        elif value == "Clockwise":

            self.layout_item.set_y_axis_rotation(-90)

        else:
            self.layout_item.set_y_axis_rotation(90)

    def widget_rotate(self) -> QgsCollapsibleGroupBoxBasic:

        cg_rotate = QgsCollapsibleGroupBoxBasic('Rotate Legend')
        cg_rotate_layout = QVBoxLayout()

        self.rotate_legend = QCheckBox("Rotate")
        self.rotate_legend.setChecked(self.layout_item.legend_rotated)
        self.rotate_legend.stateChanged.connect(self.update_rotate_legend)

        cg_rotate_layout.addWidget(QLabel("Rotate legend by 45 degrees"))
        cg_rotate_layout.addWidget(self.rotate_legend)

        cg_rotate.setLayout(cg_rotate_layout)

        return cg_rotate

    def widget_arrow_axes(self) -> QgsCollapsibleGroupBoxBasic:

        cg_axes_arrows = QgsCollapsibleGroupBoxBasic('Axes Arrows')
        cg_axes_arrows_layout = QVBoxLayout()

        self.add_arrows = QCheckBox("Add axis arrows")
        self.add_arrows.setChecked(self.layout_item.add_axes_arrows)
        self.add_arrows.stateChanged.connect(self.update_add_axes_arrow)

        self.b_line_symbol = QgsSymbolButton(self, "Arrow")
        self.b_line_symbol.setSymbolType(QgsSymbol.Line)
        self.b_line_symbol.setMinimumWidth(50)
        self.b_line_symbol.changed.connect(self.pass_linesymbol)

        if self.layout_item.line_format:
            self.b_line_symbol.setSymbol(self.layout_item.line_format)

        cg_axes_arrows_layout.addWidget(QLabel("Use axis arrows in legend"))
        cg_axes_arrows_layout.addWidget(self.add_arrows)
        cg_axes_arrows_layout.addWidget(QLabel("Arrow style"))
        cg_axes_arrows_layout.addWidget(self.b_line_symbol)

        cg_axes_arrows.setLayout(cg_axes_arrows_layout)

        return cg_axes_arrows

    def widget_text_axes(self) -> QgsCollapsibleGroupBoxBasic:

        cg_axes_descriptions = QgsCollapsibleGroupBoxBasic('Axes Descritions')
        cg_axes_descriptions_layout = QVBoxLayout()

        self.b_font = QgsFontButton()
        self.b_font.setTextFormat(self.layout_item.text_format)
        self.b_font.changed.connect(self.pass_textformat_to_item)

        self.add_axes_text = QCheckBox("Add axes texts")
        self.add_axes_text.setChecked(self.layout_item.add_axes_texts)
        self.add_axes_text.stateChanged.connect(self.update_add_axes_text)

        self.axis_x_name = QPlainTextEdit()

        if self.layout_item.text_axis_x:
            self.axis_x_name.setPlainText(self.layout_item.text_axis_x)

        self.axis_x_name.textChanged.connect(self.update_axis_x)

        self.axis_y_name = QPlainTextEdit()

        if self.layout_item.text_axis_y:
            self.axis_y_name.setPlainText(self.layout_item.text_axis_y)

        self.axis_y_name.textChanged.connect(self.update_axis_y)

        cg_axes_descriptions_layout.addWidget(QLabel("Use axes texts in legend"))
        cg_axes_descriptions_layout.addWidget(self.add_axes_text)
        cg_axes_descriptions_layout.addWidget(QLabel("Font"))
        cg_axes_descriptions_layout.addWidget(self.b_font)
        cg_axes_descriptions_layout.addWidget(QLabel("Axis X name"))
        cg_axes_descriptions_layout.addWidget(self.axis_x_name)
        cg_axes_descriptions_layout.addWidget(QLabel("Axis Y name"))
        cg_axes_descriptions_layout.addWidget(self.axis_y_name)

        cg_axes_descriptions.setLayout(cg_axes_descriptions_layout)

        return cg_axes_descriptions

    def widget_text_ticks(self) -> QgsCollapsibleGroupBoxBasic:

        cg_axes_value_descriptions = QgsCollapsibleGroupBoxBasic('Axes Numerical Values')
        cg_axes_descriptions_layout = QVBoxLayout()

        self.b_font_values = QgsFontButton()
        self.b_font_values.setTextFormat(self.layout_item.text_values_format)
        self.b_font_values.changed.connect(self.pass_textformat_values_to_item)

        self.add_axes_values_text = QCheckBox("Add numerical values")
        self.add_axes_values_text.setChecked(self.layout_item.add_axes_values_texts)
        self.add_axes_values_text.stateChanged.connect(self.update_add_axes_values_text)

        cg_axes_descriptions_layout.addWidget(QLabel("Use axes values texts in legend"))
        cg_axes_descriptions_layout.addWidget(self.add_axes_values_text)
        cg_axes_descriptions_layout.addWidget(QLabel("Font"))
        cg_axes_descriptions_layout.addWidget(self.b_font_values)

        cg_axes_value_descriptions.setLayout(cg_axes_descriptions_layout)

        return cg_axes_value_descriptions

    def pass_linesymbol(self):

        self.layout_item.beginCommand(self.tr('Change line symbol'),
                                      QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_line_format(self.b_line_symbol.symbol().clone())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

    def pass_textformat_to_item(self):

        self.layout_item.beginCommand(self.tr('Change text format'),
                                      QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_text_format(self.b_font.textFormat())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

    def pass_textformat_values_to_item(self):

        self.layout_item.beginCommand(self.tr('Change text values format'),
                                      QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_text_values_format(self.b_font_values.textFormat())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

    def update_axis_x(self):

        self.layout_item.beginCommand(self.tr('Change change x axis name'),
                                      QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_axis_x_name(self.axis_x_name.toPlainText())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

    def update_axis_y(self):

        self.layout_item.beginCommand(self.tr('Change change y axis name'),
                                      QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_axis_y_name(self.axis_y_name.toPlainText())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

    def update_rotate_legend(self):

        self.layout_item.beginCommand(self.tr('Change rotated legend'),
                                      QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_legend_rotated(self.rotate_legend.isChecked())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

        if self.rotate_legend.isChecked():
            self.rotate_direction.setEnabled(False)
        else:
            self.rotate_direction.setEnabled(True)

    def update_add_axes_text(self):

        self.layout_item.beginCommand(self.tr('Add axes text'), QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_draw_axes_text(self.add_axes_text.isChecked())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

    def update_add_axes_values_text(self):

        self.layout_item.beginCommand(self.tr('Add axes text'), QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_draw_axes_values(self.add_axes_values_text.isChecked())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

    def update_add_axes_arrow(self):

        self.layout_item.beginCommand(self.tr('Add axes arrow'), QgsLayoutItem.UndoCustomCommand)

        self.layout_item.blockSignals(True)
        self.layout_item.set_draw_axes_arrow(self.add_arrows.isChecked())
        self.layout_item.blockSignals(False)
        self.layout_item.endCommand()

    def update_layer_to_work_with(self):

        if self.cb_layers.currentText() != "":

            for layer_id in self.layers.keys():

                layer: QgsVectorLayer = self.layers[layer_id]

                if layer.name() == self.cb_layers.currentText():

                    self.layout_item.beginCommand(self.tr('Change linked layer'),
                                                  QgsLayoutItem.UndoCustomCommand)

                    self.layout_item.blockSignals(True)
                    self.layout_item.set_linked_layer(layer)
                    self.layout_item.blockSignals(False)
                    self.layout_item.endCommand()
                    break

        if self.layout_item.are_labels_default():

            self.axis_x_name.setPlainText(self.layout_item.renderer.field_name_1)
            self.axis_y_name.setPlainText(self.layout_item.renderer.field_name_2)

    def type(self):
        return IDS.plot_item_bivariate_renderer_legend


class BivariateRendererLayoutItemGuiMetadata(QgsLayoutItemAbstractGuiMetadata):
    """
    Metadata for plot item GUI classes
    """

    def __init__(self):
        super().__init__(IDS.plot_item_bivariate_renderer_legend,
                         Texts.plot_item_bivariate_renderer)

    def createItemWidget(self, item: QgsLayoutItem):  # pylint: disable=missing-docstring, no-self-use
        return BivariateRendererLayoutItemWidget(None, item)

    def creationIcon(self) -> QIcon:
        path = Path(__file__).parent.parent / "icons" / "legend_icon.png"
        return QIcon(path.absolute().as_posix())
