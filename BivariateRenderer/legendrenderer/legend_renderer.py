from typing import List
import math

from qgis.PyQt.QtCore import QPointF, QRectF, Qt
from qgis.PyQt.QtGui import QPolygonF, QBrush, QColor, QPainter

from qgis.core import (QgsTextFormat,
                       QgsLineSymbol,
                       QgsRenderContext,
                       QgsTextRenderer)

from ..renderer.bivariate_renderer import LegendPolygon
from ..utils import log, get_symbol_object


class LegendRenderer:

    axis_title_x: str
    axis_title_y: str
    text_format: QgsTextFormat

    axis_line_symbol: QgsLineSymbol

    def __init__(self):

        self.axis_title_x = "Axis X"
        self.axis_title_y = "Axis Y"

        self.text_format = QgsTextFormat()

        self.axis_line_symbol = get_symbol_object("{'type': '', 'layers_list': [{'type_layer': 'ArrowLine', 'properties_layer': {'arrow_start_width': '3', 'arrow_start_width_unit': 'Pixel', 'arrow_start_width_unit_scale': '3x:0,0,0,0,0,0', 'arrow_type': '0', 'arrow_width': '3', 'arrow_width_unit': 'Pixel', 'arrow_width_unit_scale': '3x:0,0,0,0,0,0', 'head_length': '20', 'head_length_unit': 'Pixel', 'head_length_unit_scale': '3x:0,0,0,0,0,0', 'head_thickness': '10', 'head_thickness_unit': 'Pixel', 'head_thickness_unit_scale': '3x:0,0,0,0,0,0', 'head_type': '0', 'is_curved': '1', 'is_repeated': '1', 'offset': '0', 'offset_unit': 'Pixel', 'offset_unit_scale': '3x:0,0,0,0,0,0', 'ring_filter': '0'}}]}")
        self.axis_line_symbol.setColor(QColor(0, 0, 0))

    def render(self, contex: QgsRenderContext, width: float, height: float, polygons: List[LegendPolygon]):

        min_size = min(width, height)

        width = min_size
        height = min_size

        width = width * contex.scaleFactor()
        height = height * contex.scaleFactor()

        painter: QPainter = contex.painter()

        painter.save()

        # TODO do it around each drawing
        painter.save()

        painter.setPen(Qt.NoPen)

        size_constant = (width * 0.8) / math.sqrt(len(polygons))

        for polygon in polygons:

            painter.setBrush(QBrush(polygon.symbol.color()))

            painter.drawRect(QRectF(width * 0.2 + polygon.x * size_constant,
                                    width * 0.8 - (polygon.y + 1) * size_constant,
                                    size_constant, size_constant))

        painter.restore()

        painter.save()

        self.axis_line_symbol.startRender(contex)

        self.axis_line_symbol.renderPolyline(QPolygonF([QPointF(width * 0.15, height * 0.85),
                                                        QPointF(width * 1, height * 0.85)]),
                                             None, contex)

        self.axis_line_symbol.renderPolyline(QPolygonF([QPointF(width * 0.15, height * 0.85),
                                                        QPointF(width * 0.15, height * 0)]),
                                             None, contex)

        self.axis_line_symbol.stopRender(contex)

        painter.restore()

        painter.save()

        text_height = QgsTextRenderer.textHeight(contex,
                                                 self.text_format,
                                                 textLines=[self.axis_title_x])

        QgsTextRenderer.drawText(QPointF(width * 0.6, height * 0.9 + text_height / 2),
                                 0,
                                 QgsTextRenderer.AlignCenter,
                                 [self.axis_title_x],
                                 contex,
                                 self.text_format,
                                 QgsTextRenderer.AlignVCenter)

        QgsTextRenderer.drawText(QPointF(width * 0.1, height * 0.4),
                                 math.radians(90),
                                 QgsTextRenderer.AlignCenter,
                                 [self.axis_title_y],
                                 contex,
                                 self.text_format,
                                 QgsTextRenderer.AlignVCenter)

        painter.restore()

