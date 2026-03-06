from typing import Callable

from qgis.core import QgsReadWriteContext, QgsRenderContext, QgsVectorLayer
from qgis.PyQt.QtXml import QDomDocument, QDomElement

from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampCyanViolet
from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRampGreenPink
from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer


def test_functions(
    nc_layer: QgsVectorLayer,
    prepare_bivariate_renderer: Callable[..., BivariateRenderer],
):

    bivariate_renderer = prepare_bivariate_renderer(
        nc_layer, field1="AREA", field2="PERIMETER", color_ramp=BivariateColorRampGreenPink()
    )

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

    renderer_from_xml = BivariateRenderer.create_render_from_element(element, QgsReadWriteContext())

    assert renderer_from_xml
    assert bivariate_renderer == renderer_from_xml

    assert isinstance(bivariate_renderer.save(QDomDocument("doc"), QgsReadWriteContext()), QDomElement)


def test_eq(
    nc_layer: QgsVectorLayer,
    prepare_bivariate_renderer: Callable[..., BivariateRenderer],
):

    # same renderer
    renderer = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")

    assert renderer == renderer

    # compare two empty renderers
    renderer1 = BivariateRenderer()
    renderer2 = BivariateRenderer()

    assert renderer1 == renderer2

    # compare cloned renderer
    renderer = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")

    cloned = renderer.clone()

    assert cloned == renderer

    # different field names
    renderer1 = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")
    renderer2 = prepare_bivariate_renderer(nc_layer, field1="PERIMETER", field2="AREA")

    assert renderer1 != renderer2

    # compare not a renderer
    renderer = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")

    assert renderer != "not a renderer"
    assert renderer != 42
    assert renderer != None

    # one setup and one empty renderer
    renderer_with_data = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")
    renderer_empty = BivariateRenderer()
    renderer_empty.setFieldName1("AREA")
    renderer_empty.setFieldName2("PERIMETER")

    assert renderer_with_data != renderer_empty


def test_clone(
    nc_layer: QgsVectorLayer,
    prepare_bivariate_renderer: Callable[..., BivariateRenderer],
):

    # preserve field names
    renderer = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")

    cloned = renderer.clone()

    assert cloned.field_name_1 == renderer.field_name_1
    assert cloned.field_name_2 == renderer.field_name_2

    # preserve classification ranges
    renderer = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")

    cloned = renderer.clone()

    assert len(cloned.field_1_classes) == len(renderer.field_1_classes)
    assert len(cloned.field_2_classes) == len(renderer.field_2_classes)

    for orig, copy in zip(renderer.field_1_classes, cloned.field_1_classes):
        assert orig.lowerBound() == copy.lowerBound()
        assert orig.upperBound() == copy.upperBound()

    # test cloned is independent of original
    renderer = prepare_bivariate_renderer(
        nc_layer, field1="AREA", field2="PERIMETER", color_ramp=BivariateColorRampGreenPink()
    )

    cloned_renderer = renderer.clone()
    cloned_renderer.setFieldName1("PERIMETER")
    cloned_renderer.set_bivariate_color_ramp(BivariateColorRampCyanViolet())

    assert renderer.field_name_1 == "AREA"
    assert renderer.bivariate_color_ramp.name == BivariateColorRampGreenPink().name


def test_labels_existing_preserved_through_save_load(
    nc_layer: QgsVectorLayer,
    prepare_bivariate_renderer: Callable[..., BivariateRenderer],
):

    renderer = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")

    for feature in nc_layer.getFeatures():
        renderer.symbolForFeature(feature, QgsRenderContext())

    labels_before = set(renderer.labels_existing)

    doc = QDomDocument("doc")
    context = QgsReadWriteContext()
    elem = renderer.save(doc, context)

    loaded = BivariateRenderer.create_render_from_element(elem, context)

    assert set(loaded.labels_existing) == labels_before


def test_labels_existing_not_inflated_by_legend_drawing(
    nc_layer: QgsVectorLayer,
    prepare_bivariate_renderer: Callable[..., BivariateRenderer],
):

    renderer = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")

    for feature in nc_layer.getFeatures():
        renderer.symbolForFeature(feature, QgsRenderContext())

    labels_before = set(renderer.labels_existing)

    # generate_legend_polygons calls symbol_for_values for all combinations,
    # which inflates cached_symbols — labels_existing must stay unchanged
    renderer.generate_legend_polygons()

    assert set(renderer.labels_existing) == labels_before

    doc = QDomDocument("doc")
    context = QgsReadWriteContext()
    elem = renderer.save(doc, context)

    loaded = BivariateRenderer.create_render_from_element(elem, context)

    # after save/load, only actual data combinations should be in labels_existing
    all_combinations = {
        renderer.getPositionValuesCombinationHash(x, y)
        for x in range(len(renderer.field_1_classes))
        for y in range(len(renderer.field_2_classes))
    }
    assert set(loaded.labels_existing) == labels_before
    assert set(loaded.labels_existing) != all_combinations or len(labels_before) == len(all_combinations)


def test_populate_labels_existing_from_layer_matches_feature_rendering(
    nc_layer: QgsVectorLayer,
    prepare_bivariate_renderer: Callable[..., BivariateRenderer],
):

    renderer_from_symbol_for_feature = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")
    for feature in nc_layer.getFeatures():
        renderer_from_symbol_for_feature.symbolForFeature(feature, QgsRenderContext())

    renderer_from_layer_scan = prepare_bivariate_renderer(nc_layer, field1="AREA", field2="PERIMETER")
    renderer_from_layer_scan.populate_labels_existing_from_layer(nc_layer)

    assert set(renderer_from_layer_scan.labels_existing) == set(renderer_from_symbol_for_feature.labels_existing)
