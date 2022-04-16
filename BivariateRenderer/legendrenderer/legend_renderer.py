from typing import List
import math

from qgis.PyQt.QtCore import QPointF, QRectF, Qt
from qgis.PyQt.QtGui import QPolygonF, QBrush, QColor, QPainter, QTransform

from qgis.core import (QgsTextFormat, QgsLineSymbol, QgsRenderContext, QgsTextRenderer)

from ..renderer.bivariate_renderer import LegendPolygon
from ..utils import get_symbol_object


class LegendRenderer:

    axis_title_x: str
    axis_title_y: str
    text_format: QgsTextFormat

    axis_line_symbol: QgsLineSymbol

    legend_rotated = False
    add_axes_arrows = False
    add_axes_texts = False

    width: float
    height: float

    context: QgsRenderContext

    _painter: QPainter
    _polygons_count: int

    _text_axis_x: List[str]
    _text_axis_y: List[str]

    def __init__(self):

        self._painter = None

        self.axis_title_x = "Axis X"
        self.axis_title_y = "Axis Y"

        self.text_format = QgsTextFormat()

        self.axis_line_symbol = get_symbol_object(
            "{'type': '', 'layers_list': [{'type_layer': 'ArrowLine', 'properties_layer': {'arrow_start_width': '0.8', 'arrow_start_width_unit': 'MM', 'arrow_start_width_unit_scale': '3x:0,0,0,0,0,0', 'arrow_type': '0', 'arrow_width': '0.8', 'arrow_width_unit': 'MM', 'arrow_width_unit_scale': '3x:0,0,0,0,0,0', 'head_length': '3', 'head_length_unit': 'MM', 'head_length_unit_scale': '3x:0,0,0,0,0,0', 'head_thickness': '2', 'head_thickness_unit': 'MM', 'head_thickness_unit_scale': '3x:0,0,0,0,0,0', 'head_type': '0', 'is_curved': '1', 'is_repeated': '1', 'offset': '0', 'offset_unit': 'MM', 'offset_unit_scale': '3x:0,0,0,0,0,0', 'ring_filter': '0'}}]}"
        )
        self.axis_line_symbol.setColor(QColor(0, 0, 0))

    def set_size_context(self, width: float, height: float) -> None:

        min_size = min(width, height)

        width = min_size
        height = min_size

        self.width = width * self.context.scaleFactor()
        self.height = height * self.context.scaleFactor()

    @property
    def margin_const_percent(self) -> float:
        return 0.02

    @property
    def painter(self) -> QPainter:

        if self._painter is None:
            self._painter = self.context.painter()

        return self._painter

    def set_text_height(self, text_axis_x: List[str], text_axis_y: List[str]) -> None:

        self._text_axis_x = text_axis_x
        self._text_axis_y = text_axis_y

        if self.add_axes_texts:

            self._text_height_x = QgsTextRenderer.textHeight(self.context,
                                                             self.text_format,
                                                             textLines=text_axis_x)

            self._text_height_y = QgsTextRenderer.textHeight(self.context,
                                                             self.text_format,
                                                             textLines=text_axis_y)

        else:

            self._text_height_x = 0
            self._text_height_y = 0

    @property
    def text_height_max_with_2_margin(self) -> float:

        if self.add_axes_texts:

            return self.text_height_max + (self.text_height_margin * 2)

        else:

            return 0

    @property
    def text_height_margin(self) -> float:

        if self.add_axes_texts:

            return self.height * self.margin_const_percent

        else:

            return 0

    @property
    def text_height_max(self) -> float:

        if self.add_axes_texts:

            return max(self.text_height_x, self.text_height_y)

        else:

            return 0

    @property
    def text_height_x(self) -> float:
        return self._text_height_x

    @property
    def text_height_y(self) -> float:
        return self._text_height_y

    @property
    def arrow_start_x(self) -> float:

        if self.add_axes_arrows:

            return self.text_height_max_with_2_margin + self.width * 0.025

        else:

            return 0

    @property
    def arrow_x_y(self) -> float:

        if self.add_axes_arrows:

            return self.height - self.text_height_max_with_2_margin - self.width * 0.025

        else:

            return 0

    @property
    def arrow_width(self) -> float:

        if self.add_axes_arrows:

            return self.width * 0.05

        else:

            return 0

    @property
    def all_elements(self) -> float:
        return self.text_height_max_with_2_margin + self.arrow_width

    @property
    def text_center_axis_x_x(self) -> float:
        return self.all_elements + (self.width - self.all_elements) / 2

    @property
    def text_center_axis_x_y(self) -> float:
        return self.width - self.text_height_max + self.text_height_x - self.width * self.margin_const_percent

    @property
    def text_position_x(self) -> QPointF:
        return QPointF(self.text_center_axis_x_x, self.text_center_axis_x_y)

    @property
    def text_center_axis_y_x(self) -> float:

        return self.text_height_margin + self.text_height_max

    @property
    def text_center_axis_y_y(self) -> float:
        return (self.width - self.all_elements) / 2

    @property
    def text_position_y(self) -> QPointF:

        if self.legend_rotated:

            return QPointF(self.text_center_axis_y_x - self.text_height_y,
                           self.text_center_axis_y_y)

        else:

            return QPointF(self.text_center_axis_y_x, self.text_center_axis_y_y)

    @property
    def size_constant(self) -> float:
        return (self.width - self.all_elements) / math.sqrt(self._polygons_count)

    @property
    def polygon_start_pos_x(self) -> float:
        return self.all_elements

    @property
    def polygon_start_pos_y(self) -> float:
        return self.width - self.all_elements

    @property
    def point_lines_start(self) -> QPointF:
        return QPointF(self.arrow_start_x, self.arrow_x_y)

    @property
    def point_line_x_end(self) -> QPolygonF:
        return QPointF(self.width, self.arrow_x_y)

    @property
    def point_line_y_end(self) -> float:
        return QPointF(self.arrow_start_x, self.height * 0)

    @property
    def text_rotation_x(self) -> float:

        if self.legend_rotated:

            return math.radians(45)

        else:
            return 0.0

    @property
    def text_rotation_y(self) -> float:

        if self.legend_rotated:

            return math.radians(-45)

        else:

            return math.radians(90)

    @property
    def transform(self) -> QTransform:

        transform = QTransform()

        if self.legend_rotated:

            max_size = self.height - self.arrow_start_x
            size = self.height - max_size

            scale_factor_orig = self.height / math.sqrt(
                math.pow(max_size, 2) + math.pow(max_size, 2))
            scale_factor = (int(scale_factor_orig * 100) / 100) - 0.02

            transform.translate(self.width / 2, self.height / 2)
            transform.rotate(-45)
            transform.scale(scale_factor, scale_factor)
            transform.translate(-(self.width / 2) - (size / 2) * scale_factor_orig,
                                -(self.height / 2) + (size / 2) * scale_factor_orig)

        return transform

    def draw_polygons(self, polygons: List[LegendPolygon]) -> None:

        for polygon in polygons:

            self.painter.setBrush(QBrush(polygon.symbol.color()))

            polygon = QPolygonF(
                QRectF(self.polygon_start_pos_x + polygon.x * self.size_constant,
                       self.polygon_start_pos_y - (polygon.y + 1) * self.size_constant,
                       self.size_constant, self.size_constant))

            polygon = self.transform.map(polygon)

            self.painter.drawPolygon(polygon)

    def draw_axes_arrows(self) -> None:

        self.axis_line_symbol.startRender(self.context)

        line_x = QPolygonF([self.point_lines_start, self.point_line_x_end])

        line_x = self.transform.map(line_x)

        self.axis_line_symbol.renderPolyline(line_x, None, self.context)

        line_y = QPolygonF([self.point_lines_start, self.point_line_y_end])

        line_y = self.transform.map(line_y)

        self.axis_line_symbol.renderPolyline(line_y, None, self.context)

        self.axis_line_symbol.stopRender(self.context)

    def draw_axes_texts(self) -> None:

        QgsTextRenderer.drawText(self.transform.map(self.text_position_x), self.text_rotation_x,
                                 QgsTextRenderer.AlignCenter, self._text_axis_x, self.context,
                                 self.text_format, QgsTextRenderer.AlignVCenter)

        QgsTextRenderer.drawText(self.transform.map(self.text_position_y), self.text_rotation_y,
                                 QgsTextRenderer.AlignCenter, self._text_axis_y, self.context,
                                 self.text_format, QgsTextRenderer.AlignVCenter)

    def render(self, context: QgsRenderContext, width: float, height: float,
               polygons: List[LegendPolygon]) -> None:

        self.context = context

        self._polygons_count = len(polygons)

        self.set_size_context(width, height)

        self._painter = context.painter()

        self._painter.save()

        self._painter.setPen(Qt.NoPen)

        text_axis_x = self.axis_title_x.split("\n")
        text_axis_y = self.axis_title_y.split("\n")

        self.set_text_height(text_axis_x, text_axis_y)

        self.draw_polygons(polygons)

        if self.add_axes_arrows:

            self.draw_axes_arrows()

        # https://github.com/qgis/QGIS/blob/5e98648913b82466ca9eb42ed68f4bb0b536ae96/src/core/layout/qgslayoutitemlabel.cpp#L147

        if self.add_axes_texts:

            self.draw_axes_texts()

        self.painter.restore()
