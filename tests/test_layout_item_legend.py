from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from BivariateRenderer.layoutitems.layout_item import BivariateRendererLayoutItem
from tests import assert_images_equal


def test_generate_legend_in_layout(qgis_countries_layer, qgs_layout, qgs_project, layout_page_a4,
                                   prepare_bivariate_renderer, layout_space, export_page_to_image):

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid",
                                                    color_ramp=BivariateColorRampGreenPink())

    qgis_countries_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(qgis_countries_layer)

    layout_item = BivariateRendererLayoutItem(qgs_layout)
    layout_item.set_linked_layer(qgis_countries_layer)

    layout_item.attemptSetSceneRect(layout_space)

    qgs_layout.addItem(layout_item)

    file = "./tests/images/image.png"

    export_page_to_image(qgs_layout, layout_page_a4, file)

    assert_images_equal(file, "./tests/images/correct/layout_item_legend.png")
