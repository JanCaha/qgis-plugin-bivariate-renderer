from qgis.core import QgsDefaultVectorLayerLegend, QgsSimpleLegendNode, QgsFillSymbol
from qgis.PyQt.QtGui import QPixmap, QIcon


class BivariateLegendViewerLegend(QgsDefaultVectorLayerLegend):

    def __init__(self, bivariate_renderer, layer=None):
        QgsDefaultVectorLayerLegend.__init__(self, layer)
        self.bivariate_renderer = bivariate_renderer

    def createLayerTreeModelLegendNodes(self, layer_tree_layer):
        nodeArray = []
        for classItem in self.bivariate_renderer.cached.keys():
            m = QgsSimpleLegendNode(layer_tree_layer, classItem,
                                    self.createIcon(self.bivariate_renderer.cached[classItem]),
                                    self)
            nodeArray.append(m)
        return nodeArray

    def createIcon(self, symbol: QgsFillSymbol):
        pix = QPixmap(16, 16)
        pix.fill(symbol.color())
        return QIcon(pix)
