from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import List

from qgis.core import QgsColorRamp, QgsGradientColorRamp, QgsSymbolLayerUtils
from qgis.PyQt.QtGui import QColor, QIcon
from qgis.PyQt.QtXml import QDomDocument, QDomElement

from BivariateRenderer.colormixing.color_mixing_method import ColorMixingMethod, ColorMixingMethodMultiply
from BivariateRenderer.colormixing.color_mixing_methods_register import ColorMixingMethodsRegister

from ..utils import get_icon_path


class BivariateColorRamp(ABC):
    _name: str = "Default Bivariate Color Ramp"
    _icon: str
    _color_ramp_1: QgsGradientColorRamp = QgsGradientColorRamp()
    _color_ramp_2: QgsGradientColorRamp = QgsGradientColorRamp()
    _colors: List[List[QColor]] = []

    def __init__(self, number_classes: int = 9) -> None:
        self._number_of_classes = number_classes

    @property
    def name(self) -> str:
        """Name of the color ramp."""
        return self._name

    @property
    def icon(self) -> QIcon:
        """Icon of the color ramp."""
        return QIcon(self._icon)

    @property
    def number_of_classes(self) -> int:
        """Number of classes in the color ramp."""
        return self._number_of_classes

    def set_name(self, name: str) -> None:
        """Set the name of the color ramp."""
        self._name = name

    @abstractmethod
    def get_color(self, position_value1: int, position_value2: int) -> QColor: ...

    @abstractmethod
    def save(self, doc: QDomDocument) -> QDomElement: ...

    @staticmethod
    @abstractmethod
    def load(bivariate_ramp_element: QDomElement) -> BivariateColorRamp: ...

    @abstractmethod
    def clone(self) -> BivariateColorRamp: ...

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return self._color_ramp_1

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return self._color_ramp_2


class BivariateColorRampGradient(BivariateColorRamp):
    _color_ramp_1: QgsGradientColorRamp = QgsGradientColorRamp(QColor("#000000"), QColor("#ffffff"))
    _color_ramp_2: QgsGradientColorRamp = QgsGradientColorRamp(QColor("#ffffff"), QColor("#000000"))

    def __init__(
        self, number_classes_per_ramp: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes_per_ramp)
        self._color_mixing_method = color_mixing_method

    def set_number_of_classes(self, number_of_classes: int) -> None:
        self._number_of_classes = number_of_classes

    def set_color_ramp_1(self, color_ramp: QgsColorRamp) -> None:
        """Set color ramp 1 if it is a QgsGradientColorRamp."""
        if isinstance(color_ramp, QgsGradientColorRamp):
            self._color_ramp_1 = color_ramp

    def set_color_ramp_2(self, color_ramp: QgsColorRamp) -> None:
        """Set color ramp 2 if it is a QgsGradientColorRamp."""
        if isinstance(color_ramp, QgsGradientColorRamp):
            self._color_ramp_2 = color_ramp

    @property
    def color_mixing_method(self) -> ColorMixingMethod:
        return self._color_mixing_method

    def set_color_mixing_method(self, color_mixing_method: ColorMixingMethod) -> None:
        self._color_mixing_method = color_mixing_method

    def get_color(self, position_value1: int, position_value2: int) -> QColor:
        color1 = self.color_ramp_1.color(position_value1 / (self._number_of_classes - 1))
        color2 = self.color_ramp_2.color(position_value2 / (self._number_of_classes - 1))

        result_color = self.color_mixing_method.mix_colors(color1, color2)

        return result_color

    def save(self, doc: QDomDocument) -> QDomElement:
        main_element = doc.createElement("BivariateColorRamp")

        main_element.setAttribute("type", "Gradient")

        main_element.setAttribute("number_of_classes", str(self.number_of_classes))
        main_element.setAttribute("color_mixing_method", self.color_mixing_method.name())

        color_ramp_elem = QgsSymbolLayerUtils.saveColorRamp("color_ramp_1", self.color_ramp_1, doc)
        main_element.appendChild(color_ramp_elem)

        color_ramp_elem = QgsSymbolLayerUtils.saveColorRamp("color_ramp_2", self.color_ramp_2, doc)
        main_element.appendChild(color_ramp_elem)

        return main_element

    @staticmethod
    def load(bivariate_ramp_element: QDomElement) -> BivariateColorRampGradient:
        bivariate_color_ramp = BivariateColorRampGradient()

        bivariate_color_ramp.set_number_of_classes(int(bivariate_ramp_element.attribute("number_of_classes")))

        color_mixing_method_name = bivariate_ramp_element.attribute("color_mixing_method")
        color_mixing_method = ColorMixingMethodsRegister().get_by_name(color_mixing_method_name)

        if color_mixing_method:
            bivariate_color_ramp.set_color_mixing_method(color_mixing_method)

        ramp_1 = QgsSymbolLayerUtils.loadColorRamp(bivariate_ramp_element.firstChildElement("colorramp"))
        if ramp_1 is not None:
            bivariate_color_ramp.set_color_ramp_1(ramp_1)

        ramp_2 = QgsSymbolLayerUtils.loadColorRamp(bivariate_ramp_element.lastChildElement("colorramp"))
        if ramp_2 is not None:
            bivariate_color_ramp.set_color_ramp_2(ramp_2)

        return bivariate_color_ramp

    def clone(self) -> BivariateColorRampGradient:
        bivariate_color_ramp = BivariateColorRampGradient()

        bivariate_color_ramp.set_name(self._name)
        bivariate_color_ramp.set_number_of_classes(self.number_of_classes)
        bivariate_color_ramp.set_color_mixing_method(self.color_mixing_method)
        ramp_1 = self.color_ramp_1.clone()
        if ramp_1 is not None:
            bivariate_color_ramp.set_color_ramp_1(ramp_1)
        ramp_2 = self.color_ramp_2.clone()
        if ramp_2 is not None:
            bivariate_color_ramp.set_color_ramp_2(ramp_2)

        return bivariate_color_ramp


