from typing import Union

from qgis.core import (QgsReadWriteContext, QgsTextFormat, QgsVectorLayer,
                       QgsClassificationEqualInterval, QgsGradientColorRamp)
from qgis.PyQt.QtXml import QDomElement, QDomDocument
from qgis.PyQt.QtGui import QColor, QPainter, QImage, qRgba

from PIL import Image

import numpy as np

from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer


def xml_string(element: Union[QDomElement, QgsTextFormat]) -> str:

    xml = QDomDocument("doc")

    rootNode = xml.createElement("element")

    xml.appendChild(rootNode)

    if isinstance(element, QgsTextFormat):

        t = element.writeXml(xml, QgsReadWriteContext())

        xml.appendChild(t)

    else:
        xml.appendChild(element)

    return xml.toString()


def assert_images_equal(image_1: str, image_2: str):

    img1 = Image.open(image_1)
    img2 = Image.open(image_2)

    # Convert to same mode and size for comparison
    img2 = img2.convert(img1.mode)
    img2 = img2.resize(img1.size)

    sum_sq_diff = np.sum((np.asarray(img1).astype('float') - np.asarray(img2).astype('float'))**2)

    if sum_sq_diff == 0:
        # Images are exactly the same
        pass
    else:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
        assert normalized_sum_sq_diff < 0.001


def set_up_bivariate_renderer(
        layer: QgsVectorLayer,
        field1: str = "",
        field2: str = "",
        color_ramps: Optional[BivariateColorRamp] = None) -> BivariateRenderer:

    if color_ramps is None:

    default_color_ramp_1 = QgsGradientColorRamp(QColor(255, 255, 255), QColor(255, 0, 0))
    default_color_ramp_2 = QgsGradientColorRamp(QColor(255, 255, 255), QColor(0, 0, 255))

    else:

        default_color_ramp_1 = color_ramps.color_ramp_1
        default_color_ramp_2 = color_ramps.color_ramp_2

    classification_method = QgsClassificationEqualInterval()

    bivariate_renderer = BivariateRenderer()
    bivariate_renderer.setFieldName1(field1)
    bivariate_renderer.setFieldName2(field2)
    bivariate_renderer.setColorRamp1(default_color_ramp_1)
    bivariate_renderer.setColorRamp2(default_color_ramp_2)
    bivariate_renderer.setField1Classes(
        classification_method.classes(layer, bivariate_renderer.field_name_1,
                                      bivariate_renderer.number_classes))
    bivariate_renderer.setField2Classes(
        classification_method.classes(layer, bivariate_renderer.field_name_2,
                                      bivariate_renderer.number_classes))

    return bivariate_renderer


def set_up_image() -> QImage:

    legend_size = 500

    image = QImage(legend_size, legend_size, QImage.Format_ARGB32)

    image.fill(qRgba(0, 0, 0, 0))

    assert isinstance(image, QImage)

    return image


def set_up_painter(image: QImage) -> QPainter:

    painter = QPainter(image)

    assert painter

    return painter
