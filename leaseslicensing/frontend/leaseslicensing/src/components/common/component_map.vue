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
            vm.tileLayerOsm = new TileLayer({
                title: 'OpenStreetMap',
                type: 'base',
                visible: true,
                source: new OSM(),
            });
            console.log(vm.tileLayerOsm)

            vm.map = new Map({
                layers: [
                    vm.tileLayerOsm, 
                    //vm.tileLayerSat,
                    /*
                    new TileLayer({
                        source: new OSM()
                    })
                    */
                ],
                //target: 'map',
                target: vm.elem_id,
                //target: this.$refs['map-root'],
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
            
            vm.map.on('rendercomplete', (event) => {
                console.log(event);
                console.log(vm.map.values_.view.viewportSize_);
                //this.map.setTarget(document.getElementById(this.elem_id));
                console.log(document.getElementById(this.elem_id))
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
        forceMapRefresh: async function() {
            let vm = this
            await setTimeout(function(){
                vm.map.updateSize();
            }, 50)
            console.log(document.getElementById(this.elem_id))
        },
    },
    async mounted() {
        let vm = this;
        console.log("mounted")
        console.log(document.getElementById(this.elem_id))
        //await this.initMap();
        await this.$nextTick(async () => {
            await this.initMap();
        });
        vm.tileLayerOsm.refresh();
        //await this.forceMapRefresh();
        /*
        vm.tileLayerOsm.setZIndex(1000);
        vm.tileLayerOsm.changed();
        console.log(document.getElementById(this.elem_id))
        await this.$nextTick(async () => {
            await this.map.setTarget(document.getElementById(this.elem_id));
        });
        console.log(document.getElementById(this.elem_id))
        console.log(this.map)
        console.log(this.map.values_.view.viewportSize_)

        console.log(this.map.values_.view.viewportSize_)
        */
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

