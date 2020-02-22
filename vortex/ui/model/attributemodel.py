from Qt import QtGui, QtCore


class AttributeModel(QtCore.QObject):
    def __init__(self, objectModel, parent=None):
        """
        :param objectModel: The Node ObjectModel
        :type objectModel: ::class:`ObjectModel`
        """
        super(AttributeModel, self).__init__()
        self.objectModel = objectModel
        self.parent = parent

    def __repr__(self):
        return "<{}-{}>".format(self.__class__.__name__, self.text())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        return id(self)

    def fullPathName(self):
        return ""

    def text(self):
        return "attributeName"

    def setValue(self, value):
        pass

    def value(self):
        return

    def textAlignment(self):
        if self.isInput():
            return QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        else:
            return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter

    def setText(self, text):
        return False

    def isArray(self):
        return False

    def isElement(self):
        if self.parent is not None:
            return self.parent.isArray()

    def isCompound(self):
        return False

    def elements(self):
        return []

    def children(self):
        return []

    def canAcceptConnection(self, plug):
        return True

    def acceptsMultipleConnections(self):
        if self.isInput():
            return False
        return True

    def isConnected(self):
        return False

    def createConnection(self, attribute):
        return False

    def deleteConnection(self, attribute):
        return False

    def toolTip(self):
        return "Im a tooltip for attributes"

    def size(self):
        return QtCore.QSize(150, 30)

    def textColour(self):
        return QtGui.QColor(200, 200, 200)

    def isInput(self):
        return True

    def isOutput(self):
        return True

    def highlightColor(self):
        return QtGui.QColor(255, 255, 255)

    def itemEdgeColor(self):
        return QtGui.QColor(0, 180, 0)

    def itemColour(self):
        return QtGui.QColor(0, 180, 0)

    def serialize(self):
        return {}
