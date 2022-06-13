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

    bivariate_renderer.generateCategories()

    xml_renderer = """
<!DOCTYPE doc>
<renderer-v2 type="BivariateRenderer">
 <number_of_classes value="3"/>
 <classificationMethod id="EqualInterval">
  <symmetricMode symmetrypoint="0" astride="0" enabled="0"/>
  <labelFormat labelprecision="4" trimtrailingzeroes="1" format="%1 - %2"/>
  <parameters>
   <Option/>
  </parameters>
  <extraInformation/>
 </classificationMethod>
 <field_name_1 name="AREA"/>
 <field_name_2 name="PERIMETER"/>
 <colorramp name="color_ramp_1" type="gradient">
  <Option type="Map">
   <Option name="color1" type="QString" value="211,211,211,255"/>
   <Option name="color2" type="QString" value="76,172,38,255"/>
   <Option name="direction" type="QString" value="ccw"/>
   <Option name="discrete" type="QString" value="0"/>
   <Option name="rampType" type="QString" value="gradient"/>
   <Option name="spec" type="QString" value="rgb"/>
  </Option>
  <prop v="211,211,211,255" k="color1"/>
  <prop v="76,172,38,255" k="color2"/>
  <prop v="ccw" k="direction"/>
  <prop v="0" k="discrete"/>
  <prop v="gradient" k="rampType"/>
  <prop v="rgb" k="spec"/>
 </colorramp>
 <colorramp name="color_ramp_2" type="gradient">
  <Option type="Map">
   <Option name="color1" type="QString" value="211,211,211,255"/>
   <Option name="color2" type="QString" value="208,37,140,255"/>
   <Option name="direction" type="QString" value="ccw"/>
   <Option name="discrete" type="QString" value="0"/>
   <Option name="rampType" type="QString" value="gradient"/>
   <Option name="spec" type="QString" value="rgb"/>
  </Option>
  <prop v="211,211,211,255" k="color1"/>
  <prop v="208,37,140,255" k="color2"/>
  <prop v="ccw" k="direction"/>
  <prop v="0" k="discrete"/>
  <prop v="gradient" k="rampType"/>
  <prop v="rgb" k="spec"/>
 </colorramp>
 <ranges_1>
  <range_1 label="0,042 - 0,1083" lower="0.042" upper="0.10833333333333334"/>
  <range_1 label="0,1083 - 0,1747" lower="0.10833333333333334" upper="0.17466666666666666"/>
  <range_1 label="0,1747 - 0,241" lower="0.17466666666666666" upper="0.241"/>
 </ranges_1>
 <ranges_2>
  <range_2 label="0,999 - 1,8793" lower="0.999" upper="1.8793333333333333"/>
  <range_2 label="1,8793 - 2,7597" lower="1.8793333333333333" upper="2.7596666666666665"/>
  <range_2 label="2,7597 - 3,64" lower="2.7596666666666665" upper="3.64"/>
 </ranges_2>
 <color_mixing_method name="Blend Darken"/>
 <symbols>
  <symbol label="0-0" color="#d3d3d3"/>
  <symbol label="0-1" color="#d27cb0"/>
  <symbol label="0-2" color="#d0258c"/>
  <symbol label="1-0" color="#90c07c"/>
  <symbol label="1-1" color="#907c7c"/>
  <symbol label="1-2" color="#90257c"/>
  <symbol label="2-0" color="#4cac26"/>
  <symbol label="2-1" color="#4c7c26"/>
  <symbol label="2-2" color="#4c2526"/>
 </symbols>
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
