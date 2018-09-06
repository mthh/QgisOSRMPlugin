# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OsrmToolsDialog
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
import csv
import json
import sys
import numpy as np
from re import match
from multiprocessing.pool import ThreadPool

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtNetwork import QNetworkReply
from qgis.core import (
    Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsFeature,
    QgsFillSymbol, QgsGeometry, QgsGraduatedSymbolRenderer, QgsLogger,
    QgsMapLayerProxyModel, QgsMessageLog, QgsPointXY, QgsProject,
    QgsRendererRange, QgsSingleSymbolRenderer, QgsSymbol, QgsVectorFileWriter,
    QgsVectorLayer)
from qgis.gui import QgsMapToolEmitPoint


from .utils import (
    _chain, BaseOsrm, check_host, check_profile_name, decode_geom,
    encode_to_polyline, get_coords_ids, get_isochrones_colors,
    get_search_frame, interpolate_from_times, make_regular_points,
    qgsgeom_from_mpl_collec, prepare_route_symbol, put_layer_on_top,
    save_dialog)

from .osrm_route_dialogUi import Ui_OsrmRouteDialog
from .osrm_table_dialogUi import Ui_OsrmTableDialog
from .osrm_access_dialogUi import Ui_OsrmAccessDialog
from .osrm_batch_route_dialogUi import Ui_OsrmBatchRouteDialog


