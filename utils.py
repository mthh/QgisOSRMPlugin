# -*- coding: utf-8 -*-
import numpy as np
from PyQt5.QtCore import QFileInfo, QSettings, Qt, QUrl
from PyQt5.QtGui import QColor
from PyQt5.QtNetwork import QNetworkRequest
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QProgressBar
from qgis.core import (
    Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform,
    QgsGeometry, QgsMessageLog, QgsNetworkAccessManager,
    QgsPoint, QgsPointXY, QgsProject, QgsSymbol)
from qgis.gui import QgsEncodingFileDialog
from matplotlib.pyplot import contourf
from scipy.interpolate import griddata


class BaseOsrm(object):
    """
    Base class to be subclassed by each OSRM dialog class.
    It contains some methods used by the five next class.
    """
    def display_error(self, error, code):
        msg = {
            1: "An error occured when trying to contact the OSRM instance",
            2: "OSRM plugin error report : Too many errors occured "
               "when trying to contact the OSRM instance at {} - "
               "Route calculation has been stopped".format(self.host),
            }
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushMessage(
            "Error", msg[code] + "(see QGis log for error traceback)",
            duration=10)
        QgsMessageLog.logMessage(
            'OSRM-plugin error report :\n {}'.format(error),
            level=Qgis.Warning)

    def make_prog_bar(self):
        progMessageBar = self.iface.messageBar().createMessage(
            "Creation in progress...")
        self.progress = QProgressBar()
        self.progress.setMaximum(10)
        self.progress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        progMessageBar.layout().addWidget(self.progress)
        self.iface.messageBar().pushWidget(
            progMessageBar, Qgis.Info)

    def query_url(self, url, callback):
        req = QNetworkRequest(QUrl(url))
        self.reply = QgsNetworkAccessManager.instance().get(req)
        self.reply.finished.connect(callback)

    def print_about(self):
        mbox = QMessageBox(self.iface.mainWindow())
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle('About')
        mbox.setTextFormat(Qt.RichText)
        mbox.setText(
            "<p><b>OSRM plugin for qgis</b><br><br>"
            "Author: mthh, 2018<br>Licence : GNU GPL v2<br><br><br>Underlying "
            "routing engine is <a href='http://project-osrm.org'>OSRM</a>"
            "(Open Source Routing Engine) :<br>- Based on <a href='http://"
            "www.openstreetmap.org/copyright'>OpenStreetMap</a> "
            "dataset<br>- Easy to start a local instance<br>"
            "- Pretty fast engine (based on contraction hierarchies and mainly"
            " writen in C++)<br>- Mainly authored by D. Luxen and C. "
            "Vetter<br>(<a href='http://project-osrm.org'>http://project-osrm"
            ".org</a> or <a href='https://github.com/Project-OSRM/osrm"
            "-backend#references-in-publications'>on GitHub</a>)<br></p>")
        mbox.open()

    def store_origin(self, point):
        """
        Method to store a click on the QGIS canvas
        """
        if '4326' not in self.canvas.mapSettings().destinationCrs().authid():
            crsSrc = self.canvas.mapSettings().destinationCrs()
            xform = QgsCoordinateTransform(
                crsSrc,
                QgsCoordinateReferenceSystem(4326),
                QgsProject.instance())
            point = xform.transform(point)
        self.origin = point
        self.canvas.unsetMapTool(self.originEmit)
        self.lineEdit_xyO.setText(
            str(tuple(map(lambda x: round(x, 6), point))))


def check_host(url):
    """
    Helper function to get the hostname in desired format
    (i.e without "http://", with the port if needed
        and without the last '/')
    """
    if len(url) < 4:
        raise ValueError('Probably empty/non-valable url')
    if not ('http' in url and '//' in url) and url[-1] == '/':
        host = url[:-1]
    elif not ('http:' in url and '//' in url):
        host = url
    elif 'http://' in url[:7] and url[-1] == '/':
        host = url[7:-1]
    elif 'http://' in url[:7]:
        host = url[7:]
    else:
        host = url
    return host


def check_profile_name(profile_name):
    assert len(profile_name) > 3
    assert "/" in profile_name
    return profile_name


def prepare_route_symbol(nb_route):
    colors = ['#1f78b4', '#ffff01', '#ff7f00',
              '#fb9a99', '#b2df8a', '#e31a1c']
    p = nb_route % len(colors)
    my_symb = QgsSymbol.defaultSymbol(1)
    my_symb.setColor(QColor(colors[p]))
    my_symb.setWidth(1.2)
    return my_symb


def _chain(*lists):
    for li in lists:
        for elem in li:
            yield elem


