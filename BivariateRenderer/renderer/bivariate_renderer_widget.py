from typing import NoReturn

from qgis.PyQt.QtGui import (QImage,
                             QColor,
                             QPainter,
                             QPixmap)

from qgis.PyQt.QtWidgets import (QLabel,
                                 QFormLayout,
                                 QLabel,
                                 QComboBox,
                                 QPushButton)

from qgis.gui import (QgsRendererWidget,
                      QgsColorRampButton,
                      QgsFieldComboBox,
                      QgsDoubleSpinBox)

from qgis.core import (QgsGradientColorRamp,
                       QgsClassificationMethod,
                       QgsClassificationJenks,
                       QgsClassificationEqualInterval,
                       QgsClassificationQuantile,
                       QgsClassificationPrettyBreaks,
                       QgsClassificationLogarithmic,
                       QgsFieldProxyModel,
                       QgsRenderContext,
                       QgsTextFormat,
                       QgsLineSymbol)


from .bivariate_renderer import BivariateRenderer
from ..legendrenderer.legend_renderer import LegendRenderer

from ..utils import (log)

from ..text_constants import Texts


class BivariateRendererWidget(QgsRendererWidget):

    # objects
    classification_method: QgsClassificationMethod
    color_ramp_1: QgsGradientColorRamp
    color_ramp_2: QgsGradientColorRamp
    number_of_classes: int
    field_name_1: str
    field_name_2: str

    default_color_ramp_1 = QgsGradientColorRamp(QColor(255, 255, 255),
                                                QColor(255, 0, 0))

    default_color_ramp_2 = QgsGradientColorRamp(QColor(255, 255, 255),
                                                QColor(0, 0, 255))

    bivariate_renderer: BivariateRenderer

    classification_methods = {QgsClassificationEqualInterval().name(): QgsClassificationEqualInterval(),
                              QgsClassificationJenks().name(): QgsClassificationJenks(),
                              QgsClassificationQuantile().name(): QgsClassificationQuantile(),
                              QgsClassificationPrettyBreaks().name(): QgsClassificationPrettyBreaks(),
                              QgsClassificationLogarithmic().name(): QgsClassificationLogarithmic()}

    def __init__(self, layer, style, renderer: BivariateRenderer):

        super().__init__(layer, style)

        if renderer is None or renderer.type() != Texts.bivariate_renderer_short_name:
            self.bivariate_renderer = BivariateRenderer()
        else:
            self.bivariate_renderer = renderer.clone()

        # objects
        self.classification_method = QgsClassificationEqualInterval()
        self.number_of_classes = self.bivariate_renderer.number_classes
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
        self.sb_number_classes.setValue(self.number_of_classes)

        self.cb_classification_methods = QComboBox()
        self.cb_classification_methods.addItems(list(self.classification_methods.keys()))
        self.cb_classification_methods.currentIndexChanged.connect(self.setClassificationMethod)

        if self.bivariate_renderer.classification_method_name:
            self.cb_classification_methods.setCurrentText(self.bivariate_renderer.classification_method_name)
        else:
            self.cb_classification_methods.setCurrentIndex(1)
            self.cb_classification_methods.setCurrentIndex(0)

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

        svg_path = path_to_legend_svg()
        write_text_to_file(svg_path, "")
        self.svg_pixmap = QIcon(svg_path.absolute().as_posix()).pixmap(QtCore.QSize(200, 200))

        self.svg_label = QLabel()
        self.svg_label.setPixmap(self.svg_pixmap)

        self.pb_render_legend = QPushButton("Render Legend")
        self.pb_render_legend.pressed.connect(self.updateLegend)

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Select number of classes:", self.sb_number_classes)
        self.form_layout.addRow("Select classification method:", self.cb_classification_methods)
        self.form_layout.addRow("Select field 1:", self.cb_field1)
        self.form_layout.addRow("Select color ramp 1:", self.bt_color_ramp1)
        self.form_layout.addRow("Select field 2:", self.cb_field2)
        self.form_layout.addRow("Select color ramp 2:", self.bt_color_ramp2)
        self.form_layout.addRow("", self.pb_render_legend)
        self.form_layout.addRow("Example of legend:", self.svg_label)
        self.setLayout(self.form_layout)

        # log(self.bivariate_renderer.getLegendCategories())

    def updateLegend(self):
        self.renderLegend()
        self.loadSVG()

    def renderLegend(self):
        self.bivariate_renderer.renderLegend()

    def loadSVG(self):
        svg_path = path_to_legend_svg()

        self.svg_pixmap = QIcon(svg_path.absolute().as_posix()).pixmap(QtCore.QSize(200, 200))

        self.svg_label.clear()
        self.svg_label.setPixmap(self.svg_pixmap)
        self.svg_label.repaint()

    def setNumberOfClasses(self) -> NoReturn:

        self.number_of_classes = int(self.sb_number_classes.value())

        self.bivariate_renderer.setNumberOfClasses(
            int(self.sb_number_classes.value())
        )

        self.setField1Classes()
        self.setField2Classes()

    def setClassificationMethod(self) -> NoReturn:

        self.classification_method = self.classification_methods[self.cb_classification_methods.currentText()]

        self.bivariate_renderer.setClassificationMethodName(self.cb_classification_methods.currentText())

        self.setField1Classes()
        self.setField2Classes()

    def setColorRamp1(self) -> NoReturn:

        self.bivariate_renderer.setColorRamp1(
            self.bt_color_ramp1.colorRamp()
        )

    def setColorRamp2(self) -> NoReturn:

        self.bivariate_renderer.setColorRamp2(
            self.bt_color_ramp2.colorRamp()
        )

    def setFieldName1(self) -> NoReturn:

        self.field_name_1 = self.cb_field1.currentText()

        self.bivariate_renderer.setFieldName1(
            self.cb_field1.currentText()
        )

        self.setField1Classes()

    def setFieldName2(self) -> NoReturn:

        self.field_name_2 = self.cb_field2.currentText()

        self.bivariate_renderer.setFieldName2(
            self.cb_field2.currentText()
        )

        self.setField2Classes()

    def setField1Classes(self):

        self.bivariate_renderer.setField1Classes(
            self.classification_method.classes(self.vectorLayer(),
                                               self.field_name_1,
                                               self.number_of_classes)
        )

    def setField2Classes(self):

        self.bivariate_renderer.setField2Classes(
            self.classification_method.classes(self.vectorLayer(),
                                               self.field_name_2,
                                               self.number_of_classes)
        )

    def log_renderer(self):

        log(repr(self.bivariate_renderer))

    def renderer(self):
        return self.bivariate_renderer
