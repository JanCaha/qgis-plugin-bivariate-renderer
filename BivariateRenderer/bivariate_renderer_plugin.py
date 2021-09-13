# -*- coding: utf-8 -*-
"""
/***************************************************************************
 test_rendeder
                                 A QGIS plugin
 test
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-01-18
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Jan Caha
        email                : jan.caha@outlook.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsApplication
from qgis.gui import QgsGui

from .renderer.bivariate_renderer_metadata import BivariateRendererMetadata

from .layoutitems.layout_item import BivariateRendererLayoutItemMetadata
from .layoutitems.layout_item_widget import BivariateRendererLayoutItemGuiMetadata


class BivariateRendererPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        self.iface = iface
        self.bivariate_renderer_metadata = BivariateRendererMetadata()

        self.bivariate_renderer_layout_item_gui_metadata = BivariateRendererLayoutItemGuiMetadata()

        self.bivariate_renderer_layout_item_metadata = BivariateRendererLayoutItemMetadata()

        QgsApplication.layoutItemRegistry().addLayoutItemType(self.bivariate_renderer_layout_item_metadata)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        QgsApplication.rendererRegistry().addRenderer(self.bivariate_renderer_metadata)

        QgsGui.layoutItemGuiRegistry().addLayoutItemGuiMetadata(self.bivariate_renderer_layout_item_gui_metadata)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        QgsApplication.rendererRegistry().removeRenderer(self.bivariate_renderer_metadata.name())

    def run(self):
        """Run method that performs all the real work"""
        pass



