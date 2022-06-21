from typing import Optional

from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtXml import QDomDocument, QDomElement
from qgis.core import (QgsLayoutItem, QgsLayout, QgsLayoutItemAbstractMetadata, QgsVectorLayer,
                       QgsTextFormat, QgsLayoutItemRenderContext, QgsLineSymbol,
                       QgsReadWriteContext, QgsSymbolLayerUtils, QgsSymbol, QgsProject,
                       QgsMapLayerType, QgsFillSymbol)

from ..text_constants import Texts, IDS
from ..utils import default_line_symbol, get_icon, log, get_symbol_dict
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

    symbol_rectangle_without_values: QgsFillSymbol
    replace_rectangle_without_values: bool
    use_rectangle_without_values_color_from_legend: bool

    legend_rotated: bool
    add_axes_arrows: bool
    add_axes_texts: bool
    add_axes_values_texts: bool
    add_colors_separators: bool

    y_axis_rotation: float

    ticks_x_precision: int
    ticks_y_precision: int

    space_above_ticks: int

    color_separator_width: float
    color_separator_color: QColor

    arrows_common_start_point: bool
    arrow_width: float

    ticks_use_category_midpoints: bool

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
        self.add_colors_separators = False

        self.arrows_common_start_point = False
        self.arrow_width = 5

        self.color_separator_width = 5
        self.color_separator_color = QColor("#ffffff")

        self.y_axis_rotation = 90

        self.ticks_x_precision = 2
        self.ticks_y_precision = 2

        self.space_above_ticks = 10

        self.ticks_use_category_midpoints = False

        self.symbol_rectangle_without_values = QgsFillSymbol.createSimple({
            "color": "255,255,255,0",
            'style': 'no',
            'outline_color': '247,247,247,0',
            'outline_style': 'solid',
            'outline_width': '0'
        })

        self.replace_rectangle_without_values = False
        self.use_rectangle_without_values_color_from_legend = False

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

        legend_render.add_colors_separators = self.add_colors_separators

        legend_render.color_separator_width_percent = self.color_separator_width
        legend_render.color_separator_color = self.color_separator_color

        legend_render.arrows_common_start_point = self.arrows_common_start_point

        legend_render.arrow_width_percent = self.arrow_width

        legend_render.use_category_midpoints = self.ticks_use_category_midpoints

        legend_render.replace_rectangle_without_values = self.replace_rectangle_without_values
        legend_render.use_rectangle_without_values_color_from_legend = self.use_rectangle_without_values_color_from_legend
        legend_render.symbol_rectangle_without_values = self.symbol_rectangle_without_values

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
        bivariate_legend_element.setAttribute("ticks_use_category_midpoints",
                                              str(self.ticks_use_category_midpoints))

        bivariate_legend_element.setAttribute("draw_colors_separators",
                                              str(self.add_colors_separators))
        bivariate_legend_element.setAttribute("color_separator_width",
                                              str(self.color_separator_width))
        bivariate_legend_element.setAttribute("color_separator_color",
                                              self.color_separator_color.name())

        bivariate_legend_element.setAttribute("arrows_common_start_point",
                                              str(self.arrows_common_start_point))
        bivariate_legend_element.setAttribute("arrow_width", str(self.arrow_width))

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

        bivariate_legend_element.setAttribute("replace_empty_rectangles",
                                              str(self.replace_rectangle_without_values))
        bivariate_legend_element.setAttribute(
            "empty_rectangle_use_legend_color",
            str(self.use_rectangle_without_values_color_from_legend))

        empty_polygon_symbol_elem = doc.createElement("emptyPolygonSymbol")

        symbol_elem = QgsSymbolLayerUtils.saveSymbol("", self.symbol_rectangle_without_values, doc,
                                                     context)

        empty_polygon_symbol_elem.appendChild(symbol_elem)

        bivariate_legend_element.appendChild(empty_polygon_symbol_elem)

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

        symbolElem = line_symbol_elem.firstChildElement("symbol")
        self.line_format = QgsSymbolLayerUtils.loadSymbol(symbolElem, context)

        text_format_node_list = element.elementsByTagName("text-style")

        text_format_elem = text_format_node_list.at(0).toElement()
        self.text_format.readXml(text_format_elem, context)

        self.text_axis_x = element.attribute("axis_x_name")
        self.text_axis_y = element.attribute("axis_y_name")

        self.ticks_x_precision = int(element.attribute("ticks_x_precision"))
        self.ticks_y_precision = int(element.attribute("ticks_y_precision"))

        self.space_above_ticks = int(element.attribute("space_above_ticks"))
        self.ticks_use_category_midpoints = element.attribute(
            "ticks_use_category_midpoints") == "True"

        self.legend_rotated = element.attribute("legend_rotated") == "True"

        self.add_axes_texts = element.attribute("draw_axes_text") == "True"

        self.add_axes_arrows = element.attribute("draw_axes_arrow") == "True"

        self.arrows_common_start_point = element.attribute("arrows_common_start_point") == "True"
        self.arrow_width = float(element.attribute("arrow_width"))

        self.y_axis_rotation = float(element.attribute("y_axis_rotation"))

        self.add_axes_values_texts = element.attribute("draw_axes_values_texts") == "True"

        axes_values_format_elem = element.firstChildElement("axesValuesFormat")

        text_format_elem = axes_values_format_elem.firstChildElement("text-style")

        if text_format_elem:

            self.text_values_format.readXml(text_format_elem, context)

        self.add_colors_separators = element.attribute("draw_colors_separators") == "True"
        self.color_separator_width = int(element.attribute("color_separator_width"))
        self.color_separator_color = QColor(element.attribute("color_separator_color"))

        self.replace_rectangle_without_values = element.attribute(
            "replace_empty_rectangles") == "True"
        self.use_rectangle_without_values_color_from_legend = element.attribute(
            "empty_rectangle_use_legend_color") == "True"

        empty_polygon_symbol_elem = element.firstChildElement("emptyPolygonSymbol")

        symbolElem = empty_polygon_symbol_elem.firstChildElement("symbol")
        self.symbol_rectangle_without_values = QgsSymbolLayerUtils.loadSymbol(symbolElem, context)

        return True

    def set_linked_layer(self, layer: QgsVectorLayer) -> None:
        self.layer = layer
        self.load_renderer_from_layer()
        self.layer.styleChanged.connect(self.load_renderer_from_layer)

    def load_renderer_from_layer(self) -> None:
        self.renderer = self.layer.renderer().clone()

        self.refresh()

    def set_y_axis_rotation(self, rotation: float) -> None:
        self.y_axis_rotation = rotation

        self.refresh()

    def set_axis_texts_settings(self, draw: bool, text_format: QgsTextFormat, axis_x_text: str,
                                axis_y_text: str) -> None:
        self.text_format = text_format.cl
        self.add_axes_texts = draw
        self.text_axis_x = axis_x_text
        self.text_axis_y = axis_y_text

        self.refresh()

    def set_legend_rotated(self, rotated: bool) -> None:
        self.legend_rotated = rotated

        self.refresh()

    def are_labels_default(self) -> bool:

        return self.text_axis_x == "Axis X" and self.text_axis_y == "Axis Y"

    def set_ticks_settings(self, draw: bool, text_format: QgsTextFormat, use_midpoint: bool,
                           axis_x_precision: int, axis_y_precision: int, space_above: int) -> None:
        self.add_axes_values_texts = draw
        self.text_values_format = text_format
        self.ticks_use_category_midpoints = use_midpoint
        self.space_above_ticks = int(space_above)
        self.ticks_x_precision = axis_x_precision
        self.ticks_y_precision = axis_y_precision

        self.refresh()

    def set_color_separator_settings(self, draw: bool, color: QColor, width: float) -> None:
        self.add_colors_separators = draw
        self.color_separator_color = color
        self.color_separator_width = width

        self.refresh()

    def set_arrows_settings(self, draw: bool, line_format: QgsLineSymbol, use_common_point: bool,
                            width: float) -> None:
        self.add_axes_arrows = draw
        self.arrows_common_start_point = use_common_point
        self.arrow_width = width
        self.line_format = line_format.clone()

        self.refresh()

    def set_rectangle_without_values_settings(self, use: bool, symbol: QgsFillSymbol,
                                              color_from_legend: bool) -> None:

        self.symbol_rectangle_without_values = symbol
        self.replace_rectangle_without_values = use
        self.use_rectangle_without_values_color_from_legend = color_from_legend

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
