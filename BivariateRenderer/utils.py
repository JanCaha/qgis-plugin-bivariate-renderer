import json
from pathlib import Path
from typing import Any, Dict

from qgis.core import Qgis, QgsLineSymbol, QgsMessageLog, QgsReadWriteContext, QgsSymbol, QgsSymbolLayerUtils
from qgis.PyQt.QtGui import QColor, QIcon
from qgis.PyQt.QtXml import QDomDocument

from .text_constants import Texts


def log(text: Any) -> None:
    QgsMessageLog.logMessage(str(text), Texts.plugin_name, Qgis.Info)


# these two functions are taken from
# https://github.com/TomasdelaBarra/QTRANUS/blob/c32c11f02faec561b1825479b3251c096c5f36ea/add_linktype_dialog.py
def get_symbol_object(symbol_obj: Dict) -> QgsLineSymbol:
    """Return dictionary with objects of symbol"""

    from qgis.core import QgsArrowSymbolLayer, QgsLineSymbol, QgsSimpleLineSymbolLayer

    # symbol_obj = json.loads(symbol_srt.replace("'", '"').replace("ArrowLine", "Arrow"))
    symbol_layers = QgsLineSymbol()

    for layer_symbol in symbol_obj["layers_list"]:
        obj_symbol = eval(f"Qgs{layer_symbol['type_layer']}SymbolLayer.create({layer_symbol['properties_layer']})")
        symbol_layers.appendSymbolLayer(obj_symbol)

    symbol_layers.deleteSymbolLayer(0)

    return symbol_layers


def get_symbol_dict(symbol: QgsSymbol) -> Dict:
    """Return dictionary with main elements of symbol"""
    symbol_dict = dict()

    symbol_dict["type"] = symbol.type()
    symbol_dict["layers_list"] = []

    for index in range(0, symbol.symbolLayerCount()):
        symbol_dict["layers_list"].append(
            {
                "type_layer": symbol.symbolLayer(index).layerType().split(":")[0],
                "properties_layer": symbol.symbolLayer(index).properties(),
            }
        )

    return symbol_dict


def path_data(file_name: str) -> Path:

    return Path(__file__).parent / "data" / file_name


def read_file_content(file_path: Path) -> str:

    with open(file_path, "r") as file:
        text = file.read()

    return text


def load_json(content: str) -> Dict:

    return json.loads(content)


def default_line_symbol() -> QgsLineSymbol:

    line_symbol = get_symbol_object(load_json(read_file_content(path_data("axis_line_symbol.json"))))
    line_symbol.setColor(QColor(0, 0, 0))

    return line_symbol


def path_icon(file_name: str) -> Path:

    return Path(__file__).parent / "icons" / file_name


def get_icon_path(file_name: str) -> str:

    path = path_icon(file_name)

    return path.absolute().as_posix()


def save_symbol_xml(symbol: QgsSymbol, file_name: Path) -> None:

    doc = QDomDocument()

    elem = QgsSymbolLayerUtils.saveSymbol("symbol", symbol, doc, QgsReadWriteContext())

    doc.appendChild(elem)

    xml = doc.toString()

    with open(file_name, "w+") as f:
        f.write(xml)


def load_symbol_xml(file_name: Path) -> QgsSymbol:

    with open(file_name) as file:
        symbol_doc = file.read()

    doc = QDomDocument()
    doc.setContent(symbol_doc)
    return QgsSymbolLayerUtils.loadSymbol(doc.documentElement(), QgsReadWriteContext())


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
