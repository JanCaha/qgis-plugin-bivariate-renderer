from typing import Optional, Union
from pathlib import Path

from qgis.core import (QgsReadWriteContext, QgsTextFormat, QgsVectorLayer,
                       QgsClassificationEqualInterval, QgsGradientColorRamp, QgsLayout,
                       QgsLayoutItemPage, QgsLayoutSize, QgsUnitTypes, QgsLayoutItemMap,
                       QgsLayoutExporter)
from qgis.gui import QgsMapCanvas
from qgis.PyQt.QtXml import QDomElement, QDomDocument
from qgis.PyQt.QtGui import QColor, QPainter, QImage, qRgba
from qgis.PyQt.QtCore import QRectF, QSize

from PIL import Image

import numpy as np

from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer
from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRamp


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


LAYOUT_WIDTH = 297
LAYOUT_HEIGHT = 210
DPMM = 300 / 25.4


def get_layout_space() -> QRectF:
    return QRectF(0, 0, LAYOUT_WIDTH, LAYOUT_HEIGHT)


def set_up_layout_page_a4(qgs_layout: QgsLayout) -> QgsLayoutItemPage:

    page = QgsLayoutItemPage(qgs_layout)
    page.setPageSize(QgsLayoutSize(LAYOUT_WIDTH, LAYOUT_HEIGHT, QgsUnitTypes.LayoutMillimeters))
    collection = qgs_layout.pageCollection()
    collection.addPage(page)

    return page


def export_page_to_image(qgs_layout: QgsLayout, page: QgsLayoutItemPage,
                         image_path: Union[Path, str]) -> None:

    if isinstance(image_path, Path):
        image_path = image_path.as_posix()

    width = int(DPMM * page.pageSize().width())
    height = int(DPMM * page.pageSize().height())

    size = QSize(width, height)

    exporter = QgsLayoutExporter(qgs_layout)

    image: QImage = exporter.renderPageToImage(0, size)

    image.save(image_path, "PNG")


def save_layout_for_layer(layer: QgsVectorLayer, qgs_layout: QgsLayout,
                          image_path: Union[str, Path]) -> QImage:

    canvas = QgsMapCanvas()

    extent = layer.extent()
    canvas.setExtent(extent)

    page = set_up_layout_page_a4(qgs_layout)

    map_item = QgsLayoutItemMap(qgs_layout)
    map_item.attemptSetSceneRect(get_layout_space())

    map_item.setCrs(layer.crs())
    map_item.zoomToExtent(extent)

    qgs_layout.addItem(map_item)

    export_page_to_image(qgs_layout, page, image_path)
