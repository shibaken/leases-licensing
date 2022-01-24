<template>
    <div>
        <CollapsibleFilters ref="collapsible_filters" @created="collapsible_component_mounted">
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Type</label>
                    <select class="form-control" v-model="filterApplicationType">
                        <option value="all">All</option>
                        <option v-for="type in application_types" :value="type.code">{{ type.description }}</option>
                    </select>
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Status</label>
                    <select class="form-control" v-model="filterApplicationStatus">
                        <option value="all">All</option>
                        <option v-for="status in application_statuses" :value="status.code">{{ status.description }}</option>
                    </select>
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Lodged From</label>
                    <div class="input-group date" ref="proposalDateFromPicker">
                        <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterProposalLodgedFrom">
                        <span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                        </span>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Lodged To</label>
                    <div class="input-group date" ref="proposalDateToPicker">
                        <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterProposalLodgedTo">
                        <span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                        </span>
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div :id="map_container_id">
            <div :id="elem_id" class="map"></div>
        </div>

    </div>
</template>

<script>
import Vue from 'vue'
import uuid from 'uuid'
import { api_endpoints, helpers } from '@/utils/hooks'
import CollapsibleFilters from '@/components/forms/collapsible_component.vue'

import 'ol/ol.css';
//import 'ol-layerswitcher/dist/ol-layerswitcher.css'
import Map from 'ol/Map';
import View from 'ol/View';
import WMTSCapabilities from 'ol/format/WMTSCapabilities';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import TileWMS from 'ol/source/TileWMS';
import WMTS, {optionsFromCapabilities} from 'ol/source/WMTS';
import Collection from 'ol/Collection';
import { Draw, Modify, Snap } from 'ol/interaction';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { Circle as CircleStyle, Fill, Stroke, Style, Text, RegularShape } from 'ol/style';
import { FullScreen as FullScreenControl, MousePosition as MousePositionControl } from 'ol/control';
import { Feature } from 'ol';
import { LineString, Point } from 'ol/geom';
import { getDistance } from 'ol/sphere';
import { circular} from 'ol/geom/Polygon';
import GeoJSON from 'ol/format/GeoJSON';
import Overlay from 'ol/Overlay';
import { getArea, getLength } from 'ol/sphere'
import Datatable from '@vue-utils/datatable.vue'
import Cluster from 'ol/source/Cluster';
import 'select2/dist/css/select2.min.css'
import 'select2-bootstrap-theme/dist/select2-bootstrap.min.css'