def encode_to_polyline(pts):
    output = []

    def write_enc(coord):
        coord = int(round(coord * 1e5))
        coord <<= 1
        coord = coord if coord >= 0 else ~coord
        while coord >= 0x20:
            output.append((0x20 | (coord & 0x1f)) + 63)
            coord >>= 5
        output.append(coord + 63)

    write_enc(pts[0][0])
    write_enc(pts[0][1])
    for i, pt in enumerate(pts[1:]):
        write_enc(pt[0] - pts[i][0])
        write_enc(pt[1] - pts[i][1])
    return ''.join([chr(i) for i in output])


def decode_geom(encoded_polyline):
    """
    Function decoding an encoded polyline (with 'encoded polyline
    algorithme') and returning a QgsGeometry object
    Params:
    encoded_polyline: str
        The encoded string to decode
    """
    return QgsGeometry.fromPolyline(
        [QgsPoint(i[1], i[0]) for i
         in PolylineCodec().decode(encoded_polyline)])


def make_regular_points(bounds, nb_pts):
    """
    Return a square grid of regular points (same number in height and width
    even if the bbox is not a square).
    """
    xmin, ymin, xmax, ymax = bounds
    nb_h = int(round(np.sqrt(nb_pts)))
    prog_x = [xmin + i * ((xmax - xmin) / nb_h) for i in range(nb_h + 1)]
    prog_y = [ymin + i * ((ymax - ymin) / nb_h) for i in range(nb_h + 1)]
    result = []
    for x in prog_x:
        for y in prog_y:
            result.append((x, y))
    return result


def save_dialog(filtering="CSV (*.csv *.CSV)"):
    settings = QSettings()
    dirName = settings.value("/UI/lastShapefileDir")
    encode = settings.value("/UI/encoding")
    fileDialog = QgsEncodingFileDialog(
        None, "Save output csv", dirName, filtering, encode
        )
    fileDialog.setDefaultSuffix('csv')
    fileDialog.setFileMode(QFileDialog.AnyFile)
    fileDialog.setAcceptMode(QFileDialog.AcceptSave)
    # fileDialog.setConfirmOverwrite(True)
    if not fileDialog.exec_() == QDialog.Accepted:
        return None, None
    files = fileDialog.selectedFiles()
    settings.setValue(
        "/UI/lastShapefileDir",
        QFileInfo(files[0]).absolutePath())
    return (files[0], fileDialog.encoding())


def get_coords_ids(layer, field, on_selected=False):
    if on_selected:
        get_features_method = layer.selectedFeatures
    else:
        get_features_method = layer.getFeatures

    if '4326' not in layer.crs().authid():
        xform = QgsCoordinateTransform(
            layer.crs(),
            QgsCoordinateReferenceSystem(4326),
            QgsProject.instance())
        coords = [xform.transform(ft.geometry().asPoint())
                  for ft in get_features_method()]
    else:
        coords = [ft.geometry().asPoint() for ft in get_features_method()]

    if field != '':
        ids = [ft.attribute(field) for ft in get_features_method()]
    else:
        ids = [ft.id() for ft in get_features_method()]

    return coords, ids


def get_search_frame(point, max_time):
    """
    Define the search frame (ie. the bbox), given a center point and
    the maximum time requested
    Return
    ------
    xmin, ymin, xmax, ymax : float
    """
    search_len = (max_time * 4) * 1000
    crsSrc = QgsCoordinateReferenceSystem(4326)
    xform = QgsCoordinateTransform(
        crsSrc,
        QgsCoordinateReferenceSystem(3857),
        QgsProject.instance())
    point = xform.transform(QgsPointXY(*point))
    xmin = point[0] - search_len
    ymin = point[1] - search_len
    xmax = point[0] + search_len
    ymax = point[1] + search_len
    crsSrc = QgsCoordinateReferenceSystem(3857)
    xform = QgsCoordinateTransform(
        crsSrc,
        QgsCoordinateReferenceSystem(4326),
        QgsProject.instance())
    xmin, ymin = xform.transform(QgsPointXY(xmin, ymin))
    xmax, ymax = xform.transform(QgsPointXY(xmax, ymax))
    return xmin, ymin, xmax, ymax


def interpolate_from_times(times, coords, levels, rev_coords=False):
    if not rev_coords:
        x = coords[..., 0]
        y = coords[..., 1]
    else:
        x = coords[..., 1]
        y = coords[..., 0]
    xi, yi = np.mgrid[np.nanmin(x):np.nanmax(x):100j, np.nanmin(y):np.nanmax(y):100j]
    # zi = griddata(x, y, times, xi, yi, interp='linear')
    zi = griddata(coords, times, (xi, yi), 'linear')
    print(zi.shape)
    collec_poly = contourf(
        xi, yi, zi, levels, vmax=np.nanmax(zi), vmin=np.nanmin(zi))
    return collec_poly


