from qgis.core import QgsLayoutItemRegistry


class Texts:

    plugin_name = "Bivariate Renderer Plugin"
    bivariate_renderer_full_name = "Bivariate Renderer"
    bivariate_renderer_short_name = "BivariateRenderer"

    temp_legend_filename = "temp_legend.svg"

    plot_item_bivariate_renderer = "Plot item Bivariate Renderer"
    plot_item_bivariate_renderer_legend = QgsLayoutItemRegistry.PluginItem + 123 + 1