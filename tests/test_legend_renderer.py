from qgis.core import QgsLayoutUtils, QgsRenderContext
from qgis.PyQt.QtGui import QColor

from BivariateRenderer.colormixing.color_mixing_method import ColorMixingMethodDirect
from BivariateRenderer.legendrenderer.legend_renderer import LegendRenderer
from BivariateRenderer.renderer.bivariate_renderer_utils import classes_to_legend_midpoints
from tests import assert_images_equal


def test_just_legend(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_only.png", "tests/images/image.png")


def test_legend_with_arrows(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_arrows.png", "tests/images/image.png")


def test_legend_with_arrows_texts(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_arrows_texts.png", "tests/images/image.png")


def test_legend_with_arrows_texts_rotated(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.legend_rotated = True
    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_arrows_texts_rotated.png", "tests/images/image.png")


def test_legend_ticks(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    bivariate_renderer.color_mixing_method = ColorMixingMethodDirect()

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = False
    legend_renderer.add_axes_texts = False
    legend_renderer.legend_rotated = False
    legend_renderer.add_axes_ticks_texts = True
    legend_renderer.texts_axis_x_ticks = bivariate_renderer.field_1_labels
    legend_renderer.texts_axis_y_ticks = bivariate_renderer.field_2_labels

    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_values_ticks.png", "tests/images/image.png")


def test_legend_all(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.legend_rotated = False
    legend_renderer.add_axes_ticks_texts = True
    legend_renderer.texts_axis_x_ticks = bivariate_renderer.field_1_labels
    legend_renderer.texts_axis_y_ticks = bivariate_renderer.field_2_labels

    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_all.png", "tests/images/image.png")


def test_legend_all_rotated(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    bivariate_renderer.color_mixing_method = ColorMixingMethodDirect()

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.legend_rotated = True
    legend_renderer.add_axes_ticks_texts = True
    legend_renderer.texts_axis_x_ticks = bivariate_renderer.field_1_labels
    legend_renderer.texts_axis_y_ticks = bivariate_renderer.field_2_labels

    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_all_rotated.png", "tests/images/image.png")


def test_legend_with_spacer(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    assert qgis_countries_layer
    assert qgs_project
    assert qgs_layout

    image = prepare_default_QImage()

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()

    legend_renderer.add_colors_separators = True
    legend_renderer.color_separator_width_percent = 5

    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_spacer.png", "tests/images/image.png")


def test_legend_with_arrows_common_origin(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.arrows_common_start_point = True
    legend_renderer.render(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_arrows_common_origin.png", "tests/images/image.png")


def test_legend_ticks_midpoints(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, prepare_painter
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    bivariate_renderer.color_mixing_method = ColorMixingMethodDirect()

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = False
    legend_renderer.add_axes_texts = False
    legend_renderer.legend_rotated = False
    legend_renderer.add_axes_ticks_texts = True
    legend_renderer.use_category_midpoints = True
    legend_renderer.texts_axis_x_ticks = classes_to_legend_midpoints(bivariate_renderer.field_1_classes)
    legend_renderer.texts_axis_y_ticks = classes_to_legend_midpoints(bivariate_renderer.field_2_classes)

    legend_renderer.render(
        render_context,
        image.width() / render_context.scaleFactor(),
        image.width() / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_with_values_ticks_midpoints.png", "tests/images/image.png")


def test_legend_empty_squares(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_painter, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = prepare_painter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()

    legend_renderer.add_colors_separators = True
    legend_renderer.color_separator_width_percent = 5
    legend_renderer.replace_rectangle_without_values = True
    legend_renderer.use_rectangle_without_values_color_from_legend = False
    legend_renderer.symbol_rectangle_without_values.setColor(QColor("#ffffff"))

    for feature in qgis_countries_layer.getFeatures():
        bivariate_renderer.symbolForFeature(feature, QgsRenderContext())

    legend_renderer.render_legend(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
        bivariate_renderer.field_1_classes,
        bivariate_renderer.field_2_classes,
        bivariate_renderer.field_1_labels,
        bivariate_renderer.field_2_labels,
    )

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("tests/images/correct/legend_replaced_missing_values.png", "tests/images/image.png")
