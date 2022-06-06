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


class BivariateColorRampCyanBrow(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Cyan - Brown"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#80b9b5"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#a86a25"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_cyan_brown.png")


class BivariateColorRampTurquoiseGold(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Turquoise - Gold"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#4e9ec2"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#f6b500"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_turquoise_gold.png")


class BivariateColorRampOrangeBlue(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Orange - Blue"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#f6742e"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#17afe7"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_orange_blue.png")


class BivariateColorRampYellowBlue(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Yellow - Blue"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#f1d301"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#0097f1"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_yellow_blue.png")


class BivariateColorRampLigthYellowPurple(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Ligth Yellow - Purple"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#cab55a"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#9a73af"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_ligth_yellow_purple.png")


class BivariateColorRampCyanViolet(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Cyan - Violet"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#5bcaca"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#bf64ad"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_cyan_violet.png")


class BivariateColorRampBlueGreen(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Blue - Green"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#6c84b7"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#73af7f"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_blue_green.png")


class BivariateColorRampVioletBlue(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Violet - Blue"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#ae3a4c"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#4886c2"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_violet_blue.png")


class BivariateColorRampPinkBlue(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Pink - Blue"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#cb5b5b"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#66adc0"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_pink_blue.png")


class BivariateColorRampGreenPink(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Green - Pink"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#4cac26"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#d0258c"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_green_pink.png")


class BivariateColorRampGreenPurple(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Green - Purple"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#028834"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#7a3293"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_green_purple.png")


class BivariateColorRampOrangePurple(BivariateColorRamp):

    @property
    def name(self) -> str:
        return "Orange - Purple"

    @property
    def color_ramp_1(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#e95f00"))

    @property
    def color_ramp_2(self) -> QgsGradientColorRamp:
        return QgsGradientColorRamp(QColor("#d3d3d3"), QColor("#5e3c96"))

    @property
    def icon(self) -> QIcon:
        return get_icon("cp_orange_purple.png")
