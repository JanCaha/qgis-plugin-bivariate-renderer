from typing import Union
import pytest

from qgis.core import (QgsReadWriteContext, QgsTextFormat)

from qgis.PyQt.QtXml import QDomElement, QDomDocument

from PIL import Image

import numpy as np

from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer


def xml_string(element: Union[QDomElement, QgsTextFormat, BivariateRenderer]) -> str:

    xml = QDomDocument("doc")

    rootNode = xml.createElement("element")

    xml.appendChild(rootNode)

    if isinstance(element, QgsTextFormat):

        t = element.writeXml(xml, QgsReadWriteContext())

        xml.appendChild(t)

    elif isinstance(element, BivariateRenderer):

        t = element.save(xml, QgsReadWriteContext())

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

    if 0 < sum_sq_diff:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
    else:
        normalized_sum_sq_diff = 0

    if normalized_sum_sq_diff > 0.001:
        __tracebackhide__ = True
        pytest.fail(f"Images \n{image_1}\n{image_2}\ndo not look the same.\n"
                    f"Difference is {normalized_sum_sq_diff}.")
    else:
        pass
