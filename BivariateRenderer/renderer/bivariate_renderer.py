from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from qgis.core import (
    QgsClassificationEqualInterval,
    QgsClassificationMethod,
    QgsClassificationRange,
    QgsColorRamp,
    QgsFeature,
    QgsFeatureRenderer,
    QgsFillSymbol,
    QgsLegendSymbolItem,
    QgsSymbolLayerUtils,
    QgsVectorLayer,
)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtXml import QDomDocument, QDomElement

from BivariateRenderer.colorramps.bivariate_color_ramp import (
    BivariateColorRamp,
    BivariateColorRampCyanViolet,
    BivariateColorRampGradient,
)

from ..colormixing.color_mixing_method import ColorMixingMethod
from ..text_constants import Texts


class BivariateRenderer(QgsFeatureRenderer):
    def __init__(self, syms=None):
        super().__init__(Texts.bivariate_renderer_short_name)

        self.classification_method = QgsClassificationEqualInterval()

        self.bivariate_color_ramp: BivariateColorRamp = BivariateColorRampCyanViolet()

        self.field_name_1: str = None
        self.field_name_2: str = None

        self.cached_symbols: Dict[str, QgsFillSymbol] = {}
        self.labels_existing: List[str] = []

        self.field_1_classes: List[QgsClassificationRange] = []
        self.field_2_classes: List[QgsClassificationRange] = []

    def __repr__(self) -> str:
        return (
            f"BivariateRenderer with {self.bivariate_color_ramp.number_of_classes} classes for each attribute, "
            f"for fields {self.field_name_1} and {self.field_name_2}, "
            f"with classification method {self.classification_method.name()},"
            f"field 1 vals {self.field_1_min};{self.field_1_max} "
            f"field 2 vals {self.field_2_min};{self.field_2_max} "
        )

    def _reset_cache(self):
        self.cached_symbols = {}

    def setColorMixingMethod(self, method: ColorMixingMethod) -> None:
        self.bivariate_color_ramp.set_color_mixing_method(method)
        self._reset_cache()

    def setClassificationMethod(self, method: QgsClassificationMethod) -> None:
        self.classification_method = method
        self._reset_cache()

    def setNumberOfClasses(self, number: int) -> None:
        self.bivariate_color_ramp.set_number_of_classes(int(number))
        self._reset_cache()

    def setColorRamp1(self, color_ramp: QgsColorRamp) -> None:
        self.bivariate_color_ramp.set_color_ramp_1(color_ramp)
        self._reset_cache()

    def setColorRamp2(self, color_ramp: QgsColorRamp) -> None:
        self.bivariate_color_ramp.set_color_ramp_2(color_ramp)
        self._reset_cache()

    def setFieldName1(self, field_name: str) -> None:
        self.field_name_1 = field_name
        self._reset_cache()

    def setFieldName2(self, field_name: str) -> None:
        self.field_name_2 = field_name
        self._reset_cache()

    @staticmethod
    def classes_to_legend_breaks(classes: List[QgsClassificationRange]) -> List[float]:
        values = []

        for i, interval_class in enumerate(classes):
            if i == 0:
                values.append(interval_class.lowerBound())

            values.append(interval_class.upperBound())

        return values

    @staticmethod
    def classes_to_legend_midpoints(classes: List[QgsClassificationRange]) -> List[float]:
        values = []

        for interval_class in classes:
            values.append((interval_class.lowerBound() + interval_class.upperBound()) / 2)

        return values

    def setField1ClassificationData(self, layer: QgsVectorLayer, attribute: str) -> None:
        self.field_1_classes = self.classification_method.classes(
            layer, attribute, self.bivariate_color_ramp.number_of_classes
        )

        self._reset_cache()

    def setField2ClassificationData(self, layer: QgsVectorLayer, attribute: str) -> None:
        self.field_2_classes = self.classification_method.classes(
            layer, attribute, self.bivariate_color_ramp.number_of_classes
        )

        self._reset_cache()

    def _positionValue(self, value: float, classes: List[QgsClassificationRange]) -> int:
        for i, range_class in enumerate(classes):
            if range_class.lowerBound() <= value <= range_class.upperBound():
                class_value = i

        return class_value

    def positionValueField1(self, value: float) -> int:
        return self._positionValue(value, self.field_1_classes)

    def positionValueField2(self, value: float) -> int:
        return self._positionValue(value, self.field_2_classes)

    def getFeatureCombinationHash(self, feature: QgsFeature) -> str:
        position_value1, position_value2 = self.position_values(feature)
        return self.getPositionValuesCombinationHash(position_value1, position_value2)

    def getPositionValuesCombinationHash(self, value1: int, value2: int) -> str:
        return f"{value1 + 1}-{value2 + 1}"

    def getFeatureColor(self, position_value1: int, position_value2: int) -> QColor:
        return self.bivariate_color_ramp.get_color(position_value1, position_value2)

    def position_values(self, feature: QgsFeature) -> Tuple[int, int]:
        value1 = feature.attribute(self.field_name_1)
        value2 = feature.attribute(self.field_name_2)

        position_value1 = self.positionValueField1(value1)
        position_value2 = self.positionValueField2(value2)

        return (position_value1, position_value2)

    def symbolForFeature(self, feature: QgsFeature, context):
        position_value1, position_value2 = self.position_values(feature)

        identifier = self.getPositionValuesCombinationHash(position_value1, position_value2)

        if identifier not in self.cached_symbols:
            feature_symbol = self.get_default_symbol()
            feature_symbol.setColor(self.getFeatureColor(position_value1, position_value2))

            self.cached_symbols[identifier] = feature_symbol.clone()
            self.labels_existing.append(identifier)

        self.cached_symbols[identifier].startRender(context)

        return self.cached_symbols[identifier]

    def startRender(self, context, fields):
        super().startRender(context, fields)

    def stopRender(self, context):
        for s in list(self.cached_symbols.values()):
            s.stopRender(context)
        super().stopRender(context)

    def usedAttributes(self, context):
        return [self.field_name_1, self.field_name_2]

    def symbols(self, context):
        return list(self.cached_symbols.values())

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
        r.cached_symbols = self.cached_symbols
        r.labels_existing = self.labels_existing

        return r

    def save(self, doc: QDomDocument, context):
        renderer_elem = doc.createElement("renderer-v2")

        renderer_elem.setAttribute("type", Texts.bivariate_renderer_short_name)

        classification_method_elem = self.classification_method.save(doc, context)
        renderer_elem.appendChild(classification_method_elem)

        field_1_elem = doc.createElement("field_name_1")
        field_1_elem.setAttribute("name", self.field_name_1)
        renderer_elem.appendChild(field_1_elem)

        field_2_elem = doc.createElement("field_name_2")
        field_2_elem.setAttribute("name", self.field_name_2)
        renderer_elem.appendChild(field_2_elem)

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

        symbols_elem = doc.createElement("symbols")

        for symbol in self.cached_symbols.keys():
            symbol_elem = doc.createElement("symbol")
            symbol_elem.setAttribute("color", self.cached_symbols[symbol].color().name())
            symbol_elem.setAttribute("label", symbol)
            symbols_elem.appendChild(symbol_elem)

        renderer_elem.appendChild(symbols_elem)

        number_classes_elem = doc.createElement("existing_labels")
        labels = ""
        if self.existing_labels():
            labels = "|".join(self.labels_existing)
        number_classes_elem.setAttribute("value", labels)
        renderer_elem.appendChild(number_classes_elem)

        renderer_elem.appendChild(self.bivariate_color_ramp.save(doc))

        return renderer_elem

    @staticmethod
    def create_render_from_element(element: QDomElement, context) -> BivariateRenderer:
        r = BivariateRenderer()

        r.setFieldName1(element.firstChildElement("field_name_1").attribute("name"))
        r.setFieldName2(element.firstChildElement("field_name_2").attribute("name"))

        method_elem = element.firstChildElement("classificationMethod")
        r.setClassificationMethod(QgsClassificationMethod.create(method_elem, context))

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

        symbols_elem = element.firstChildElement("symbols")

        symbol_elem = symbols_elem.firstChildElement()

        while not symbol_elem.isNull():
            if symbol_elem.tagName() == "symbol":
                color = QColor(symbol_elem.attribute("color"))
                label = symbol_elem.attribute("label")

                symbol = BivariateRenderer.get_default_symbol()
                symbol.setColor(color)

                r.cached_symbols[label] = symbol

            symbol_elem = symbol_elem.nextSiblingElement()

        labels_value = element.firstChildElement("existing_labels").attribute("value")
        labels = []
        if labels_value != "":
            labels = labels_value.split("|")

        r.labels_existing = labels

        bivariate_ramp_elem = element.firstChild("BivariateColorRamp")
        bivariate_ramp = None
        if not bivariate_ramp_elem.isNull():
            bivariate_ramp_type = bivariate_ramp_elem.attribute("type")
            if bivariate_ramp_type == "Gradient":
                bivariate_ramp = BivariateColorRampGradient.load(bivariate_ramp_elem)

        if bivariate_ramp:
            r.bivariate_color_ramp = bivariate_ramp

        return r

    def load(self, symbology_elem: QDomElement, context):
        return self.create_render_from_element(symbology_elem, context)

    @staticmethod
    def get_default_symbol() -> QgsFillSymbol:
        symbol = QgsFillSymbol.createSimple(
            {"color": "#cccccc", "outline_width": "0.0", "outline_color": "0,0,0", "outline_style": "no"}
        )

        return symbol

    def symbol_for_values(self, value1: int, value2: int) -> QgsFillSymbol:
        identifier = self.getPositionValuesCombinationHash(value1, value2)

        if identifier not in self.cached_symbols:
            feature_symbol = self.get_default_symbol()
            feature_symbol.setColor(self.getFeatureColor(value1, value2))

            self.cached_symbols[identifier] = feature_symbol.clone()

        return self.cached_symbols[identifier]

    def generate_legend_polygons(self) -> List[LegendPolygon]:
        polygons = []

        for x, field_1_cat in enumerate(self.field_1_classes):
            for y, field_2_cat in enumerate(self.field_2_classes):
                exist = True

                if self.getPositionValuesCombinationHash(x, y) not in self.existing_labels():
                    exist = False

                polygons.append(LegendPolygon(x=x, y=y, symbol=self.symbol_for_values(x, y), exist_in_map=exist))

        return polygons

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BivariateRenderer):
            return False

        else:
            if (
                self.field_name_1 == other.field_name_1
                and self.field_name_2 == other.field_name_2
                and self.number_classes == other.number_classes
                and
                # self.classification_method.id() == other.classification_method.id() and
                self.field_1_min == other.field_1_min
                and self.field_1_max == other.field_1_max
                and self.field_2_min == other.field_2_min
                and self.field_2_max == other.field_2_max
                and self.color_ramp_1.properties() == other.color_ramp_1.properties()
                and self.color_ramp_2.properties() == other.color_ramp_2.properties()
            ):
                return True

            else:
                return False

    @property
    def field_2_min(self) -> float:
        return (self.field_2_classes[0].lowerBound() + self.field_2_classes[0].upperBound()) / 2

    @property
    def field_2_max(self) -> float:
        return (
            self.field_2_classes[len(self.field_2_classes) - 1].lowerBound()
            + self.field_2_classes[len(self.field_2_classes) - 1].upperBound()
        ) / 2

    @property
    def field_2_labels(self) -> List[float]:
        return self.classes_to_legend_breaks(self.field_2_classes)

    @property
    def field_1_min(self) -> float:
        return (self.field_1_classes[0].lowerBound() + self.field_1_classes[0].upperBound()) / 2

    @property
    def field_1_max(self) -> float:
        return (
            self.field_1_classes[len(self.field_1_classes) - 1].lowerBound()
            + self.field_1_classes[len(self.field_1_classes) - 1].upperBound()
        ) / 2

    @property
    def field_1_labels(self) -> List[float]:
        return self.classes_to_legend_breaks(self.field_1_classes)

    def legendSymbolItem(self, identifier: str) -> QgsLegendSymbolItem:
        return QgsLegendSymbolItem(self.cached_symbols[identifier], identifier, "")

    def legendSymbolItems(self) -> List[QgsLegendSymbolItem]:
        legend_items = []
        for identifier in sorted(self.cached_symbols.keys()):
            if identifier in self.labels_existing:
                legend_items.append(self.legendSymbolItem(identifier))
        return legend_items

    def existing_labels(self) -> List[str]:
        return [x for x in sorted(self.labels_existing)]

    def generateCategories(self):
        for x in range(self.number_classes):
            for y in range(self.number_classes):
                identifier = self.getPositionValuesCombinationHash(x, y)
                self.cached_symbols[identifier] = self.symbol_for_values(x, y)


@dataclass
class LegendPolygon:
    x: float
    y: float
    symbol: QgsFillSymbol
    exist_in_map: bool = True
