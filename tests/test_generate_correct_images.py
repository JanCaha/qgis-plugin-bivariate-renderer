import pytest

from qgis.PyQt.QtGui import QPainter, QImage, qRgba
from qgis.core import (QgsLayoutUtils)

from BivariateRenderer.legendrenderer.legend_renderer import LegendRenderer
from BivariateRenderer.colormixing.color_mixing_method import ColorMixingMethodDarken, ColorMixingMethodDirect

from tests import set_up_bivariate_renderer

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
