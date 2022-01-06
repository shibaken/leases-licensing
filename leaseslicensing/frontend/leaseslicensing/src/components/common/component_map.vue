<template>
        <div class="map-wrapper row col-sm-12">
            <div id='popup-container'>
                <p id='popup-coordinates'></p>
            </div>
            <div :id="elem_id" ref="map-root" class="map">
                <div class="basemap-button">
                    <img v-if="showSatIcon" id="basemap_sat" src="../../assets/satellite_icon.jpg" @click="setBaseLayer('sat')" />
                    <img v-if="!showSatIcon" id="basemap_osm" src="../../assets/map_icon.png" @click="setBaseLayer('osm')" />
                </div>
            </div>
        </div>
</template>

<script>
import uuid from 'uuid';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import WMTSCapabilities from 'ol/format/WMTSCapabilities';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import TileWMS from 'ol/source/TileWMS';
import WMTS, {optionsFromCapabilities} from 'ol/source/WMTS';
import GeoJSON from 'ol/format/GeoJSON';
import Overlay from 'ol/Overlay';
import { FullScreen, MousePosition, defaults as olDefaults, OverviewMap, ScaleLine, ZoomSlider, ZoomToExtent } from 'ol/control';
import { Draw, Modify, Snap } from 'ol/interaction';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';

export default {
    name: 'ComponentMap',
    data: function() {
        return {
            elem_id: uuid(),
            //elem_id: 'elem_id',
            optionalLayers: [],
            mode: 'normal',
            map: null,
            tileLayerOsm: null,
            tileLayerSat: null,
            showSatIcon: true,
        }
    },
    props: {
    },
    computed: {
    },
    methods: {
        toggleSatIcon: function(layer) {
            if (layer === 'osm') {
                this.showSatIcon = true;
            } else {
                this.showSatIcon = false;
            }
        },
        initMap: async function() {
            let vm = this;
            // Full screen toggle
            const fullScreenControl = new FullScreen();
            // Show mouse coordinates
            const mousePositionControl = new MousePosition({
                coordinateFormat: function(coords){
                    let message = vm.getDegrees(coords) + "\n";
                    return  message;
                },
                target: document.getElementById('mouse-position'),
                className: 'custom-mouse-position',
            });
            const overviewMapControl = new OverviewMap({
                collapsed: false,
                layers: [
                            new TileLayer({
                                source: new OSM()
                            })
                        ]
                });
            const scaleLineControl = new ScaleLine();
            const zoomSliderControl = new ZoomSlider();
            const zoomToExtentControl = new ZoomToExtent();

            let satelliteTileWms = new TileWMS({
                        url: env['kmi_server_url'] + '/geoserver/public/wms',
                        params: {
                            'FORMAT': 'image/png',
                            'VERSION': '1.1.1',
                            tiled: true,
                            STYLES: '',
                            LAYERS: 'public:mapbox-satellite',
                        }
                    });

            vm.tileLayerOsm = new TileLayer({
                title: 'OpenStreetMap',
                type: 'base',
                visible: true,
                source: new OSM(),
            });
            vm.tileLayerSat = new TileLayer({
                title: 'Satellite',
                type: 'base',
                visible: false,
                source: satelliteTileWms,
            })

            vm.map = new Map({
                controls: olDefaults().extend([
                    fullScreenControl,
                    mousePositionControl,
                    zoomSliderControl,
                    zoomToExtentControl,
                    //overviewMapControl,
                    scaleLineControl,
                    ]),
                layers: [
                    vm.tileLayerOsm, 
                    vm.tileLayerSat,
                ],
                target: vm.elem_id,
                view: new View({
                    center: [115.95, -31.95],
                    zoom: 7,
                    projection: 'EPSG:4326',
                    maxZoom: 12,
                    minZoom: 3,
                })
            });
            /*
            // Measure tool
            let draw_source = new VectorSource({ wrapX: false })
            vm.drawForMeasure = new Draw({
                source: draw_source,
                type: 'LineString',
                style: vm.styleFunctionForMeasurement,
            })
            // Set a custom listener to the Measure tool
            vm.drawForMeasure.set('escKey', '')
            vm.drawForMeasure.on('change:escKey', function(evt){
                //vm.drawForMeasure.finishDrawing()
            })
            vm.drawForMeasure.on('drawstart', function(evt){
                vm.measuring = true
            })
            vm.drawForMeasure.on('drawend', function(evt){
                vm.measuring = false
            })

            // Create a layer to retain the measurement
            vm.measurementLayer = new VectorLayer({
                title: 'Measurement Layer',
                source: draw_source,
                style: function(feature, resolution){
                    feature.set('for_layer', true)
                    return vm.styleFunctionForMeasurement(feature, resolution)
                },
            });
            vm.map.addInteraction(vm.drawForMeasure)
            vm.map.addLayer(vm.measurementLayer)
            */
        },
        forceMapRefresh: function() {
            let vm = this
            setTimeout(function(){
                vm.map.updateSize();
            }, 50)
            console.log(document.getElementById(this.elem_id))
        },
        setBaseLayer: function(selected_layer_name){
            console.log('in setBaseLayer')
            if (selected_layer_name == 'sat') {
                this.toggleSatIcon('sat');
                this.tileLayerOsm.setVisible(false)
                this.tileLayerSat.setVisible(true)
            } else {
                this.toggleSatIcon('osm');
                this.tileLayerOsm.setVisible(true)
                this.tileLayerSat.setVisible(false)
            }
        },
        getDegrees: function(coords){
            return coords[0].toFixed(6) + ', ' + coords[1].toFixed(6);
        },
    },
    mounted() {
        let vm = this;
        console.log("mounted")
        this.initMap();
        this.map.setSize([690, 400]);
        vm.map.renderSync();
        console.log(this.map.getSize())
    },
}
</script>

