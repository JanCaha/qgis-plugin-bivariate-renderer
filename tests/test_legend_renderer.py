from qgis.core import (QgsTextFormat, QgsLayoutUtils)
from qgis.PyQt.QtGui import QColor

from BivariateRenderer.legendrenderer.legend_renderer import LegendRenderer
from BivariateRenderer.colormixing.color_mixing_method import ColorMixingMethodDirect
from BivariateRenderer.utils import get_symbol_dict

from tests import (xml_string, assert_images_equal)


def test_default_values():

    legend_renderer = LegendRenderer()

    assert legend_renderer.axis_title_x == "Axis X"
    assert legend_renderer.axis_title_y == "Axis Y"

    assert xml_string(legend_renderer.text_format) == xml_string(QgsTextFormat())

    assert get_symbol_dict(legend_renderer.axis_line_symbol)["layers_list"] == [{
        'type_layer': 'ArrowLine',
        'properties_layer': {
            'arrow_start_width': '0.8',
            'arrow_start_width_unit': 'MM',
            'arrow_start_width_unit_scale': '3x:0,0,0,0,0,0',
            'arrow_type': '0',
            'arrow_width': '0.8',
            'arrow_width_unit': 'MM',
            'arrow_width_unit_scale': '3x:0,0,0,0,0,0',
            'head_length': '3',
            'head_length_unit': 'MM',
            'head_length_unit_scale': '3x:0,0,0,0,0,0',
            'head_thickness': '2',
            'head_thickness_unit': 'MM',
            'head_thickness_unit_scale': '3x:0,0,0,0,0,0',
            'head_type': '0',
            'is_curved': '1',
            'is_repeated': '1',
            'offset': '0',
            'offset_unit': 'MM',
            'offset_unit_scale': '3x:0,0,0,0,0,0',
            'ring_filter': '0'
        }
    }]

    assert QColor(0, 0, 0).name() == legend_renderer.axis_line_symbol.color().name()

    assert legend_renderer.legend_rotated is False
    assert legend_renderer.add_axes_arrows is False
    assert legend_renderer.add_axes_texts is False


def test_just_legend(qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage,
                     prepare_bivariate_renderer, prepare_painter):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.render(render_context,
                           image.width() / render_context.scaleFactor(),
                           image.width() / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_only.png", "tests/images/image.png")


def test_legend_with_arrows(qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage,
                            prepare_bivariate_renderer, prepare_painter):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.render(render_context,
                           image.width() / render_context.scaleFactor(),
                           image.width() / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_arrows.png", "tests/images/image.png")


def test_legend_with_arrows_texts(qgis_countries_layer, qgs_project, qgs_layout,
                                  prepare_default_QImage, prepare_bivariate_renderer,
                                  prepare_painter):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.render(render_context,
                           image.width() / render_context.scaleFactor(),
                           image.width() / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_arrows_texts.png",
                        "tests/images/image.png")


def test_legend_with_arrows_texts_rotated(qgis_countries_layer, qgs_project, qgs_layout,
                                          prepare_default_QImage, prepare_bivariate_renderer,
                                          prepare_painter):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.legend_rotated = True
    legend_renderer.render(render_context,
                           image.width() / render_context.scaleFactor(),
                           image.width() / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_arrows_texts_rotated.png",
                        "tests/images/image.png")


def test_legend_ticks(qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage,
                      prepare_bivariate_renderer, prepare_painter):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")

    bivariate_renderer.color_mixing_method = ColorMixingMethodDirect()

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = False
    legend_renderer.add_axes_texts = False
    legend_renderer.legend_rotated = False
    legend_renderer.add_axes_ticks_texts = True
    legend_renderer.texts_axis_x_ticks = bivariate_renderer.field_1_labels
    legend_renderer.texts_axis_y_ticks = bivariate_renderer.field_2_labels

    legend_renderer.render(render_context,
                           image.width() / render_context.scaleFactor(),
                           image.width() / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_values_ticks.png",
                        "tests/images/image.png")


def test_legend_all(qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage,
                    prepare_bivariate_renderer, prepare_painter):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.legend_rotated = False
    legend_renderer.add_axes_ticks_texts = True
    legend_renderer.texts_axis_x_ticks = bivariate_renderer.field_1_labels
    legend_renderer.texts_axis_y_ticks = bivariate_renderer.field_2_labels

    legend_renderer.render(render_context,
                           image.width() / render_context.scaleFactor(),
                           image.width() / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_all.png", "tests/images/image.png")


def test_legend_all_rotated(qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage,
                            prepare_bivariate_renderer, prepare_painter):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")

    bivariate_renderer.color_mixing_method = ColorMixingMethodDirect()

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.legend_rotated = True
    legend_renderer.add_axes_ticks_texts = True
    legend_renderer.texts_axis_x_ticks = bivariate_renderer.field_1_labels
    legend_renderer.texts_axis_y_ticks = bivariate_renderer.field_2_labels

    legend_renderer.render(render_context,
                           image.width() / render_context.scaleFactor(),
                           image.width() / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_all_rotated.png",
                        "tests/images/image.png")


def test_legend_with_spacer(qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage,
                            prepare_bivariate_renderer, prepare_painter):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")

    legend_renderer = LegendRenderer()

    legend_renderer.add_colors_separators = True
    legend_renderer.color_separator_width_percent = 5

    legend_renderer.render(render_context,
                           image.width() / render_context.scaleFactor(),
                           image.width() / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_spacer.png", "tests/images/image.png")
