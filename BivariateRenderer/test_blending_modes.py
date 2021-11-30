import sys

from qgis.PyQt.QtWidgets import QApplication, QLabel
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon, QImage, QPainter, QColor, QPixmap, QTransform
from qgis.gui import QgsBlendModeComboBox


def generate_image_for_colors(
        color,
        width,
        height,
        square_size):

    origin_x = 0
    origin_y = 0
    w, h = width, height
    img = QImage(w, h, QImage.Format_ARGB32)

    qp = QPainter()
    qp.begin(img)

    print(color)

    qp.setBrush(QColor(*color))
    qp.setPen(Qt.NoPen)

    qp.drawRect(
        origin_x,
        origin_y,
        origin_x + square_size,
        origin_y + square_size
    )

    qp.end()
    return img

def generate_image(color: QColor) -> QImage:

    img = QImage(1, 1, QImage.Format_ARGB32)

    qp = QPainter()

    qp.begin(img)

    qp.setBrush(color)
    qp.setPen(Qt.NoPen)

    qp.drawRect(0, 0, 1, 1)

    qp.end()

    return img


def mix_colors(color_1: QColor, color_2: QColor, blend_mode: QPainter.CompositionMode) -> QColor:

    img_top = generate_image(color_1)
    img_bottom = generate_image(color_2)

    painter = QPainter()

    painter.begin(img_top)
    painter.setCompositionMode(blend_mode)
    painter.drawImage(0, 0, img_bottom)
    painter.end()

    return img_top.pixelColor(0, 0)

# img_top = generate_image_for_colors([8, 48, 108], 500, 500, 100)
# img_bottom = generate_image_for_colors([255, 0, 0], 500, 500, 500)
# # img_top = generate_image_for_colors([8, 48, 108], 500, 500, 100)
#
# painter = QPainter()
#
# # Start from first image
# painter.begin(img_top)
# # Apply blending/composition
# painter.setCompositionMode(20)
# painter.drawImage(0, 0, img_bottom)
# painter.end()
#
# col: QColor = img_top.pixelColor(10, 10)
# print(col.name())
# col: QColor = img_top.pixelColor(500, 10)
# print(col.name())

# pixmap: QPixmap = QPixmap.fromImage(img_top)
# col = pixmap.colorCount()
# print(col)

# app = QApplication(sys.argv)
#
# ex = QLabel()
# ex.setPixmap(QPixmap.fromImage(img_top))
# ex.show()
# sys.exit(app.exec_())


color1 = QColor(255, 0, 0)
color2 = QColor(8, 48, 108)
QPainter.Comp
col_res = mix_colors(color1, color2, QPainter.CompositionMode_Darken)

print(col_res.name())