class OsrmRouteDialog(QtWidgets.QDialog, Ui_OsrmRouteDialog, BaseOsrm):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(OsrmRouteDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.originEmit = QgsMapToolEmitPoint(self.canvas)
        self.intermediateEmit = QgsMapToolEmitPoint(self.canvas)
        self.destinationEmit = QgsMapToolEmitPoint(self.canvas)
        self.nb_route = 0
        self.intermediate = []
        self.pushButtonTryIt.clicked.connect(self.do_work)
        self.pushButtonReverse.clicked.connect(self.reverse_OD)
        self.pushButtonClear.clicked.connect(self.clear_all_single)

    def store_intermediate(self, point):
        if '4326' not in self.canvas.mapSettings().destinationCrs().authid():
            # Convert coordinates from canvas crs to EPSG:4326 crs :
            xform = QgsCoordinateTransform(
                self.canvas.mapSettings().destinationCrs(),
                QgsCoordinateReferenceSystem(4326),
                QgsProject.instance())
            point = xform.transform(point)
        self.intermediate.append(tuple(map(lambda x: round(x, 6), point)))
        self.canvas.unsetMapTool(self.intermediateEmit)
        self.lineEdit_xyI.setText(str(self.intermediate)[1:-1])
        self.putOnTop()

    def store_destination(self, point):
        if '4326' not in self.canvas.mapSettings().destinationCrs().authid():
            # Convert coordinates from canvas crs to EPSG:4326 crs :
            xform = QgsCoordinateTransform(
                self.canvas.mapSettings().destinationCrs(),
                QgsCoordinateReferenceSystem(4326),
                QgsProject.instance())
            point = xform.transform(point)
        self.destination = point
        self.canvas.unsetMapTool(self.destinationEmit)
        self.lineEdit_xyD.setText(
            str(tuple(map(lambda x: round(x, 6), point))))
        self.putOnTop()

    def get_alternatives(self, provider):
        """
        Fetch the geometry of alternatives roads if requested
        """
        for i, alt_geom in enumerate(self.parsed['routes'][1:]):
            decoded_alt_line = decode_geom(alt_geom["geometry"])
            fet = QgsFeature()
            fet.setGeometry(decoded_alt_line)
            fet.setAttributes([
                i + 1,
                alt_geom["duration"],
                alt_geom["distance"]
                ])
            provider.addFeatures([fet])

    def reverse_OD(self):
        try:
            tmp = self.lineEdit_xyD.text()
            self.lineEdit_xyD.setText(str(self.lineEdit_xyO.text()))
            self.lineEdit_xyO.setText(str(tmp))
        except Exception as err:
            print(err)

    def clear_all_single(self):
        self.lineEdit_xyO.setText('')
        self.lineEdit_xyD.setText('')
        self.lineEdit_xyI.setText('')
        self.intermediate = []
        for layer in QgsProject.instance().mapLayers():
            if 'route_osrm' in layer:
                QgsProject.instance().removeMapLayer(layer)
        self.nb_route = 0

    def do_work(self):
        """
        Main method to prepare the request and display the result on the
        QGIS canvas.
        """
        try:
            self.host = check_host(self.lineEdit_host.text())
            profile = check_profile_name(self.lineEdit_profileName.text())
        except (ValueError, AssertionError) as err:
            print(err)
            self.iface.messageBar().pushMessage(
                "Error",
                "Please provide a valid non-empty URL and profile name",
                duration=10)
            return

        origin = self.lineEdit_xyO.text()
        interm = self.lineEdit_xyI.text()
        destination = self.lineEdit_xyD.text()

        try:
            assert match('^[^a-zA-Z]+$', origin) \
                and 46 > len(origin) > 4
            assert match('^[^a-zA-Z]+$', destination) \
                and 46 > len(destination) > 4
            xo, yo = eval(origin)
            xd, yd = eval(destination)
        except:
            self.iface.messageBar().pushMessage(
                "Error", "Invalid coordinates !", duration=10)
            return -1

        if interm:
            try:
                assert match('^[^a-zA-Z]+$', interm) \
                    and 150 > len(interm) > 4
                interm = eval(''.join(['[', interm, ']']))
                tmp = ';'.join(
                    ['{},{}'.format(xi, yi) for xi, yi in interm])
                url = ''.join([
                    "http://", self.host, "/route/", profile, "/",
                    "{},{};".format(xo, yo), tmp, ";{},{}".format(xd, yd),
                    "?overview=full&alternatives={}".format(
                        str(self.checkBox_alternative.isChecked()).lower())])
            except:
                self.iface.messageBar().pushMessage(
                    "Error", "Invalid intemediates coordinates", duration=10)
        else:
            url = ''.join([
                "http://", self.host, "/route/", profile, "/",
                "polyline(", encode_to_polyline([(yo, xo), (yd, xd)]), ")",
                "?overview=full&alternatives={}"
                .format(str(self.checkBox_alternative.isChecked()).lower())])

        self.query_url(url, self.query_done)

    def query_done(self, result):
        if 'error' in result:
            self.display_error(result['error'], 1)
            return
        self.parsed = result['value']

        try:
            enc_line = self.parsed['routes'][0]["geometry"]
            line_geom = decode_geom(enc_line)
        except KeyError:
            self.iface.messageBar().pushMessage(
                "Error",
                "No route found between selected origin/destination",
                duration=5)
            return

        self.nb_route += 1
        osrm_route_layer = QgsVectorLayer(
            "Linestring?crs=epsg:4326&field=id:integer"
            "&field=total_time:integer(20)&field=distance:integer(20)",
            "route_osrm{}".format(self.nb_route), "memory")
        my_symb = prepare_route_symbol(self.nb_route)
        osrm_route_layer.setRenderer(QgsSingleSymbolRenderer(my_symb))
        provider = osrm_route_layer.dataProvider()
        fet = QgsFeature()
        fet.setGeometry(line_geom)
        fet.setAttributes([0, self.parsed['routes'][0]['duration'],
                           self.parsed['routes'][0]['distance']])
        provider.addFeatures([fet])

        osrm_route_layer.updateExtents()
        QgsProject.instance().addMapLayer(osrm_route_layer)
        put_layer_on_top(osrm_route_layer.id())
        self.iface.setActiveLayer(osrm_route_layer)
        self.iface.zoomToActiveLayer()
        # put_layer_on_top(OD_layer.id(), osrm_route_layer.id())
#        if self.checkBox_instruction.isChecked():
#            pr_instruct, instruct_layer = self.prep_instruction()
#            QgsMapLayerRegistry.instance().addMapLayer(instruct_layer)
#            self.iface.setActiveLayer(instruct_layer)

        if self.checkBox_alternative.isChecked() \
                and 'alternative_geometries' in self.parsed:
            self.nb_alternative = len(self.parsed['routes'] - 1)
            self.get_alternatives(provider)
#            if self.dlg.checkBox_instruction.isChecked():
#                for i in range(self.nb_alternative):
#                    pr_instruct, instruct_layer = \
#                       self.prep_instruction(
#                           i + 1, pr_instruct, instruct_layer)
        return


class OsrmTableDialog(QtWidgets.QDialog, Ui_OsrmTableDialog, BaseOsrm):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(OsrmTableDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.encoding = "System"
        self.pushButton_fetch.setDisabled(True)
        self.comboBox_layer.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.comboBox_layer.layerChanged.connect(
            lambda x: self.comboBox_idfield.setLayer(x)
            )
        self.lineEdit_output.textChanged.connect(
            lambda x: self.pushButton_fetch.setEnabled(True)
            if '.csv' in x else self.pushButton_fetch.setDisabled(True)
            )
        self.comboBox_layer_2.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.comboBox_layer_2.layerChanged.connect(
            lambda x: self.comboBox_idfield_2.setLayer(x)
            )
        self.pushButton_browse.clicked.connect(self.output_dialog)
        self.pushButton_fetch.clicked.connect(self.do_work)

    def output_dialog(self):
        self.lineEdit_output.clear()
        self.filename, self.encoding = save_dialog()
        if self.filename is None:
            return
        self.lineEdit_output.setText(self.filename)

    def do_work(self):
        """
        Main method to prepare the query and fecth the table to a .csv file
        """
        try:
            self.host = check_host(self.lineEdit_host.text())
            profile = check_profile_name(self.lineEdit_profileName.text())
        except:
            self.iface.messageBar().pushMessage(
                "Error", "Please provide valid non-empty URL and profile name",
                duration=10)
            return

        self.filename = self.lineEdit_output.text()

        s_layer = self.comboBox_layer.currentLayer()
        d_layer = self.comboBox_layer_2.currentLayer() \
            if self.comboBox_layer_2.currentLayer() != s_layer else None

        self.d_layer = d_layer

        coords_src, self.ids_src = \
            get_coords_ids(s_layer, self.comboBox_idfield.currentField())

        coords_dest, self.ids_dest = \
            get_coords_ids(d_layer, self.comboBox_idfield_2.currentField()) \
            if d_layer else (None, None)

        url = ''.join(["http://", self.host, '/table/', profile, '/'])

        if not coords_dest:
            query = ''.join(
                [url, "polyline(",
                 encode_to_polyline([(c[1], c[0]) for c in coords_src]), ")"])
        else:
            src_end = len(coords_src)
            dest_end = src_end + len(coords_dest)
            query = ''.join([
                url,
                "polyline(",
                encode_to_polyline([
                    (c[1], c[0]) for c in _chain(coords_src, coords_dest)]),
                ")",
                '?sources=',
                ';'.join([str(i) for i in range(src_end)]),
                '&destinations=',
                ';'.join([str(j) for j in range(src_end, dest_end)])
                ])

        self.query_url(query, self.query_done)

    def query_done(self, result):
        if 'error' in result:
            self.display_error(result['error'], 1)
            return

        self.parsed = result['value']

        table = np.array(self.parsed["durations"], dtype=float)

        # Convert the matrix in minutes if needed :
        if self.checkBox_minutes.isChecked():
            table = (table / 60.0).round(2)

        # Replace the value corresponding to a not-found connection :
        if self.checkBox_empty_val.isChecked():
            if self.checkBox_minutes.isChecked():
                table[table == 3579139.4] = np.NaN
            else:
                table[table == 2147483647] = np.NaN

        # Fetch the default encoding if selected :
        if self.encoding == "System":
            self.encoding = sys.getdefaultencoding()

        # Write the result in csv :
        try:
            with open(self.filename, 'w', encoding=self.encoding) as out_file:
                writer = csv.writer(out_file, lineterminator='\n')
                if self.checkBox_flatten.isChecked():
                    table = table.ravel()
                    if self.d_layer:
                        idsx = [
                            (i, j)
                            for i in self.ids_src
                            for j in self.ids_dest
                        ]
                    else:
                        idsx = [
                            (i, j)
                            for i in self.ids_src
                            for j in self.ids_src
                        ]
                    writer.writerow([u'Origin', u'Destination', u'Time'])
                    writer.writerows([
                        [idsx[i][0], idsx[i][1], table[i]]
                        for i in range(len(idsx))
                        ])
                else:
                    if self.d_layer:
                        writer.writerow([u''] + self.ids_dest)
                        writer.writerows(
                            [[self.ids_src[_id]] + line
                             for _id, line in enumerate(table.tolist())])
                    else:
                        writer.writerow([u''] + self.ids_src)
                        writer.writerows(
                            [[self.ids_src[_id]] + line
                             for _id, line in enumerate(table.tolist())])
            QtWidgets.QMessageBox.information(
                self.iface.mainWindow(), 'Done',
                "OSRM table saved in {}".format(self.filename))
        except Exception as err:
            print(err)
            QtWidgets.QMessageBox.information(
                self.iface.mainWindow(), 'Error',
                "Something went wrong...(See Qgis log for traceback)")
            QgsMessageLog.logMessage(
                'OSRM-plugin error report :\n {}'.format(err),
                level=Qgis.Warning)


class OsrmAccessDialog(QtWidgets.QDialog, Ui_OsrmAccessDialog, BaseOsrm):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(OsrmAccessDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.originEmit = QgsMapToolEmitPoint(self.canvas)
        self.intermediateEmit = QgsMapToolEmitPoint(self.canvas)
        self.comboBox_pointlayer.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.comboBox_method.activated[str].connect(self.enable_functionnality)
        self.pushButton_fetch.clicked.connect(self.do_work)
        self.pushButtonClear.clicked.connect(self.clear_all_isochrone)
        self.lineEdit_xyO.textChanged.connect(self.change_nb_center)
        self.nb_isocr = 0
        self.host = None
        self.progress = None

    def change_nb_center(self):
        nb_center = self.lineEdit_xyO.text().count('(')
        self.textBrowser_nb_centers.setHtml(
            """<p style=" margin-top:0px; margin-bottom:0px;"""
            """margin-left:0px; margin-right:0px; -qt-block-indent:0; """
            """text-indent:0px;"><span style=" font-style:italic;">"""
            """{} center(s) selected</span></p>""".format(nb_center))

    def enable_functionnality(self, text):
        functions = (
            self.pushButtonOrigin.setEnabled,
            self.lineEdit_xyO.setEnabled,
            self.textBrowser_nb_centers.setEnabled,
            self.toolButton_poly.setEnabled,
            self.comboBox_pointlayer.setEnabled,
            self.label_3.setEnabled,
            self.checkBox_selectedFt.setEnabled,
            self.pushButton_fetch.setEnabled
        )
        if 'clicking' in text:
            values = (True, True, True, True, False, False, False, True)
        elif 'selecting' in text:
            values = (False, False, False, False, True, True, True, True)
        elif 'method' in text:
            values = (False, False, False, False, False, False, False, False)
        else:
            return
        for func, bool_value in zip(functions, values):
            func(bool_value)

    def clear_all_isochrone(self):
        """
        Clear previously done isochrone polygons and clear the coordinate field
        """
        self.lineEdit_xyO.setText('')
        self.nb_isocr = 0
        for layer in QgsProject.instance().mapLayers():
            if 'isochrone_osrm' in layer or 'isochrone_center' in layer:
                QgsProject.instance().removeMapLayer(layer)

    def store_intermediate_acces(self, point):
        if '4326' not in self.canvas.mapSettings().destinationCrs().authid():
            crsSrc = self.canvas.mapSettings().destinationCrs()
            xform = QgsCoordinateTransform(
                crsSrc,
                QgsCoordinateReferenceSystem(4326),
                QgsProject.instance())
            point = xform.transform(point)
        tmp = self.lineEdit_xyO.text()
        self.change_nb_center()
        self.lineEdit_xyO.setText(
            ', '.join([tmp, str(tuple(map(lambda x: round(x, 6), point)))]))
        self.putOnTop()

    def get_points_from_canvas(self):
        pts = self.lineEdit_xyO.text()
        try:
            assert match('^[^a-zA-Z]+$', pts) and len(pts) > 4
            pts = eval(pts)
            if len(pts) < 2:
                raise ValueError
            elif len(pts) == 2 and not isinstance(pts[0], tuple):
                assert isinstance(pts[0], (int, float))
                assert isinstance(pts[1], (int, float))
                pts = [pts]
            else:
                assert all([isinstance(pt, tuple) for pt in pts])
                assert all([
                    isinstance(coord[0], (float, int))
                    & isinstance(coord[1], (float, int))
                    for coord in pts])
            return pts
        except Exception as err:
            print(err)
            QtWidgets.QMessageBox.warning(
                self.iface.mainWindow(), 'Error',
                "Invalid coordinates selected!")
            return None

    def add_final_pts(self):
        center_pt_layer = QgsVectorLayer(
            "Point?crs=epsg:4326&field=id_center:integer&field=role:string(80)",
            "isochrone_center_{}".format(self.nb_isocr), "memory")
        my_symb = QgsSymbol.defaultSymbol(0)
        my_symb.setColor(QColor("#e31a1c"))
        my_symb.setSize(1.2)
        center_pt_layer.setRenderer(QgsSingleSymbolRenderer(my_symb))
        features = []
        for nb, pt in enumerate(self.pts):
            xo, yo = pt
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPointXY(
                QgsPointXY(float(xo), float(yo))))
            fet.setAttributes([nb, 'Origin'])
            features.append(fet)
        center_pt_layer.dataProvider().addFeatures(features)
        QgsProject.instance().addMapLayer(center_pt_layer)
        put_layer_on_top(center_pt_layer.id())

    def do_work(self):
        """
        Making the accessibility isochrones in few steps:
        - make a grid of points aroung the origin point,
        - snap each point (using OSRM locate function) on the road network,
        - get the time-distance between the origin point and each of these pts
            (using OSRM table function),
        - make an interpolation grid to extract polygons corresponding to the
            desired time intervals (using matplotlib library),
        - render the polygon.
        """
        try:
            self.host = check_host(self.lineEdit_host.text())
            self.profile = check_profile_name(self.lineEdit_profileName.text())
        except (ValueError, AssertionError) as err:
            self.iface.messageBar().pushMessage(
                "Error", "Please provide a valid non-empty URL", duration=10)
            return

        if 'clicking' in self.comboBox_method.currentText():
            pts = self.get_points_from_canvas()
        elif 'selecting' in self.comboBox_method.currentText():
            layer = self.comboBox_pointlayer.currentLayer()
            pts, _ = get_coords_ids(
                layer, '', on_selected=self.checkBox_selectedFt.isChecked())
            pts = tuple(pts)

        if not pts:
            return

        self.make_prog_bar()
        self.polygons = []
        self.pts = pts

        nb_points = 1900 if len(pts) == 1 else 1300
        max_time = self.spinBox_max.value()
        self.interval_time = self.spinBox_intervall.value()
        nb_inter = int(round(max_time / self.interval_time)) + 1
        self.levels = tuple([nb for nb in range(
                0, int(max_time + 1) + self.interval_time,
                self.interval_time)][:nb_inter])

        # self.pts = [{
        #     "levels": self.levels,
        #     "host": self.host,
        #     "max": max_time,
        #     "max_points": nb_points,
        #     "point": pt,
        #     "profile": self.profile,
        #     } for pt in pts]

        self.polygons = []
        self.total_query = len(pts)
        self.done = 0
        for point in self.pts:
            # point = time_param['point']
            # max_time = time_param['max']

            coords_grid = make_regular_points(
                get_search_frame(point, max_time),
                nb_points)

            src_end = 1
            dest_end = src_end + len(coords_grid)

            base_url = ''.join([
                "http://",
                self.host,
                '/table/',
                self.profile,
                '/'])
            url = ''.join([
                base_url,
                "polyline(",
                encode_to_polyline(
                    [(c[1], c[0]) for c in _chain([point], coords_grid)]),
                ")",
                '?sources=',
                ';'.join([str(i) for i in range(src_end)]),
                '&destinations=',
                ';'.join([str(j) for j in range(src_end, dest_end)])
                ])

            self.query_url(url, self.query_done)


    def query_done(self, result):
        if 'error' in result:
            self.display_error(result['error'], 1)
            return

        parsed = result['value']
        durations = np.array(parsed['durations'], dtype=float)
        # new_src_coords = [ft["location"] for ft in parsed["sources"]][0]
        snapped_dest_coords = [
            ft['location'] for ft in parsed['destinations']]
        durations = (durations[0] / 60.0).round(2)  # Round values in minutes

        # Fetch MatPlotLib polygons from a griddata interpolation
        collec_poly = interpolate_from_times(
            durations, np.array(snapped_dest_coords), self.levels)

        # Convert MatPlotLib polygons to QgsGeometry polygons :
        polygons = qgsgeom_from_mpl_collec(collec_poly.collections)
        self.polygons.append(polygons)
        self.done += 1
        if self.done == self.total_query:
            self.all_done()

    def all_done(self):
        if len(self.polygons) == 1:
            self.polygons = self.polygons[0]
        else:
            # Merge the contours from the various isochrones
            self.polygons = np.array(self.polygons).transpose().tolist()
            self.polygons = \
                [QgsGeometry.unaryUnion(polys) for polys in self.polygons]
            self.polygons = list(reversed(self.polygons))
            newpolygons = []
            for i, poly in enumerate(self.polygons):
                if i + 1 == len(self.polygons):
                    newpolygons.append(poly)
                else:
                    poly = poly.difference(
                        QgsGeometry.unaryUnion(self.polygons[i+1:]))
                    newpolygons.append(poly)
            self.polygons = list(reversed(newpolygons))

        isochrone_layer = QgsVectorLayer(
            "MultiPolygon?crs=epsg:4326&field=id:integer"
            "&field=min:integer(10)"
            "&field=max:integer(10)",
            "isochrone_osrm_{}".format(self.nb_isocr), "memory")
        data_provider = isochrone_layer.dataProvider()
        # Add the features to the layer to display :
        features = []
        levels = self.levels[1:]
        self.progress.setValue(8.5)
        for i, poly in enumerate(self.polygons):
            if not poly:
                continue
            ft = QgsFeature()
            ft.setGeometry(poly)
            ft.setAttributes(
                [i, levels[i] - self.interval_time, levels[i]])
            features.append(ft)
        data_provider.addFeatures(features[::-1])
        self.progress.setValue(9.5)

        # Render the value :
        renderer = self.prepare_renderer(
            levels, self.interval_time, len(self.polygons))
        isochrone_layer.setRenderer(renderer)
        # isochrone_layer.setLayerTransparency(25)
        self.iface.messageBar().clearWidgets()
        QgsProject.instance().addMapLayer(isochrone_layer)
        put_layer_on_top(isochrone_layer.id())
        self.add_final_pts()
        self.iface.setActiveLayer(isochrone_layer)
        self.nb_isocr += 1

    @staticmethod
    def prepare_renderer(levels, inter_time, lenpoly):
        cats = [
            ('{} - {} min'.format(levels[i] - inter_time, levels[i]),
             levels[i] - inter_time,
             levels[i])
            for i in range(lenpoly)
            ]  # label, lower bound, upper bound
        colors = get_isochrones_colors(len(levels))
        ranges = []
        for ix, cat in enumerate(cats):
            symbol = QgsFillSymbol()
            symbol.setColor(QColor(colors[ix]))
            ranges.append(QgsRendererRange(cat[1], cat[2], symbol, cat[0]))
        return QgsGraduatedSymbolRenderer('max', ranges)


class OsrmBatchRouteDialog(QtWidgets.QDialog, Ui_OsrmBatchRouteDialog, BaseOsrm):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(OsrmBatchRouteDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.ComboBoxOrigin.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.ComboBoxDestination.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.pushButtonReverse.clicked.connect(self.reverse_OD)
        # self.pushButtonBrowse.clicked.connect(self.output_dialog_geo)
        self.pushButtonRun.clicked.connect(self.do_work)
        # self.comboBox_host.activated[str].connect(self.add_host)

    def reverse_OD(self):
        """ Switch the Origin and the Destination layer"""
        try:
            tmp_o = self.ComboBoxOrigin.currentLayer()
            tmp_d = self.ComboBoxDestination.currentLayer()
            self.ComboBoxOrigin.setLayer(tmp_d)
            self.ComboBoxDestination.setLayer(tmp_o)
        except Exception as err:
            QgsMessageLog.logMessage(
                'OSRM-plugin error report :\n {}'.format(err),
                level=Qgis.Warning)

    def do_work(self):
        try:
            self.host = check_host(self.lineEdit_host.text())
            self.profile = check_profile_name(self.lineEdit_profileName.text())
        except (ValueError, AssertionError) as err:
            print(err)
            self.iface.messageBar().pushMessage(
                "Error",
                "Please provide a valid non-empty URL and profile name",
                duration=10)
            return
        self.nb_routes_done, self.errors, self.consecutive_errors = 0, 0, 0
        self.features = []
        queries = self._prepare_queries()
        self.nb_queries = len(queries)
        urls = []
        self.make_prog_bar()
        for yo, xo, yd, xd in queries:
            urls.append(''.join([
                'http://',
                self.host,
                '/route/',
                self.profile,
                '/',
                '{},{};{},{}'.format(xo, yo, xd, yd),
                '?overview=full',
                '&steps=false',
                '&alternatives=false',
            ]))
        for ix, url in enumerate(urls):
            self.nb_queries -= 1
            self.query_url(url, self.query_done)

    def query_done(self, result):
        if 'error' in result:
            self.display_error(result['error'], 1)
            self.errors += 1
            self.consecutive_errors += 1
            return
        self.consecutive_errors = 0
        parsed = result['value']
        line_geom = decode_geom(parsed['routes'][0]['geometry'])
        ft = QgsFeature()
        ft.setGeometry(line_geom)
        ft.setAttributes([
            self.nb_routes_done,
            parsed['routes'][0]['duration'],
            parsed['routes'][0]['distance'],
        ])
        self.features.append(ft)
        self.nb_routes_done += 1
        if self.nb_queries == 0:
            self.return_batch_route()

    def _prepare_queries(self):
        """Get the coordinates for each viaroute to query"""
        origin_layer = self.ComboBoxOrigin.currentLayer()
        destination_layer = self.ComboBoxDestination.currentLayer()
        if '4326' not in origin_layer.crs().authid():
            xform = QgsCoordinateTransform(
                origin_layer.crs(),
                QgsCoordinateReferenceSystem(4326),
                QgsProject.instance())
            origin_ids_coords = \
                [(ft.id(), xform.transform(ft.geometry().asPoint()))
                 for ft in origin_layer.getFeatures()]
        else:
            origin_ids_coords = \
                [(ft.id(), ft.geometry().asPoint())
                 for ft in origin_layer.getFeatures()]

        if '4326' not in destination_layer.crs().authid():
            xform = QgsCoordinateTransform(
                origin_layer.crs(),
                QgsCoordinateReferenceSystem(4326),
                QgsProject.instance())
            destination_ids_coords = \
                [(ft.id(), xform.transform(ft.geometry().asPoint()))
                 for ft in destination_layer.getFeatures()]
        else:
            destination_ids_coords = \
                [(ft.id(), ft.geometry().asPoint())
                 for ft in destination_layer.getFeatures()]
        return [(origin[1][1], origin[1][0], dest[1][1], dest[1][0])
                for origin in origin_ids_coords
                for dest in destination_ids_coords]

    def return_batch_route(self):
        """Save and/or display the routes retrieved"""
        osrm_batch_route_layer = QgsVectorLayer(
            "Linestring?crs=epsg:4326&field=id:integer"
            "&field=total_time:integer(20)&field=distance:integer(20)",
            "routes_osrm_{}".format(self.nb_routes_done), "memory")
        provider = osrm_batch_route_layer.dataProvider()
        provider.addFeatures(self.features)

        if self.filename:
            error = QgsVectorFileWriter.writeAsVectorFormat(
                osrm_batch_route_layer, self.filename,
                self.encoding, None, "ESRI Shapefile")
            if error != QgsVectorFileWriter.NoError:
                self.iface.messageBar().pushMessage(
                    "Error",
                    "Can't save the result into {} - Output have been "
                    "added to the canvas (see QGis log for error trace"
                    "back)".format(self.filename), duration=10)
                QgsMessageLog.logMessage(
                    'OSRM-plugin error report :\n {}'.format(error),
                    level=Qgis.Warning)
                QgsProject.instance().addMapLayer(osrm_batch_route_layer)
                self.iface.setActiveLayer(osrm_batch_route_layer)
                return -1
            else:
                QtWidgets.QMessageBox.information(
                    self.iface.mainWindow(), 'Info',
                    "Result saved in {}".format(self.filename))
        if self.check_add_layer.isChecked():
            self.iface.setActiveLayer(osrm_batch_route_layer)
        else:
            QgsProject.instance().removeMapLayer(
                osrm_batch_route_layer.id())
        self.iface.messageBar().clearWidgets()
