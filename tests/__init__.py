import inspect
import tempfile
from pathlib import Path
from typing import Union

import numpy as np
import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch
from qgis.core import QgsReadWriteContext, QgsTextFormat
from qgis.PyQt.QtXml import QDomDocument, QDomElement

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
