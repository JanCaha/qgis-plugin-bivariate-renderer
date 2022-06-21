from qgis.PyQt.QtWidgets import (QComboBox, QVBoxLayout, QLabel, QCheckBox, QPlainTextEdit,
                                 QSpinBox, QDoubleSpinBox)

from qgis.PyQt.QtGui import QIcon

from qgis.core import (QgsLayoutItem, QgsProject, QgsVectorLayer, QgsMapLayer, QgsMapLayerType,
                       Qgis)

from qgis.gui import (QgsLayoutItemBaseWidget, QgsLayoutItemAbstractGuiMetadata, QgsFontButton,
                      QgsSymbolButton, QgsCollapsibleGroupBoxBasic, QgsColorButton)

from ..text_constants import Texts, IDS
from ..utils import log, get_symbol_dict, get_icon
from .layout_item import BivariateRendererLayoutItem


class BivariateRendererLayoutItemWidget(QgsLayoutItemBaseWidget):

    cb_layers: QComboBox

    axis_x_name: QPlainTextEdit
    axis_y_name: QPlainTextEdit
    rotate_legend: QCheckBox
    add_arrows: QCheckBox
    add_axes_values_text: QCheckBox
    rotate_direction: QComboBox

    ticks_precision_x: QSpinBox
    ticks_precision_y: QSpinBox
    space_above_ticks: QSpinBox

    b_line_symbol: QgsSymbolButton
    b_font: QgsFontButton
    b_font_values: QgsFontButton

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

                if layer.renderer():
                    if layer.renderer().type() == Texts.bivariate_renderer_short_name:
                        usable_layers.append(layer.name())

        self.cb_layers = QComboBox()
        self.cb_layers.addItem("")
        self.cb_layers.addItems(usable_layers)

        if self.layout_item.linked_layer_name:
            self.cb_layers.setCurrentText(self.layout_item.linked_layer_name)

        self.form_layout = QVBoxLayout()

        self.form_layout.addWidget(QLabel("Select layer to obtain the renderer from"))
        self.form_layout.addWidget(self.cb_layers)

        self.form_layout.addWidget(self.widget_rotate())

        self.form_layout.addWidget(self.widget_spacer())

        self.form_layout.addWidget(self.widget_arrow_axes())

        self.form_layout.addWidget(self.widget_text_axes())

        self.form_layout.addWidget(self.widget_text_ticks())

        self.form_layout.addWidget(self.widget_rotate_y_axis_texts())

        self.form_layout.addWidget(self.widget_non_existing_symbols())

        self.setLayout(self.form_layout)

        self.cb_layers.currentIndexChanged.connect(self.update_layer_to_work_with)

        if 0 < len(usable_layers):
            self.cb_layers.setCurrentIndex(1)

    def widget_rotate_y_axis_texts(self) -> QgsCollapsibleGroupBoxBasic:

        cg_rotate = QgsCollapsibleGroupBoxBasic('Rotate Y Axis')
        cg_rotate_layout = QVBoxLayout()

        self.rotate_direction = QComboBox()
        self.rotate_direction.addItem("Counterclockwise", 90)
        self.rotate_direction.addItem("Clockwise", -90)
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

        index = self.rotate_direction.currentIndex()

        self.layout_item.set_y_axis_rotation(self.rotate_direction.itemData(index))

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

    def widget_non_existing_symbols(self) -> QgsCollapsibleGroupBoxBasic:

        cg_nonexisting_symbol = QgsCollapsibleGroupBoxBasic('Symbol that do not exist in values')
        cg_nonexisting_symbol_layout = QVBoxLayout()

        self.replace_empty_symbols = QCheckBox("Replace symbols without values")
        self.replace_empty_symbols.setChecked(self.layout_item.replace_rectangle_without_values)
        self.replace_empty_symbols.stateChanged.connect(
            self.pass_rectangle_without_values_settings)

        self.empty_symbol = QgsSymbolButton()
        self.empty_symbol.setMinimumWidth(50)
        self.empty_symbol.setMaximumWidth(150)
        self.empty_symbol.setSymbolType(Qgis.SymbolType.Fill)
        self.empty_symbol.setSymbol(self.layout_item.symbol_rectangle_without_values.clone())
        self.empty_symbol.changed.connect(self.pass_rectangle_without_values_settings)

        self.replace_symbol_color = QCheckBox("Replace symbol color by color from legend")
        self.replace_symbol_color.setChecked(
            self.layout_item.use_rectangle_without_values_color_from_legend)
        self.replace_symbol_color.stateChanged.connect(self.pass_rectangle_without_values_settings)

        cg_nonexisting_symbol_layout.addWidget(self.replace_empty_symbols)
        cg_nonexisting_symbol_layout.addWidget(QLabel("Replacement symbol"))
        cg_nonexisting_symbol_layout.addWidget(self.empty_symbol)
        cg_nonexisting_symbol_layout.addWidget(self.replace_symbol_color)

        cg_nonexisting_symbol.setLayout(cg_nonexisting_symbol_layout)

        return cg_nonexisting_symbol

    def widget_arrow_axes(self) -> QgsCollapsibleGroupBoxBasic:

        cg_axes_arrows = QgsCollapsibleGroupBoxBasic('Axes Arrows')
        cg_axes_arrows_layout = QVBoxLayout()

        self.add_arrows = QCheckBox("Add axis arrows")
        self.add_arrows.setChecked(self.layout_item.add_axes_arrows)
        self.add_arrows.stateChanged.connect(self.pass_arrow_settings)

        self.b_line_symbol = QgsSymbolButton(self, "Arrow")
        self.b_line_symbol.setSymbolType(Qgis.SymbolType.Line)
        self.b_line_symbol.setMinimumWidth(50)

        if self.layout_item.line_format:
            self.b_line_symbol.setSymbol(self.layout_item.line_format.clone())

        self.b_line_symbol.changed.connect(self.pass_arrow_settings)

        self.arrows_start_same_point = QCheckBox("Arrows start at common point")
        self.arrows_start_same_point.setChecked(self.layout_item.arrows_common_start_point)
        self.arrows_start_same_point.stateChanged.connect(self.pass_arrow_settings)

        self.arrow_width = QDoubleSpinBox()
        self.arrow_width.setMinimum(0.01)
        self.arrow_width.setMaximum(15.0)
        self.arrow_width.setValue(self.layout_item.arrow_width)
        self.arrow_width.setDecimals(1)
        self.arrow_width.setSuffix("%")
        self.arrow_width.valueChanged.connect(self.pass_arrow_settings)

        cg_axes_arrows_layout.addWidget(QLabel("Use axis arrows in legend"))
        cg_axes_arrows_layout.addWidget(self.add_arrows)
        cg_axes_arrows_layout.addWidget(QLabel("Arrow style"))
        cg_axes_arrows_layout.addWidget(self.b_line_symbol)
        cg_axes_arrows_layout.addWidget(QLabel("Arrow width (in % of legend)"))
        cg_axes_arrows_layout.addWidget(self.arrow_width)
        cg_axes_arrows_layout.addWidget(self.arrows_start_same_point)

        cg_axes_arrows.setLayout(cg_axes_arrows_layout)

        return cg_axes_arrows

    def widget_text_axes(self) -> QgsCollapsibleGroupBoxBasic:

        cg_axes_descriptions = QgsCollapsibleGroupBoxBasic('Axes Descriptions')
        cg_axes_descriptions_layout = QVBoxLayout()

        self.b_font = QgsFontButton()
        self.b_font.setTextFormat(self.layout_item.text_format)
        self.b_font.changed.connect(self.pass_axis_texts_settings)

        self.add_axes_text = QCheckBox("Add axes texts")
        self.add_axes_text.setChecked(self.layout_item.add_axes_texts)
        self.add_axes_text.stateChanged.connect(self.pass_axis_texts_settings)

        self.axis_x_name = QPlainTextEdit()

        if self.layout_item.text_axis_x:
            self.axis_x_name.setPlainText(self.layout_item.text_axis_x)

        self.axis_x_name.textChanged.connect(self.pass_axis_texts_settings)

        self.axis_y_name = QPlainTextEdit()

        if self.layout_item.text_axis_y:
            self.axis_y_name.setPlainText(self.layout_item.text_axis_y)

        self.axis_y_name.textChanged.connect(self.pass_axis_texts_settings)

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

        self.ticks_use_midpoint = QCheckBox("Use midpoints instead of category breaks")
        self.ticks_use_midpoint.setChecked(self.layout_item.ticks_use_category_midpoints)
        self.ticks_use_midpoint.stateChanged.connect(self.pass_use_midpoint)

        self.ticks_precision_x = QSpinBox()
        self.ticks_precision_x.setMinimum(0)
        self.ticks_precision_x.setMaximum(15)
        self.ticks_precision_x.setValue(self.layout_item.ticks_x_precision)

        self.ticks_precision_x.valueChanged.connect(self.pass_precisions)

        self.ticks_precision_y = QSpinBox()
        self.ticks_precision_y.setMinimum(0)
        self.ticks_precision_y.setMaximum(15)
        self.ticks_precision_y.setValue(self.layout_item.ticks_y_precision)

        self.ticks_precision_y.valueChanged.connect(self.pass_precisions)

        self.space_above_ticks = QSpinBox()
        self.space_above_ticks.setMinimum(0)
        self.space_above_ticks.setMaximum(100)
        self.space_above_ticks.setSuffix("px")
        self.space_above_ticks.setValue(int(self.layout_item.space_above_ticks))

        self.space_above_ticks.valueChanged.connect(self.pass_space)

        cg_axes_descriptions_layout.addWidget(QLabel("Use axes values texts in legend"))
        cg_axes_descriptions_layout.addWidget(self.add_axes_values_text)
        cg_axes_descriptions_layout.addWidget(self.ticks_use_midpoint)
        cg_axes_descriptions_layout.addWidget(QLabel("Font"))
        cg_axes_descriptions_layout.addWidget(self.b_font_values)
        cg_axes_descriptions_layout.addWidget(QLabel("Values precision on X axis"))
        cg_axes_descriptions_layout.addWidget(self.ticks_precision_x)
        cg_axes_descriptions_layout.addWidget(QLabel("Values precision on Y axis"))
        cg_axes_descriptions_layout.addWidget(self.ticks_precision_y)
        cg_axes_descriptions_layout.addWidget(QLabel("Space above value (to arrow or legend)"))
        cg_axes_descriptions_layout.addWidget(self.space_above_ticks)

        cg_axes_value_descriptions.setLayout(cg_axes_descriptions_layout)

        return cg_axes_value_descriptions

    def widget_spacer(self) -> QgsCollapsibleGroupBoxBasic:

        cg_color_separator = QgsCollapsibleGroupBoxBasic('Color separators')
        cg_color_separator_layout = QVBoxLayout()

        self.add_color_spacer = QCheckBox("Add color separators")
        self.add_color_spacer.setChecked(self.layout_item.add_colors_separators)
        self.add_color_spacer.stateChanged.connect(self.pass_color_spacer_settings)

        self.color_spacer_width = QSpinBox()
        self.color_spacer_width.setMinimum(1)
        self.color_spacer_width.setMaximum(10)
        self.color_spacer_width.setValue(self.layout_item.color_separator_width)
        self.color_spacer_width.setSuffix("%")
        self.color_spacer_width.valueChanged.connect(self.pass_color_spacer_settings)

        self.color_spacer_color = QgsColorButton()
        self.color_spacer_color.setColor(self.layout_item.color_separator_color)
        self.color_spacer_color.colorChanged.connect(self.pass_color_spacer_settings)

        cg_color_separator_layout.addWidget(QLabel("Use color separator lines in legend"))
        cg_color_separator_layout.addWidget(self.add_color_spacer)
        cg_color_separator_layout.addWidget(QLabel("Color spacer width (in % of color rectangle)"))
        cg_color_separator_layout.addWidget(self.color_spacer_width)
        cg_color_separator_layout.addWidget(QLabel("Color used to create space in legend"))
        cg_color_separator_layout.addWidget(self.color_spacer_color)

        cg_color_separator.setLayout(cg_color_separator_layout)

        return cg_color_separator

    def pass_rectangle_without_values_settings(self):

        self.layout_item.beginCommand(self.tr('Rectangle without values settings'),
                                      QgsLayoutItem.UndoCustomCommand)

        self.layout_item.set_rectangle_without_values_settings(
            self.replace_empty_symbols.isChecked(),
            self.empty_symbol.symbol().clone(), self.replace_symbol_color.isChecked())

        self.layout_item.endCommand()

    def pass_arrow_settings(self):
        self.layout_item.beginCommand(self.tr('Arrows settings'), QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_arrows_settings(self.add_arrows.isChecked(),
                                             self.b_line_symbol.symbol().clone(),
                                             self.arrows_start_same_point.isChecked(),
                                             self.arrow_width.value())
        self.layout_item.endCommand()

    def pass_color_spacer_settings(self):
        self.layout_item.beginCommand(self.tr('Change color spacer settings'),
                                      QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_color_separator_settings(self.add_color_spacer.isChecked(),
                                                      self.color_spacer_color.color(),
                                                      self.color_spacer_width.value())
        self.layout_item.endCommand()

    def pass_use_midpoint(self):
        self.layout_item.beginCommand(self.tr('Use midpoints instead of category breaks'),
                                      QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_ticks_use_category_midpoints(self.ticks_use_midpoint.isChecked())
        self.layout_item.endCommand()

    def pass_space(self):
        self.layout_item.beginCommand(self.tr('Change space above ticks'),
                                      QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_space_above_ticks(self.space_above_ticks.value())
        self.layout_item.endCommand()

    def pass_precisions(self):

        self.layout_item.beginCommand(self.tr('Change ticks precisions'),
                                      QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_ticks_precisions(self.ticks_precision_x.value(),
                                              self.ticks_precision_y.value())
        self.layout_item.endCommand()

    def pass_axis_texts_settings(self):
        self.layout_item.beginCommand(self.tr('Axis texts settings'),
                                      QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_axis_texts_settings(self.add_axes_text.isChecked(),
                                                 self.b_font.textFormat(),
                                                 self.axis_x_name.toPlainText(),
                                                 self.axis_y_name.toPlainText())
        self.layout_item.endCommand()

    def pass_textformat_values_to_item(self):
        self.layout_item.beginCommand(self.tr('Change text values format'),
                                      QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_text_values_format(self.b_font_values.textFormat())
        self.layout_item.endCommand()

    def update_rotate_legend(self):
        self.layout_item.beginCommand(self.tr('Change rotated legend'),
                                      QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_legend_rotated(self.rotate_legend.isChecked())
        self.layout_item.endCommand()

        if self.rotate_legend.isChecked():
            self.rotate_direction.setEnabled(False)
        else:
            self.rotate_direction.setEnabled(True)

    def update_add_axes_values_text(self):
        self.layout_item.beginCommand(self.tr('Add axes text'), QgsLayoutItem.UndoCustomCommand)
        self.layout_item.set_draw_axes_values(self.add_axes_values_text.isChecked())
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
        return get_icon("add_legend_icon.png")
