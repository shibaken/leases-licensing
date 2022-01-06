<template>
        <div class="row col-sm-12">
            <div id='popup-container'>
                <p id='popup-coordinates'></p>
            </div>
            <div :id="elem_id" ref="map-root" class="map-bb">
            <!--div :id="elem_id" ref="map-root"-->
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

export default {
    name: 'ComponentMap',
    data: function() {
        return {
            //elem_id: uuid(),
            elem_id: 'elem_id',
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
        initMap: function() {
            let vm = this;
            vm.tileLayerOsm = new TileLayer({
                title: 'OpenStreetMap',
                type: 'base',
                visible: true,
                source: new OSM(),
            });
            console.log(vm.tileLayerOsm)

            vm.map = new Map({
                layers: [
                    //vm.tileLayerOsm, 
                    //vm.tileLayerSat,
                    new TileLayer({
                        source: new OSM()
                    })
                ],
                //target: 'map',
                //target: 'elem_id',
                target: this.$refs['map-root'],
                /*
                view: new View({
                    center: [115.95, -31.95],
                    zoom: 7,
                    projection: 'EPSG:4326'
                })
                */
               view: new View({
                   center: [-12080385, 7567433],
                   zoom: 3,
                   maxZoom: 12,
                   minZoom: 2,
                   rotation: 0
               }),
            });
            /*
            const popupContainerElement = document.getElementById('popup-coordinates');
            const popup = new Overlay({
                element: popupContainerElement,
                //positioning: 'bottom-left'
                positioning: 'top-right'
            })
            vm.map.addOverlay(popup);
            vm.map.on('click', function(e){
                //console.log(e);
                const clickedCoordinate = e.coordinate;
                popup.setPosition(undefined);
                popup.setPosition(clickedCoordinate);
                popupContainerElement.innerHTML = clickedCoordinate;
            })
            */
        },
    },
    created: async function() {
        /*
        await this.$nextTick(() => {
            this.initMap();
        });
        console.log(this.map)
        */
    },
    mounted: function() {
        this.initMap();
        console.log(this.map)
    },
}
</script>

<style lang="css" scoped>
    .map-bb{
        height: 400px;
        width: 100%;
    }
    .map-wrapper {
        position: relative;
        padding: 0;
        margin: 0;
    }
</style>

