from vortex import api
from Qt import QtCore, QtWidgets
from zoo.libs.pyqt.widgets import elements


class OutlinerPlugin(api.UIPlugin):
    id = "Outliner"
    autoLoad = True
    creator = "David Sparrow"
    dockArea = QtCore.Qt.LeftDockWidgetArea

    def show(self, parent):
        return Outliner(self.application, parent=parent)


class Outliner(QtWidgets.QFrame):
    def __init__(self, application, parent=None):
        super(Outliner, self).__init__(parent)
        self.application = application
        self.setObjectName("Outliner")
        layout = elements.vBoxLayout(self)
        self.tree = QtWidgets.QTreeWidget(parent=self)
        layout.addWidget(self.tree)
        self.tree.header().hide()
        # self.newNode(application.graphNoteBook.currentPage().model)
        self.application.events.selectionChanged.connect(self.onSceneSelection)
        self.application.events.nodeDeleted.connect(self.removeNode)
        self.application.events.nodeCreated.connect(self.newNode)
        # self.newNode({"model": self.application.currentModel})
        # self.graph.setShortcutForWidget(self, "Outliner")

    def onSceneSelection(self, selection):

        iterator = QtWidgets.QTreeWidgetItemIterator(self.tree)
        for it in iterator:
            item = it.value()
            itemModel = item.data(0, QtCore.Qt.UserRole + 1)
            item.setSelected(itemModel.isSelected())

    def _findItemForModel(self, objectModel):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.tree)
        for it in iterator:
            item = it.value()
            if item.data(0, QtCore.Qt.UserRole + 1) == objectModel:
                return item

    def newNode(self, objectModel):
        objectModel = objectModel
        if not objectModel:
            return
        parentModel = objectModel.parentObject()
        parentItem = self.tree.invisibleRootItem()
        if parentModel:
            parent = self._findItemForModel(parentModel)
            if parent is not None:
                parentItem = parent

        item = QtWidgets.QTreeWidgetItem(parentItem, [objectModel.text()])
        item.setData(0, QtCore.Qt.UserRole + 1, objectModel)
        parentItem.addChild(item)
        item.setExpanded(True)

    def removeNode(self, objectModels):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.tree)
        for it in iterator:
            item = it.value()
            if item.data(0, QtCore.Qt.UserRole + 1) in objectModels:
                parent = item.parent()
                parent.removeChild(item)
