from PyQt5.QtXml import QDomElement
from qgis.core import (QgsVectorLayer, QgsProject, QgsLayout, QgsReadWriteContext)
from qgis.PyQt.QtXml import QDomDocument

from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRampGreenPink
from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer

from tests import assert_images_equal, xml_string

import pytest


@pytest.mark.skip(reason="Problem with comparing the outcomes")
def test_layer_bivariate_render(nc_layer: QgsVectorLayer, qgs_project: QgsProject,
                                qgs_layout: QgsLayout, prepare_bivariate_renderer,
                                save_layout_for_layer):

    bivariate_renderer = prepare_bivariate_renderer(nc_layer,
                                                    field1="AREA",
                                                    field2="PERIMETER",
                                                    color_ramps=BivariateColorRampGreenPink())

    nc_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(nc_layer)

    rendered_layout = "./tests/images/image.png"

    save_layout_for_layer(nc_layer, qgs_layout, rendered_layout)

    assert_images_equal("tests/images/correct/layout_polygons_render.png", rendered_layout)


def test_functions(nc_layer: QgsVectorLayer, prepare_bivariate_renderer):

    bivariate_renderer = prepare_bivariate_renderer(nc_layer,
                                                    field1="AREA",
                                                    field2="PERIMETER",
                                                    color_ramps=BivariateColorRampGreenPink())

    categories = bivariate_renderer.getLegendCategories()

    assert isinstance(categories, dict)
    assert isinstance(categories[list(categories.keys())[0]], dict)
    assert "color" in categories[list(categories.keys())[0]].keys()

    xml_renderer = """
<!DOCTYPE doc>
<renderer-v2 type="BivariateRenderer">
 <number_of_classes value="3"/>
 <classificationMethod id="EqualInterval">
  <symmetricMode symmetrypoint="0" enabled="0" astride="0"/>
  <labelFormat format="%1 - %2" trimtrailingzeroes="1" labelprecision="4"/>
  <parameters>
   <Option/>
  </parameters>
  <extraInformation/>
 </classificationMethod>
 <field_name_1 name="AREA"/>
 <field_name_2 name="PERIMETER"/>
 <colorramp type="gradient" name="color_ramp_1">
  <Option type="Map">
   <Option type="QString" name="color1" value="211,211,211,255"/>
   <Option type="QString" name="color2" value="76,172,38,255"/>
   <Option type="QString" name="direction" value="ccw"/>
   <Option type="QString" name="discrete" value="0"/>
   <Option type="QString" name="rampType" value="gradient"/>
   <Option type="QString" name="spec" value="rgb"/>
  </Option>
  <prop v="211,211,211,255" k="color1"/>
  <prop v="76,172,38,255" k="color2"/>
  <prop v="ccw" k="direction"/>
  <prop v="0" k="discrete"/>
  <prop v="gradient" k="rampType"/>
  <prop v="rgb" k="spec"/>
 </colorramp>
 <colorramp type="gradient" name="color_ramp_2">
  <Option type="Map">
   <Option type="QString" name="color1" value="211,211,211,255"/>
   <Option type="QString" name="color2" value="208,37,140,255"/>
   <Option type="QString" name="direction" value="ccw"/>
   <Option type="QString" name="discrete" value="0"/>
   <Option type="QString" name="rampType" value="gradient"/>
   <Option type="QString" name="spec" value="rgb"/>
  </Option>
  <prop v="211,211,211,255" k="color1"/>
  <prop v="208,37,140,255" k="color2"/>
  <prop v="ccw" k="direction"/>
  <prop v="0" k="discrete"/>
  <prop v="gradient" k="rampType"/>
  <prop v="rgb" k="spec"/>
 </colorramp>
 <ranges_1>
  <range_1 upper="0.10833333333333334" label="0,042 - 0,1083" lower="0.042"/>
  <range_1 upper="0.17466666666666666" label="0,1083 - 0,1747" lower="0.10833333333333334"/>
  <range_1 upper="0.241" label="0,1747 - 0,241" lower="0.17466666666666666"/>
 </ranges_1>
 <ranges_2>
  <range_2 upper="1.8793333333333333" label="0,999 - 1,8793" lower="0.999"/>
  <range_2 upper="2.7596666666666665" label="1,8793 - 2,7597" lower="1.8793333333333333"/>
  <range_2 upper="3.64" label="2,7597 - 3,64" lower="2.7596666666666665"/>
 </ranges_2>
 <color_mixing_method name="Darken blend color mixing"/>
</renderer-v2>
"""

    xml = QDomDocument()
    xml.setContent(xml_renderer)
    element = xml.documentElement()

    renderer_from_xml = BivariateRenderer.create_render_from_element(element,
                                                                     QgsReadWriteContext())

    assert renderer_from_xml
    assert bivariate_renderer == renderer_from_xml

    assert isinstance(bivariate_renderer.save(QDomDocument("doc"), QgsReadWriteContext()),
                      QDomElement)
