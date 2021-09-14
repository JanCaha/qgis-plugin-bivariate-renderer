from typing import NoReturn, List
from pathlib import Path

from PyQt5.QtCore import QSize, Qt, QCoreApplication, QRectF, QPoint, QPointF
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtGui import QPalette, QPolygonF, QColor, QTransform

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

    axis_x_name: str
    axis_y_name: str

    text_axis_x: QgsLayoutItem = None

    def __init__(self, layout: QgsLayout):

        super().__init__(layout)

        self.layout = layout

        self.axis_x_name = DEFAULT_AXIS_X_TEXT
        self.axis_y_name = DEFAULT_AXIS_Y_TEXT

        self.text_axis_x = QgsLayoutItemLabel(self.layout)
        self.text_axis_x.setText(self.axis_x_name)
        text_size: QRectF = self.text_axis_x.sizeForText()
        self.text_axis_x.setRect(0, 0, text_size.width(), text_size.height())
        self.text_axis_x.setReferencePoint(QgsLayoutItem.Middle)
        self.text_axis_x.setPos(50 - text_size.width() / 2, 110)

        self.text_axis_y = QgsLayoutItemLabel(self.layout)
        self.text_axis_y.setText(self.axis_y_name)
        text_size: QRectF = self.text_axis_y.sizeForText()
        self.text_axis_y.setRect(0, 0, text_size.width(), text_size.height())
        self.text_axis_y.setReferencePoint(QgsLayoutItem.Middle)
        self.text_axis_y.setPos(-10, 50)
        self.text_axis_y.rotateItem(-90, self.text_axis_y.positionAtReferencePoint(self.referencePoint()))

        self.layout.addItem(self.text_axis_y)
        self.layout.addItem(self.text_axis_x)

        self.addItem(self.text_axis_y)
        self.addItem(self.text_axis_x)
        
    def set_linked_layer(self, layer: QgsVectorLayer) -> NoReturn:
        self.layer = layer
        self.renderer = layer.renderer()

        if self.axis_x_name == DEFAULT_AXIS_X_TEXT:
            self.set_axis_x_name(self.renderer.field_name_1)

        if self.axis_y_name == DEFAULT_AXIS_Y_TEXT:
            self.set_axis_y_name(self.renderer.field_name_2)

    def updated(self):
        self.update(self.rect())

    def set_axis_x_name(self, name: str) -> NoReturn:
        self.text_axis_x.setText(name)
        text_size: QRectF = self.text_axis_x.sizeForText()
        self.text_axis_x.setRect(0, 0, text_size.width(), text_size.height())

    def set_axis_y_name(self, name: str) -> NoReturn:
        self.text_axis_y.setText(name)
        text_size: QRectF = self.text_axis_y.sizeForText()
        self.text_axis_y.setRect(0, 0, text_size.width(), text_size.height())

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
