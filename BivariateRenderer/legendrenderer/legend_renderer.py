from typing import List
import math

from qgis.PyQt.QtCore import QPointF, QRectF, Qt
from qgis.PyQt.QtGui import QPolygonF, QBrush, QColor, QPainter, QTransform

from qgis.core import (QgsTextFormat,
                       QgsLineSymbol,
                       QgsRenderContext,
                       QgsTextRenderer,
                       QgsUnitTypes)

from ..renderer.bivariate_renderer import LegendPolygon
from ..utils import log, get_symbol_object


class LegendRenderer:

    axis_title_x: str
    axis_title_y: str
    text_format: QgsTextFormat

    axis_line_symbol: QgsLineSymbol
    
    legend_rotated = False

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

        text_height = QgsTextRenderer.textHeight(contex,
                                                 self.text_format,
                                                 textLines=[self.axis_title_x])
                
        if self.legend_rotated:
            
            scale_factor = 0.73
            
            painter.translate(width/2, height/2)
            painter.rotate(-45)
            painter.scale(scale_factor, scale_factor)
            painter.translate(-width/2, -height/2)
            
            size_constant = width * 0.9 / math.sqrt(len(polygons))
            polygon_start_pos_x = width * 0.05
            polygon_start_pos_y = width * 0.95
            
            point_lines_start = QPointF(width * 0.025, height * 0.975)
            point_line_x_end = QPointF(width * 0.95, height * 0.975)
            point_line_y_end = QPointF(width * 0.025, height * 0.05)
            
            text_position_x = QPointF(width * 0.5, height + text_height / 2)
            text_rotation_x = 0
            
            text_position_y = QPointF(width * 0 - text_height / 2, height * 0.5)
            text_rotation_y = math.radians(-90)
            
        else:
            
            size_constant = (width * 0.8) / math.sqrt(len(polygons))
            polygon_start_pos_x = width * 0.2
            polygon_start_pos_y = width * 0.8

            point_lines_start = QPointF(width * 0.15, height * 0.85)
            point_line_x_end = QPointF(width * 1, height * 0.85)
            point_line_y_end = QPointF(width * 0.15, height * 0)
            
            text_position_x = QPointF(width * 0.6, height * 0.9 + text_height / 2)
            text_rotation_x = 0
            
            text_position_y = QPointF(width * 0.1, height * 0.4)
            text_rotation_y = math.radians(90)
            
        for polygon in polygons:

            painter.setBrush(QBrush(polygon.symbol.color()))

            painter.drawRect(QRectF(polygon_start_pos_x + polygon.x * size_constant,
                                    polygon_start_pos_y - (polygon.y + 1) * size_constant,
                                    size_constant, size_constant))
        
        # painter.restore()

        # painter.save()
                
        self.axis_line_symbol.startRender(contex)
            
        self.axis_line_symbol.renderPolyline(QPolygonF([point_lines_start,
                                                        point_line_x_end]),
                                             None, contex)

        self.axis_line_symbol.renderPolyline(QPolygonF([point_lines_start,
                                                        point_line_y_end]),
                                             None, contex)

        self.axis_line_symbol.stopRender(contex)

        # painter.restore()

        # painter.save()

        text_height = QgsTextRenderer.textHeight(contex,
                                                 self.text_format,
                                                 textLines=[self.axis_title_x])

        QgsTextRenderer.drawText(text_position_x,
                                 text_rotation_x,
                                 QgsTextRenderer.AlignCenter,
                                 [self.axis_title_x],
                                 contex,
                                 self.text_format,
                                 QgsTextRenderer.AlignVCenter)

        QgsTextRenderer.drawText(text_position_y,
                                 text_rotation_y,
                                 QgsTextRenderer.AlignCenter,
                                 [self.axis_title_y],
                                 contex,
                                 self.text_format,
                                 QgsTextRenderer.AlignVCenter)

        painter.restore()

