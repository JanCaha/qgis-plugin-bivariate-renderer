from abc import ABC, abstractmethod

from PyQt5.QtGui import QColor


class ColorMixingMethod(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def mix_colors(self, color1: QColor, color2: QColor) -> QColor:
        pass


class ColorMixingMethodDirect(ColorMixingMethod):

    def __init__(self):
        pass

    def name(self) -> str:
        return "Direct Mixing"

    def mix_colors(self, color1: QColor, color2: QColor) -> QColor:

        return QColor(
            int((color1.red() + color2.red()) / 2),
            int((color1.green() + color2.green()) / 2),
            int((color1.blue() + color2.blue()) / 2),
        )


class ColorMixingMethodDarken(ColorMixingMethod):

    def __init__(self):
        pass

    def name(self) -> str:
        return "Blend Darken"

    def mix_colors(self, color1: QColor, color2: QColor) -> QColor:

        return QColor(
            min(color1.red(), color2.red()), min(color1.green(), color2.green()), min(color1.blue(), color2.blue())
        )


class ColorMixingMethodMultiply(ColorMixingMethod):

    def __init__(self):
        pass

    def name(self) -> str:
        return "Blend Multiply"

    def mix_colors(self, color1: QColor, color2: QColor) -> QColor:

        return QColor(
            int((color1.redF() * color2.redF()) * 255),
            int((color1.greenF() * color2.greenF()) * 255),
            int((color1.blueF() * color2.blueF()) * 255),
        )
