import pytest
from pathlib import Path

from qgis.core import QgsProject, QgsLayout, QgsVectorLayer


@pytest.fixture
def qgs_project() -> QgsProject:
    return QgsProject.instance()


@pytest.fixture
def qgs_layout(qgs_project) -> QgsLayout:
    return QgsLayout(qgs_project)


@pytest.fixture
def nc_layer() -> QgsVectorLayer:

    path = Path(__file__).parent / "data" / "nc_data.gpkg"

    return QgsVectorLayer(f"{path.as_posix()}|layername=nc_data", "layer", "ogr")
