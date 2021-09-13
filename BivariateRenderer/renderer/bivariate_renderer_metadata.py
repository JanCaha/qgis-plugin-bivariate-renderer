from qgis.core import (QgsRendererAbstractMetadata,
                       QgsSymbolLayerUtils
                       )

from PyQt5.QtXml import QDomElement

from .bivariate_renderer import BivariateRenderer
from .bivariate_renderer_widget import BivariateRendererWidget
from BivariateRenderer.text_constants import Texts


class BivariateRendererMetadata(QgsRendererAbstractMetadata):

    def __init__(self):
        super().__init__(Texts.bivariate_renderer_short_name, Texts.bivariate_renderer_full_name)

    def name(self) -> str:
        return Texts.bivariate_renderer_short_name

    def visibleName(self):
        return Texts.bivariate_renderer_full_name

    def createRenderer(self, element: QDomElement, context):

        r = BivariateRenderer()

        r.setFieldName1(element.attribute("field_name_1"))
        r.setFieldName2(element.attribute("field_name_2"))

        r.setNumberOfClasses(element.attribute("number_of_classes"))
        r.setClassificationMethodName(element.attribute("classification_method_name "))

        r.setLimitValues(float(element.attribute("field_1_min")), float(element.attribute("field_1_max")),
                         float(element.attribute("field_2_min")), float(element.attribute("field_2_max")))

        color_ramp_1_elem = element.firstChildElement("colorramp")
        r.setColorRamp1(QgsSymbolLayerUtils.loadColorRamp(color_ramp_1_elem))

        color_ramp_2_elem = element.lastChildElement("colorramp")
        r.setColorRamp2(QgsSymbolLayerUtils.loadColorRamp(color_ramp_2_elem))

        r.setField1Classes(BivariateRenderer.string_2_class_ranges(element.attribute("field_1_classes")))
        r.setField2Classes(BivariateRenderer.string_2_class_ranges(element.attribute("field_2_classes")))

        return r

    def createRendererWidget(self, layer, style, renderer):
        return BivariateRendererWidget(layer, style, renderer)

    def compatibleLayerTypes(self):
        return QgsRendererAbstractMetadata.PolygonLayer
