## QgisOSRMPlugin - OSRM plugin for QGIS
**WIP**
This is basically a rewrite of https://github.com/mthh/osrm-qgis-plugin trying to avoid the pitfalls previously encountered (and adapting the code for QGIS3).


#### Overview

Tiny [QGIS](http://project-osrm.org/) plug-in allowing to retrieve and display data from an instance of  [OSRM](http://project-osrm.org/).

This plug-in is in its early stage of development and the code is hosted [on github](https://github.com/mthh/QgisOSRMplugin).


#### Functionality

- Find a route
- Get a time matrix
- Make accessibility isochrones
- Compute and export many routes


#### Usage

This plug-in is primarily aimed to be used on a local instance of OSRM.

If used to request the public API you have to adhere to the [API Usage Policy](https://github.com/Project-OSRM/osrm-backend/wiki/Api-usage-policy) (which include no heavy usage, like computing many `/viaroute` with this plug-in)

<!-- #### Example

Images of this page are displayed on OpenStreetMap tiles (© OpenStreetMap contributors) and route computations were done with Open Source Routing Machine. -->

#### Licence and attribution

If the information computed by this plugin is intend to be reused, you have to properly display the source of the routes and the data licence attribution :

- All the routes/time matrix displayed are computed by the underlying routing engine [OSRM](http://project-osrm.org/).
- Route computed by the OSRM public API rely on [openStreetMap](http://www.openstreetmap.org/copyright) dataset which is under [ODbL](http://www.openstreetmap.org/copyright)
