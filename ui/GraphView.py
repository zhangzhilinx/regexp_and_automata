from PyQt5.QtCore import pyqtSignal, qFuzzyCompare, Qt
from PyQt5.QtGui import QPainter, QPixmap, QColor, QBrush
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QWidget


class GraphView(QGraphicsView):
    TYPE_NATIVE = 'native'
    TYPE_OPENGL = 'opengl'
    zoomChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent=parent)

        self.setScene(QGraphicsScene(self))
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        tile_pixmap = QPixmap(64, 64)
        tile_pixmap.fill(Qt.white)
        tile_painter = QPainter(tile_pixmap)
        tile_color = QColor(220, 220, 220)
        tile_painter.fillRect(0, 0, 32, 32, tile_color)
        tile_painter.fillRect(32, 32, 32, 32, tile_color)
        tile_painter.end()
        self.setBackgroundBrush(QBrush(tile_pixmap))

    def paintEvent(self, event):
        super(GraphView, self).paintEvent(event)

    def wheelEvent(self, event):
        exp = event.angleDelta().y() / 240
        self.zoom_by(1.2 ** exp)

    def set_renderer(self, renderer_type=TYPE_NATIVE):
        if renderer_type == self.TYPE_OPENGL:
            self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
        else:
            self.setViewport(QWidget())

    def set_high_quality_antialiasing(self, high_quality_antialiasing):
        self.setRenderHint(QPainter.HighQualityAntialiasing,
                           high_quality_antialiasing)

    def zoom_factor(self):
        return self.transform().m11()

    def zoom_by(self, factor):
        current_zoom = self.zoom_factor()

        if factor < 1 and current_zoom < 0.1:
            return
        elif factor > 1 and current_zoom > 10:
            return
        else:
            self.scale(factor, factor)
            self.zoomChanged.emit()

    def zoom_in(self):
        self.zoom_by(2)

    def zoom_out(self):
        self.zoom_by(0.5)

    def zoom_reset(self):
        if qFuzzyCompare(self.zoom_factor(), 1.0):
            self.resetTransform()
            self.zoomChanged.emit()

    def load_pixmap(self, pixmap, transformation_mode=None):
        scene = self.scene()

        scene.clear()
        self.resetTransform()

        pixmap_item = QGraphicsPixmapItem(pixmap)
        if transformation_mode is not None:
            pixmap_item.setTransformationMode(transformation_mode)
        pixmap_item.setFlags(QGraphicsItem.ItemClipsToShape)
        pixmap_item.setCacheMode(QGraphicsItem.NoCache)
        pixmap_item.setZValue(0)

        scene.addItem(pixmap_item)
        scene.setSceneRect(scene.itemsBoundingRect())

    def load_svg_bytes(self, svg_bytes):
        scene = self.scene()

        scene.clear()
        self.resetTransform()

        renderer = QSvgRenderer(svg_bytes)
        svg_item = QGraphicsSvgItem()
        svg_item.setSharedRenderer(renderer)
        svg_item.setFlags(QGraphicsItem.ItemClipsToShape)
        svg_item.setCacheMode(QGraphicsItem.NoCache)
        svg_item.setZValue(0)

        scene.addItem(svg_item)
        scene.setSceneRect(scene.itemsBoundingRect())
