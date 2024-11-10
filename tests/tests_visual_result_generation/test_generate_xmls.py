from qgis.core import QgsVectorLayer

from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from tests import xml_string


def test_generate_xml(nc_layer: QgsVectorLayer, prepare_bivariate_renderer):

    bivariate_renderer = prepare_bivariate_renderer(
        nc_layer, field1="AREA", field2="PERIMETER", color_ramp=BivariateColorRampGreenPink()
    )

    bivariate_renderer.generateCategories()

    xml = xml_string(bivariate_renderer)
    assert isinstance(xml, str)
    print(xml)