def qgsgeom_from_mpl_collec(collections):
    polygons = []
    for i, polygon in enumerate(collections):
        mpoly = []
        for path in polygon.get_paths():
            path.should_simplify = False
            poly = path.to_polygons()
            if len(poly) > 0 and len(poly[0]) > 3:
                exterior = [QgsPointXY(*p.tolist()) for p in poly[0]]
                holes = [[QgsPointXY(*p.tolist()) for p in h]
                         for h in poly[1:] if len(h) > 3]
                if len(holes) == 1:
                    mpoly.append([exterior, holes[0]])
                elif len(holes) > 1:
                    mpoly.append([exterior] + [h for h in holes])
                else:
                    mpoly.append([exterior])

        if len(mpoly) == 1:
            polygons.append(QgsGeometry.fromPolygonXY(mpoly[0]))
        elif len(mpoly) > 1:
            polygons.append(QgsGeometry.fromMultiPolygonXY(mpoly))
        else:
            polygons.append(QgsGeometry.fromPolygonXY([]))
    return polygons


def get_isochrones_colors(nb_features):
    """ Ugly "helper" function to rewrite to avoid repetitions """
    return {
            1: ('#a6d96a',),
            2: ('#fee08b', '#a6d96a'),
            3: ('#66bd63',
                '#fee08b', '#f46d43'),
            4: ('#1a9850', '#a6d96a',
                '#fee08b', '#f46d43'),
            5: ('#1a9850', '#66bd63',
                '#ffffbf', '#fc8d59', '#d73027'),
            6: ('#1a9850', '#66bd63', '#d9ef8b',
                '#fee08b', '#fc8d59', '#d73027'),
            7: ('#1a9850', '#66bd63', '#d9ef8b', '#ffffbf',
                '#fee08b', '#fc8d59', '#d73027'),
            8: ('#1a9850', '#66bd63', '#a6d96a', '#d9ef8b',
                '#fee08b', '#fdae61', '#f46d43', '#d73027'),
            9: ('#1a9850', '#66bd63', '#a6d96a', '#d9ef8b', '#ffffbf',
                '#fee08b', '#fdae61', '#f46d43', '#d73027'),
            10: ('#006837', '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b',
                 '#fee08b', '#fdae61', '#f46d43', '#d73027', '#a50026'),
            11: ('#006837', '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b',
                 '#ffffbf', '#fee08b', '#fdae61', '#f46d43', '#d73027',
                 '#a50026'),
            12: ('#006837', '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b',
                 '#e7ef88', '#ffffbf', '#fee08b', '#fdae61', '#f46d43',
                 '#d73027', '#a50026'),
            13: ('#006837', '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b',
                 '#e7ef88', '#ffffbf', '#fee08b', '#fdae61', '#f46d43',
                 '#d73027', '#bb2921', '#a50026'),
            14: ('#006837', '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b',
                 '#e7ef88', '#ffffbf', '#fff6a0', '#fee08b', '#fdae61',
                 '#f46d43', '#d73027', '#bb2921', '#a50026'),
            15: ('#006837', '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b',
                 '#e7ef88', '#ffffbf', '#ffffbf', '#fff6a0', '#fee08b',
                 '#fdae61', '#f46d43', '#d73027', '#bb2921', '#a50026'),
            16: ('#006837', '#1a9850', '#66bd63', '#a6d96a',
                 '#d9ef8b', '#e7ef88', '#ffffbf', '#ffffbf', '#ffffbf',
                 '#fff6a0', '#fee08b', '#fdae61', '#f46d43', '#d73027',
                 '#bb2921', '#a50026'),
            }[nb_features]

###############################################################################
#
#    Ligthweighted copy of the Polyline Codec for Python
#    (https://pypi.python.org/pypi/polyline)
#    realeased under MIT licence, 2014, by Bruno M. Custodio :
#
###############################################################################


class PolylineCodec(object):
    """
    Copy of the "_trans" and "decode" functions
    from the Polyline Codec (https://pypi.python.org/pypi/polyline) released
    under MIT licence, 2014, by Bruno M. Custodio.
    """
    def _trans(self, value, index):
        byte, result, shift = None, 0, 0
        while (byte is None or byte >= 0x20):
            byte = ord(value[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            comp = result & 1
        return ~(result >> 1) if comp else (result >> 1), index

    def decode(self, expression):
        coordinates, index, lat, lng, length = [], 0, 0, 0, len(expression)
        while (index < length):
            lat_change, index = self._trans(expression, index)
            lng_change, index = self._trans(expression, index)
            lat += lat_change
            lng += lng_change
            coordinates.append((lat / 1e5, lng / 1e5))
        return coordinates
