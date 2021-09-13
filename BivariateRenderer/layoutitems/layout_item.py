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

from ..text_constants import Texts
from ..utils import log
from ..renderer.bivariate_renderer import BivariateRenderer


class BivariateRendererLayoutItem(QgsLayoutItemGroup):

    layer: QgsVectorLayer = None
    text_axis_x: QgsLayoutItem = None

    def __init__(self, layout: QgsLayout):

        super().__init__(layout)

        self.layout = layout

        self.text_axis_x = QgsLayoutItemLabel(self.layout)
        self.text_axis_x.setText("Text Axis X")
        text_size: QRectF = self.text_axis_x.sizeForText()
        self.text_axis_x.setRect(0, 0, text_size.width(), text_size.height())
        self.text_axis_x.setReferencePoint(QgsLayoutItem.Middle)
        self.text_axis_x.setPos(50 - text_size.width() / 2, 110)

        self.text_axis_y = QgsLayoutItemLabel(self.layout)
        self.text_axis_y.setText("Text Axis Y")
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

    @property
    def linked_layer_name(self):

        if self.layer is not None:
            return self.layer.name()

        return None

    def type(self) -> int:
        return Texts.plot_item_bivariate_renderer_legend


class BivariateRendererLayoutItemMetadata(QgsLayoutItemAbstractMetadata):

    def __init__(self):
        super().__init__(Texts.plot_item_bivariate_renderer_legend, Texts.plot_item_bivariate_renderer)

    def createItem(self, layout):
        return BivariateRendererLayoutItem(layout)
