from pathlib import Path
from typing import Callable, Union

from qgis.core import QgsLayout, QgsLayoutItemPage, QgsProject, QgsReadWriteContext, QgsVectorLayer
from qgis.PyQt.QtCore import QRectF
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtXml import QDomDocument

from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from BivariateRenderer.layoutitems.layout_item import BivariateRendererLayoutItem
from tests import assert_images_equal, export_page_to_image, prepare_bivariate_renderer


def test_generate_legend_in_layout(
    qgis_countries_layer: QgsVectorLayer,
    qgs_layout: QgsLayout,
    qgs_project: QgsProject,
    layout_page_a4: QgsLayoutItemPage,
    layout_space: QRectF,
    layout_dpmm: float,
):

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, "fid", "fid", BivariateColorRampGreenPink())

    qgis_countries_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(qgis_countries_layer)

    layout_item = BivariateRendererLayoutItem(qgs_layout)
    layout_item.set_linked_layer(qgis_countries_layer)

    layout_item.attemptSetSceneRect(layout_space)

    qgs_layout.addItem(layout_item)

    file = "./tests/images/image.png"

    export_page_to_image(qgs_layout, layout_page_a4, file, layout_dpmm)

    assert_images_equal(file, "./tests/images/correct/layout_item_legend.png")


def test_layout_item_xml_save_load(qgs_layout: QgsLayout):

    bivariate_legend_item = BivariateRendererLayoutItem(qgs_layout)

    bivariate_legend_item.text_axis_x = "Field A"
    bivariate_legend_item.text_axis_y = "Field B"
    bivariate_legend_item.legend_rotated = True
    bivariate_legend_item.add_axes_arrows = False
    bivariate_legend_item.add_axes_texts = True
    bivariate_legend_item.add_axes_values_texts = True
    bivariate_legend_item.add_colors_separators = True
    bivariate_legend_item.color_separator_width = 3.0
    bivariate_legend_item.color_separator_color = QColor("#ff0000")
    bivariate_legend_item.arrows_common_start_point = True
    bivariate_legend_item.arrow_width = 7.0
    bivariate_legend_item.y_axis_rotation = 45.0
    bivariate_legend_item.ticks_x_precision = 3
    bivariate_legend_item.ticks_y_precision = 1
    bivariate_legend_item.space_above_ticks = 5
    bivariate_legend_item.ticks_use_category_midpoints = True
    bivariate_legend_item.replace_rectangle_without_values = True
    bivariate_legend_item.use_rectangle_without_values_color_from_legend = True

    doc = QDomDocument("test")
    elem = doc.createElement("BivariateRendererLayoutItem")
    context = QgsReadWriteContext()

    bivariate_legend_item.writePropertiesToElement(elem, doc, context)

    bivariate_legend_item_restored = BivariateRendererLayoutItem(qgs_layout)
    bivariate_legend_item_restored.readPropertiesFromElement(elem, doc, context)

    assert bivariate_legend_item_restored.text_axis_x == bivariate_legend_item.text_axis_x
    assert bivariate_legend_item_restored.text_axis_y == bivariate_legend_item.text_axis_y
    assert bivariate_legend_item_restored.legend_rotated == bivariate_legend_item.legend_rotated
    assert bivariate_legend_item_restored.add_axes_arrows == bivariate_legend_item.add_axes_arrows
    assert bivariate_legend_item_restored.add_axes_texts == bivariate_legend_item.add_axes_texts
    assert bivariate_legend_item_restored.add_axes_values_texts == bivariate_legend_item.add_axes_values_texts
    assert bivariate_legend_item_restored.add_colors_separators == bivariate_legend_item.add_colors_separators
    assert bivariate_legend_item_restored.color_separator_width == bivariate_legend_item.color_separator_width
    assert (
        bivariate_legend_item_restored.color_separator_color.name()
        == bivariate_legend_item.color_separator_color.name()
    )
    assert bivariate_legend_item_restored.arrows_common_start_point == bivariate_legend_item.arrows_common_start_point
    assert bivariate_legend_item_restored.arrow_width == bivariate_legend_item.arrow_width
    assert bivariate_legend_item_restored.y_axis_rotation == bivariate_legend_item.y_axis_rotation
    assert bivariate_legend_item_restored.ticks_x_precision == bivariate_legend_item.ticks_x_precision
    assert bivariate_legend_item_restored.ticks_y_precision == bivariate_legend_item.ticks_y_precision
    assert bivariate_legend_item_restored.space_above_ticks == bivariate_legend_item.space_above_ticks
    assert (
        bivariate_legend_item_restored.ticks_use_category_midpoints
        == bivariate_legend_item.ticks_use_category_midpoints
    )
    assert (
        bivariate_legend_item_restored.replace_rectangle_without_values
        == bivariate_legend_item.replace_rectangle_without_values
    )
    assert (
        bivariate_legend_item_restored.use_rectangle_without_values_color_from_legend
        == bivariate_legend_item.use_rectangle_without_values_color_from_legend
    )
