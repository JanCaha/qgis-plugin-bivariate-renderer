from typing import Union, NoReturn, Dict
import json
from pathlib import Path

from qgis.core import (QgsMessageLog,
                       Qgis,
                       QgsProcessingUtils,
                       QgsLineSymbol,
                       QgsSymbol)

from .text_constants import Texts


def log(text):
    QgsMessageLog.logMessage(str(text),
                             Texts.plugin_name,
                             Qgis.Info)


def write_text_to_file(file: Union[Path, str], text: str) -> NoReturn:

    with open(file, "w") as file_to_write:
        file_to_write.writelines(text)
        file_to_write.close()


def path_to_legend_svg():
    return Path(__file__).parent / Texts.temp_legend_filename


def get_symbol_object(symbol_srt) -> QgsLineSymbol:
    """ Return dictionary with objects of symbol"""

    from qgis.core import (QgsArrowSymbolLayer,
                           QgsSimpleLineSymbolLayer,
                           QgsLineSymbol)

    symbol_obj = json.loads(symbol_srt.replace("'", '"').replace("ArrowLine", "Arrow"))
    symbol_layers = QgsLineSymbol()

    for layer_symbol in symbol_obj['layers_list']:
        obj_symbol = eval(f"Qgs{layer_symbol['type_layer']}SymbolLayer.create({layer_symbol['properties_layer']})")
        symbol_layers.appendSymbolLayer(obj_symbol)

    symbol_layers.deleteSymbolLayer(0)

    return symbol_layers


def get_symbol_dict(symbol: QgsSymbol) -> Dict:
    """ Return dictionary with main elements of symbol """
    symbol_dict = dict()

    symbol_dict['type'] = symbol.type()
    symbol_dict['layers_list'] = []

    for index in range(0, symbol.symbolLayerCount()):
        symbol_dict['layers_list'].append({
            'type_layer': symbol.symbolLayer(index).layerType().split(':')[0],
            'properties_layer': symbol.symbolLayer(index).properties(),
        })

    return symbol_dict
