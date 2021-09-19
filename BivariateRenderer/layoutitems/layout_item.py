from typing import NoReturn, List

from qgis.core import (QgsLayoutItem,
                       QgsLayout,
                       QgsLayoutItemAbstractMetadata,
                       QgsVectorLayer,
                       QgsTextFormat,
                       QgsLayoutItemRenderContext,
                       QgsLineSymbol)

from ..text_constants import Texts, IDS
from ..utils import log
from ..renderer.bivariate_renderer import BivariateRenderer

from ..legendrenderer.legend_renderer import LegendRenderer

DEFAULT_AXIS_X_TEXT = "Axis X"
DEFAULT_AXIS_Y_TEXT = "Axis Y"


class BivariateRendererLayoutItem(QgsLayoutItem):

    layer: QgsVectorLayer = None
    renderer: BivariateRenderer

    def __init__(self, layout: QgsLayout):

        super().__init__(layout)

        self.text_axis_x = "Axis X"
        self.text_axis_y = "Axis Y"
        self.text_format = QgsTextFormat()

        self.renderer = None

    def draw(self, context: QgsLayoutItemRenderContext) -> None:

        render_context = context.renderContext()

        legend_render = LegendRenderer()

        legend_render.axis_title_x = self.text_axis_x
        legend_render.axis_title_y = self.text_axis_y

        legend_render.text_format = self.text_format

        item_size = self.layout().convertToLayoutUnits(self.sizeWithUnits())

        if self.renderer:

            legend_render.render(render_context,
                                 item_size.width(),
                                 item_size.height(),
                                 self.renderer.generate_legend_polygons())

    # def writePropertiesToElement(self, element: QtXml.QDomElement, document: QtXml.QDomDocument, context: QgsReadWriteContext) -> bool:
    #     # todo add
    #     pass

    # def readPropertiesFromElement(self, element: QtXml.QDomElement, document: QtXml.QDomDocument, context: QgsReadWriteContext) -> bool:
    #     # todo add
    #     pass

    def set_linked_layer(self, layer: QgsVectorLayer) -> NoReturn:
        self.layer = layer
        self.renderer = layer.renderer().clone()

    def set_text_format(self, text_format: QgsTextFormat):
        self.text_format = text_format
        self.refresh()

    def set_axis_x_name(self, name: str) -> NoReturn:
        self.text_axis_x = name
        self.refresh()

    def set_axis_y_name(self, name: str) -> NoReturn:
        self.text_axis_y = name
        self.refresh()

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
