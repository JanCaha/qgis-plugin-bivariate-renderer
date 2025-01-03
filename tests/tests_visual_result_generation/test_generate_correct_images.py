import os

import pytest
from qgis.core import QgsLayoutUtils, QgsRenderContext
from qgis.PyQt.QtGui import QColor, QPainter

from BivariateRenderer.colormixing.color_mixing_method import ColorMixingMethodDarken, ColorMixingMethodDirect
from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from BivariateRenderer.layoutitems.layout_item import BivariateRendererLayoutItem
from BivariateRenderer.legendrenderer.legend_renderer import LegendRenderer
from BivariateRenderer.renderer.bivariate_renderer_utils import classes_to_legend_midpoints

env_value = os.getenv("BIVARIATE_GENERATE")

if env_value:
    generate_images = env_value.lower() == "true"
else:
    generate_images = False

skip_setting = pytest.mark.skipif(not generate_images, reason="do not generate with every run")


@skip_setting
def test_generate_just_legend(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.render(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/correct/legend_only.png", "PNG")


@skip_setting
def test_generate_legend_with_arrows(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.render(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/correct/legend_with_arrows.png", "PNG")


@skip_setting
def test_generate_legend_with_arrows_common_origin(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

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

    image.save("./tests/images/correct/legend_with_arrows_common_origin.png", "PNG")


@skip_setting
def test_generate_legend_with_arrows_text(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.render(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/correct/legend_with_arrows_texts.png", "PNG")


@skip_setting
def test_generate_legend_with_arrows_text_rotated(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.legend_rotated = True
    legend_renderer.render(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/correct/legend_with_arrows_texts_rotated.png", "PNG")


@skip_setting
def test_generate_legend_darken(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")
    bivariate_renderer.color_mixing_method = ColorMixingMethodDarken()

    legend_renderer = LegendRenderer()
    legend_renderer.render(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/correct/legend_only_darken.png", "PNG")


@skip_setting
def test_generate_legend_direct_mixing(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")
    bivariate_renderer.color_mixing_method = ColorMixingMethodDirect()

    legend_renderer = LegendRenderer()
    legend_renderer.render(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/correct/legend_only_direct_mixing.png", "PNG")


@skip_setting
def test_generate_legend_in_layout(
    qgis_countries_layer,
    qgs_layout,
    qgs_project,
    layout_page_a4,
    prepare_bivariate_renderer,
    layout_space,
    export_page_to_image,
):

    bivariate_renderer = prepare_bivariate_renderer(
        qgis_countries_layer, field1="fid", field2="fid", color_ramp=BivariateColorRampGreenPink()
    )

    qgis_countries_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(qgis_countries_layer)

    layout_item = BivariateRendererLayoutItem(qgs_layout)
    layout_item.set_linked_layer(qgis_countries_layer)

    layout_item.attemptSetSceneRect(layout_space)

    qgs_layout.addItem(layout_item)

    export_page_to_image(qgs_layout, layout_page_a4, "./tests/images/correct/layout_item_legend.png")


@skip_setting
def test_legend_ticks(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

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

    image.save("./tests/images/correct/legend_with_values_ticks.png", "PNG")


@skip_setting
def test_legend_all(qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

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

    image.save("./tests/images/correct/legend_with_all.png", "PNG")


@skip_setting
def test_legend_all_rotated(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

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

    image.save("./tests/images/correct/legend_with_all_rotated.png", "PNG")


@skip_setting
def test_layer_bivariate_render(
    nc_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer, save_layout_for_layer
):

    bivariate_renderer = prepare_bivariate_renderer(
        nc_layer, field1="AREA", field2="PERIMETER", color_ramp=BivariateColorRampGreenPink()
    )

    nc_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(nc_layer)

    save_layout_for_layer(nc_layer, "tests/images/correct/layout_polygons_render.png")


@skip_setting
def test_generate_legend_white_spacer(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer, field1="fid", field2="fid")

    legend_renderer = LegendRenderer()

    legend_renderer.add_colors_separators = True
    legend_renderer.color_separator_width_percent = 5

    legend_renderer.render(
        render_context,
        legend_size / render_context.scaleFactor(),
        legend_size / render_context.scaleFactor(),
        bivariate_renderer.generate_legend_polygons(),
    )

    painter.end()

    image.save("./tests/images/correct/legend_with_spacer.png", "PNG")


@skip_setting
def test_legend_ticks_midpoints(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

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

    image.save("./tests/images/correct/legend_with_values_ticks_midpoints.png", "PNG")


@skip_setting
def test_generate_legend_empty_squares(
    qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage, prepare_bivariate_renderer
):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

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

    image.save("./tests/images/correct/legend_replaced_missing_values.png", "PNG")
