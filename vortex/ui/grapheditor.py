"""Main Graph editor widget which is attached to a page of the graphnote book,
Each editor houses a graphicsview and graphicsScene.
"""

import os, logging
from functools import partial

from Qt import QtWidgets, QtCore, QtGui

from vortex.ui import utils
from vortex.ui.graphics import graphpanels, graphicsnode, graph

logger = logging.getLogger(__name__)


class GraphEditor(QtWidgets.QWidget):
    """Graph UI manager
    """
    requestCompoundExpansion = QtCore.Signal(object)

    def __init__(self, model, application, parent=None):
        super(GraphEditor, self).__init__(parent=parent)
        self.model = model
        self.application = application
        self.init()
        self.view.deletePress.connect(self.scene.onDelete)
        self.view.tabPress.connect(self.showNodeLibrary)
        self.nodeLibraryWidget = application.loadUIPlugin("NodeLibrary", dock=False)
        # self.nodeLibraryWidget.widget.finished.connect(self.nodeLibraryWidget.hide)
        self.nodeLibraryWidget.hide()

    def showNodeLibrary(self, point):
        self.nodeLibraryWidget.initUI(dock=False)
        self.nodeLibraryWidget.widget.move(self.mapFromGlobal(point))

    def showPanels(self, state):
        self.view.showPanels(state)

    def init(self):
        self.editorLayout = QtWidgets.QVBoxLayout()
        self.editorLayout.setContentsMargins(0, 0, 0, 0)
        self.editorLayout.setSpacing(0)
        self.toolbar = QtWidgets.QToolBar(parent=self)
        self.createAlignmentActions(self.toolbar)
        self.toolbar.addSeparator()
        self.application.customToolbarActions(self.toolbar)
        self.editorLayout.addWidget(self.toolbar)
        # constructor view and set scene
        self.scene = graph.Scene(self.application, parent=self)

        self.view = graph.View(self.application, self.model, parent=self)
        self.view.setScene(self.scene)
        self.view.contextMenuRequest.connect(self._onViewContextMenu)
        self.view.requestCompoundExpansion.connect(self.requestCompoundExpansion.emit)
        # add the view to the layout
        self.editorLayout.addWidget(self.view)
        self.setLayout(self.editorLayout)

    def createAlignmentActions(self, parent):
        icons = os.environ["VORTEX_ICONS"]
        iconsData = {
            "horizontalAlignCenter.png": ("Aligns the selected nodes to the horizontal center", utils.CENTER | utils.X),
            "horizontalAlignLeft.png": ("Aligns the selected nodes to the Left", utils.LEFT),
            "horizontalAlignRight.png": ("Aligns the selected nodes to the Right", utils.RIGHT),
            "verticalAlignBottom.png": ("Aligns the selected nodes to the bottom", utils.BOTTOM),
            "verticalAlignCenter.png": ("Aligns the selected nodes to the vertical center", utils.CENTER | utils.Y),
            "verticalAlignTop.png": ("Aligns the selected nodes to the Top", utils.TOP)}

        for name, tip in iconsData.items():
            act = QtWidgets.QAction(QtGui.QIcon(os.path.join(icons, name)), "", self)
            act.setStatusTip(tip[0])
            act.setToolTip(tip[0])
            act.triggered.connect(partial(self.alignSelectedNodes, tip[1]))
            parent.addAction(act)

    def _onViewContextMenu(self, menu, item):
        if item and not isinstance(item, graphpanels.PanelWidget):

            if isinstance(item, (graphicsnode.GraphicsNode, graphpanels.Panel)) and item.model.supportsContextMenu():
                item.model.contextMenu(menu)
            elif isinstance(item.parentObject(), (graphicsnode.GraphicsNode, graphpanels.Panel)):
                model = item.parentObject().model
                if model.supportsContextMenu():
                    model.contextMenu(menu)
            return
        edgeStyle = menu.addMenu("ConnectionStyle")
        for i in self.application.config.connectionStyles.keys():
            edgeStyle.addAction(i, self.scene.onSetConnectionStyle)
        alignment = menu.addMenu("Alignment")
        self.createAlignmentActions(alignment)
        menu.addAction("Save Graph", partial(self.application.saveGraph, self.model))

    def alignSelectedNodes(self, direction):
        nodes = self.scene.selectedNodes()
        if len(nodes) < 2:
            return
        if direction == utils.CENTER | utils.X:
            utils.nodesAlignX(nodes, utils.CENTER)
        elif direction == utils.CENTER | utils.Y:
            utils.nodesAlignY(nodes, utils.CENTER)
        elif direction == utils.RIGHT:
            utils.nodesAlignX(nodes, utils.RIGHT)
        elif direction == utils.LEFT:
            utils.nodesAlignX(nodes, utils.LEFT)
        elif direction == utils.TOP:
            utils.nodesAlignY(nodes, utils.TOP)
        else:
            utils.nodesAlignY(nodes, utils.BOTTOM)
        # :todo: only update the selected nodes
        self.scene.updateAllConnections()

    def addNode(self, objectModel):
        return self.scene.createNode(objectModel)
