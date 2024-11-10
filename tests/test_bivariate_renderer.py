from PyQt5.QtXml import QDomElement
from qgis.core import QgsProject, QgsReadWriteContext, QgsVectorLayer
from qgis.PyQt.QtXml import QDomDocument

from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRampGreenPink
from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer
from tests import assert_images_equal


def test_layer_bivariate_render(nc_layer: QgsVectorLayer, qgs_project: QgsProject,
                                prepare_bivariate_renderer, save_layout_for_layer):

    bivariate_renderer = prepare_bivariate_renderer(nc_layer,
                                                    field1="AREA",
                                                    field2="PERIMETER",
                                                    color_ramp=BivariateColorRampGreenPink())

    nc_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(nc_layer)

    rendered_layout = "./tests/images/image.png"

    save_layout_for_layer(nc_layer, rendered_layout)

    assert_images_equal("tests/images/correct/layout_polygons_render.png", rendered_layout)


def test_functions(nc_layer: QgsVectorLayer, prepare_bivariate_renderer):

    bivariate_renderer = prepare_bivariate_renderer(nc_layer,
                                                    field1="AREA",
                                                    field2="PERIMETER",
                                                    color_ramp=BivariateColorRampGreenPink())

    xml_renderer = """
    <!DOCTYPE doc>
    <renderer-v2 type="BivariateRenderer">
     <number_of_classes value="3"/>
     <classificationMethod id="EqualInterval">
      <symmetricMode enabled="0" astride="0" symmetrypoint="0"/>
      <labelFormat trimtrailingzeroes="1" labelprecision="4" format="%1 - %2"/>
      <parameters>
       <Option/>
      </parameters>
      <extraInformation/>
     </classificationMethod>
     <field_name_1 name="AREA"/>
     <field_name_2 name="PERIMETER"/>
     <colorramp type="gradient" name="color_ramp_1">
      <Option type="Map">
       <Option type="QString" value="211,211,211,255" name="color1"/>
       <Option type="QString" value="76,172,38,255" name="color2"/>
       <Option type="QString" value="0" name="discrete"/>
       <Option type="QString" value="gradient" name="rampType"/>
      </Option>
      <prop k="color1" v="211,211,211,255"/>
      <prop k="color2" v="76,172,38,255"/>
      <prop k="discrete" v="0"/>
      <prop k="rampType" v="gradient"/>
     </colorramp>
     <colorramp type="gradient" name="color_ramp_2">
      <Option type="Map">
       <Option type="QString" value="211,211,211,255" name="color1"/>
       <Option type="QString" value="208,37,140,255" name="color2"/>
       <Option type="QString" value="0" name="discrete"/>
       <Option type="QString" value="gradient" name="rampType"/>
      </Option>
      <prop k="color1" v="211,211,211,255"/>
      <prop k="color2" v="208,37,140,255"/>
      <prop k="discrete" v="0"/>
      <prop k="rampType" v="gradient"/>
     </colorramp>
     <ranges_1>
      <range_1 label="0.042 - 0.1083" lower="0.042" upper="0.10833333333333334"/>
      <range_1 label="0.1083 - 0.1747" lower="0.10833333333333334" upper="0.17466666666666666"/>
      <range_1 label="0.1747 - 0.241" lower="0.17466666666666666" upper="0.241"/>
     </ranges_1>
     <ranges_2>
      <range_2 label="0.999 - 1.8793" lower="0.999" upper="1.8793333333333333"/>
      <range_2 label="1.8793 - 2.7597" lower="1.8793333333333333" upper="2.7596666666666665"/>
      <range_2 label="2.7597 - 3.64" lower="2.7596666666666665" upper="3.64"/>
     </ranges_2>
     <color_mixing_method name="Blend Darken"/>
     <symbols>
      <symbol color="#d3d3d3" label="1-1"/>
      <symbol color="#d27cb0" label="1-2"/>
      <symbol color="#d0258c" label="1-3"/>
      <symbol color="#90c07c" label="2-1"/>
      <symbol color="#907c7c" label="2-2"/>
      <symbol color="#90257c" label="2-3"/>
      <symbol color="#4cac26" label="3-1"/>
      <symbol color="#4c7c26" label="3-2"/>
      <symbol color="#4c2526" label="3-3"/>
     </symbols>
     <existing_labels value=""/>
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
