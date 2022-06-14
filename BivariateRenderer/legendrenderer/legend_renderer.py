from typing import List
import math

from qgis.PyQt.QtCore import QPointF, QRectF, Qt
from qgis.PyQt.QtGui import QPolygonF, QBrush, QPainter, QTransform, QColor, QPen

from qgis.core import (QgsTextFormat, QgsLineSymbol, QgsRenderContext, QgsTextRenderer,
                       QgsBasicNumericFormat, QgsNumericFormatContext, QgsLineString, QgsPoint)

from ..renderer.bivariate_renderer import LegendPolygon, BivariateRenderer
from ..utils import default_line_symbol


class LegendRenderer:

    axis_title_x: str
    axis_title_y: str
    text_format: QgsTextFormat
    text_format_ticks: QgsTextFormat

    axis_line_symbol: QgsLineSymbol

    legend_rotated = False
    add_axes_arrows = False
    add_axes_texts = False
    add_axes_ticks_texts = False
    add_colors_separators = False

    arrows_common_start_point = False

    width: float
    height: float

    context: QgsRenderContext

    _painter: QPainter
    _polygons_count: int

    _text_axis_x: List[str]
    _text_axis_y: List[str]

    _transform: QTransform = None

    texts_axis_x_ticks: List[float]
    texts_axis_y_ticks: List[float]

    ticks_x_precision: int
    ticks_y_precision: int

    _numeric_format: QgsBasicNumericFormat
    _numeric_format_context: QgsNumericFormatContext

    _text_rotation_y: float

    _space_above_ticks: int

    color_separator_width_percent: float
    color_separator_color: QColor

    arrow_width_percent: float

    use_category_midpoints: bool

    def __init__(self):

        self._painter = None

        self.axis_title_x = "Axis X"
        self.axis_title_y = "Axis Y"

        self.text_format = QgsTextFormat()
        self.text_format_ticks = QgsTextFormat()

        self.axis_line_symbol = default_line_symbol().clone()

        self._text_rotation_y = 90

        self._space_above_ticks = 10

        self.ticks_x_precision = 2
        self.ticks_y_precision = 2

        self._numeric_format = QgsBasicNumericFormat()
        self._numeric_format_context = QgsNumericFormatContext()

        self.color_separator_width_percent = 3
        self.color_separator_color = QColor("#ffffff")

        self.arrow_width_percent = 5

        self.use_category_midpoints = False

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
    def text_height_max_with_margin(self) -> float:

        if self.add_axes_texts:

            return self.text_height_max + self.margin

        else:

            return 0

    @property
    def margin(self) -> float:

        return self.height * self.margin_const_percent

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

            return self.axis_text_tics_top + (self.arrow_width / 2)

        else:

            return 0

    @property
    def arrow_x_y(self) -> float:

        if self.add_axes_arrows:

            return self.height - self.axis_text_tics_top - (self.arrow_width / 2)

        else:

            return 0

    @property
    def arrow_width(self) -> float:

        if self.add_axes_arrows:

            return self.width * (self.arrow_width_percent / 100)

        else:

            return 0

    @property
    def axis_text_tics_top(self):
        return self.text_height_max_with_margin + self.axis_tick_text_height_with_margin

    @property
    def all_elements_top(self) -> float:
        return self.axis_text_tics_top + self.arrow_width

    @property
    def text_position_x(self) -> QPointF:

        x = self.all_elements_top + (self.width - self.all_elements_top) / 2
        y = self.width - (self.text_height_x / len(self._text_axis_x)) * 0.15

        if self.legend_rotated:
            y = self.width + self.text_height_max / 2

        return QPointF(x, y)

    @property
    def axis_y_text_rotated_counterclockwise(self) -> bool:

        return self._text_rotation_y == 90

    @property
    def text_position_y(self) -> QPointF:

        x = self.text_height_max / 2
        y = (self.width - self.all_elements_top) / 2

        if self.legend_rotated:

            x = -self.text_height_max / 2

            return QPointF(x, y)

        else:

            if self.axis_y_text_rotated_counterclockwise:

                x = self.text_height_max

            else:

                x = 0

            return QPointF(x, y)

    @property
    def size_constant(self) -> float:
        return (self.width - self.all_elements_top) / math.sqrt(self._polygons_count)

    @property
    def polygon_start_pos_x(self) -> float:
        return self.all_elements_top

    @property
    def polygon_start_pos_y(self) -> float:
        return self.width - self.all_elements_top

    @property
    def arrow_x_start_point(self) -> QPointF:
        if self.arrows_common_start_point:
            return QPointF(self.arrow_start_x, self.arrow_x_y)
        else:
            return QPointF(self.polygon_start_pos_x, self.arrow_x_y)

    @property
    def arrow_y_start_point(self) -> QPointF:
        if self.arrows_common_start_point:
            return QPointF(self.arrow_start_x, self.arrow_x_y)
        else:
            return QPointF(self.arrow_start_x, self.polygon_start_pos_y)

    @property
    def arrow_x_end_point(self) -> QPolygonF:
        return QPointF(self.width, self.arrow_x_y)

    @property
    def arrow_y_end_point(self) -> float:
        return QPointF(self.arrow_start_x, 0.0)

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

            return math.radians(self._text_rotation_y)

    def set_text_rotation_y(self, rotation: float) -> None:
        self._text_rotation_y = rotation

    @property
    def transform(self) -> QTransform:

        if self._transform is None:

            self._transform = QTransform()

            max_size = self.height

            if self.add_axes_ticks_texts:
                if not self.use_category_midpoints:
                    max_size = self.height + self.axis_tick_last_value_max_width / 2

            if self.legend_rotated:

                size = self.height - max_size

                scale_factor_orig = self.height / math.sqrt(
                    math.pow(max_size, 2) + math.pow(max_size, 2))
                scale_factor = (int(scale_factor_orig * 100) / 100) - 0.02

                self._transform.translate(self.width / 2, self.height / 2)
                self._transform.rotate(-45)
                self._transform.scale(scale_factor, scale_factor)
                self._transform.translate(-(self.width / 2) - (size / 2) * scale_factor_orig,
                                          -(self.height / 2) + (size / 2) * scale_factor_orig)

            else:

                scale_factor = self.height / max_size

                self._transform.scale(scale_factor, scale_factor)
                self._transform.translate(0, self.axis_tick_last_value_max_width / 2)

        return self._transform

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

        line_x = QPolygonF([self.arrow_x_start_point, self.arrow_x_end_point])

        line_x = self.transform.map(line_x)

        self.axis_line_symbol.renderPolyline(line_x, None, self.context)

        line_y = QPolygonF([self.arrow_y_start_point, self.arrow_y_end_point])

        line_y = self.transform.map(line_y)

        self.axis_line_symbol.renderPolyline(line_y, None, self.context)

        self.axis_line_symbol.stopRender(self.context)

    @property
    def axis_text_max_lines(self) -> int:
        return max(len(self._text_axis_x), len(self._text_axis_y))

    def add_empty_lines(self,
                        text: List[str],
                        number_of_lines: int,
                        add_before_text: bool = False) -> List[str]:

        if add_before_text:

            return ["\n"] * number_of_lines + text

        else:

            return text + ["\n"] * number_of_lines

    def add_lines_if_shorter(self,
                             text: List[str],
                             required_length: int,
                             add_before_text: bool = False) -> List[str]:

        if len(text) == required_length:

            return text

        else:

            return self.add_empty_lines(text, required_length - len(text), add_before_text)

    @property
    def text_axis_x(self) -> List[str]:

        return self.add_lines_if_shorter(self._text_axis_x, self.axis_text_max_lines)

    @property
    def text_axis_y(self) -> List[str]:

        rotated_counterclockwise = self._text_rotation_y == 90

        return self.add_lines_if_shorter(self._text_axis_y, self.axis_text_max_lines,
                                         rotated_counterclockwise)

    def draw_axes_texts(self) -> None:

        QgsTextRenderer.drawText(self.transform.map(self.text_position_x), self.text_rotation_x,
                                 QgsTextRenderer.AlignCenter, self.text_axis_x, self.context,
                                 self.text_format, QgsTextRenderer.AlignBottom)

        QgsTextRenderer.drawText(self.transform.map(self.text_position_y), self.text_rotation_y,
                                 QgsTextRenderer.AlignCenter, self.text_axis_y, self.context,
                                 self.text_format, QgsTextRenderer.AlignBottom)

    def format_tick_value(self, value: float, precision: int) -> List[str]:

        self._numeric_format.setNumberDecimalPlaces(int(precision))

        value_str = self._numeric_format.formatDouble(value, self._numeric_format_context)

        return [value_str]

    @property
    def axis_tick_text_height(self) -> float:

        if self.add_axes_ticks_texts:

            return QgsTextRenderer.textHeight(self.context,
                                              self.text_format_ticks,
                                              textLines=self.format_tick_value(
                                                  self.texts_axis_x_ticks[0],
                                                  self.ticks_x_precision))

        else:

            return 0

    @property
    def axis_tick_last_y_value_width(self) -> float:

        if self.add_axes_ticks_texts and not self.use_category_midpoints:

            return QgsTextRenderer.textWidth(self.context,
                                             self.text_format_ticks,
                                             textLines=self.format_tick_value(
                                                 max(self.texts_axis_y_ticks),
                                                 self.ticks_y_precision))

        else:

            return 0

    @property
    def axis_tick_last_x_value_width(self) -> float:

        if self.add_axes_ticks_texts and not self.use_category_midpoints:

            return QgsTextRenderer.textWidth(self.context,
                                             self.text_format_ticks,
                                             textLines=self.format_tick_value(
                                                 max(self.texts_axis_x_ticks),
                                                 self.ticks_x_precision))

        else:

            return 0

    @property
    def axis_tick_last_value_max_width(self) -> float:

        return max(self.axis_tick_last_x_value_width, self.axis_tick_last_y_value_width)

    @property
    def axis_tick_text_height_with_margin(self) -> float:

        if self.add_axes_ticks_texts:

            return self.axis_tick_text_height + self._space_above_ticks

        else:

            return 0

    def position_axis_tick_x(self, index: int) -> QPointF:

        if not self.add_axes_texts:

            y = self.height - (self.margin)

        else:

            y = self.height - self.text_height_max_with_margin

        x = self.polygon_start_pos_x + index * self.size_constant

        if self.categories_midpoint:
            x += self.size_constant / 2

        return QPointF(x, y)

    def position_axis_tick_y(self, index: int) -> QPointF:

        x = self.text_height_max_with_margin + self.axis_tick_text_height

        y = index * self.size_constant

        if self.categories_midpoint:
            y += self.size_constant / 2

        if self.legend_rotated:

            x = self.text_height_max_with_margin

        else:

            if not self.axis_y_text_rotated_counterclockwise:

                if self.add_axes_texts is False:

                    x = self.text_height_max_with_margin + self.margin

                else:

                    x = self.text_height_max_with_margin

        return QPointF(x, y)

    @property
    def categories_midpoint(self) -> bool:
        return len(self.texts_axis_x_ticks) == math.sqrt(self._polygons_count)

    def draw_values(self) -> None:

        if self.add_axes_ticks_texts:

            for i, value in enumerate(self.texts_axis_x_ticks):

                text_position = self.position_axis_tick_x(i)

                QgsTextRenderer.drawText(self.transform.map(text_position), self.text_rotation_x,
                                         QgsTextRenderer.AlignCenter,
                                         self.format_tick_value(value, self.ticks_x_precision),
                                         self.context, self.text_format_ticks,
                                         QgsTextRenderer.AlignBottom)

            for i, value in enumerate(self.texts_axis_y_ticks):

                text_position = self.position_axis_tick_y(len(self.texts_axis_y_ticks) - i - 1)

                QgsTextRenderer.drawText(self.transform.map(text_position), self.text_rotation_y,
                                         QgsTextRenderer.AlignCenter,
                                         self.format_tick_value(value, self.ticks_y_precision),
                                         self.context, self.text_format_ticks,
                                         QgsTextRenderer.AlignBottom)

    def set_space_above_ticks(self, space: int) -> None:
        self._space_above_ticks = int(space)

    def draw_spacers(self, polygons):

        self.painter.save()

        spacer_size = int(self.size_constant * (self.color_separator_width_percent / 100))

        if spacer_size % 2 == 0:
            spacer_size += 1

        pen = QPen(self.color_separator_color, spacer_size, Qt.SolidLine)

        self.painter.setPen(pen)

        for polygon in polygons:

            polygon = QPolygonF(
                QRectF(self.polygon_start_pos_x + polygon.x * self.size_constant,
                       self.polygon_start_pos_y - (polygon.y + 1) * self.size_constant,
                       self.size_constant, self.size_constant))

            polygon = self.transform.map(polygon)

            points = []
            for i in range(polygon.count()):
                p = polygon.at(i)
                points.append(QgsPoint(p.x(), p.y()))

            line = QgsLineString(points)

            line.draw(self.painter)

        self.painter.restore()

    def draw_debug_lines(self):

        self.painter.save()

        pen = QPen(QColor(255, 0, 0, 255), 3, Qt.SolidLine)

        self.painter.setPen(pen)

        line = QgsLineString([
            QgsPoint(0, self.height - self.text_height_max),
            QgsPoint(self.width, self.height - self.text_height_max)
        ])

        line.draw(self.painter)

        line = QgsLineString(
            [QgsPoint(self.text_height_max, 0),
             QgsPoint(self.text_height_max, self.height)])

        line.draw(self.painter)

        # Lines
        pen = QPen(QColor(0, 255, 0, 255), 3, Qt.SolidLine)

        self.painter.setPen(pen)

        line = QgsLineString([
            QgsPoint(0, self.height - self.axis_text_tics_top),
            QgsPoint(self.width, self.height - self.axis_text_tics_top)
        ])

        line.draw(self.painter)

        line = QgsLineString(
            [QgsPoint(self.axis_text_tics_top, 0),
             QgsPoint(self.axis_text_tics_top, self.height)])

        line.draw(self.painter)

        self.painter.restore()

    def render_legend(self, context: QgsRenderContext, width: float, height: float,
                      renderer: BivariateRenderer) -> None:

        if self.use_category_midpoints:
            self.texts_axis_x_ticks = BivariateRenderer.classes_to_legend_midpoints(
                renderer.field_1_classes)
            self.texts_axis_y_ticks = BivariateRenderer.classes_to_legend_midpoints(
                renderer.field_2_classes)
        else:
            self.texts_axis_x_ticks = renderer.field_1_labels
            self.texts_axis_y_ticks = renderer.field_2_labels

        self.render(context, width, height, renderer.generate_legend_polygons())

    def render(self, context: QgsRenderContext, width: float, height: float,
               polygons: List[LegendPolygon]) -> None:

        self.context = context

        self._polygons_count = len(polygons)

        self.set_size_context(width, height)

        self._painter = context.painter()

        self._painter.save()

        self._painter.setPen(Qt.NoPen)

        self.set_text_height(self.axis_title_x.split("\n"), self.axis_title_y.split("\n"))

        self.draw_polygons(polygons)

        if self.add_colors_separators:
            self.draw_spacers(polygons)

        if self.add_axes_arrows:
            self.draw_axes_arrows()

        # https://github.com/qgis/QGIS/blob/5e98648913b82466ca9eb42ed68f4bb0b536ae96/src/core/layout/qgslayoutitemlabel.cpp#L147

        if self.add_axes_texts:
            self.draw_axes_texts()

        if self.add_axes_ticks_texts:
            self.draw_values()

        # self.draw_debug_lines()

        self.painter.restore()
