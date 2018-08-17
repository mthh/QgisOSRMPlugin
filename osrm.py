# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OsrmTools
                                 A QGIS plugin
 Plugin to use OSRM API in Qgis
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-07-24
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Matthieu Viry
        email                : matthieu.viry@cnrs.fr
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
import os.path
from PyQt5.QtCore import (
    QSettings, QTranslator, qVersion, QCoreApplication, QObject)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .osrm_dialog import (
    OsrmRouteDialog,
    OsrmTableDialog,
    OsrmAccessDialog,
    OsrmTspDialog,
    OsrmBatchRouteDialog)


class OsrmTools:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'OsrmTools_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg_route = OsrmRouteDialog(self.iface)
        self.dlg_access = OsrmAccessDialog()
        self.dlg_table = OsrmTableDialog(self.iface)
        self.dlg_tsp = OsrmTspDialog()
        self.dlg_batchroute = OsrmBatchRouteDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&OSRM')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'OsrmTools')
        self.toolbar.setObjectName(u'OsrmTools')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('OsrmTools', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.add_action(
            ':/plugins/osrm/img/icon.png',
            text=self.tr(u'Find a route with OSRM'),
            callback=self.run_route,
            parent=self.iface.mainWindow(),
            )

        self.add_action(
            ':/plugins/osrm/img/icon_table.png',
            text=self.tr(u'Get a time matrix with OSRM'),
            callback=self.run_table,
            parent=self.iface.mainWindow(),
            )

        self.add_action(
            ':/plugins/osrm/img/icon_access.png',
            text=self.tr(u'Make accessibility isochrones with OSRM'),
            callback=self.run_accessibility,
            parent=self.iface.mainWindow(),
            )

        self.add_action(
            None,
            text=self.tr(u'Solve the Traveling Salesman Problem with OSRM'),
            callback=self.run_tsp,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            )

        self.add_action(
            None,
            text=self.tr(u'Export many routes from OSRM'),
            callback=self.run_batchroute,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False,
            )

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&OSRM'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run_route(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg_route.show()
        self.dlg_route.originEmit.canvasClicked.connect(
            self.dlg_route.store_origin)
        self.dlg_route.intermediateEmit.canvasClicked.connect(
            self.dlg_route.store_intermediate)
        self.dlg_route.destinationEmit.canvasClicked.connect(
            self.dlg_route.store_destination)
        self.dlg_route.pushButtonOrigin.clicked.connect(
            lambda _: self.canvas.setMapTool(self.dlg_route.originEmit))
        self.dlg_route.pushButtonIntermediate.clicked.connect(
            lambda _: self.canvas.setMapTool(self.dlg_route.intermediateEmit))
        self.dlg_route.pushButtonDest.clicked.connect(
            lambda _: self.canvas.setMapTool(self.dlg_route.destinationEmit))
        self.dlg_route.pushButton_about.clicked.connect(
            self.dlg_route.print_about)

        # Run the dialog event loop
        result = self.dlg_route.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def run_table(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg_table.show()
        # Run the dialog event loop
        result = self.dlg_table.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def run_accessibility(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg_access.show()
        # Run the dialog event loop
        result = self.dlg_access.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def run_tsp(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg_tsp.show()
        # Run the dialog event loop
        result = self.dlg_tsp.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def run_batchroute(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg_batchroute.show()
        # Run the dialog event loop
        result = self.dlg_batchroute.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
