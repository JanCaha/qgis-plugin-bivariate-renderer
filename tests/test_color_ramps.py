import pytest
from qgis.core import QgsGradientColorRamp
from qgis.PyQt.QtGui import QColor, QIcon
from qgis.PyQt.QtXml import QDomDocument

from BivariateRenderer.colormixing.color_mixing_method import ColorMixingMethodDarken
from BivariateRenderer.colorramps.bivariate_color_ramp import (
    BivariateColorRamp,
    BivariateColorRampBlueGreen,
    BivariateColorRampCyanBrown,
    BivariateColorRampCyanViolet,
    BivariateColorRampGradient,
    BivariateColorRampGreenPink,
    BivariateColorRampGreenPurple,
    BivariateColorRampLigthYellowPurple,
    BivariateColorRampManual,
    BivariateColorRampOrangeBlue,
    BivariateColorRampOrangePurple,
    BivariateColorRampPinkBlue,
    BivariateColorRampTurquoiseGold,
    BivariateColorRampVioletBlue,
    BivariateColorRampYellowBlue,
)
from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRampsRegister

color_ramps = [
    BivariateColorRampBlueGreen(),
    BivariateColorRampCyanBrown(),
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
    BivariateColorRampYellowBlue(),
]


@pytest.mark.parametrize("color_ramp", color_ramps)
def test_color_ramp(color_ramp: BivariateColorRamp):

    assert issubclass(type(color_ramp), BivariateColorRamp)

    assert isinstance(color_ramp.name, str)
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

    assert isinstance(register.get_by_name("Orange - Purple"), BivariateColorRampOrangePurple)


def test_gradient_ramp_save_load():

    ramp = BivariateColorRampGreenPink()
    ramp.set_number_of_classes(4)
    ramp.set_color_mixing_method(ColorMixingMethodDarken())

    doc = QDomDocument("test")
    elem = ramp.save(doc)

    loaded_ramp = BivariateColorRampGradient.load(elem)

    assert loaded_ramp.number_of_classes == ramp.number_of_classes
    assert loaded_ramp.color_mixing_method.name() == ramp.color_mixing_method.name()
    assert loaded_ramp.color_ramp_1.color1().name() == ramp.color_ramp_1.color1().name()
    assert loaded_ramp.color_ramp_1.color2().name() == ramp.color_ramp_1.color2().name()
    assert loaded_ramp.color_ramp_2.color1().name() == ramp.color_ramp_2.color1().name()
    assert loaded_ramp.color_ramp_2.color2().name() == ramp.color_ramp_2.color2().name()


def test_gradient_ramp_clone():

    ramp = BivariateColorRampGreenPink()
    ramp.set_number_of_classes(4)
    ramp.set_color_mixing_method(ColorMixingMethodDarken())

    cloned_ramp = ramp.clone()

    assert cloned_ramp.number_of_classes == ramp.number_of_classes
    assert cloned_ramp.color_mixing_method.name() == ramp.color_mixing_method.name()
    assert cloned_ramp.color_ramp_1.color1().name() == ramp.color_ramp_1.color1().name()
    assert cloned_ramp.color_ramp_1.color2().name() == ramp.color_ramp_1.color2().name()
    assert cloned_ramp.color_ramp_2.color1().name() == ramp.color_ramp_2.color1().name()
    assert cloned_ramp.color_ramp_2.color2().name() == ramp.color_ramp_2.color2().name()

    # cloned is independent
    cloned_ramp.set_number_of_classes(2)
    assert ramp.number_of_classes == 4


def test_manual_ramp_save_load():
    colors = [
        [QColor("#ff0000"), QColor("#00ff00"), QColor("#0000ff")],
        [QColor("#ffff00"), QColor("#ff00ff"), QColor("#00ffff")],
        [QColor("#ffffff"), QColor("#808080"), QColor("#000000")],
    ]
    ramp = BivariateColorRampManual(colors)

    doc = QDomDocument("test")
    elem = ramp.save(doc)

    loaded = BivariateColorRampManual.load(elem)

    assert loaded.number_of_classes == ramp.number_of_classes
    for i in range(ramp.number_of_classes):
        for j in range(ramp.number_of_classes):
            assert loaded.get_color(i, j).name() == ramp.get_color(i, j).name()


def test_manual_ramp_clone_independence():
    colors = [
        [QColor("#ff0000"), QColor("#00ff00")],
        [QColor("#0000ff"), QColor("#ffff00")],
    ]
    ramp = BivariateColorRampManual(colors)
    cloned = ramp.clone()

    for i in range(ramp.number_of_classes):
        for j in range(ramp.number_of_classes):
            assert cloned.get_color(i, j).name() == ramp.get_color(i, j).name()

    # cloned has its own separate color lists
    assert cloned._colors is not ramp._colors
    assert cloned._colors[0] is not ramp._colors[0]


def test_manual_ramp_requires_square_colors():
    with pytest.raises(ValueError, match="square"):
        BivariateColorRampManual(
            [
                [QColor("#ff0000"), QColor("#00ff00")],
                [QColor("#0000ff")],
            ]
        )
