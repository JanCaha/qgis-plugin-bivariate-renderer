from qgis.PyQt.QtGui import QPainter
from qgis.core import (QgsLayoutUtils)

from BivariateRenderer.legendrenderer.legend_renderer import LegendRenderer
from BivariateRenderer.colormixing.color_mixing_method import ColorMixingMethodDarken, ColorMixingMethodDirect, ColorMixingMethod
from BivariateRenderer.colormixing.color_mixing_methods_register import ColorMixingMethodsRegister

from tests import assert_images_equal


def test_color_mixing_register():

    register = ColorMixingMethodsRegister()

    assert isinstance(register.names, list)
    assert isinstance(register.names[0], str)

    assert isinstance(register.methods, list)
    assert isinstance(register.methods[0], ColorMixingMethodDirect)
    assert issubclass(type(register.methods[0]), ColorMixingMethod)

    assert register.get_by_name("Direct Mixing")
    assert issubclass(type(register.get_by_name("Direct Mixing")), ColorMixingMethod)
    assert register.get_by_name("does not exist") is None


def test_color_mixing_direct_mixing(qgis_countries_layer, qgs_project, qgs_layout,
                                    prepare_default_QImage, prepare_bivariate_renderer):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")
    bivariate_renderer.color_mixing_method = ColorMixingMethodDirect()

    legend_renderer = LegendRenderer()
    legend_renderer.render(render_context, legend_size / render_context.scaleFactor(),
                           legend_size / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("./tests/images/correct/legend_only_direct_mixing.png",
                        "./tests/images/image.png")


def test_color_mixing_darken(qgis_countries_layer, qgs_project, qgs_layout, prepare_default_QImage,
                             prepare_bivariate_renderer):

    legend_size = 500

    image = prepare_default_QImage(legend_size)

    painter = QPainter(image)

    render_context = QgsLayoutUtils.createRenderContextForLayout(qgs_layout, painter)

    assert render_context

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid")
    bivariate_renderer.color_mixing_method = ColorMixingMethodDarken()

    legend_renderer = LegendRenderer()
    legend_renderer.render(render_context, legend_size / render_context.scaleFactor(),
                           legend_size / render_context.scaleFactor(),
                           bivariate_renderer.generate_legend_polygons())

    painter.end()

    image.save("./tests/images/image.png", "PNG")

    assert_images_equal("./tests/images/correct/legend_only_darken.png",
                        "./tests/images/image.png")
