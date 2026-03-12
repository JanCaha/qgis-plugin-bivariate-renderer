from pathlib import Path
from typing import Callable, Optional, Union

import pytest
from qgis.core import (
    QgsFillSymbol,
    QgsLayout,
    QgsLayoutExporter,
    QgsLayoutItemMap,
    QgsLayoutItemPage,
    QgsLayoutSize,
    QgsProject,
    QgsStyle,
    QgsUnitTypes,
    QgsVectorLayer,
)
from qgis.gui import QgsMapCanvas
from qgis.PyQt.QtCore import QLocale, QRectF, QSize, Qt
from qgis.PyQt.QtGui import QFont, QGuiApplication, QImage, QPainter, qRgba
from qgis.PyQt.QtWidgets import QApplication

from BivariateRenderer.colorramps.color_ramps_register import (
    BivariateColorRamp,
    BivariateColorRampGreenPink,
    BivariateColorRampsRegister,
)
from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer
from BivariateRenderer.renderer.bivariate_renderer_widget import BivariateRendererWidget


def pytest_configure(config):
    QApplication.setAttribute(Qt.AA_Use96Dpi)
    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)

    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Round) # Qt6


@pytest.fixture(autouse=True, scope="session")
def change_locale():
    """Sets locale to English, United Kingdom for all tests to ensure consistent results."""
    QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedKingdom))


@pytest.fixture(autouse=True, scope="session")
def set_application_font():
    """Sets a consistent application font for all tests to ensure reproducible visual results."""
    QApplication.instance().setFont(QFont("DejaVu Sans", 12))
    QApplication.instance().setStyle("Fusion")


@pytest.fixture
def qgs_project(qgis_iface) -> QgsProject:
    qgis_iface.newProject()
    project = QgsProject.instance()
    return project


@pytest.fixture
def qgs_layout(qgs_project) -> QgsLayout:
    layout = QgsLayout(qgs_project)
    return layout


@pytest.fixture
def nc_layer_path() -> str:

    path = Path(__file__).parent / "data" / "nc_data.gpkg"

    return f"{path.as_posix()}|layername=nc_data"


@pytest.fixture()
def nc_layer(nc_layer_path) -> QgsVectorLayer:

    layer = QgsVectorLayer(nc_layer_path, "layer", "ogr")
    return layer


@pytest.fixture
def prepare_default_QImage() -> Callable[[int], QImage]:

    def return_QImage(size: int = 500) -> QImage:
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(qRgba(254, 254, 254, 254))
        assert isinstance(image, QImage)
        return image

    return return_QImage


@pytest.fixture
def prepare_painter() -> Callable[[QImage], QPainter]:

    def return_painter(image: QImage) -> QPainter:
        painter = QPainter(image)
        assert painter
        return painter

    return return_painter


@pytest.fixture
def layout_width() -> float:
    return 297


@pytest.fixture
def layout_height() -> float:
    return 210


@pytest.fixture
def layout_dpmm() -> float:
    return 300 / 25.4


@pytest.fixture
def layout_space(layout_height, layout_width) -> QRectF:
    return QRectF(0, 0, layout_width, layout_height)


@pytest.fixture
def layout_page_a4(
    qgs_layout: QgsLayout, layout_dpmm: float, layout_height: float, layout_width: float
) -> QgsLayoutItemPage:

    page = QgsLayoutItemPage(qgs_layout)
    page.setPageSize(QgsLayoutSize(layout_width, layout_height, QgsUnitTypes.LayoutMillimeters))
    collection = qgs_layout.pageCollection()
    collection.addPage(page)
    return page


@pytest.fixture
def prepare_bivariate_renderer() -> (
    Callable[[QgsVectorLayer, str, str, Optional[BivariateColorRamp]], BivariateRenderer]
):

    def return_bivariate_renderer(
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

    return return_bivariate_renderer


@pytest.fixture
def prepare_bivariate_renderer_widget(prepare_bivariate_renderer):

    def return_bivariate_renderer_widget(layer: QgsVectorLayer) -> BivariateRendererWidget:
        bivariate_renderer = prepare_bivariate_renderer(
            layer, field1="AREA", field2="PERIMETER", color_ramp=BivariateColorRampGreenPink()
        )

        widget = BivariateRendererWidget(layer=layer, style=QgsStyle(), renderer=bivariate_renderer)

        return widget

    return return_bivariate_renderer_widget


@pytest.fixture
def export_page_to_image(layout_dpmm) -> Callable[[QgsLayout, QgsLayoutItemPage, Union[Path, str], float], None]:

    def function_to_run(
        qgs_layout: QgsLayout, page: QgsLayoutItemPage, image_path: Union[Path, str], DPMM: float = layout_dpmm
    ) -> None:

        if isinstance(image_path, Path):
            image_path = image_path.as_posix()

        width = int(DPMM * page.pageSize().width())
        height = int(DPMM * page.pageSize().height())

        size = QSize(width, height)

        exporter = QgsLayoutExporter(qgs_layout)

        image: QImage = exporter.renderPageToImage(0, size)

        image.save(image_path, "PNG")

    return function_to_run


@pytest.fixture
def custom_polygon_symbol() -> QgsFillSymbol:
    custom_symbol = QgsFillSymbol.createSimple(
        {
            "outline_width": "3.0",
            "outline_width_unit": "MM",
            "outline_color": "255,0,0,255",
            "outline_style": "dashed",
        }
    )
    return custom_symbol
