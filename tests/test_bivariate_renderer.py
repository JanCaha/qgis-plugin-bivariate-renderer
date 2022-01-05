from qgis.core import (QgsVectorLayer, QgsProject, QgsLayout)

from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRampGreenPink

from tests import set_up_bivariate_renderer, save_layout_for_layer, assert_images_equal


def test_layer_bivariate_render(nc_layer: QgsVectorLayer, qgs_project: QgsProject,
                                qgs_layout: QgsLayout):

    bivariate_renderer = set_up_bivariate_renderer(nc_layer,
                                                   field1="AREA",
                                                   field2="PERIMETER",
                                                   color_ramps=BivariateColorRampGreenPink())

    nc_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(nc_layer)

    rendered_layout = "./tests/images/image.png"

    save_layout_for_layer(nc_layer, qgs_layout, rendered_layout)

    assert_images_equal("tests/images/correct/layout_polygons_render.png", rendered_layout)
