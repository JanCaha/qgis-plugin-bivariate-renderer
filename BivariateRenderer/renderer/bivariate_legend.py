from typing import List, Dict

from qgis.core import (QgsDefaultVectorLayerLegend, QgsVectorLayer, QgsLayerTreeModelLegendNode,
                       QgsSymbolLegendNode)

from .bivariate_renderer import BivariateRenderer


class BivariateLegendViewerLegend(QgsDefaultVectorLayerLegend):

    def __init__(self, bivariate_renderer: BivariateRenderer, layer: QgsVectorLayer = None):
        QgsDefaultVectorLayerLegend.__init__(self, layer)
        self.bivariate_renderer = bivariate_renderer
        self.layer = layer

    def createLayerTreeModelLegendNodes(self,
                                        layer_tree_layer) -> List[QgsLayerTreeModelLegendNode]:

        items: Dict[str, QgsSymbolLegendNode] = {}

        for feature in self.layer.getFeatures():

            label = self.bivariate_renderer.getFeatureCombinationHash(feature)

            if label not in items.keys():
                legend_item = QgsSymbolLegendNode(layer_tree_layer,
                                                  self.bivariate_renderer.legendSymbolItem(label),
                                                  self)
                legend_item.setUserLabel(label)
                items[label] = legend_item

        self.bivariate_renderer.labels_existing = list(items.keys())

        node_array = []

        for key in sorted(items.keys()):
            node_array.append(items[key])

        return node_array
