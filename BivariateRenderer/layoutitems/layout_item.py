from typing import NoReturn, List
from pathlib import Path

from PyQt5.QtCore import QSize, Qt, QCoreApplication, QRectF, QPoint, QPointF
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtGui import QPalette, QPolygonF, QColor, QTransform, QFont

from qgis.core import (QgsLayoutItemHtml,
                       QgsNetworkAccessManager,
QgsLayoutSize,
                       QgsLayoutItem,
                    QgsLayoutItemPicture,
QgsLayoutItemGroup,
QgsLayoutItemPolygon,
QgsLayoutItemPolyline,
QgsLayoutItemLabel,
QgsLayout,
QgsLayoutItemShape,
                       QgsLayoutItemAbstractMetadata,
                       QgsVectorLayer)

from ..text_constants import Texts, IDS
from ..utils import log
from ..renderer.bivariate_renderer import BivariateRenderer

DEFAULT_AXIS_X_TEXT = "Axis X"
DEFAULT_AXIS_Y_TEXT = "Axis Y"


class BivariateRendererLayoutItem(QgsLayoutItemGroup):

    layer: QgsVectorLayer = None
    renderer: BivariateRenderer

    text_axis_x: QgsLayoutItemLabel
    text_axis_y: QgsLayoutItemLabel

    axis_arrow_x: QgsLayoutItemPolyline
    axis_arrow_y: QgsLayoutItemPolyline

    rectangles: List[QgsLayoutItemPolygon] = []

    def __init__(self, layout: QgsLayout):

        super().__init__(layout)

        self.layout = layout

        self.text_axis_x = QgsLayoutItemLabel(self.layout)
        self.text_axis_x.setText(DEFAULT_AXIS_X_TEXT)
        text_size: QRectF = self.text_axis_x.sizeForText()
        self.text_axis_x.setRect(0, 0, text_size.width(), text_size.height())
        self.text_axis_x.setReferencePoint(QgsLayoutItem.Middle)
        self.text_axis_x.setPos(50 - text_size.width() / 2, 110)

        self.text_axis_y = QgsLayoutItemLabel(self.layout)
        self.text_axis_y.setText(DEFAULT_AXIS_Y_TEXT)
        text_size: QRectF = self.text_axis_y.sizeForText()
        self.text_axis_y.setRect(0, 0, text_size.width(), text_size.height())
        self.text_axis_y.setReferencePoint(QgsLayoutItem.Middle)
        self.text_axis_y.setPos(-10 - text_size.height(), 50 + text_size.width() / 2)
        self.text_axis_y.rotateItem(-90, self.text_axis_y.positionAtReferencePoint(self.referencePoint()))

        line_x = QPolygonF([QPointF(-5, 105),
                            QPointF(100, 105)])

        self.axis_arrow_x = QgsLayoutItemPolyline(line_x, self.layout)

        line_y = QPolygonF([QPointF(-5, 105),
                            QPointF(-5, 0)])

        self.axis_arrow_y = QgsLayoutItemPolyline(line_y, self.layout)

        self.layout.addItem(self.text_axis_y)
        self.layout.addItem(self.text_axis_x)
        self.layout.addItem(self.axis_arrow_x)
        self.layout.addItem(self.axis_arrow_y)

        # self.addItem(self.text_axis_y)
        # self.addItem(self.text_axis_x)
        
    def set_linked_layer(self, layer: QgsVectorLayer) -> NoReturn:
        self.layer = layer
        self.renderer = layer.renderer()

        if self.text_axis_x.text() == DEFAULT_AXIS_X_TEXT:
            self.set_axis_x_name(self.renderer.field_name_1)

        if self.text_axis_y.text() == DEFAULT_AXIS_Y_TEXT:
            self.set_axis_y_name(self.renderer.field_name_2)

        self.draw_polygons()

    def draw_polygons(self):

        if self.rectangles:

            for rect in self.rectangles:
                self.layout.removeItem(rect)

            self.rectangles = []

        if self.layer:

            polygons = self.renderer.generate_legend_polygons(0, 100, 0, 100)

            for poly in polygons:

                polygon_f = QPolygonF(QRectF(0, 0, poly.size, poly.size))

                polygon = QgsLayoutItemPolygon(polygon_f, self.layout)
                polygon.setPos(poly.x, poly.y)
                polygon.setSymbol(poly.symbol)

                self.rectangles.append(polygon)
                self.layout.addItem(polygon)

    def updated(self):
        self.update(self.rect())

    def set_font(self, font: QFont):

        self.text_axis_x.setFont(font)
        self.text_axis_y.setFont(font)

        self.update_axis_x_text_size()
        self.update_axis_y_text_size()

    def update_axis_x_text_size(self):
        text_size: QRectF = self.text_axis_x.sizeForText()
        self.text_axis_x.setRect(0, 0, text_size.width(), text_size.height())

    def update_axis_y_text_size(self):
        text_size: QRectF = self.text_axis_y.sizeForText()
        self.text_axis_y.setRect(0, 0, text_size.width(), text_size.height())

    def set_axis_x_name(self, name: str) -> NoReturn:
        self.text_axis_x.setText(name)
        self.update_axis_x_text_size()

    def set_axis_y_name(self, name: str) -> NoReturn:
        self.text_axis_y.setText(name)
        self.update_axis_y_text_size()

    @property
    def get_font(self):
        return self.text_axis_x.font()

    @property
    def linked_layer_name(self):

        if self.layer is not None:
            return self.layer.name()

        return None

    def type(self) -> int:
        return IDS.plot_item_bivariate_renderer_legend


class BivariateRendererLayoutItemMetadata(QgsLayoutItemAbstractMetadata):

    def __init__(self):
        super().__init__(IDS.plot_item_bivariate_renderer_legend, Texts.plot_item_bivariate_renderer)

    def createItem(self, layout):
        return BivariateRendererLayoutItem(layout)
