import pytest
from pathlib import Path

from qgis.core import QgsGradientColorRamp
from qgis.PyQt.QtGui import QIcon

from BivariateRenderer.colorramps.bivariate_color_ramp import (
    BivariateColorRamp, BivariateColorRampAquamarinePink, BivariateColorRampBlueGreen,
    BivariateColorRampDarkRedLightBlue, BivariateColorRampGreenPink, BivariateColorRampYellowPink,
    BivariateColorRampOrangeBlue)
from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRampsRegister

color_ramps = [
    BivariateColorRampAquamarinePink(),
    BivariateColorRampBlueGreen(),
    BivariateColorRampDarkRedLightBlue(),
    BivariateColorRampGreenPink(),
    BivariateColorRampYellowPink(),
    BivariateColorRampOrangeBlue()
]


@pytest.mark.parametrize("color_ramp", color_ramps)
def test_color_ramp(color_ramp: BivariateColorRamp):

    assert issubclass(type(color_ramp), BivariateColorRamp)

    assert isinstance(color_ramp.name, str)
    assert isinstance(color_ramp.icons_path, Path)
    assert isinstance(color_ramp.icon, QIcon)
    assert isinstance(color_ramp.color_ramp_1, QgsGradientColorRamp)
    assert isinstance(color_ramp.color_ramp_2, QgsGradientColorRamp)

    assert color_ramp.color_ramp_1.color1().name() != color_ramp.color_ramp_1.color2().name()
    assert color_ramp.color_ramp_2.color1().name() != color_ramp.color_ramp_2.color2().name()


def test_color_ramp_register():

    register = BivariateColorRampsRegister()

    assert register

    assert isinstance(register.names, list)
    assert isinstance(register.names[0], str)

    assert isinstance(register.icons, list)
    assert isinstance(register.icons[0], QIcon)

    assert isinstance(register.get_by_name("Dark red - Light Blue"),
                      BivariateColorRampDarkRedLightBlue)
