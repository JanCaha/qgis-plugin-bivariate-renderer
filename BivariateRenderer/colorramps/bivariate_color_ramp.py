from abc import ABC, abstractmethod

from qgis.core import QgsGradientColorRamp
from qgis.PyQt.QtGui import QIcon, QColor

from ..utils import get_icon


class BivariateColorRamp(ABC):

    @property
    @abstractmethod
    def color_ramp_1(self) -> QgsGradientColorRamp:
        pass

    @property
    @abstractmethod
    def color_ramp_2(self) -> QgsGradientColorRamp:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def icon(self) -> QIcon:
        pass


class BivariateColorRampDarkRedLightBlue(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Dark red - Light Blue"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#e8e8e8"), QColor("#c85a5a"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#e8e8e8"), QColor("#64acbe"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_darkred_lightblue.png")


class BivariateColorRampAquamarinePink(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Aquamarine - Pink"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#e8e8e8"), QColor("#5ac8c8"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#e8e8e8"), QColor("#be64ac"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_aquamarine_pink.png")


class BivariateColorRampYellowPink(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Yellow - Violet"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#e8e8e8"), QColor("#c8b35a"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#e8e8e8"), QColor("#9972af"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_yellow_violet.png")


class BivariateColorRampBlueGreen(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Blue - Green"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#e8e8e8"), QColor("#6c83b5"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#e8e8e8"), QColor("#73ae80"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_blue_green.png")


class BivariateColorRampGreenPink(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Green - Pink"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#f3f3f3"), QColor("#8ae1ae"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#f3f3f3"), QColor("#e6a2d0"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_green_pink.png")


class BivariateColorRampOrangeBlue(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Orange - Blue"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#f3f3f3"), QColor("#cc8855"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#f3f3f3"), QColor("#64acbe"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_orange_blue.png")
