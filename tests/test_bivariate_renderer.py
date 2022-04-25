from PyQt5.QtXml import QDomElement
from qgis.core import (QgsVectorLayer, QgsProject, QgsLayout, QgsReadWriteContext)
from qgis.PyQt.QtXml import QDomDocument

from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRampGreenPink
from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer

from tests import set_up_bivariate_renderer, save_layout_for_layer, assert_images_equal

import pytest


@pytest.mark.skip(reason="Problem with comparing the outcomes")
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


def test_functions(nc_layer: QgsVectorLayer):

    bivariate_renderer = set_up_bivariate_renderer(nc_layer,
                                                   field1="AREA",
                                                   field2="PERIMETER",
                                                   color_ramps=BivariateColorRampGreenPink())

    assert isinstance(bivariate_renderer.getLegendCategorySize(), int)
    assert bivariate_renderer.getLegendCategorySize() == 83

    categories = bivariate_renderer.getLegendCategories()

    assert isinstance(categories, dict)
    assert isinstance(categories[list(categories.keys())[0]], dict)
    assert "x" in categories[list(categories.keys())[0]].keys()
    assert "y" in categories[list(categories.keys())[0]].keys()
    assert "color" in categories[list(categories.keys())[0]].keys()

    xml_renderer = """<!DOCTYPE doc>
<renderer-v2 field_name_2="PERIMETER" field_name_1="AREA" classification_method_name="" type="BivariateRenderer" number_of_classes="3" color_mixing_method="Darken blend color mixing">
 <colorramp name="color_ramp_1" type="gradient">
  <Option type="Map">
   <Option value="243,243,243,255" name="color1" type="QString"/>
   <Option value="138,225,174,255" name="color2" type="QString"/>
   <Option value="0" name="discrete" type="QString"/>
   <Option value="gradient" name="rampType" type="QString"/>
  </Option>
  <prop k="color1" v="243,243,243,255"/>
  <prop k="color2" v="138,225,174,255"/>
  <prop k="discrete" v="0"/>
  <prop k="rampType" v="gradient"/>
 </colorramp>
 <colorramp name="color_ramp_2" type="gradient">
  <Option type="Map">
   <Option type="QString" value="243,243,243,255" name="color1"/>
   <Option type="QString" value="230,162,208,255" name="color2"/>
   <Option type="QString" value="0" name="discrete"/>
   <Option type="QString" value="gradient" name="rampType"/>
  </Option>
  <prop k="color1" v="243,243,243,255"/>
  <prop k="color2" v="230,162,208,255"/>
  <prop k="discrete" v="0"/>
  <prop k="rampType" v="gradient"/>
 </colorramp>
 <ranges_1>
  <range_1 lower="0.042" label="0.042 - 0.1083" upper="0.10833333333333334"/>
  <range_1 lower="0.10833333333333334" label="0.1083 - 0.1747" upper="0.17466666666666666"/>
  <range_1 lower="0.17466666666666666" label="0.1747 - 0.241" upper="0.241"/>
 </ranges_1>
 <ranges_2>
  <range_2 lower="0.999" label="0.999 - 1.8793" upper="1.8793333333333333"/>
  <range_2 lower="1.8793333333333333" label="1.8793 - 2.7597" upper="2.7596666666666665"/>
  <range_2 lower="2.7596666666666665" label="2.7597 - 3.64" upper="3.64"/>
 </ranges_2>
</renderer-v2>
"""

    xml = QDomDocument()
    xml.setContent(xml_renderer)
    element = xml.documentElement()

    renderer_from_xml = BivariateRenderer.create_render_from_element(element)

    assert renderer_from_xml
    assert bivariate_renderer == renderer_from_xml

    assert isinstance(bivariate_renderer.save(QDomDocument("doc"), QgsReadWriteContext()),
                      QDomElement)