export default {
    name: 'MapComponent',
    props: {
        level:{
            type: String,
            required: true,
            validator: function(val) {
                let options = ['internal', 'referral', 'external'];
                return options.indexOf(val) != -1 ? true: false;
            }
        },
        /*
        target_email_user_id: {
            type: Number,
            required: false,
            default: 0,
        }
        */
    },
    data() {
        let vm = this;

        return {
            // selected values for filtering
            filterApplicationType: sessionStorage.getItem('filterApplicationType') ? sessionStorage.getItem('filterApplicationType') : 'all',
            filterApplicationStatus: sessionStorage.getItem('filterApplicationStatus') ? sessionStorage.getItem('filterApplicationStatus') : 'all',
            filterProposalLodgedFrom: sessionStorage.getItem('filterProposalLodgedFrom') ? sessionStorage.getItem('filterProposalLodgedFrom') : '',
            filterProposalLodgedTo: sessionStorage.getItem('filterProposalLodgedTo') ? sessionStorage.getItem('filterProposalLodgedTo') : '',

            // filtering options
            application_types: [],
            application_statuses: [],

            dateFormat: 'DD/MM/YYYY',
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },

            elem_id: uuid(),
            map_container_id: uuid(),
            map: null,
            tileLayerOsm: null,
            tileLayerSat: null,
        }
    },
    computed: {
        filterApplied: function(){
            let filter_applied = true
            if(this.filterApplicationStatus.toLowerCase() === 'all' && this.filterApplicationType.toLowerCase() === 'all' && 
                this.filterProposalLodgedFrom.toLowerCase() === '' && this.filterProposalLodgedTo.toLowerCase() === ''){
                filter_applied = false
            }
            return filter_applied
        },
    },
    components:{
        CollapsibleFilters,
    },
    watch: {
        filterApplicationStatus: function() {
            sessionStorage.setItem('filterApplicationStatus', this.filterApplicationStatus);
        },
        filterApplicationType: function() {
            sessionStorage.setItem('filterApplicationType', this.filterApplicationType);
        },
        filterProposalLodgedFrom: function() {
            sessionStorage.setItem('filterProposalLodgedFrom', this.filterProposalLodgedFrom);
        },
        filterProposalLodgedTo: function() {
            sessionStorage.setItem('filterProposalLodgedTo', this.filterProposalLodgedTo);
        },
        filterApplied: function(){
            if (this.$refs.collapsible_filters){
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        }
    },
    methods: {
        forceToRefreshMap() {
            console.log('forceToRefreshMap()')
            let vm = this
            setTimeout(function(){
                console.log('updateSize()')
                vm.map.updateSize();
            }, 700)
        },
        initMap: function(){
            console.log('initMap()')
            let vm = this;
            //const map = new Map({
            //    layers: [
            //            new TileLayer({
            //                      source: new OSM(),
            //                    }),
            //          ],
            //    //target: 'map',
            //    target: vm.elem_id,
            //    view: new View({
            //            center: [0, 0],
            //            zoom: 2,
            //          }),
            //})

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

            vm.map = new Map({
                layers: [
                    vm.tileLayerOsm, 
                    vm.tileLayerSat,
                ],
                //target: 'map',
                target: vm.elem_id,
                view: new View({
                    center: [115.95, -31.95],
                    zoom: 7,
                    projection: 'EPSG:4326'
                })
            });

        },
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        fetchFilterLists: function(){
            let vm = this;

            // Application Types
            vm.$http.get(api_endpoints.application_types_dict+'?apply_page=False').then((response) => {
                vm.application_types = response.body
            },(error) => {
            })

            // Application Statuses
            vm.$http.get(api_endpoints.application_statuses_dict).then((response) => {
                if (vm.is_internal){
                    vm.application_statuses = response.body.internal_statuses
                } else {
                    vm.application_statuses = response.body.external_statuses
                }
            },(error) => {
            })
        },
        addEventListeners: function(){
            let vm = this

            // Lodged From
            $(vm.$refs.proposalDateFromPicker).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.proposalDateFromPicker).on('dp.change',function (e) {
                if ($(vm.$refs.proposalDateFromPicker).data('DateTimePicker').date()) {
                    // DateFrom has been picked
                    vm.filterProposalLodgedFrom = e.date.format('DD/MM/YYYY');
                    $(vm.$refs.proposalDateToPicker).data("DateTimePicker").minDate(e.date);
                }
                else if ($(vm.$refs.proposalDateFromPicker).data('date') === "") {
                    vm.filterProposalLodgedFrom = "";
                    $(vm.$refs.proposalDateToPicker).data("DateTimePicker").minDate(false);
                }
            });

            // Lodged To
            $(vm.$refs.proposalDateToPicker).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.proposalDateToPicker).on('dp.change',function (e) {
                if ($(vm.$refs.proposalDateToPicker).data('DateTimePicker').date()) {
                    // DateTo has been picked
                    vm.filterProposalLodgedTo = e.date.format('DD/MM/YYYY');
                    $(vm.$refs.proposalDateFromPicker).data("DateTimePicker").maxDate(e.date);
                }
                else if ($(vm.$refs.proposalDateToPicker).data('date') === "") {
                    vm.filterProposalLodgedTo = "";
                    $(vm.$refs.proposalDateFromPicker).data("DateTimePicker").maxDate(false);
                }
            });
        }
    },
    created: function(){
        console.log('created()')
        this.fetchFilterLists()
    },
    mounted: function(){
        console.log('mounted()')
        let vm = this;

        this.$nextTick(() => {
            vm.addEventListeners()
            vm.initMap()
            //vm.map.setSize([window.innerWidth, window.innerHeight])  // Now sure if we need this or forceToRefreshMap() is sufficient
        });
    }
}
</script>
<style scoped>
.map {
    width: 100%;
    height: 600px;
}
</style>
