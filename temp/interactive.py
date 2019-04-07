class QField(QtWidgets.QLineEdit): 

    def __init__(self, parent=None):
        super(QField, self).__init__(parent)

        self.stepSize = 2

        # ui set up
        self._build_ui()
        self._initialize_ui()
        self._connect_signals()

    def _build_ui(self):
        pass

    def _initialize_ui(self):
        pass

    def _connect_signals(self):
        pass

    def wheelEvent(self, event):
        event.accept()
        delta = event.angleDelta() / 120 * self.stepSize