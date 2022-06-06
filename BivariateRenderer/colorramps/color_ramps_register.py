from typing import List, Optional

from qgis.PyQt.QtGui import QIcon

from ..utils import Singleton
from .bivariate_color_ramp import (BivariateColorRamp, BivariateColorRampBlueGreen,
                                   BivariateColorRampCyanBrow, BivariateColorRampCyanViolet,
                                   BivariateColorRampGreenPink, BivariateColorRampGreenPurple,
                                   BivariateColorRampLigthYellowPurple,
                                   BivariateColorRampOrangeBlue, BivariateColorRampOrangePurple,
                                   BivariateColorRampPinkBlue, BivariateColorRampTurquoiseGold,
                                   BivariateColorRampVioletBlue, BivariateColorRampYellowBlue)


class BivariateColorRampsRegister(metaclass=Singleton):

    color_ramps = [
        BivariateColorRampBlueGreen(),
        BivariateColorRampCyanBrow(),
        BivariateColorRampCyanViolet(),
        BivariateColorRampBlueGreen(),
        BivariateColorRampGreenPink(),
        BivariateColorRampOrangeBlue(),
        BivariateColorRampGreenPurple(),
        BivariateColorRampLigthYellowPurple(),
        BivariateColorRampOrangePurple(),
        BivariateColorRampPinkBlue(),
        BivariateColorRampTurquoiseGold(),
        BivariateColorRampVioletBlue(),
        BivariateColorRampYellowBlue()
    ]

    @property
    def names(self) -> List[str]:
        return [x.name for x in self.color_ramps]

    @property
    def icons(self) -> List[QIcon]:
        return [x.icon for x in self.color_ramps]

    def get_by_name(self, name: str) -> Optional[BivariateColorRamp]:

        found = None

        for color_ramp in self.color_ramps:
            if color_ramp.name == name:
                found = color_ramp

        return found