<style lang="css" scoped>
    .map{
        height: 400px;
        width: 100%;
    }
    .map-wrapper {
        position: relative;
        padding: 0;
        margin: 0;
    }
    .basemap-button {
        position: absolute;
        bottom: 25px;
        right: 10px;
        z-index: 400;
        -moz-box-shadow: 3px 3px 3px #777;
        -webkit-box-shadow: 3px 3px 3px #777;
        box-shadow: 3px 3px 3px #777;
        -moz-filter: brightness(1.0);
        -webkit-filter: brightness(1.0);
        filter: brightness(1.0);
        border: 2px white solid;
    }
    .basemap-button:hover,.optional-layers-button:hover{
        cursor: pointer;
        -moz-filter: brightness(0.9);
        -webkit-filter: brightness(0.9);
        filter: brightness(0.9);
    }
    .basemap-button:active {
        bottom: 24px;
        right: 9px;
        -moz-box-shadow: 2px 2px 2px #555;
        -webkit-box-shadow: 2px 2px 2px #555;
        box-shadow: 2px 2px 2px #555;
        -moz-filter: brightness(0.8);
        -webkit-filter: brightness(0.8);
        filter: brightness(0.8);
    }
    .optional-layers-wrapper {
        position: absolute;
        top: 70px;
        left: 10px;
    }
    .optional-layers-button {
        position: relative;
        z-index: 400;
        background: white;
        border-radius: 2px;
        border: 3px solid rgba(5, 5, 5, .1);
        margin-bottom: 2px;
        cursor: pointer;
        display: block;
    }
    .layer_options {
        position: absolute;
        top: 0;
        left: 0;
        z-index: 410;
        background: white;
        border-radius: 2px;
        cursor: auto;
        min-width: max-content;
        /*
        box-shadow: 3px 3px 3px #777;
        -moz-filter: brightness(1.0);
        -webkit-filter: brightness(1.0);
        */
        padding: 0.5em;
        border: 3px solid rgba(5, 5, 5, .1);
    }
    .ol-popup {
        position: absolute;
        min-width: 95px;
        background-color: white;
        -webkit-filter: drop-shadow(0 1px 4px rgba(0,0,0,0.2));
        filter: drop-shadow(0 1px 4px rgba(0,0,0,0.2));
        padding: 2px;
        border-radius: 4px;
        border: 1px solid #ccc;
        bottom: 12px;
        left: -50px;
    }
    .ol-popup:after, .ol-popup:before {
        top: 100%;
        border: solid transparent;
        content: " ";
        height: 0;
        width: 0;
        position: absolute;
        pointer-events: none;
    }
    .ol-popup:after {
        border-top-color: white;
        border-width: 10px;
        left: 48px;
        margin-left: -10px;
    }
    .ol-popup:before {
        border-top-color: #cccccc;
        border-width: 11px;
        left: 48px;
        margin-left: -11px;
    }
    .ol-popup-closer {
        text-decoration: none;
        position: absolute;
        top: 2px;
        right: 8px;
    }
    .close-icon:hover {
        filter: brightness(80%);
    }
    .close-icon {
        position: absolute;
        left: 1px;
        top: -11px;
        filter: drop-shadow(0 1px 4px rgba(0,0,0,0.2));
    }
    .popup-wrapper {
        padding: 0.25em;
    }
    .popup-content-header {
        background: darkgray;
        color: white;
    }
    .popup-content {
        font-size: small;
    }
    .table_caption {
        color: green;
    }
    .layer_option:hover {
        cursor: pointer;
    }

</style>

