from qgis.core import QgsLayout, QgsLayoutItemMap, QgsLayoutItemPage, QgsProject, QgsVectorLayer

from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from tests import assert_images_equal


def test_generate_map_in_layout(
    nc_layer: QgsVectorLayer,
    qgs_layout: QgsLayout,
    qgs_project: QgsProject,
    layout_page_a4: QgsLayoutItemPage,
    prepare_bivariate_renderer,
    layout_space,
    export_page_to_image,
):

    bivariate_renderer = prepare_bivariate_renderer(
        nc_layer, field1="PERIMETER", field2="AREA", color_ramp=BivariateColorRampGreenPink()
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

    export_page_to_image(qgs_layout, layout_page_a4, file)

    assert_images_equal(file, "./tests/images/correct/layout_item_map.png")
