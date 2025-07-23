from qgis.core import (
    Qgis,
    QgsClassificationEqualInterval,
    QgsClassificationJenks,
    QgsClassificationLogarithmic,
    QgsClassificationPrettyBreaks,
    QgsClassificationQuantile,
    QgsFieldProxyModel,
    QgsRenderContext,
    QgsSymbol,
)
from qgis.gui import QgsColorRampButton, QgsDoubleSpinBox, QgsFieldComboBox, QgsRendererWidget, QgsSymbolButton
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor, QImage, QPainter, QPixmap
from qgis.PyQt.QtWidgets import QComboBox, QFormLayout, QLabel, QMessageBox

from ..colormixing.color_mixing_methods_register import ColorMixingMethodsRegister
from ..colorramps.bivariate_color_ramp import BivariateColorRampGradient
from ..colorramps.color_ramps_register import BivariateColorRampsRegister
from ..legendrenderer.legend_renderer import LegendRenderer
from ..text_constants import Texts
from ..utils import default_fill_symbol, log
from .bivariate_renderer import BivariateRenderer


class BivariateRendererWidget(QgsRendererWidget):

    # objects
    field_name_1: str
    field_name_2: str

    register_color_mixing = ColorMixingMethodsRegister()

    register_color_ramps = BivariateColorRampsRegister()

    default_color_ramp_1 = register_color_ramps.get_by_name("Violet - Blue").color_ramp_1
    default_color_ramp_2 = register_color_ramps.get_by_name("Violet - Blue").color_ramp_2

    bivariate_color_ramp = BivariateColorRampGradient(9)
    bivariate_color_ramp.set_color_ramp_1(default_color_ramp_1)
    bivariate_color_ramp.set_color_ramp_2(default_color_ramp_2)

    bivariate_renderer: BivariateRenderer

    legend_renderer: LegendRenderer

    classification_methods = {
        QgsClassificationEqualInterval().name(): QgsClassificationEqualInterval(),
        QgsClassificationJenks().name(): QgsClassificationJenks(),
        QgsClassificationQuantile().name(): QgsClassificationQuantile(),
        QgsClassificationPrettyBreaks().name(): QgsClassificationPrettyBreaks(),
        QgsClassificationLogarithmic().name(): QgsClassificationLogarithmic(),
    }

    scale_factor = 1

    legend_changed = pyqtSignal()

    base_symbol: QgsSymbol = default_fill_symbol()

    def __init__(self, layer, style, renderer: BivariateRenderer):

        super().__init__(layer, style)

        if renderer is None or renderer.type() != Texts.bivariate_renderer_short_name:
            self.bivariate_renderer = BivariateRenderer()
        else:
            self.bivariate_renderer = renderer.clone()
            self.bivariate_renderer.generateCategories()
            self.bivariate_color_ramp = self.bivariate_renderer.bivariate_color_ramp

        self.legend_renderer = LegendRenderer()

        self.calculate_legend_sizes()

        # objects
        self.field_name_1 = None
        self.field_name_2 = None

        # setup UI

        fields = layer.fields()

        self.field_name_1 = fields.field(0).name()
        self.field_name_2 = fields.field(0).name()

        self.cb_field1 = QgsFieldComboBox()
        self.cb_field1.setFields(fields)
        self.cb_field1.setFilters(QgsFieldProxyModel.Numeric)
        self.cb_field1.currentIndexChanged.connect(self.setFieldName1)

        if self.bivariate_renderer.field_name_1:
            self.cb_field1.setField(self.bivariate_renderer.field_name_1)
            self.field_name_1 = self.bivariate_renderer.field_name_1
        else:
            self.cb_field1.setCurrentIndex(1)
            self.cb_field1.setCurrentIndex(0)

        self.cb_field2 = QgsFieldComboBox()
        self.cb_field2.setFields(layer.fields())
        self.cb_field2.setFilters(QgsFieldProxyModel.Numeric)
        self.cb_field2.currentIndexChanged.connect(self.setFieldName2)

        if self.bivariate_renderer.field_name_2:
            self.cb_field2.setField(self.bivariate_renderer.field_name_2)
            self.field_name_2 = self.bivariate_renderer.field_name_2
        else:
            self.cb_field2.setCurrentIndex(1)
            self.cb_field2.setCurrentIndex(0)

        self.sb_number_classes = QgsDoubleSpinBox()
        self.sb_number_classes.setDecimals(0)
        self.sb_number_classes.setMinimum(2)
        self.sb_number_classes.setMaximum(5)
        self.sb_number_classes.setSingleStep(1)
        self.sb_number_classes.setValue(self.bivariate_renderer.bivariate_color_ramp.number_of_classes)

        self.cb_classification_methods = QComboBox()
        self.cb_classification_methods.addItems(list(self.classification_methods.keys()))

        if self.bivariate_renderer.classification_method:

            if self.bivariate_renderer.classification_method.name() in list(self.classification_methods.keys()):

                index = list(self.classification_methods.keys()).index(
                    self.bivariate_renderer.classification_method.name()
                )

            else:

                index = 0

            self.cb_classification_methods.setCurrentIndex(index)

        else:
            self.cb_classification_methods.setCurrentIndex(1)
            self.cb_classification_methods.setCurrentIndex(0)

        self.cb_colormixing_methods = QComboBox()

        self.cb_colormixing_methods.addItems(self.register_color_mixing.names)

        if self.bivariate_renderer.bivariate_color_ramp.color_mixing_method:
            self.cb_colormixing_methods.setCurrentText(
                self.bivariate_renderer.bivariate_color_ramp.color_mixing_method.name()
            )
        else:
            self.cb_colormixing_methods.setCurrentIndex(1)

        self.cb_color_ramps = QComboBox()

        self.cb_color_ramps.addItem("")

        self.cb_color_ramps.setEditable(True)

        for color_ramp in self.register_color_ramps.color_ramps:
            index = self.cb_color_ramps.count()
            self.cb_color_ramps.addItem(color_ramp.name)
            self.cb_color_ramps.setItemIcon(index, color_ramp.icon)

        self.cb_color_ramps.setEditable(False)

        self.cb_color_ramps.currentIndexChanged.connect(self.change_color_ramps)

        self.bt_color_ramp1 = QgsColorRampButton()

        if self.bivariate_renderer.bivariate_color_ramp.color_ramp_1:
            self.bt_color_ramp1.setColorRamp(self.bivariate_renderer.bivariate_color_ramp.color_ramp_1)
        else:
            self.bt_color_ramp1.setColorRamp(self.default_color_ramp_1)

        self.bt_color_ramp2 = QgsColorRampButton()

        if self.bivariate_renderer.bivariate_color_ramp.color_ramp_2:
            self.bt_color_ramp2.setColorRamp(self.bivariate_renderer.bivariate_color_ramp.color_ramp_2)
        else:
            self.bt_color_ramp2.setColorRamp(self.default_color_ramp_2)

        self.label_legend = QLabel()

        self.legend_changed.connect(self.update_legend)

        self.rotate_color_palette = QComboBox()
        self.rotate_color_palette.addItem("Normal", 0)
        self.rotate_color_palette.addItem("90° clockwise", 1)
        self.rotate_color_palette.addItem("180° clockwise", 2)
        self.rotate_color_palette.addItem("270° clockwise", 3)
        self.rotate_color_palette.currentIndexChanged.connect(self.rotate_palette)

        self.symbol_selector = QgsSymbolButton(self, "Main symbol selection")
        self.symbol_selector.setMinimumWidth(200)
        self.base_symbol = self.bivariate_renderer.polygon_symbol
        self.symbol_selector.setSymbol(self.base_symbol.clone())
        self.symbol_selector.changed.connect(self.update_base_symbol)

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Default Symbol", self.symbol_selector)
        self.form_layout.addRow("Color ramps", self.cb_color_ramps)
        self.form_layout.addRow("Number of classes", self.sb_number_classes)
        self.form_layout.addRow(
            QLabel(
                "Data are categorized using Equal Interval classification\nmethod into provided number of categories for both fields."
            )
        )
        # self.form_layout.addRow("Select classification method:", self.cb_classification_methods)
        self.form_layout.addRow("Color mixing method", self.cb_colormixing_methods)
        self.form_layout.addRow("Field 1", self.cb_field1)
        self.form_layout.addRow("Color Ramp 1", self.bt_color_ramp1)
        self.form_layout.addRow("Field 2", self.cb_field2)
        self.form_layout.addRow("Color Ramp 2", self.bt_color_ramp2)
        self.form_layout.addRow("Rotate color palette", self.rotate_color_palette)
        self.form_layout.addRow("Legend", self.label_legend)
        self.setLayout(self.form_layout)

        self.sb_number_classes.valueChanged.connect(self.update_bivariate_color_ramp)
        self.cb_classification_methods.currentIndexChanged.connect(self.update_bivariate_color_ramp)
        self.bt_color_ramp1.colorRampChanged.connect(self.update_bivariate_color_ramp)
        self.bt_color_ramp2.colorRampChanged.connect(self.update_bivariate_color_ramp)
        self.cb_colormixing_methods.currentIndexChanged.connect(self.update_bivariate_color_ramp)
        self.symbol_selector.changed.connect(self.update_bivariate_color_ramp)

        self.update_bivariate_color_ramp()

        self.update_legend()

    def rotate_palette(self):
        index = self.rotate_color_palette.currentIndex()
        rotation = self.rotate_color_palette.itemData(index, Qt.UserRole)

        if rotation == 0:
            pass
        elif rotation == 1:
            cr1 = self.bt_color_ramp1.colorRamp()
            cr2 = self.bt_color_ramp2.colorRamp()
            cr1.invert()
            self.bt_color_ramp1.setColorRamp(cr2)
            self.bt_color_ramp2.setColorRamp(cr1)
        elif rotation == 2:
            cr1 = self.bt_color_ramp1.colorRamp()
            cr2 = self.bt_color_ramp2.colorRamp()
            cr1.invert()
            cr2.invert()
            self.bt_color_ramp1.setColorRamp(cr1)
            self.bt_color_ramp2.setColorRamp(cr2)
        elif rotation == 3:
            cr1 = self.bt_color_ramp1.colorRamp()
            cr2 = self.bt_color_ramp2.colorRamp()
            cr2.invert()
            self.bt_color_ramp1.setColorRamp(cr2)
            self.bt_color_ramp2.setColorRamp(cr1)

        self.rotate_color_palette.blockSignals(True)
        self.rotate_color_palette.setCurrentIndex(0)
        self.rotate_color_palette.blockSignals(False)

    def calculate_legend_sizes(self) -> None:
        self.legend_size = int(self.size().width() / 3)
        self.text_ticks_size = self.legend_size / 5

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.calculate_legend_sizes()
        self.update_legend()

    def update_legend(self):

        self.label_legend.clear()

        image = QImage(self.legend_size, self.legend_size, QImage.Format_ARGB32)
        image.fill(QColor(0, 0, 0, 0))

        painter = QPainter(image)

        context = QgsRenderContext.fromQPainter(painter)
        context.setScaleFactor(self.scale_factor)

        self.legend_renderer.add_axes_ticks_texts = True

        self.legend_renderer.texts_axis_x_ticks = self.bivariate_renderer.field_1_labels
        self.legend_renderer.texts_axis_y_ticks = self.bivariate_renderer.field_2_labels

        self.legend_renderer.text_format_ticks.setSize(self.text_ticks_size)

        self.legend_renderer._text_rotation_y = -90

        self.legend_renderer.set_space_above_ticks(self.text_ticks_size / 2)

        self.legend_renderer.render(
            context, self.legend_size, self.legend_size, self.bivariate_renderer.generate_legend_polygons()
        )

        painter.end()

        self.label_legend.setPixmap(QPixmap.fromImage(image))

    def update_bivariate_color_ramp(self) -> None:
        self.bivariate_color_ramp.set_number_of_classes(int(self.sb_number_classes.value()))

        self.bivariate_color_ramp.set_color_mixing_method(
            self.register_color_mixing.get_by_name(self.cb_colormixing_methods.currentText())
        )

        self.bivariate_color_ramp.set_color_ramp_1(self.bt_color_ramp1.colorRamp())
        self.bivariate_color_ramp.set_color_ramp_2(self.bt_color_ramp2.colorRamp())

        self.bivariate_renderer.set_bivariate_color_ramp(self.bivariate_color_ramp)

        classification_method = self.classification_methods[self.cb_classification_methods.currentText()]

        self.bivariate_renderer.setClassificationMethod(classification_method)

        self.setField1Classes()
        self.setField2Classes()

        self.bivariate_renderer.polygon_symbol = self.base_symbol

        self.legend_changed.emit()

    def setFieldName1(self) -> None:

        self.field_name_1 = self.cb_field1.currentText()

        self.bivariate_renderer.setFieldName1(self.cb_field1.currentText())

        self.setField1Classes()

        self.legend_changed.emit()

    def setFieldName2(self) -> None:

        self.field_name_2 = self.cb_field2.currentText()

        self.bivariate_renderer.setFieldName2(self.cb_field2.currentText())

        self.setField2Classes()

        self.legend_changed.emit()

    def setField1Classes(self) -> None:

        self.bivariate_renderer.setField1ClassificationData(self.vectorLayer(), self.field_name_1)

    def setField2Classes(self) -> None:

        self.bivariate_renderer.setField2ClassificationData(self.vectorLayer(), self.field_name_2)

    def log_renderer(self) -> None:

        log(repr(self.bivariate_renderer))

    def renderer(self) -> BivariateRenderer:
        return self.bivariate_renderer

    def change_color_ramps(self) -> None:
        name = self.cb_color_ramps.currentText()

        if name != "":
            bivariate_color_ramp = self.register_color_ramps.get_by_name(name)
            self.bivariate_color_ramp = bivariate_color_ramp
            self.bivariate_renderer.set_bivariate_color_ramp(bivariate_color_ramp)

            self.bt_color_ramp1.blockSignals(True)
            self.bt_color_ramp2.blockSignals(True)
            self.bt_color_ramp1.setColorRamp(bivariate_color_ramp.color_ramp_1)
            self.bt_color_ramp2.setColorRamp(bivariate_color_ramp.color_ramp_2)
            self.bt_color_ramp1.blockSignals(False)
            self.bt_color_ramp2.blockSignals(False)

            self.legend_changed.emit()

    def update_base_symbol(self):
        symbol = self.symbol_selector.symbol().clone()
        types = all([x.layerType() == "SimpleFill" for x in symbol.symbolLayers()])
        if symbol.symbolLayerCount() > 1 or types is False:
            QMessageBox.warning(
                self,
                "Incorrect symbol definition",
                "For Bivariate Renderer, the symbol must have exactly one fill symbol layer. More complex symbols are not supported.\n\n"
                "This should only be used for the border of the polygons definition.",
            )
            self.symbol_selector.setSymbol(self.base_symbol.clone())
        else:
            self.base_symbol = symbol
