from dataclasses import dataclass
from typing import List

from qgis.core import QgsClassificationRange, QgsFillSymbol


def classes_to_legend_midpoints(classes: List[QgsClassificationRange]) -> List[float]:
    values = []

    for interval_class in classes:
        values.append((interval_class.lowerBound() + interval_class.upperBound()) / 2)

    return values


@dataclass
class LegendPolygon:
    x: float
    y: float
    symbol: QgsFillSymbol
    exist_in_map: bool = True
