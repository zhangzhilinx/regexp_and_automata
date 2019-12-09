from PyQt5.QtCore import pyqtSignal, qFuzzyCompare
from PyQt5.QtGui import QPainter
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtWidgets import QGraphicsView, QWidget


class SvgView(QGraphicsView):
    TYPE_NATIVE = 'native'
    TYPE_OPENGL = 'opengl'
    zoomChanged = pyqtSignal()

    def __init__(self):
        super(SvgView, self).__init__()

    def wheelEvent(self, event):
        self.zoom_by(1.2 ** (event.pixelDelta() / 240.0))

    def paintEvent(self, event):
        raise NotImplementedError()

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
        need_scale = factor < 1 and current_zoom < 0.1
        need_scale = need_scale or (factor > 1 and current_zoom > 10)
        if need_scale:
            self.scale(factor, factor)
            self.zoomChanged.emit()

    def zoom_in(self):
        self.zoomBy(2)

    def zoom_out(self):
        self.zoom_by(0.5)

    def zoom_reset(self):
        if qFuzzyCompare(self.zoom_factor(), 1.0):
            self.resetTransform()
            self.zoomChanged.emit()
