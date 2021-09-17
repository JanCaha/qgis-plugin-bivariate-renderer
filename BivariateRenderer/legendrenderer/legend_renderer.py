from qgis.PyQt.QtCore import QPointF, QRectF, Qt
from qgis.PyQt.QtGui import QPolygonF, QBrush, QColor

from qgis.core import (QgsTextFormat,
                       QgsLineSymbol,
                       QgsRenderContext,
                       QgsTextRenderer)


class LegendRenderer:

    axis_title_x: str
    axis_title_y: str
    text_format: QgsTextFormat

    axis_line_symbol: QgsLineSymbol

    def __init__(self):

        self.axis_title_x = "Axis X"
        self.axis_title_y = "Axis Y"

        self.text_format = QgsTextFormat()

        self.axis_line_symbol = QgsLineSymbol.createSimple({})

    def render(self, contex: QgsRenderContext, width: float, height: float):

        width = width * contex.scaleFactor()
        height = height * contex.scaleFactor()

        painter = contex.painter()

        painter.save()

        # painter.scale(contex.scaleFactor(), contex.scaleFactor())

        # TODO do it around each drawing
        painter.save()
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(QRectF(20 * contex.scaleFactor(), 20 * contex.scaleFactor(),
                                50 * contex.scaleFactor(), 50 * contex.scaleFactor()))
        painter.restore()

        self.axis_line_symbol.startRender(contex)

        self.axis_line_symbol.renderPolyline(QPolygonF([QPointF(0 * contex.scaleFactor(), 0 * contex.scaleFactor()),
                                                        QPointF(60 * contex.scaleFactor(), 60 * contex.scaleFactor())]),
                                             None, contex)

        self.axis_line_symbol.stopRender(contex)

        QgsTextRenderer.drawText(QPointF(50 * contex.scaleFactor(), 50 * contex.scaleFactor()), 0, QgsTextRenderer.AlignCenter, [self.axis_title_x], contex, self.text_format)
        QgsTextRenderer.drawText(QPointF(10 * contex.scaleFactor(), 30 * contex.scaleFactor()), 0, QgsTextRenderer.AlignCenter, [self.axis_title_y], contex, self.text_format)

        painter.restore()

