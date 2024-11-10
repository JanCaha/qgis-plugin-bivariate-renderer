import os

import pytest
from qgis.core import QgsVectorLayer

from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from BivariateRenderer.layoutitems.layout_item import BivariateRendererLayoutItem
from BivariateRenderer.layoutitems.layout_item_widget import BivariateRendererLayoutItemWidget
from BivariateRenderer.utils import default_line_symbol

env_value = os.getenv("BIVARIATE_GENERATE")

if env_value:
    generate_images = env_value.lower() == "true"
else:
    generate_images = False

skip_setting = pytest.mark.skipif(not generate_images, reason="do not generate with every run")


@skip_setting
def test_generate_widget_renderer(nc_layer: QgsVectorLayer, prepare_bivariate_renderer_widget):

    widget = prepare_bivariate_renderer_widget(nc_layer)

    widget.show()

    pixmap = widget.grab()

    pixmap.save("./tests/images/correct/widget_renderer.png", "png")


@skip_setting
def test_generate_widget_layout_item(
    qgis_countries_layer: QgsVectorLayer, qgs_layout, qgis_parent, qgs_project, prepare_bivariate_renderer
):

    qgs_project.addMapLayer(qgis_countries_layer)

    bivariate_renderer = prepare_bivariate_renderer(
        qgis_countries_layer, field1="fid", field2="fid", color_ramp=BivariateColorRampGreenPink()
    )

    qgis_countries_layer.setRenderer(bivariate_renderer)

    layout_item = BivariateRendererLayoutItem(qgs_layout)
    layout_item.set_linked_layer(qgis_countries_layer)

    widget = BivariateRendererLayoutItemWidget(None, layout_item)

    widget.show()

    pixmap = widget.grab()

    pixmap.save("./tests/images/correct/widget_layout_item.png", "png")


def test_z():
    pass
