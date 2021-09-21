from pathlib import Path

from qgis.core import (QgsRendererAbstractMetadata)

from qgis.PyQt.QtXml import QDomElement
from qgis.PyQt.QtGui import QIcon

from .bivariate_renderer import BivariateRenderer
from .bivariate_renderer_widget import BivariateRendererWidget
from ..text_constants import Texts


class BivariateRendererMetadata(QgsRendererAbstractMetadata):

    def __init__(self):
        super().__init__(Texts.bivariate_renderer_short_name, Texts.bivariate_renderer_full_name)

    def name(self) -> str:
        return Texts.bivariate_renderer_short_name

    def visibleName(self):
        return Texts.bivariate_renderer_full_name

    def createRenderer(self, element: QDomElement, context):
        return BivariateRenderer.create_render_from_element(element)

    def createRendererWidget(self, layer, style, renderer):
        return BivariateRendererWidget(layer, style, renderer)

    def compatibleLayerTypes(self):
        return QgsRendererAbstractMetadata.PolygonLayer

    def icon(self) -> QIcon:
        path = Path(__file__).parent.parent / "icons" / "legend_icon.png"
        return QIcon(path.absolute().as_posix())
