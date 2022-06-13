from qgis.PyQt.QtWidgets import (QComboBox, QCheckBox, QPlainTextEdit, QSpinBox, QMainWindow)
from qgis.gui import (QgsFontButton, QgsSymbolButton)
from qgis.core import QgsVectorLayer

from BivariateRenderer.layoutitems.layout_item import BivariateRendererLayoutItem
from BivariateRenderer.layoutitems.layout_item_widget import BivariateRendererLayoutItemWidget
from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from BivariateRenderer.utils import default_line_symbol

from tests import (assert_images_equal)


def test_layout_item_widget(qgis_countries_layer: QgsVectorLayer, qgs_layout, qgis_parent,
                            qgs_project, prepare_bivariate_renderer):

    qgs_project.addMapLayer(qgis_countries_layer)

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid",
                                                    color_ramps=BivariateColorRampGreenPink())

    qgis_countries_layer.setRenderer(bivariate_renderer)

    layout_item = BivariateRendererLayoutItem(qgs_layout)
    layout_item.set_linked_layer(qgis_countries_layer)

    layout_item.set_line_format(default_line_symbol())

    assert isinstance(layout_item, BivariateRendererLayoutItem)

    assert isinstance(qgis_parent, QMainWindow)

    widget = BivariateRendererLayoutItemWidget(qgis_parent, layout_item)

    assert isinstance(widget, BivariateRendererLayoutItemWidget)

    assert isinstance(widget.cb_layers, QComboBox)
    assert isinstance(widget.axis_x_name, QPlainTextEdit)
    assert isinstance(widget.axis_y_name, QPlainTextEdit)
    assert isinstance(widget.rotate_legend, QCheckBox)
    assert isinstance(widget.add_arrows, QCheckBox)
    assert isinstance(widget.add_axes_values_text, QCheckBox)
    assert isinstance(widget.rotate_direction, QComboBox)
    assert isinstance(widget.ticks_precision_x, QSpinBox)
    assert isinstance(widget.ticks_precision_y, QSpinBox)

    assert isinstance(widget.b_font_values, QgsFontButton)
    assert isinstance(widget.b_font, QgsFontButton)
    assert isinstance(widget.b_line_symbol, QgsSymbolButton)

    assert isinstance(widget.layout_item, BivariateRendererLayoutItem)


def test_visual(qgis_countries_layer: QgsVectorLayer, qgs_layout, qgis_parent, qgs_project,
                prepare_bivariate_renderer):

    qgs_project.addMapLayer(qgis_countries_layer)

    bivariate_renderer = prepare_bivariate_renderer(qgis_countries_layer,
                                                    field1="fid",
                                                    field2="fid",
                                                    color_ramps=BivariateColorRampGreenPink())

    qgis_countries_layer.setRenderer(bivariate_renderer)

    layout_item = BivariateRendererLayoutItem(qgs_layout)
    layout_item.set_linked_layer(qgis_countries_layer)

    layout_item.set_line_format(default_line_symbol())

    widget = BivariateRendererLayoutItemWidget(None, layout_item)

    widget.show()

    pixmap = widget.grab()

    pixmap.save("tests/images/image.png", "png")

    assert_images_equal("tests/images/correct/widget_layout_item.png", "tests/images/image.png")
