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
        return "Direct color mixing"

    def mix_colors(self, color1: QColor, color2: QColor) -> QColor:

        return QColor(int((color1.red() + color2.red())/2),
                      int((color1.green() + color2.green())/2),
                      int((color1.blue() + color2.blue())/2))


class ColorMixingMethodDarken(ColorMixingMethod):

    def __init__(self):
        pass

    def name(self) -> str:
        return "Darken blend color mixing"

    def mix_colors(self, color1: QColor, color2: QColor) -> QColor:

        return QColor(min(color1.red(), color2.red()),
                      min(color1.green(), color2.green()),
                      min(color1.blue(), color2.blue()))
