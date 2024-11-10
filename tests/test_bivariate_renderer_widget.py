from qgis.core import QgsClassificationMethod, QgsTextFormat, QgsVectorLayer
from qgis.gui import QgsColorRampButton, QgsDoubleSpinBox, QgsFieldComboBox
from qgis.PyQt.QtWidgets import QComboBox, QFormLayout, QLabel

from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from BivariateRenderer.legendrenderer.legend_renderer import LegendRenderer
from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer
from tests import assert_images_equal


def test_widget_elements(nc_layer: QgsVectorLayer, prepare_bivariate_renderer_widget):

    widget = prepare_bivariate_renderer_widget(nc_layer)

    assert isinstance(widget.field_name_1, str)
    assert isinstance(widget.field_name_2, str)
    assert isinstance(widget.bivariate_renderer, BivariateRenderer)
    assert isinstance(widget.legend_renderer, LegendRenderer)
    assert isinstance(widget.classification_methods, dict)
    assert isinstance(widget.cb_field1, QgsFieldComboBox)
    assert isinstance(widget.cb_field2, QgsFieldComboBox)
    assert isinstance(widget.sb_number_classes, QgsDoubleSpinBox)
    assert isinstance(widget.cb_colormixing_methods, QComboBox)
    assert isinstance(widget.cb_color_ramps, QComboBox)
    assert isinstance(widget.bt_color_ramp1, QgsColorRampButton)
    assert isinstance(widget.bt_color_ramp1, QgsColorRampButton)
    assert isinstance(widget.label_legend, QLabel)
    assert isinstance(widget.form_layout, QFormLayout)


def test_widget_values(nc_layer: QgsVectorLayer, prepare_bivariate_renderer_widget):

    widget = prepare_bivariate_renderer_widget(nc_layer)

    assert widget.cb_field1.fields() == nc_layer.fields()
    assert widget.cb_field2.fields() == nc_layer.fields()
    assert len(widget.cb_color_ramps) == 14
    assert len(widget.cb_colormixing_methods) == 3

    color_ramp = BivariateColorRampGreenPink()

    assert widget.bt_color_ramp1.colorRamp().properties() == color_ramp.color_ramp_1.properties()
    assert widget.bt_color_ramp2.colorRamp().properties() == color_ramp.color_ramp_2.properties()


def test_visual(nc_layer: QgsVectorLayer, prepare_bivariate_renderer_widget):

    widget = prepare_bivariate_renderer_widget(nc_layer)

    widget.show()

    pixmap = widget.grab()

    pixmap.save("tests/images/image.png", "png")

    assert_images_equal("tests/images/correct/widget_renderer.png", "tests/images/image.png")
