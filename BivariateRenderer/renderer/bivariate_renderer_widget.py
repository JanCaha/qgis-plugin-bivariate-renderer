from qgis.PyQt.QtGui import (QImage, QColor, QPainter, QPixmap)

from qgis.PyQt.QtWidgets import (QFormLayout, QLabel, QComboBox)

from qgis.PyQt.QtCore import pyqtSignal

from qgis.gui import (QgsRendererWidget, QgsColorRampButton, QgsFieldComboBox, QgsDoubleSpinBox)

from qgis.core import (QgsGradientColorRamp, QgsClassificationJenks,
                       QgsClassificationEqualInterval, QgsClassificationQuantile,
                       QgsClassificationPrettyBreaks, QgsClassificationLogarithmic,
                       QgsFieldProxyModel, QgsRenderContext)

from .bivariate_renderer import BivariateRenderer
from ..legendrenderer.legend_renderer import LegendRenderer
from ..colormixing.color_mixing_methods_register import ColorMixingMethodsRegister
from ..colorramps.color_ramps_register import BivariateColorRampsRegister

from ..utils import (log)

from ..text_constants import Texts


class BivariateRendererWidget(QgsRendererWidget):

    # objects
    color_ramp_1: QgsGradientColorRamp
    color_ramp_2: QgsGradientColorRamp
    field_name_1: str
    field_name_2: str

    register_color_mixing = ColorMixingMethodsRegister()

    register_color_ramps = BivariateColorRampsRegister()

    default_color_ramp_1 = QgsGradientColorRamp(QColor(255, 255, 255), QColor(255, 0, 0))

    default_color_ramp_2 = QgsGradientColorRamp(QColor(255, 255, 255), QColor(0, 0, 255))

    bivariate_renderer: BivariateRenderer

    legend_renderer: LegendRenderer

    classification_methods = {
        QgsClassificationEqualInterval().name(): QgsClassificationEqualInterval(),
        QgsClassificationJenks().name(): QgsClassificationJenks(),
        QgsClassificationQuantile().name(): QgsClassificationQuantile(),
        QgsClassificationPrettyBreaks().name(): QgsClassificationPrettyBreaks(),
        QgsClassificationLogarithmic().name(): QgsClassificationLogarithmic()
    }

    scale_factor = 1

    legend_changed = pyqtSignal()

    def __init__(self, layer, style, renderer: BivariateRenderer):

        super().__init__(layer, style)

        if renderer is None or renderer.type() != Texts.bivariate_renderer_short_name:
            self.bivariate_renderer = BivariateRenderer()
        else:
            self.bivariate_renderer = renderer.clone()

        self.legend_renderer = LegendRenderer()

        self.legend_size = self.size().width() / 3
        self.text_ticks_size = self.legend_size / 5

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
        self.sb_number_classes.valueChanged.connect(self.setNumberOfClasses)
        self.sb_number_classes.setValue(self.bivariate_renderer.number_classes)

        self.cb_classification_methods = QComboBox()
        self.cb_classification_methods.addItems(list(self.classification_methods.keys()))
        self.cb_classification_methods.currentIndexChanged.connect(self.setClassificationMethod)

        if self.bivariate_renderer.classification_method:

            if self.bivariate_renderer.classification_method.name() in list(
                    self.classification_methods.keys()):

                index = list(self.classification_methods.keys()).\
                    index(self.bivariate_renderer.classification_method.name())

            else:

                index = 0

            self.cb_classification_methods.setCurrentIndex(index)

        else:
            self.cb_classification_methods.setCurrentIndex(1)
            self.cb_classification_methods.setCurrentIndex(0)

        self.cb_colormixing_methods = QComboBox()
        self.cb_colormixing_methods.addItems(self.register_color_mixing.names)
        self.cb_colormixing_methods.currentIndexChanged.connect(self.setColorMixingMethod)

        if self.bivariate_renderer.color_mixing_method:
            self.cb_colormixing_methods.setCurrentText(
                self.bivariate_renderer.color_mixing_method.name())
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
        self.bt_color_ramp1.colorRampChanged.connect(self.setColorRamp1)

        if self.bivariate_renderer.color_ramp_1:
            self.bt_color_ramp1.setColorRamp(self.bivariate_renderer.color_ramp_1)
        else:
            self.bt_color_ramp1.setColorRamp(self.default_color_ramp_1)

        self.bt_color_ramp2 = QgsColorRampButton()
        self.bt_color_ramp2.colorRampChanged.connect(self.setColorRamp2)

        if self.bivariate_renderer.color_ramp_2:
            self.bt_color_ramp2.setColorRamp(self.bivariate_renderer.color_ramp_2)
        else:
            self.bt_color_ramp2.setColorRamp(self.default_color_ramp_2)

        self.label_legend = QLabel()

        self.legend_changed.connect(self.update_legend)

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Color ramps", self.cb_color_ramps)
        self.form_layout.addRow("Number of classes", self.sb_number_classes)
        self.form_layout.addRow(
            QLabel(
                "Data are categorized using Equal Interval classification\nmethod into provided number of categories for both fields."
            ))
        # self.form_layout.addRow("Select classification method:", self.cb_classification_methods)
        self.form_layout.addRow("Color mixing method", self.cb_colormixing_methods)
        self.form_layout.addRow("Field 1", self.cb_field1)
        self.form_layout.addRow("Color Ramp 1", self.bt_color_ramp1)
        self.form_layout.addRow("Field 2", self.cb_field2)
        self.form_layout.addRow("Color Ramp 2", self.bt_color_ramp2)
        self.form_layout.addRow("Legend", self.label_legend)
        self.setLayout(self.form_layout)

        self.update_legend()

    def update_legend(self):

        self.label_legend.clear()

        image = QImage(int(self.legend_size), int(self.legend_size), QImage.Format_ARGB32)
        image.fill(QColor(0, 0, 0, 0))

        painter = QPainter(image)

        context = QgsRenderContext.fromQPainter(painter)
        context.setScaleFactor(self.scale_factor)

        self.legend_renderer.add_axes_ticks_texts = True

        self.legend_renderer.texts_axis_x_ticks = self.bivariate_renderer.field_1_labels
        self.legend_renderer.texts_axis_y_ticks = self.bivariate_renderer.field_2_labels

        self.legend_renderer.text_format_ticks.setSize(self.text_ticks_size)

        self.legend_renderer._text_rotation_y = -90

        self.legend_renderer._space_above_ticks = self.text_ticks_size / 10

        self.legend_renderer.render(context, self.legend_size, self.legend_size,
                                    self.bivariate_renderer.generate_legend_polygons())

        painter.end()

        self.label_legend.setPixmap(QPixmap.fromImage(image))

    def setNumberOfClasses(self) -> None:

        self.bivariate_renderer.setNumberOfClasses(int(self.sb_number_classes.value()))

        self.setField1Classes()
        self.setField2Classes()

        self.legend_changed.emit()

    def setColorMixingMethod(self) -> None:

        self.bivariate_renderer.setColorMixingMethod(
            self.register_color_mixing.get_by_name(self.cb_colormixing_methods.currentText()))

        self.legend_changed.emit()

    def setClassificationMethod(self) -> None:

        classification_method = self.classification_methods[
            self.cb_classification_methods.currentText()]

        self.bivariate_renderer.setClassificationMethodName(classification_method)

        self.setField1Classes()
        self.setField2Classes()

        self.legend_changed.emit()

    def setColorRamp1(self) -> None:

        self.bivariate_renderer.setColorRamp1(self.bt_color_ramp1.colorRamp())

        self.legend_changed.emit()

    def setColorRamp2(self) -> None:

        self.bivariate_renderer.setColorRamp2(self.bt_color_ramp2.colorRamp())

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
            self.bt_color_ramp1.setColorRamp(bivariate_color_ramp.color_ramp_1)
            self.bt_color_ramp2.setColorRamp(bivariate_color_ramp.color_ramp_2)