class BivariateColorRampManual(BivariateColorRamp):
    _colors: List[List[QColor]] = []

    def __init__(self, colors: List[List[QColor]]) -> None:
        number_classes = len(colors)

        super().__init__(number_classes)
        self._colors = colors

        for row_colors in self._colors:
            if not len(row_colors) != number_classes:
                raise ValueError("Colors list do not create a square.")

    def get_color(self, position_value1: int, position_value2: int) -> QColor:
        return self._colors[position_value1][position_value2]

    def save(self, doc: QDomDocument) -> QDomElement:
        main_element = doc.createElement("BivariateColorRamp")

        main_element.setAttribute("type", "Manual")

        main_element.setAttribute("number_of_classes", str(self.number_of_classes))

        colors_element = doc.createElement("colors")

        squareColors = int(math.sqrt(self.number_of_classes))

        for i in range(squareColors):
            for j in range(squareColors):
                color_element = doc.createElement("color")
                color_element.setAttribute("value", self._colors[i][j].name())
                colors_element.appendChild(color_element)

        main_element.appendChild(colors_element)

        return main_element

    @staticmethod
    def load(bivariate_ramp_element: QDomElement) -> BivariateColorRampManual:

        number_of_classes = bivariate_ramp_element.attribute("number_of_classes")
        try:
            number_of_classes = int(number_of_classes)
        except ValueError:
            raise ValueError(f"Invalid number of classes: {number_of_classes}")

        squareColors = int(math.sqrt(number_of_classes))

        colors_elements = bivariate_ramp_element.childNodes()

        colors: List[List[QColor]] = []
        for _ in range(squareColors):
            colors.append([QColor("#000000") for _ in range(squareColors)])

        for i in range(squareColors):
            for j in range(squareColors):
                color_element = colors_elements.at(i * squareColors + j)
                if color_element.nodeName() != "color":
                    raise ValueError(f"Invalid child node name `{color_element.nodeName()}` element.")
                else:
                    colors[i][j] = QColor(color_element.attribute("value"))

        return BivariateColorRampManual(colors)

    def clone(self) -> BivariateColorRampManual:

        cols = []
        for _, colors in enumerate(self._colors):
            cols_row = []
            for _, color in enumerate(colors):
                cols_row.append(QColor(color))
            cols.append(cols_row)

        bivariate_color_ramp = BivariateColorRampManual(cols)

        bivariate_color_ramp.set_name(self._name)

        return bivariate_color_ramp


class BivariateColorRampCyanBrow(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Cyan - Brown"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#80b9b5"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#a86a25"))
        self._icon = get_icon_path("cp_cyan_brown.png")


class BivariateColorRampTurquoiseGold(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Turquoise - Gold"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#4e9ec2"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#f6b500"))
        self._icon = get_icon_path("cp_turquoise_gold.png")


class BivariateColorRampOrangeBlue(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Orange - Blue"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#f6742e"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#17afe7"))
        self._icon = get_icon_path("cp_orange_blue.png")


class BivariateColorRampYellowBlue(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Yellow - Blue"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#f1d301"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#0097f1"))
        self._icon = get_icon_path("cp_yellow_blue.png")


class BivariateColorRampLigthYellowPurple(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Ligth Yellow - Purple"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#cab55a"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#9a73af"))
        self._icon = get_icon_path("cp_ligth_yellow_purple.png")


class BivariateColorRampCyanViolet(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Cyan - Violet"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#5bcaca"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#bf64ad"))
        self._icon = get_icon_path("cp_cyan_violet.png")


class BivariateColorRampBlueGreen(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Blue - Green"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#6c84b7"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#73af7f"))
        self._icon = get_icon_path("cp_blue_green.png")


class BivariateColorRampVioletBlue(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Violet - Blue"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#ae3a4c"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#4886c2"))
        self._icon = get_icon_path("cp_violet_blue.png")


class BivariateColorRampPinkBlue(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Pink - Blue"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#cb5b5b"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#66adc0"))
        self._icon = get_icon_path("cp_pink_blue.png")


class BivariateColorRampGreenPink(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Green - Pink"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#4cac26"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#d0258c"))
        self._icon = get_icon_path("cp_green_pink.png")


class BivariateColorRampGreenPurple(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Green - Purple"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#028834"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#7a3293"))
        self._icon = get_icon_path("cp_green_purple.png")


class BivariateColorRampOrangePurple(BivariateColorRampGradient):
    def __init__(
        self, number_classes: int = 3, color_mixing_method: ColorMixingMethod = ColorMixingMethodMultiply()
    ) -> None:
        super().__init__(number_classes, color_mixing_method)
        self._name = "Orange - Purple"
        self._color_ramp_1 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#e95f00"))
        self._color_ramp_2 = QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#5e3c96"))
        self._icon = get_icon_path("cp_orange_purple.png")
