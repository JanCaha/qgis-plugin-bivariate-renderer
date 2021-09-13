from typing import Union, NoReturn
from pathlib import Path

from qgis.core import (QgsMessageLog,
                       Qgis,
                       QgsProcessingUtils)

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
