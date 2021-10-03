from typing import List

from qgis.PyQt.QtGui import QIcon

from ..utils import Singleton
from .bivariate_color_ramp import (BivariateColorRamp,
                                   BivariateColorRampDarkRedLightBlue,
                                   BivariateColorRampAquamarinePink,
                                   BivariateColorRampYellowPink,
                                   BivariateColorRampBlueGreen,
                                   BivariateColorRampGreenPink)


class BivariateColorRampsRegister(metaclass=Singleton):

    color_ramps = [BivariateColorRampDarkRedLightBlue(),
                   BivariateColorRampAquamarinePink(),
                   BivariateColorRampYellowPink(),
                   BivariateColorRampBlueGreen(),
                   BivariateColorRampGreenPink()]

    @property
    def names(self) -> List[str]:
        return [x.name for x in self.color_ramps]

    @property
    def icons(self) -> List[QIcon]:
        return [x.icon for x in self.color_ramps]

    def get_by_name(self, name: str) -> BivariateColorRamp:
        for color_ramp in self.color_ramps:
            if color_ramp.name == name:
                return color_ramp
