import pytest
from pathlib import Path
from typing import Optional, Union

from qgis.core import (QgsProject, QgsVectorLayer, QgsLayout, QgsLayoutItemPage, QgsLayoutSize,
                       QgsUnitTypes, QgsGradientColorRamp, QgsStyle, QgsLayoutItemMap,
                       QgsLayoutExporter)
from qgis.gui import QgsMapCanvas
from qgis.PyQt.QtGui import QImage, qRgba, QPainter, QColor
from qgis.PyQt.QtCore import QRectF, QSize

from BivariateRenderer.renderer.bivariate_renderer import BivariateRenderer
from BivariateRenderer.renderer.bivariate_renderer_widget import BivariateRendererWidget
from BivariateRenderer.colorramps.color_ramps_register import (BivariateColorRamp,
                                                               BivariateColorRampGreenPink,
                                                               BivariateColorRampsRegister)


@pytest.fixture
def qgs_project() -> QgsProject:
    return QgsProject.instance()


@pytest.fixture
def qgs_layout(qgs_project) -> QgsLayout:
    return QgsLayout(qgs_project)


@pytest.fixture
def nc_layer_path() -> str:

    path = Path(__file__).parent / "data" / "nc_data.gpkg"

    return f"{path.as_posix()}|layername=nc_data"


@pytest.fixture
def nc_layer(nc_layer_path) -> QgsVectorLayer:

    return QgsVectorLayer(nc_layer_path, "layer", "ogr")


@pytest.fixture
def prepare_default_QImage():

    def return_QImage(size: int = 500) -> QImage:
        image = QImage(size, size, QImage.Format_ARGB32)
        image.fill(qRgba(254, 254, 254, 254))
        assert isinstance(image, QImage)
        return image

    return return_QImage


@pytest.fixture
def prepare_painter():

    def return_painter(image: QImage) -> QPainter:
        painter = QPainter(image)
        assert painter
        return painter

    return return_painter


@pytest.fixture
def layout_width():
    return 297


@pytest.fixture
def layout_height():
    return 210


@pytest.fixture
def layout_dpmm():
    return 300 / 25.4


@pytest.fixture
def layout_space(layout_height, layout_width) -> QRectF:
    return QRectF(0, 0, layout_width, layout_height)


@pytest.fixture
def layout_page_a4(qgs_layout: QgsLayout, layout_dpmm, layout_height,
                   layout_width) -> QgsLayoutItemPage:

    page = QgsLayoutItemPage(qgs_layout)
    page.setPageSize(QgsLayoutSize(layout_width, layout_height, QgsUnitTypes.LayoutMillimeters))
    collection = qgs_layout.pageCollection()
    collection.addPage(page)

    return page


@pytest.fixture
def prepare_bivariate_renderer():

    def return_bivariate_renderer(
            layer: QgsVectorLayer,
            field1: str = "",
            field2: str = "",
            color_ramps: Optional[BivariateColorRamp] = None) -> BivariateRenderer:

        if color_ramps is None:

            color_ramp = BivariateColorRampsRegister().get_by_name("Violet - Blue")

            default_color_ramp_1 = color_ramp.color_ramp_1
            default_color_ramp_2 = color_ramp.color_ramp_2

        else:

            default_color_ramp_1 = color_ramps.color_ramp_1
            default_color_ramp_2 = color_ramps.color_ramp_2

        bivariate_renderer = BivariateRenderer()
        bivariate_renderer.setFieldName1(field1)
        bivariate_renderer.setFieldName2(field2)
        bivariate_renderer.setColorRamp1(default_color_ramp_1)
        bivariate_renderer.setColorRamp2(default_color_ramp_2)
        bivariate_renderer.setField1ClassificationData(layer, bivariate_renderer.field_name_1)
        bivariate_renderer.setField2ClassificationData(layer, bivariate_renderer.field_name_2)

        return bivariate_renderer

    return return_bivariate_renderer


@pytest.fixture
def prepare_bivariate_renderer_widget(prepare_bivariate_renderer):

    def return_bivariate_renderer_widget(layer: QgsVectorLayer) -> BivariateRendererWidget:
        bivariate_renderer = prepare_bivariate_renderer(layer,
                                                        field1="AREA",
                                                        field2="PERIMETER",
                                                        color_ramps=BivariateColorRampGreenPink())

        widget = BivariateRendererWidget(layer=layer,
                                         style=QgsStyle(),
                                         renderer=bivariate_renderer)

        return widget

    return return_bivariate_renderer_widget


@pytest.fixture
def save_layout_for_layer(qgs_layout, layout_page_a4, layout_space, export_page_to_image):

    def function_to_run(layer: QgsVectorLayer,
                        image_path: Union[str, Path],
                        qgs_layout: QgsLayout = qgs_layout,
                        page=layout_page_a4,
                        layout_space=layout_space,
                        export_page_to_image=export_page_to_image) -> None:

        canvas = QgsMapCanvas()

        extent = layer.extent()
        canvas.setExtent(extent)

        map_item = QgsLayoutItemMap(qgs_layout)
        map_item.attemptSetSceneRect(layout_space)

        map_item.setCrs(layer.crs())
        map_item.zoomToExtent(extent)

        qgs_layout.addItem(map_item)

        export_page_to_image(qgs_layout, page, image_path)

    return function_to_run


@pytest.fixture
def export_page_to_image(layout_dpmm):

    def function_to_run(qgs_layout: QgsLayout,
                        page: QgsLayoutItemPage,
                        image_path: Union[Path, str],
                        DPMM=layout_dpmm) -> None:

        if isinstance(image_path, Path):
            image_path = image_path.as_posix()

        width = int(DPMM * page.pageSize().width())
        height = int(DPMM * page.pageSize().height())

        size = QSize(width, height)

        exporter = QgsLayoutExporter(qgs_layout)

        image: QImage = exporter.renderPageToImage(0, size)

        image.save(image_path, "PNG")

    return function_to_run
