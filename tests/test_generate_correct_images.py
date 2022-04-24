import pytest

from qgis.PyQt.QtGui import QPainter, QImage, qRgba
from qgis.core import (QgsLayoutUtils)

from BivariateRenderer.legendrenderer.legend_renderer import LegendRenderer
from BivariateRenderer.colormixing.color_mixing_method import ColorMixingMethodDarken, ColorMixingMethodDirect
from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from BivariateRenderer.layoutitems.layout_item import BivariateRendererLayoutItem

from tests import set_up_bivariate_renderer, set_up_layout_page_a4, get_layout_space, export_page_to_image

skip_setting = pytest.mark.skipif(True, reason="do not generate with every run")


@skip_setting
def test_generate_just_legend(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))
    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer)

    legend_renderer = LegendRenderer()
    legend_renderer.render(render_context, legend_size / render_context.scaleFactor(),
                           legend_size / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/correct/legend_only.png", "PNG")


@skip_setting
def test_generate_legend_with_arrows(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))
    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer)

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.render(render_context, legend_size / render_context.scaleFactor(),
                           legend_size / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/correct/legend_with_arrows.png", "PNG")


@skip_setting
def test_generate_legend_with_arrows_text(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))

    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer)

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.render(render_context, legend_size / render_context.scaleFactor(),
                           legend_size / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/correct/legend_with_arrows_texts.png", "PNG")


@skip_setting
def test_generate_legend_with_arrows_text_rotated(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))

    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer)

    legend_renderer = LegendRenderer()
    legend_renderer.add_axes_arrows = True
    legend_renderer.add_axes_texts = True
    legend_renderer.legend_rotated = True
    legend_renderer.render(render_context, legend_size / render_context.scaleFactor(),
                           legend_size / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/correct/legend_with_arrows_texts_rotated.png", "PNG")


@skip_setting
def test_generate_legend_darken(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))
    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer,
                                                   field1="fid",
                                                   field2="fid")
    bivariate_renderer.color_mixing_method = ColorMixingMethodDarken()

    legend_renderer = LegendRenderer()
    legend_renderer.render(render_context, legend_size / render_context.scaleFactor(),
                           legend_size / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/correct/legend_only_darken.png", "PNG")


@skip_setting
def test_generate_legend_direct_mixing(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))
    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer,
                                                   field1="fid",
                                                   field2="fid")
    bivariate_renderer.color_mixing_method = ColorMixingMethodDirect()

    legend_renderer = LegendRenderer()
    legend_renderer.render(render_context, legend_size / render_context.scaleFactor(),
                           legend_size / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/correct/legend_only_direct_mixing.png", "PNG")


@skip_setting
def test_generate_legend_in_layout(qgis_countries_layer, qgs_layout, qgs_project):

    page = set_up_layout_page_a4(qgs_layout)

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer,
                                                   field1="fid",
                                                   field2="fid",
                                                   color_ramps=BivariateColorRampGreenPink())

    qgis_countries_layer.setRenderer(bivariate_renderer)

    qgs_project.addMapLayer(qgis_countries_layer)

    layout_item = BivariateRendererLayoutItem(qgs_layout)
    layout_item.set_linked_layer(qgis_countries_layer)

    layout_item.attemptSetSceneRect(get_layout_space())

    qgs_layout.addItem(layout_item)

    export_page_to_image(qgs_layout, page, "./tests/images/correct/layout_item_legend.png")


@skip_setting
def test_legend_ticks(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))
    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer,
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

    image.save("./tests/images/correct/legend_with_values_ticks.png", "PNG")


@skip_setting
def test_legend_all(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))
    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer,
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

    image.save("./tests/images/correct/legend_with_all.png", "PNG")


@skip_setting
def test_legend_all_rotated(qgis_countries_layer, qgs_project, qgs_layout):

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)
    image.fill(qRgba(0, 0, 0, 0))
    assert isinstance(image, QImage)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = set_up_bivariate_renderer(qgis_countries_layer,
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

    image.save("./tests/images/correct/legend_with_all_rotated.png", "PNG")
