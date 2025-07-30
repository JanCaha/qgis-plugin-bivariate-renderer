from pathlib import Path
from typing import Any

from qgis.core import (
    Qgis,
    QgsArrowSymbolLayer,
    QgsFillSymbol,
    QgsLinePatternFillSymbolLayer,
    QgsLineSymbol,
    QgsMessageLog,
    QgsRenderContext,
    QgsSimpleFillSymbolLayer,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import Qt

from .text_constants import Texts


def log(text: Any) -> None:
    QgsMessageLog.logMessage(str(text), Texts.plugin_name, Qgis.MessageLevel.Info)


def default_line_symbol() -> QgsLineSymbol:
    """Return a default line symbol with specific properties."""

    symbol = QgsLineSymbol.createSimple({})

    assert symbol is not None

    symbol.takeSymbolLayer(0)

    symbol_layer = QgsArrowSymbolLayer.create(
        {
            "color": "0,0,0,255,rgb:0,0,0,1",
            "arrow_start_width": "0.8",
            "arrow_start_width_unit": "MM",
            "arrow_start_width_unit_scale": "3x: 0, 0, 0, 0, 0, 0",
            "arrow_type": "0",
            "arrow_width": "0.8",
            "arrow_width_unit": "MM",
            "arrow_width_unit_scale": "3x: 0, 0, 0, 0, 0, 0",
            "head_length": "3",
            "head_length_unit": "MM",
            "head_length_unit_scale": "3x: 0, 0, 0, 0, 0, 0",
            "head_thickness": "2",
            "head_thickness_unit": "MM",
            "head_thickness_unit_scale": "3x: 0, 0, 0, 0, 0, 0",
            "head_type": "0",
            "is_curved": "1",
            "is_repeated": "1",
            "offset": "0",
            "offset_unit": "MM",
            "offset_unit_scale": "3x: 0, 0, 0, 0, 0, 0",
            "ring_filter": "0",
        }
    )

    assert symbol_layer is not None

    symbol.insertSymbolLayer(0, symbol_layer)

    return symbol


def path_icon(file_name: str) -> Path:

    return Path(__file__).parent / "icons" / file_name


def get_icon_path(file_name: str) -> str:

    path = path_icon(file_name)

    return path.absolute().as_posix()


def default_fill_symbol() -> QgsFillSymbol:
    """Return a default fill symbol with specific properties."""

    symbol = QgsFillSymbol.createSimple(
        {
            "color": "204,204,204,0,rgb:0.8,0.8,0.8,0",
            "outline_width": "0.5",
            "outline_width_unit": "MM",
            "outline_color": "0,0,0,255,rgb:0,0,0,1",
            "outline_style": "solid",
        }
    )

    if symbol is None:
        raise ValueError("Failed to create a valid QgsFillSymbol.")

    return symbol


def symbol_layers_properties(layer: QgsVectorLayer) -> str:
    """Return a string representation of the symbol layers properties of a given layer."""

    str_repr = ""

    renderer = layer.renderer()
    assert renderer is not None

    context = QgsRenderContext()

    for symbol in renderer.symbols(context):
        for symbol_layer in symbol.symbolLayers():
            str_repr = f"{str_repr}{'-' * 10}{symbol_layer.layerType()}{'-' * 10}\n{symbol_layer.properties()}\n"
        str_repr = f"{str_repr}{'*' * 50}\n"

    return str_repr


def only_color_fill_symbol() -> QgsFillSymbol:
    """Return a fill symbol with only color set."""

    symbol = QgsFillSymbol.createSimple({})

    assert symbol is not None

    symbol.takeSymbolLayer(0)

    symbol_layer = QgsSimpleFillSymbolLayer.create({})

    assert symbol_layer is not None

    symbol_layer.setStrokeStyle(Qt.PenStyle.NoPen)
    symbol.appendSymbolLayer(symbol_layer)

    return symbol


def default_missing_values_symbol() -> QgsFillSymbol:
    """Return a fill symbol for missing values with a specific pattern."""

    symbol = QgsFillSymbol.createSimple({})

    assert symbol is not None

    symbol_settings = {
        "angle": "45",
        "color": "0,0,0,255,rgb:0,0,0,1.0",
        "distance": "2.5",
        "distance_unit": "MM",
        "line_width": "0.5",
        "line_width_unit": "MM",
    }

    symbol_layer_1 = QgsLinePatternFillSymbolLayer.create(symbol_settings)
    symbol_settings["angle"] = "-45"
    symbol_layer_2 = QgsLinePatternFillSymbolLayer.create(symbol_settings)

    symbol.takeSymbolLayer(0)

    symbol.insertSymbolLayer(0, symbol_layer_1)
    symbol.insertSymbolLayer(0, symbol_layer_2)

    return symbol


class Singleton(type):
    """A metaclass for creating singleton classes."""

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
