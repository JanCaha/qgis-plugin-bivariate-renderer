from __future__ import annotations
from typing import List, Dict
from dataclasses import dataclass

from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtXml import QDomDocument, QDomElement

from qgis.core import (QgsFeatureRenderer, QgsClassificationRange, QgsFeature, QgsColorRamp,
                       QgsFillSymbol, QgsSymbolLayerUtils, QgsVectorLayer, QgsClassificationMethod,
                       QgsClassificationEqualInterval)

from ..text_constants import Texts
from ..colormixing.color_mixing_methods_register import ColorMixingMethodsRegister
from ..colormixing.color_mixing_method import ColorMixingMethod, ColorMixingMethodDarken


class BivariateRenderer(QgsFeatureRenderer):

    number_classes: int
    color_ramp_1: QgsColorRamp
    color_ramp_2: QgsColorRamp
    field_name_1: str
    field_name_2: str
    field_1_classes: List[QgsClassificationRange]
    field_2_classes: List[QgsClassificationRange]

    color_mixing_method: ColorMixingMethod
    classification_method: QgsClassificationMethod

    def __init__(self, syms=None):

        super().__init__(Texts.bivariate_renderer_short_name)

        self.number_classes = 3

        self.color_mixing_method = ColorMixingMethodDarken()

        self.classification_method = QgsClassificationEqualInterval()

        self.field_name_1 = None
        self.field_name_2 = None

        self.color_ramp_1 = None
        self.color_ramp_2 = None

        self.cached = {}

    def __repr__(self) -> str:
        return f"BivariateRenderer with {self.number_classes} classes for each attribute, " \
               f"for fields {self.field_name_1} and {self.field_name_2}, " \
               f"with classification method {self.classification_method.name()}," \
               f"field 1 vals {self.field_1_min};{self.field_1_max} " \
               f"field 2 vals {self.field_2_min};{self.field_2_max} "

    def _reset_cache(self):
        self.cached = {}

    def setColorMixingMethod(self, method: ColorMixingMethod) -> None:
        self.color_mixing_method = method
        self._reset_cache()

    def setClassificationMethod(self, method: QgsClassificationMethod) -> None:
        self.classification_method = method
        self._reset_cache()

    def setNumberOfClasses(self, number: int) -> None:
        self.number_classes = int(number)
        self._reset_cache()

    def setColorRamp1(self, color_ramp: QgsColorRamp) -> None:
        self.color_ramp_1 = color_ramp
        self._reset_cache()

    def setColorRamp2(self, color_ramp: QgsColorRamp) -> None:
        self.color_ramp_2 = color_ramp
        self._reset_cache()

    def setFieldName1(self, field_name: str) -> None:
        self.field_name_1 = field_name
        self._reset_cache()

    def setFieldName2(self, field_name: str) -> None:
        self.field_name_2 = field_name
        self._reset_cache()

    def classes_to_legend_breaks(self, classes: List[QgsClassificationRange]) -> List[float]:

        values = []

        for i, interval_class in enumerate(classes):

            if i == 0:

                values.append(interval_class.lowerBound())

            values.append(interval_class.upperBound())

        return values

    def setField1ClassificationData(self, layer: QgsVectorLayer, attribute: str) -> None:
        self.field_1_classes = self.classification_method.classes(layer, attribute,
                                                                  self.number_classes)

        self._reset_cache()

    def setField2ClassificationData(self, layer: QgsVectorLayer, attribute: str) -> None:
        self.field_2_classes = self.classification_method.classes(layer, attribute,
                                                                  self.number_classes)

        self._reset_cache()

    def positionValueField1(self, value: float) -> float:

        class_value1 = None

        for range_class in self.field_1_classes:

            if range_class.lowerBound() <= value <= range_class.upperBound():
                class_value1 = (range_class.lowerBound() + range_class.upperBound()) / 2

        position_value1 = (class_value1 - self.field_1_min) / (self.field_1_max - self.field_1_min)

        return position_value1

    def positionValueField2(self, value: float) -> float:

        class_value2 = None

        for range_class in self.field_2_classes:

            if range_class.lowerBound() <= value <= range_class.upperBound():
                class_value2 = (range_class.lowerBound() + range_class.upperBound()) / 2

        position_value2 = (class_value2 - self.field_2_min) / (self.field_2_max - self.field_2_min)

        return position_value2

    def getFeatureValueCombinationHash(self, value1: float, value2: float) -> int:
        return hash(f"{value1}-{value2}")

    def getFeatureColor(self, value1: float, value2: float) -> QColor:

        position_value1 = self.positionValueField1(value1)
        position_value2 = self.positionValueField2(value2)

        color1 = self.color_ramp_1.color(position_value1)
        color2 = self.color_ramp_2.color(position_value2)

        result_color = self.color_mixing_method.mix_colors(color1, color2)

        return result_color

    def symbolForFeature(self, feature: QgsFeature, context):

        value1 = feature.attribute(self.field_name_1)
        value2 = feature.attribute(self.field_name_2)

        identifier = self.getFeatureValueCombinationHash(value1, value2)

        if identifier not in self.cached:
            feature_symbol = self.get_default_symbol()
            feature_symbol.setColor(self.getFeatureColor(value1, value2))

            self.cached[identifier] = feature_symbol.clone()

        self.cached[identifier].startRender(context)

        return self.cached[identifier]

    def startRender(self, context, fields):
        super().startRender(context, fields)

    def stopRender(self, context):
        for s in list(self.cached.values()):
            s.stopRender(context)
        super().stopRender(context)

    def usedAttributes(self, context):
        return [self.field_name_1, self.field_name_2]

    def symbols(self, context):
        return list(self.cached.values())

    def clone(self) -> QgsFeatureRenderer:
        r = BivariateRenderer()
        r.setFieldName1(self.field_name_1)
        r.setFieldName2(self.field_name_2)
        r.classification_method = self.classification_method.clone()
        r.setNumberOfClasses(self.number_classes)
        r.setColorRamp1(self.color_ramp_1.clone())
        r.setColorRamp2(self.color_ramp_2.clone())
        r.field_1_classes = self.field_1_classes
        r.field_2_classes = self.field_2_classes
        r.setColorMixingMethod(self.color_mixing_method)
        r._reset_cache()

        return r

    def save(self, doc: QDomDocument, context):

        renderer_elem = doc.createElement("renderer-v2")

        renderer_elem.setAttribute('type', Texts.bivariate_renderer_short_name)

        number_classes_elem = doc.createElement('number_of_classes')
        number_classes_elem.setAttribute("value", str(self.number_classes))
        renderer_elem.appendChild(number_classes_elem)

        classification_method_elem = self.classification_method.save(doc, context)
        renderer_elem.appendChild(classification_method_elem)

        field_1_elem = doc.createElement('field_name_1')
        field_1_elem.setAttribute("name", self.field_name_1)
        renderer_elem.appendChild(field_1_elem)

        field_2_elem = doc.createElement('field_name_2')
        field_2_elem.setAttribute("name", self.field_name_2)
        renderer_elem.appendChild(field_2_elem)

        color_ramp_elem = QgsSymbolLayerUtils.saveColorRamp("color_ramp_1", self.color_ramp_1, doc)
        renderer_elem.appendChild(color_ramp_elem)

        color_ramp_elem = QgsSymbolLayerUtils.saveColorRamp("color_ramp_2", self.color_ramp_2, doc)
        renderer_elem.appendChild(color_ramp_elem)

        ranges_elem1 = doc.createElement("ranges_1")

        for class_range in self.field_1_classes:
            range_elem = doc.createElement("range_1")

            range_elem.setAttribute("lower", str(class_range.lowerBound()))
            range_elem.setAttribute("upper", str(class_range.upperBound()))
            range_elem.setAttribute("label", class_range.label())

            ranges_elem1.appendChild(range_elem)

        renderer_elem.appendChild(ranges_elem1)

        ranges_elem2 = doc.createElement("ranges_2")

        for class_range in self.field_2_classes:
            range_elem = doc.createElement("range_2")

            range_elem.setAttribute("lower", str(class_range.lowerBound()))
            range_elem.setAttribute("upper", str(class_range.upperBound()))
            range_elem.setAttribute("label", class_range.label())

            ranges_elem2.appendChild(range_elem)

        renderer_elem.appendChild(ranges_elem2)

        color_mixing_method_elem = doc.createElement('color_mixing_method')
        color_mixing_method_elem.setAttribute("name", self.color_mixing_method.name())
        renderer_elem.appendChild(color_mixing_method_elem)

        return renderer_elem

    @staticmethod
    def create_render_from_element(element: QDomElement, context) -> BivariateRenderer:

        r = BivariateRenderer()

        r.setFieldName1(element.firstChildElement("field_name_1").attribute("name"))
        r.setFieldName2(element.firstChildElement("field_name_2").attribute("name"))
        element.firstChildElement("number_of_classes").attributes().item(0)
        r.setNumberOfClasses(int(
            element.firstChildElement("number_of_classes").attribute("value")))

        method_elem = element.firstChildElement("classificationMethod")
        r.setClassificationMethod(QgsClassificationMethod.create(method_elem, context))

        color_ramp_1_elem = element.firstChildElement("colorramp")
        r.setColorRamp1(QgsSymbolLayerUtils.loadColorRamp(color_ramp_1_elem))

        color_ramp_2_elem = element.lastChildElement("colorramp")
        r.setColorRamp2(QgsSymbolLayerUtils.loadColorRamp(color_ramp_2_elem))

        ranges_field_1 = element.firstChildElement("ranges_1")

        field_1_classes = []

        range_elem = ranges_field_1.firstChildElement()

        while not range_elem.isNull():

            if range_elem.tagName() == "range_1":
                lower_value = float(range_elem.attribute("lower"))
                upper_value = float(range_elem.attribute("upper"))
                label = range_elem.attribute("label")

                field_1_classes.append(QgsClassificationRange(label, lower_value, upper_value))

            range_elem = range_elem.nextSiblingElement()

        ranges_field_2 = element.firstChildElement("ranges_2")

        field_2_classes = []

        range_elem = ranges_field_2.firstChildElement()

        while not range_elem.isNull():

            if range_elem.tagName() == "range_2":
                lower_value = float(range_elem.attribute("lower"))
                upper_value = float(range_elem.attribute("upper"))
                label = range_elem.attribute("label")

                field_2_classes.append(QgsClassificationRange(label, lower_value, upper_value))

            range_elem = range_elem.nextSiblingElement()

        r.field_1_classes = field_1_classes
        r.field_2_classes = field_2_classes

        r.setColorMixingMethod(ColorMixingMethodsRegister().get_by_name(
            element.firstChildElement("color_mixing_method").attribute("name")))

        return r

    def load(self, symbology_elem: QDomElement, context):
        return self.create_render_from_element(symbology_elem, context)

    @staticmethod
    def get_default_symbol():

        symbol = QgsFillSymbol.createSimple({
            "color": "#cccccc",
            "outline_width": "0.0",
            "outline_color": "0,0,0",
            'outline_style': 'no'
        })

        return symbol

    def get_symbol_for_values(self, value1: float, value2: float) -> QgsFillSymbol:

        return self.symbol_for_values(value1, value2)

    def symbol_for_values(self, value1: float, value2: float) -> QgsFillSymbol:

        identifier = self.getFeatureValueCombinationHash(value1, value2)

        if identifier not in self.cached:
            feature_symbol = self.get_default_symbol()
            feature_symbol.setColor(self.getFeatureColor(value1, value2))

            self.cached[identifier] = feature_symbol.clone()

        return self.cached[identifier]

    def legend_polygon_size(self, width: float) -> float:

        size_constant = width / self.number_classes

        return size_constant

    def generate_legend_polygons(self) -> List[LegendPolygon]:

        polygons = []

        x = 0
        for field_1_cat in self.field_1_classes:

            y = 0
            for field_2_cat in self.field_2_classes:

                polygons.append(
                    LegendPolygon(x=x,
                                  y=y,
                                  symbol=self.get_symbol_for_values(
                                      (field_1_cat.lowerBound() + field_1_cat.upperBound()) / 2,
                                      (field_2_cat.lowerBound() + field_2_cat.upperBound()) / 2)))
                y += 1
            x += 1

        return polygons

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, BivariateRenderer):
            return False

        else:
            if (self.field_name_1 == other.field_name_1 and
                    self.field_name_2 == other.field_name_2 and
                    self.number_classes == other.number_classes and
                    # self.classification_method.id() == other.classification_method.id() and
                    self.field_1_min == other.field_1_min and
                    self.field_1_max == other.field_1_max and
                    self.field_2_min == other.field_2_min and
                    self.field_2_max == other.field_2_max and
                    self.color_ramp_1.properties() == other.color_ramp_1.properties() and
                    self.color_ramp_2.properties() == other.color_ramp_2.properties()):
                return True

            else:
                return False

    @property
    def field_2_min(self) -> float:
        return (self.field_2_classes[0].lowerBound() + self.field_2_classes[0].upperBound()) / 2

    @property
    def field_2_max(self) -> float:
        return (self.field_2_classes[len(self.field_2_classes) - 1].lowerBound() +
                self.field_2_classes[len(self.field_2_classes) - 1].upperBound()) / 2

    @property
    def field_2_labels(self) -> List[float]:
        return self.classes_to_legend_breaks(self.field_2_classes)

    @property
    def field_1_min(self) -> float:
        return (self.field_1_classes[0].lowerBound() + self.field_1_classes[0].upperBound()) / 2

    @property
    def field_1_max(self) -> float:
        return (self.field_1_classes[len(self.field_1_classes) - 1].lowerBound() +
                self.field_1_classes[len(self.field_1_classes) - 1].upperBound()) / 2

    @property
    def field_1_labels(self) -> List[float]:
        return self.classes_to_legend_breaks(self.field_1_classes)


@dataclass
class LegendPolygon:

    x: float
    y: float
    symbol: QgsFillSymbol
