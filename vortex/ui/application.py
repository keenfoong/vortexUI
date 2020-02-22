import os
from functools import partial

from Qt import QtCore, QtWidgets, QtGui
from zoo.libs.plugin import pluginmanager
from vortex.ui import plugin


class UIApplication(QtCore.QObject):
    """High Level Application object, handles node plugins, UI Plugins, global events
    """

    def __init__(self, uiConfig):
        """
        :param uiConfig:
        :type uiConfig:
        """
        super(UIApplication, self).__init__()
        self.pluginManager = pluginmanager.PluginManager(plugin.UIPlugin, variableName="id")
        self.pluginManager.registerPaths(os.environ["VORTEX_UI_PLUGINS"].split(os.pathsep))
        self.config = uiConfig
        self._keyBoardMapping = {}

    def loadUIPlugin(self, pluginId, dock=True):
        # pass
        uiExt = self.pluginManager.loadPlugin(pluginId, application=self)
        if not uiExt:
            return
        uiExt.initUI(dock=dock)
        return uiExt

    def uiPlugin(self, pluginId):
        return self.pluginManager.getPlugin(pluginId)

    def loadPlugins(self):
        for uiPlugin in self.pluginManager.plugins.values():
            if uiPlugin.autoLoad:
                self.loadUIPlugin(uiPlugin.id)

    def mainWindow(self):
        for wid in QtWidgets.QApplication.topLevelWidgets():
            if wid.objectName() == "Vortex":
                return wid

    def customToolbarActions(self, parent):
        pass

    def initialize(self):
        pass

    def registeredNodes(self):
        """Returns a full list of registered nodes

        :return:
        :rtype: list(str)
        """
        return []

    def setShortcutForWidget(self, widget, name):
        keymap = self._keyBoardMapping.get(name)
        if not keymap:
            return

        for k, command in keymap:
            if command:
                QtWidgets.QShortcut(QtGui.QKeySequence(k), widget, partial(self.executeCommand, widget, command))

    def executeCommand(self, widget, command):
        print("executingCommand", widget, command)

    def saveGraph(self, objectModel):
        print("test")
        return {}