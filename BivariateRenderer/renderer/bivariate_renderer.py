from __future__ import annotations
from typing import NoReturn, List, Dict, Union
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from PyQt5.QtGui import QColor
from PyQt5.QtXml import QDomDocument, QDomElement

from qgis.core import (QgsFeatureRenderer, QgsClassificationRange,
                       QgsFeature,
                       QgsColorRamp,
                       QgsFillSymbol,
                       QgsSymbolLayerUtils,
                       QgsProcessingUtils)

from BivariateRenderer.utils import (write_text_to_file,
                                     path_to_legend_svg)

from BivariateRenderer.text_constants import Texts


class BivariateRenderer(QgsFeatureRenderer):

    number_classes: int
    classification_method_name: str
    color_ramp_1: QgsColorRamp
    color_ramp_2: QgsColorRamp
    field_name_1: str
    field_name_2: str
    field_1_classes: List[QgsClassificationRange]
    field_2_classes: List[QgsClassificationRange]
    field_1_min: float
    field_1_max: float
    field_2_min: float
    field_2_max: float

    def __init__(self, syms=None):

        super().__init__(Texts.bivariate_renderer_short_name)

        self.number_classes = 3

        self.field_name_1 = None
        self.field_name_2 = None

        self.classification_method_name = None

        self.color_ramp_1 = None
        self.color_ramp_2 = None

        self.cached = {}

        self.setUpJinjaTemplates()

    def __repr__(self) -> str:
        return f"BivariateRenderer with {self.number_classes} classes for each attribute, " \
               f"for fields {self.field_name_1} and {self.field_name_2}, " \
               f"with classification method {self.classification_method_name}," \
               f"field 1 vals {self.field_1_min};{self.field_1_max} " \
               f"field 2 vals {self.field_2_min};{self.field_2_max} "

    def setUpJinjaTemplates(self):

        path = Path(__file__).parent.parent / "svg_templates"

        self.file_loader = FileSystemLoader(path.absolute().as_posix())
        self.env = Environment(loader=self.file_loader)
        self.legend_template = self.env.get_template("legend_template.svg")

    def getLegendCategorySize(self) -> int:

        size_constant = 250 / self.number_classes

        return int(size_constant)

    def getLegendCategories(self) -> Dict[int, Dict[str, Union[int, str]]]:

        position = {}

        size_constant = self.getLegendCategorySize()
        start_y = 250 - size_constant
        start_x = 50

        x = 0
        for field_1_cat in self.field_1_classes:

            y = 0
            for field_2_cat in self.field_2_classes:

                color = self.getFeatureColor((field_1_cat.lowerBound() + field_1_cat.upperBound())/2,
                                             (field_2_cat.lowerBound() + field_2_cat.upperBound())/2)

                value_hash = self.getFeatureValueCombinationHash((field_1_cat.lowerBound() + field_1_cat.upperBound())/2,
                                                                 (field_2_cat.lowerBound() + field_2_cat.upperBound())/2)

                position.update({value_hash: {"x": int(start_x + x*size_constant),
                                              "y": int(start_y - y*size_constant),
                                              "color": str(color.name())}})

                y += 1

            x += 1

        return position

    @property
    def temp_folder_legend_file(self) -> str:
        p = Path(QgsProcessingUtils.tempFolder()) / "bivariate_legend.svg"
        return str(p.absolute().as_posix())

    def render_legend_to_temp(self) -> NoReturn:

        write_text_to_file(self.temp_folder_legend_file, self.legend_svg)

    def renderLegend(self) -> NoReturn:

        write_text_to_file(path_to_legend_svg(), self.legend_svg)

    @property
    def legend_svg(self) -> str:
        return self.legend_template.render(rectangles=self.getLegendCategories(),
                                           xy=self.getLegendCategorySize(),
                                           field_name_x=self.field_name_1,
                                           field_name_y=self.field_name_2)

    def setClassificationMethodName(self, name: str) -> NoReturn:
        self.classification_method_name = name

    def setNumberOfClasses(self, number: int) -> NoReturn:
        self.number_classes = int(number)

    def setColorRamp1(self, color_ramp: QgsColorRamp) -> NoReturn:
        self.color_ramp_1 = color_ramp

    def setColorRamp2(self, color_ramp: QgsColorRamp) -> NoReturn:
        self.color_ramp_2 = color_ramp

    def setFieldName1(self, field_name: str) -> NoReturn:
        self.field_name_1 = field_name

    def setFieldName2(self, field_name: str) -> NoReturn:
        self.field_name_2 = field_name

    def setField1Classes(self, classes: List[QgsClassificationRange]) -> NoReturn:
        self.field_1_classes = classes

        self.field_1_min = (self.field_1_classes[0].lowerBound() + self.field_1_classes[0].upperBound()) / 2
        self.field_1_max = (self.field_1_classes[len(self.field_1_classes)-1].lowerBound() +
                            self.field_1_classes[len(self.field_1_classes)-1].upperBound()) / 2

    def setField2Classes(self, classes: List[QgsClassificationRange]) -> NoReturn:
        self.field_2_classes = classes

        self.field_2_min = (self.field_2_classes[0].lowerBound() + self.field_2_classes[0].upperBound()) / 2
        self.field_2_max = (self.field_2_classes[len(self.field_2_classes) - 1].lowerBound() +
                            self.field_2_classes[len(self.field_2_classes) - 1].upperBound()) / 2

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

    def create_legend_example(self):
        pass

    def getFeatureValueCombinationHash(self, value1: float, value2: float) -> int:
        return hash(f"{value1}-{value2}")

    def getFeatureColor(self, value1: float, value2: float) -> QColor:

        position_value1 = self.positionValueField1(value1)
        position_value2 = self.positionValueField2(value2)

        color1 = self.color_ramp_1.color(position_value1)
        color2 = self.color_ramp_2.color(position_value2)

        result_color = QColor((color1.red() + color2.red())/2,
                              (color1.green() + color2.green())/2,
                              (color1.blue() + color2.blue())/2)

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
        r.classification_method_name = self.classification_method_name
        r.setNumberOfClasses(self.number_classes)
        r.setColorRamp1(self.color_ramp_1.clone())
        r.setColorRamp2(self.color_ramp_2.clone())
        r.setField1Classes(self.field_1_classes)
        r.setField2Classes(self.field_2_classes)

        return r

    def save(self, doc: QDomDocument, context):

        renderer_elem = doc.createElement("renderer-v2")

        renderer_elem.setAttribute('type', Texts.bivariate_renderer_short_name)

        renderer_elem.setAttribute('number_of_classes', self.number_classes)

        renderer_elem.setAttribute('classification_method_name', self.classification_method_name)

        renderer_elem.setAttribute('field_name_1', self.field_name_1)
        renderer_elem.setAttribute('field_name_2', self.field_name_2)

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

        return renderer_elem

    @staticmethod
    def create_render_from_element(element: QDomElement) -> BivariateRenderer:

        r = BivariateRenderer()

        r.setFieldName1(element.attribute("field_name_1"))
        r.setFieldName2(element.attribute("field_name_2"))

        r.setNumberOfClasses(element.attribute("number_of_classes"))
        r.setClassificationMethodName(element.attribute("classification_method_name "))

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

        r.setField1Classes(field_1_classes)
        r.setField2Classes(field_2_classes)

        return r

    def load(self, symbology_elem: QDomElement, context):

        r = BivariateRenderer()

        r.setFieldName1(symbology_elem.attribute("field_name_1"))
        r.setFieldName2(symbology_elem.attribute("field_name_2"))

        r.setNumberOfClasses(symbology_elem.attribute("number_of_classes"))

        r.setColorRamp1(QgsSymbolLayerUtils.loadColorRamp(symbology_elem.attribute("color_ramp_1")))
        r.setColorRamp2(QgsSymbolLayerUtils.loadColorRamp(symbology_elem.attribute("color_ramp_2")))

        r.setField1Classes(self.string_2_class_ranges(symbology_elem.attribute("field_1_classes")))
        r.setField2Classes(self.string_2_class_ranges(symbology_elem.attribute("field_2_classes")))

        r.field_1_min = symbology_elem.attribute("field_1_min")
        r.field_1_max = symbology_elem.attribute("field_1_max")
        r.field_2_min = symbology_elem.attribute("field_2_min")
        r.field_2_max = symbology_elem.attribute("field_2_max")

        return r

    @staticmethod
    def get_default_symbol():

        symbol = QgsFillSymbol.createSimple({"color": "#cccccc",
                                             "outline_width": "0.0",
                                             "outline_color": "0,0,0",
                                             'outline_style': 'no'})

        return symbol
