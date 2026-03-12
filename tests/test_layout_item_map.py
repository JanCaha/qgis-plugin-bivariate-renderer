from qgis.core import QgsFillSymbol, QgsLayout, QgsLayoutItemMap, QgsLayoutItemPage, QgsProject, QgsVectorLayer

from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from tests import assert_images_equal, export_page_to_image, prepare_bivariate_renderer


def test_generate_map_in_layout(
    nc_layer: QgsVectorLayer,
    qgs_layout: QgsLayout,
    qgs_project: QgsProject,
    layout_page_a4: QgsLayoutItemPage,
    layout_space,
    layout_dpmm: float,
):

    bivariate_renderer = prepare_bivariate_renderer(
        layer=nc_layer, field1="PERIMETER", field2="AREA", color_ramp=BivariateColorRampGreenPink()
    )

    nc_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(nc_layer)

    layout_item_map = QgsLayoutItemMap(qgs_layout)
    layout_item_map.setLayers([nc_layer])
    layout_item_map.attemptSetSceneRect(layout_space)
    layout_item_map.setCrs(nc_layer.crs())
    layout_item_map.zoomToExtent(nc_layer.extent())

    qgs_layout.addItem(layout_item_map)

    file = "./tests/images/image.png"

    export_page_to_image(qgs_layout, layout_page_a4, file, layout_dpmm)

    assert_images_equal(file, "./tests/images/correct/layout_item_map.png")


def test_polygon_symbol_used_in_feature_rendering(
    nc_layer: QgsVectorLayer,
    qgs_layout: QgsLayout,
    qgs_project: QgsProject,
    layout_page_a4: QgsLayoutItemPage,
    layout_space,
    layout_dpmm: float,
    custom_polygon_symbol: QgsFillSymbol,
):
    bivariate_renderer = prepare_bivariate_renderer(
        layer=nc_layer, field1="PERIMETER", field2="AREA", color_ramp=BivariateColorRampGreenPink()
    )
    bivariate_renderer.polygon_symbol = custom_polygon_symbol

    nc_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(nc_layer)

    layout_item_map = QgsLayoutItemMap(qgs_layout)
    layout_item_map.setLayers([nc_layer])
    layout_item_map.attemptSetSceneRect(layout_space)
    layout_item_map.setCrs(nc_layer.crs())
    layout_item_map.zoomToExtent(nc_layer.extent())

    qgs_layout.addItem(layout_item_map)

    file = "./tests/images/image.png"

    export_page_to_image(qgs_layout, layout_page_a4, file, layout_dpmm)

    assert_images_equal(file, "./tests/images/correct/layout_item_map_custom_symbol.png")
