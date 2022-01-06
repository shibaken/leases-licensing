<template>
        <div class="map-wrapper row col-sm-12">
            <div id='popup-container'>
                <p id='popup-coordinates'></p>
            </div>
            <div :id="elem_id" ref="map-root" class="map">
                <div class="basemap-button">
                    <img id="basemap_sat" src="../../assets/satellite_icon.jpg" @click="setBaseLayer('sat')" />
                    <img id="basemap_osm" src="../../assets/map_icon.png" @click="setBaseLayer('osm')" />
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
import { FullScreen as FullScreenControl, MousePosition as MousePositionControl } from 'ol/control';

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
        }
    },
    props: {
    },
    computed: {
    },
    methods: {
        initMap: async function() {
            let vm = this;
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
                visible: true,
                source: satelliteTileWms,
            })
            console.log(vm.tileLayerOsm)

            vm.map = new Map({
                layers: [
                    vm.tileLayerOsm, 
                    //vm.tileLayerSat,
                ],
                target: vm.elem_id,
                view: new View({
                    center: [115.95, -31.95],
                    zoom: 7,
                    projection: 'EPSG:4326'
                })
            });
            // Full screen toggle
            vm.map.addControl(new FullScreenControl());
            vm.tileLayerOsm.on('postcompose', (evt) => {
                console.log(evt);
            });

            vm.map.on('rendercomplete', (evt) => {
                console.log(evt);
                console.log(this.map.getSize())
                console.log(document.getElementById(this.elem_id))
            });
            window.addEventListener('resize', (evt) => {
                console.log(evt);
            });
            console.log("initMap complete");
        },
        forceMapRefresh: function() {
            let vm = this
            setTimeout(function(){
                vm.map.updateSize();
            }, 50)
            console.log(document.getElementById(this.elem_id))
        },
    },
    async mounted() {
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

</style>

