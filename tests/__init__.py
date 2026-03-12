import inspect
import tempfile
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from qgis.core import (
    QgsLayout,
    QgsLayoutExporter,
    QgsLayoutItemPage,
    QgsReadWriteContext,
    QgsStyle,
    QgsTextFormat,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtGui import QImage, QPainter, qRgba
from qgis.PyQt.QtXml import QDomDocument, QDomElement

from BivariateRenderer.colorramps.bivariate_color_ramp import BivariateColorRampGreenPink
from BivariateRenderer.colorramps.color_ramps_register import BivariateColorRamp, BivariateColorRampsRegister
from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer
from BivariateRenderer.renderer.bivariate_renderer_widget import BivariateRendererWidget


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

    sum_sq_diff = np.sum((np.asarray(img1).astype("float") - np.asarray(img2).astype("float")) ** 2)

    if 0 < sum_sq_diff:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
    else:
        normalized_sum_sq_diff = 0

    if normalized_sum_sq_diff > 0.001:
        diff_mask = Image.new("RGBA", img1.size)
        pixelmatch(img1, img2, diff_mask, includeAA=True)

        diff_image_filenaname = diff_image_name(inspect.stack()[1])
        diff_mask.save(diff_image_filenaname)

        __tracebackhide__ = True
        pytest.fail(
            f"Images \n{image_1}\n{image_2}\ndo not look the same.\n"
            f"Difference is {normalized_sum_sq_diff}. Diff file {diff_image_filenaname.as_posix()}."
        )


def diff_image_name(frame: inspect.FrameInfo) -> Path:
    """Get the filename for the diff image based on previous frame - file na function name."""
    diff_dir = Path(tempfile.gettempdir()) / "images_diff"
    if not diff_dir.exists():
        diff_dir.mkdir(exist_ok=True)
    filename = diff_dir / f"{Path(frame.filename).stem}-{frame.function}.png"
    return filename


def prepare_bivariate_renderer(
    layer: QgsVectorLayer, field1: str = "", field2: str = "", color_ramp: Optional[BivariateColorRamp] = None
) -> BivariateRenderer:

    color_ramp_bivariate = BivariateColorRampsRegister().get_by_name("Violet - Blue")

    if color_ramp:
        color_ramp_bivariate = color_ramp

    bivariate_renderer = BivariateRenderer()
    bivariate_renderer.setFieldName1(field1)
    bivariate_renderer.setFieldName2(field2)
    bivariate_renderer.set_bivariate_color_ramp(color_ramp_bivariate)
    bivariate_renderer.setField1ClassificationData(layer, bivariate_renderer.field_name_1)
    bivariate_renderer.setField2ClassificationData(layer, bivariate_renderer.field_name_2)

    return bivariate_renderer


def prepare_bivariate_renderer_widget(layer: QgsVectorLayer) -> BivariateRendererWidget:
    bivariate_renderer = prepare_bivariate_renderer(
        layer, field1="AREA", field2="PERIMETER", color_ramp=BivariateColorRampGreenPink()
    )

    widget = BivariateRendererWidget(layer=layer, style=QgsStyle(), renderer=bivariate_renderer)

    return widget


def prepare_QImage(size: int = 500) -> QImage:
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(qRgba(254, 254, 254, 254))
    assert isinstance(image, QImage)
    return image


def prepare_painter(image: QImage) -> QPainter:
    painter = QPainter(image)
    assert painter
    return painter


def export_page_to_image(
    qgs_layout: QgsLayout, page: QgsLayoutItemPage, image_path: Union[Path, str], DPMM: float
) -> None:

    if isinstance(image_path, Path):
        image_path = image_path.as_posix()

    width = int(DPMM * page.pageSize().width())
    height = int(DPMM * page.pageSize().height())

    size = QSize(width, height)

    exporter = QgsLayoutExporter(qgs_layout)

    image: QImage = exporter.renderPageToImage(0, size)

    image.save(image_path, "PNG")
