from typing import Optional

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtXml import QDomDocument, QDomElement
from qgis.core import (QgsLayoutItem, QgsLayout, QgsLayoutItemAbstractMetadata, QgsVectorLayer,
                       QgsTextFormat, QgsLayoutItemRenderContext, QgsLineSymbol,
                       QgsReadWriteContext, QgsSymbolLayerUtils, QgsSymbol, QgsProject,
                       QgsMapLayerType)

from ..text_constants import Texts, IDS
from ..utils import default_line_symbol, get_icon
from ..renderer.bivariate_renderer import BivariateRenderer

from ..legendrenderer.legend_renderer import LegendRenderer

DEFAULT_AXIS_X_TEXT = "Axis X"
DEFAULT_AXIS_Y_TEXT = "Axis Y"


class BivariateRendererLayoutItem(QgsLayoutItem):

    layer: QgsVectorLayer = None
    renderer: BivariateRenderer

    text_axis_x: str
    text_axis_y: str

    text_format: QgsTextFormat
    text_values_format: QgsTextFormat
    line_format: QgsSymbol

    legend_rotated: bool
    add_axes_arrows: bool
    add_axes_texts: bool
    add_axes_values_texts: bool

    y_axis_rotation: float

    ticks_x_precision: int
    ticks_y_precision: int

    space_above_ticks: int

    def __init__(self, layout: QgsLayout):

        super().__init__(layout)

        self.setBackgroundEnabled(False)

        self.text_axis_x = "Axis X"
        self.text_axis_y = "Axis Y"
        self.text_format = QgsTextFormat()
        self.text_values_format = QgsTextFormat()

        self.line_format = default_line_symbol().clone()

        self.renderer = None

        self.legend_rotated = False
        self.add_axes_arrows = True
        self.add_axes_texts = True
        self.add_axes_values_texts = False

        self.y_axis_rotation = 90

        self.ticks_x_precision = 2
        self.ticks_y_precision = 2

        self.space_above_ticks = 10

    def to_legend_renderer(self) -> LegendRenderer:

        legend_render = LegendRenderer()

        legend_render.axis_title_x = self.text_axis_x
        legend_render.axis_title_y = self.text_axis_y

        legend_render.text_format = self.text_format

        legend_render.axis_line_symbol = self.line_format

        legend_render.legend_rotated = self.legend_rotated

        legend_render.add_axes_texts = self.add_axes_texts

        legend_render.add_axes_arrows = self.add_axes_arrows

        legend_render.add_axes_ticks_texts = self.add_axes_values_texts

        legend_render.text_format_ticks = self.text_values_format

        legend_render.ticks_x_precision = self.ticks_x_precision
        legend_render.ticks_y_precision = self.ticks_y_precision

        legend_render.set_text_rotation_y(self.y_axis_rotation)

        legend_render.set_space_above_ticks(self.space_above_ticks)

        return legend_render

    def draw(self, context: QgsLayoutItemRenderContext) -> None:

        render_context = context.renderContext()

        item_size = self.layout().convertToLayoutUnits(self.sizeWithUnits())

        legend_render = self.to_legend_renderer()

        if self.renderer:

            legend_render.render_legend(render_context, item_size.width(), item_size.height(),
                                        self.renderer)

    def writePropertiesToElement(self, bivariate_legend_element: QDomElement, doc: QDomDocument,
                                 context: QgsReadWriteContext) -> bool:

        bivariate_legend_element.setAttribute("axis_x_name", self.text_axis_x)
        bivariate_legend_element.setAttribute("axis_y_name", self.text_axis_y)

        bivariate_legend_element.setAttribute("legend_rotated", str(self.legend_rotated))
        bivariate_legend_element.setAttribute("draw_axes_text", str(self.add_axes_texts))
        bivariate_legend_element.setAttribute("draw_axes_arrow", str(self.add_axes_arrows))
        bivariate_legend_element.setAttribute("draw_axes_values_texts",
                                              str(self.add_axes_values_texts))
        bivariate_legend_element.setAttribute("y_axis_rotation", str(self.y_axis_rotation))
        bivariate_legend_element.setAttribute("ticks_x_precision", str(self.ticks_x_precision))
        bivariate_legend_element.setAttribute("ticks_y_precision", str(self.ticks_y_precision))
        bivariate_legend_element.setAttribute("space_above_ticks", str(self.space_above_ticks))

        line_symbol = doc.createElement("lineSymbol")

        symbol_elem = QgsSymbolLayerUtils.saveSymbol("", self.line_format, doc, context)

        line_symbol.appendChild(symbol_elem)

        bivariate_legend_element.appendChild(line_symbol)

        text_elem = self.text_format.writeXml(doc, context)

        symbol_elem.appendChild(text_elem)

        text_axes_values_format = doc.createElement("axesValuesFormat")

        text_elem = self.text_values_format.writeXml(doc, context)

        text_axes_values_format.appendChild(text_elem)

        bivariate_legend_element.appendChild(text_axes_values_format)

        if self.layer:
            bivariate_legend_element.setAttribute("vectorLayerId", self.layer.id())

        return True

    def readPropertiesFromElement(self, element: QDomElement, document: QDomDocument,
                                  context: QgsReadWriteContext) -> bool:

        if self.linked_layer:
            self.layer = None

        if element.hasAttribute("vectorLayerId"):

            layerId = element.attribute("vectorLayerId")

            layer = QgsProject.instance().mapLayer(layerId)

            if layer:

                if layer.type() == QgsMapLayerType.VectorLayer:

                    if isinstance(layer.renderer(), BivariateRenderer):
                        self.set_linked_layer(layer)

        line_symbol_elem = element.firstChildElement("lineSymbol")

        if not line_symbol_elem.isNull():

            symbolElem = line_symbol_elem.firstChildElement("symbol")
            self.line_format = QgsSymbolLayerUtils.loadSymbol(symbolElem, context)

        text_format_node_list = element.elementsByTagName("text-style")

        if not text_format_node_list.isEmpty():

            text_format_elem = text_format_node_list.at(0).toElement()
            self.text_format.readXml(text_format_elem, context)

        self.text_axis_x = element.attribute("axis_x_name")
        self.text_axis_y = element.attribute("axis_y_name")

        if element.hasAttribute("ticks_x_precision"):

            self.ticks_x_precision = int(element.attribute("ticks_x_precision"))
            self.ticks_y_precision = int(element.attribute("ticks_y_precision"))

        if element.hasAttribute("space_above_ticks"):
            self.space_above_ticks = int(element.attribute("space_above_ticks"))

        if element.hasAttribute("legend_rotated"):

            self.legend_rotated = element.attribute("legend_rotated") == "True"

        else:
            self.legend_rotated = False

        if element.hasAttribute("draw_axes_text"):

            self.add_axes_texts = element.attribute("draw_axes_text") == "True"

        else:
            self.add_axes_texts = True

        if element.hasAttribute("draw_axes_arrow"):

            self.add_axes_arrows = element.attribute("draw_axes_arrow") == "True"

        else:
            self.add_axes_arrows = True

        if element.hasAttribute("y_axis_rotation"):

            self.y_axis_rotation = float(element.attribute("y_axis_rotation"))

        else:
            self.y_axis_rotation = 90

        if element.hasAttribute("draw_axes_values_texts"):

            self.add_axes_values_texts = element.attribute("draw_axes_values_texts") == "True"

        else:

            self.add_axes_values_texts = False

        axes_values_format_elem = element.firstChildElement("axesValuesFormat")

        if not axes_values_format_elem.isNull():

            text_format_elem = axes_values_format_elem.firstChildElement("text-style")

            if text_format_elem:

                self.text_values_format.readXml(text_format_elem, context)

        return True

    def set_linked_layer(self, layer: QgsVectorLayer) -> None:
        self.layer = layer
        self.load_renderer_from_layer()
        self.layer.styleChanged.connect(self.load_renderer_from_layer)

    def load_renderer_from_layer(self) -> None:
        self.renderer = self.layer.renderer().clone()

        self.refresh()

    def set_line_format(self, line_format: QgsLineSymbol) -> None:
        self.line_format = line_format.clone()

        self.refresh()

    def set_text_format(self, text_format: QgsTextFormat) -> None:
        self.text_format = text_format

        self.refresh()

    def set_text_values_format(self, text_format: QgsTextFormat) -> None:
        self.text_values_format = text_format

        self.refresh()

    def set_y_axis_rotation(self, rotation: float) -> None:
        self.y_axis_rotation = rotation

        self.refresh()

    def set_axis_x_name(self, name: str) -> None:
        self.text_axis_x = name

        self.refresh()

    def set_axis_y_name(self, name: str) -> None:
        self.text_axis_y = name

        self.refresh()

    def set_legend_rotated(self, rotated: bool) -> None:
        self.legend_rotated = rotated

        self.refresh()

    def are_labels_default(self) -> bool:

        return self.text_axis_x == "Axis X" and self.text_axis_y == "Axis Y"

    def set_draw_axes_text(self, draw: bool) -> None:
        self.add_axes_texts = draw

        self.refresh()

    def set_draw_axes_arrow(self, draw: bool) -> None:
        self.add_axes_arrows = draw

        self.refresh()

    def set_draw_axes_values(self, draw: bool) -> None:
        self.add_axes_values_texts = draw

        self.refresh()

    def set_ticks_precisions(self, axis_x_precision: int, axis_y_precision: int) -> None:
        self.ticks_x_precision = axis_x_precision
        self.ticks_y_precision = axis_y_precision

        self.refresh()

    def set_space_above_ticks(self, space: int) -> None:
        self.space_above_ticks = int(space)

        self.refresh()

    @property
    def get_font(self):
        return self.text_axis_x.font()

    @property
    def linked_layer(self) -> Optional[QgsVectorLayer]:

        if self.layer is not None:
            return self.layer

        return None

    @property
    def linked_layer_name(self):

        if self.layer is not None:
            return self.layer.name()

        return None

    def type(self) -> int:
        return IDS.plot_item_bivariate_renderer_legend

    def icon(self) -> QIcon:

        return get_icon("legend_icon.png")


class BivariateRendererLayoutItemMetadata(QgsLayoutItemAbstractMetadata):

    def __init__(self):
        super().__init__(IDS.plot_item_bivariate_renderer_legend,
                         Texts.plot_item_bivariate_renderer)

    def createItem(self, layout):
        return BivariateRendererLayoutItem(layout)
