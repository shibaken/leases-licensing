<template>
    <div>
        <CollapsibleFilters ref="collapsible_filters" @created="collapsible_component_mounted">
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Type</label>
                    <template v-show="select2AppliedToApplicationType">
                        <select class="form-control" ref="filter_application_type" ></select>
                    </template>
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Status</label>
                    <template v-show="select2AppliedToApplicationStatus">
                        <select class="form-control" ref="filter_application_status" ></select>
                    </template>
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Lodged From</label>
                    <div class="input-group date" ref="proposalDateFromPicker">
                        <!-- input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterProposalLodgedFrom" -->
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" v-model="filterProposalLodgedFrom">
                        <!-- span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                        </span -->
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label for="">Lodged To</label>
                    <div class="input-group date" ref="proposalDateToPicker">
                        <!-- input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterProposalLodgedTo" -->
                        <input type="date" class="form-control" placeholder="DD/MM/YYYY" v-model="filterProposalLodgedTo">
                        <!-- span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                        </span -->
                    </div>
                </div>
            </div>
        </CollapsibleFilters>

        <div class="text-right">
            <button type="button" class="btn btn-secondary" @click="geoJsonButtonClicked">GeoJson</button>
        </div>

        <div :id="map_container_id">
            <div :id="elem_id" class="map" style="position: relative;">
                <div class="basemap-button">
                    <img id="basemap_sat" src="../../assets/satellite_icon.jpg" @click="setBaseLayer('sat')" />
                    <img id="basemap_osm" src="../../assets/map_icon.png" @click="setBaseLayer('osm')" />
                </div>
                <div class="optional-layers-wrapper">
                    <div class="optional-layers-button">
                        <template v-if="mode === 'layer'">
                            <img src="../../assets/info-bubble.svg" @click="set_mode('measure')" />
                        </template>
                        <template v-else>
                            <img src="../../assets/ruler.svg" @click="set_mode('layer')" />
                        </template>
                    </div>
                    <div style="position:relative">
                        <transition v-if="optionalLayers.length">
                            <div class="optional-layers-button" @mouseover="hover=true">
                                <img src="../../assets/layers.svg" />
                            </div>
                        </transition>
                        <transition v-if="optionalLayers.length">
                            <div div class="layer_options" v-show="hover" @mouseleave="hover=false" >
                                <div v-for="layer in optionalLayers">
                                    <input
                                        type="checkbox"
                                        :id="layer.ol_uid"
                                        :checked="layer.values_.visible"
                                        @change="changeLayerVisibility(layer)"
                                        class="layer_option"
                                    />
                                    <label :for="layer.ol_uid" class="layer_option">{{ layer.get('title') }}</label>
                                </div>
                            </div>
                        </transition>
                    </div>
                </div>
            </div>
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
/*
import 'select2/dist/css/select2.min.css'
import 'select2-bootstrap-theme/dist/select2-bootstrap.min.css'
*/
import MeasureStyles, { formatLength } from '@/components/common/measure.js'
require("select2/dist/css/select2.min.css");
//require("select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.css");

export default {
    name: 'MapComponentWithFilters',
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
        let default_show_statuses = [
            'draft', 
            'with_assessor', 
            'with_assessor_conditions', 
            'with_approver', 
            'with_referral', 
            'with_referral_conditions',
            'approved_application',
            'approved_competitive_process',
            'approved_editing_invoicing',
            'approved',
            'declined',
            'discarded',
        ]

        return {
            // selected values for filtering
            filterApplicationTypes: sessionStorage.getItem('filterApplicationTypesForMap') ?
                JSON.parse(sessionStorage.getItem('filterApplicationTypesForMap')) :
                [],
            filterApplicationStatuses: sessionStorage.getItem('filterApplicationStatusesForMap') ? 
                JSON.parse(sessionStorage.getItem('filterApplicationStatusesForMap')) : 
                [],
            filterProposalLodgedFrom: sessionStorage.getItem('filterProposalLodgedFromForMap') ? sessionStorage.getItem('filterProposalLodgedFromForMap') : '',
            filterProposalLodgedTo: sessionStorage.getItem('filterProposalLodgedToForMap') ? sessionStorage.getItem('filterProposalLodgedToForMap') : '',

            // filtering options
            application_types: null,
            application_statuses: null,
            select2AppliedToApplicationType: false,
            select2AppliedToApplicationStatus: false,

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
            optionalLayers: [],
            hover: false,
            mode: 'normal',
            drawForMeasure: null,
            measurementLayer: null,
            style: MeasureStyles.defaultStyle,
            segmentStyle: MeasureStyles.segmentStyle,
            labelStyle: MeasureStyles.labelStyle,
            segmentStyles: null,

            proposals: null,
            proposalQuerySource: null,
            proposalQueryLayer: null,

            show_hide_instructions: [ // This array is used as instructions when showing/hiding the apiary sites on the map
                {
                    'id': 'draft',
                    'text': 'Draft',
                    'show': default_show_statuses.includes('draft'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'with_assessor',
                    'text': 'With Assessor',
                    'show': default_show_statuses.includes('with_assessor'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'with_assessor_conditions',
                    'text': 'With Assessor (Conditions)',
                    'show': default_show_statuses.includes('with_assessor_conditions'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'with_approver',
                    'text': 'With Approver',
                    'show': default_show_statuses.includes('with_approver'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'with_referral',
                    'text': 'With Referral',
                    'show': default_show_statuses.includes('with_referral'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'with_referral_conditions',
                    'text': 'With Referral (Conditions)',
                    'show': default_show_statuses.includes('with_referral_conditions'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'approved_application',
                    'text': 'Approved (Application)',
                    'show': default_show_statuses.includes('approved_application'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'approved_competitive_process',
                    'text': 'Approved (Competitive Process)',
                    'show': default_show_statuses.includes('approved_competitive_process'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'approved_editing_invoicing',
                    'text': 'Approved (Editing Invoicing)',
                    'show': default_show_statuses.includes('approved_editing_invoicing'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'approved',
                    'text': 'Approved',
                    'show': default_show_statuses.includes('approved'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'declined',
                    'text': 'Declined',
                    'show': default_show_statuses.includes('declined'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
                {
                    'id': 'discarded',
                    'text': 'Discarded',
                    'show': default_show_statuses.includes('discarded'),
                    'shown': false,
                    'loaded': false,
                    'features': [],
                    'ajax_obj': null,
                },
            ]
        }
    },
    computed: {
        filterApplied: function(){
            console.log('in filterApplied')
            let filter_applied = true
            if(this.filterApplicationStatuses.length == 0 && this.filterApplicationTypes.length == 0 && 
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
        filterProposalLodgedFrom: function() {
            sessionStorage.setItem('filterProposalLodgedFromForMap', this.filterProposalLodgedFrom);
        },
        filterProposalLodgedTo: function() {
            sessionStorage.setItem('filterProposalLodgedToForMap', this.filterProposalLodgedTo);
        },
        filterApplied: function(){
            if (this.$refs.collapsible_filters){
                // Collapsible component exists
                this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
            }
        }
    },
    methods: {
        updateApplicationTypeFilterCache: function(){
            let vm = this
            vm.filterApplicationTypes = $(vm.$refs.filter_application_type).select2('data').map(x => { return x.id })
            sessionStorage.setItem('filterApplicationTypesForMap', JSON.stringify(vm.filterApplicationTypes));
        },
        updateApplicationStatusFilterCache: function(){
            let vm = this
            vm.filterApplicationStatuses = $(vm.$refs.filter_application_status).select2('data').map(x => { return x.id })
            sessionStorage.setItem('filterApplicationStatusesForMap', JSON.stringify(vm.filterApplicationStatuses));
        },
        updateInstructions: function(){
            let vm = this

            if (vm.filterApplicationStatuses.length === 0){
                // Nothing selected means show all
                for (let site_status of vm.show_hide_instructions){
                    console.log('Show: ' + site_status.id)
                    site_status.show = true
                }
            } else {
                for (let site_status of vm.show_hide_instructions){
                    if (vm.filterApplicationStatuses.includes(site_status.id)){
                        console.log('Show: ' + site_status.id)
                        site_status.show = true
                    } else {
                        console.log('Hide: ' + site_status.id)
                        site_status.show = false
                    }
                }
            }
        },
        applySelect2ToApplicationTypes: function(application_types){
            let vm = this
            if (!vm.select2AppliedToApplicationType){
                $(vm.$refs.filter_application_type).select2({
                    "theme": "bootstrap",
                    allowClear: false,
                    placeholder:"Select Type",
                    multiple:true,
                    data: application_types,
                }).
                on('select2:select', function(e){
                    vm.updateApplicationTypeFilterCache()
                    vm.updateInstructions()
                    vm.showHideProposals()
                }).
                on('select2:unselect', function(e){
                    vm.updateApplicationTypeFilterCache()
                    vm.updateInstructions()
                    vm.showHideProposals()
                })
            }
            vm.select2AppliedToApplicationType = true
            $(vm.$refs.filter_application_type).val(vm.filterApplicationTypes).trigger('change')
        },
        applySelect2ToApplicationStatuses: function(application_statuses){
            console.log('in applySelect2ToApplicationStatuses')
            console.log(application_statuses)
            let vm = this
            if (!vm.select2AppliedToApplicationStatus){
                $(vm.$refs.filter_application_status).select2({
                    "theme": "bootstrap",
                    allowClear: false,
                    placeholder:"Select Status",
                    multiple:true,
                    data: application_statuses,
                }).
                on('select2:select', function(e){
                    vm.updateApplicationStatusFilterCache()
                    vm.updateInstructions()
                    vm.showHideProposals()
                }).
                on('select2:unselect', function(e){
                    vm.updateApplicationStatusFilterCache()
                    vm.updateInstructions()
                    vm.showHideProposals()
                })
            }
            vm.select2AppliedToApplicationStatus = true
            $(vm.$refs.filter_application_status).val(vm.filterApplicationStatuses).trigger('change')
        },
        geoJsonButtonClicked: function(){
            console.log('geoJsonButtonClicked')
            // TODO: export all the polygons shown as geojson file
        },
        setBaseLayer: function(selected_layer_name){
            let vm = this
            if (selected_layer_name == 'sat') {
                vm.tileLayerOsm.setVisible(false)
                vm.tileLayerSat.setVisible(true)
                $('#basemap_sat').hide()
                $('#basemap_osm').show()
            } else {
                vm.tileLayerOsm.setVisible(true)
                vm.tileLayerSat.setVisible(false)
                $('#basemap_osm').hide()
                $('#basemap_sat').show()
            }
        },
        set_mode: function(mode){
            this.mode = mode
            if (this.mode === 'layer'){
                this.clearMeasurementLayer()
                this.drawForMeasure.setActive(false)
            } else if (this.mode === 'measure') {
                this.drawForMeasure.setActive(true)
            }
        },
        changeLayerVisibility: function(targetLayer){
            targetLayer.setVisible(!targetLayer.getVisible())
        },
        clearMeasurementLayer: function(){
            let vm = this
            let features = vm.measurementLayer.getSource().getFeatures()
            features.forEach((feature) => {
                vm.measurementLayer.getSource().removeFeature(feature)
            })
        },
        forceToRefreshMap() {
            console.log('forceToRefreshMap()')
            let vm = this
            setTimeout(function(){
                console.log('updateSize()')
                vm.map.updateSize();
            }, 700)
        },
        addJoint: function(point, styles){
            let s = new Style({
                image: new CircleStyle({
                    radius: 2,
                    fill: new Fill({
                        color: '#3399cc'
                    }),
                }),
            })
            s.setGeometry(point)
            styles.push(s)

            return styles
        },
        styleFunctionForMeasurement: function (feature, resolution){
            let vm = this
            let for_layer = feature.get('for_layer', false)

            const styles = []
            styles.push(vm.style)  // This style is for the feature itself
            styles.push(vm.segmentStyle)

            ///////
            // From here, adding labels and tiny circles at the end points of the linestring
            ///////
            const geometry = feature.getGeometry();
            if (geometry.getType() === 'LineString'){
                let segment_count = 0;
                geometry.forEachSegment(function (a, b) {
                    const segment = new LineString([a, b]);
                    const label = formatLength(segment);
                    const segmentPoint = new Point(segment.getCoordinateAt(0.5));

                    // Add a style for this segment
                    let segment_style = vm.segmentStyle.clone() // Because there could be multilpe segments, we should copy the style per segment
                    segment_style.setGeometry(segmentPoint)
                    segment_style.getText().setText(label)
                    styles.push(segment_style)

                    if (segment_count == 0){
                        // Add a tiny circle to the very first coordinate of the linestring
                        let p = new Point(a)
                        vm.addJoint(p, styles)
                    }
                    // Add tiny circles to the end of the linestring
                    let p = new Point(b)
                    vm.addJoint(p, styles)

                    segment_count++;
                });
            }

            if (!for_layer){
                // We don't need the last label when draw on the layer.
                let label_on_mouse = formatLength(geometry);  // Total length of the linestring
                let point = new Point(geometry.getLastCoordinate());
                vm.labelStyle.setGeometry(point);
                vm.labelStyle.getText().setText(label_on_mouse);
                styles.push(vm.labelStyle);
            }

            return styles
        },
        addOptionalLayers: function(){
            let vm = this
            this.$http.get('/api/map_layers/').then(response => {
                let layers = response.body
                for (var i = 0; i < layers.length; i++){
                    let l = new TileWMS({
                        url: env['kmi_server_url'] + '/geoserver/' + layers[i].layer_group_name + '/wms',
                        params: {
                            'FORMAT': 'image/png',
                            'VERSION': '1.1.1',
                            tiled: true,
                            STYLES: '',
                            LAYERS: layers[i].layer_full_name
                        }
                    });

                    let tileLayer= new TileLayer({
                        title: layers[i].display_name.trim(),
                        visible: false,
                        source: l,
                    })

                    // Set additional attributes to the layer
                    tileLayer.set('columns', layers[i].columns)
                    tileLayer.set('display_all_columns', layers[i].display_all_columns)

                    vm.optionalLayers.push(tileLayer)
                    vm.map.addLayer(tileLayer)
                }
            })
        },
        initMap: function(){
            console.log('initMap()')
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

            // Full screen toggle
            let fullScreenControl = new FullScreenControl()
            vm.map.addControl(fullScreenControl)

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

            vm.proposalQuerySource = new VectorSource({ });
            vm.proposalQueryLayer = new VectorLayer({
                source: vm.proposalQuerySource,
            //    style: function(feature, resolution){
            //        let status = getStatusForColour(feature, false, vm.display_at_time_of_submitted)
            //        return getApiaryFeatureStyle(status, feature.get('checked'))
            //    },
            });
            vm.map.addLayer(vm.proposalQueryLayer);
        },
        collapsible_component_mounted: function(){
            this.$refs.collapsible_filters.show_warning_icon(this.filterApplied)
        },
        showHideProposals: function(){
            let vm = this;

            for (let site_status of vm.show_hide_instructions){
                if (site_status.show == site_status.shown){
                    console.log('skip: ' + site_status.id)
                    continue  // All the polygons have been already updated on the map.  Go to the next status
                }

                if (site_status.show){
                    // Show
                    console.log('show: ' + site_status.id)
                    if (site_status.loaded){
                        for (let feature of site_status.features){
                            vm.proposalQuerySource.addFeature(feature);
                        }
                    } else {
                        // Polygon data not loaded yet
                        if (site_status.ajax_obj != null) {
                            // Cancel all the previous requests for this site status
                            site_status.ajax_obj.abort();
                            site_status.ajax_obj = null;
                        }

                        site_status.ajax_obj = $.ajax('/api/proposal/?status=' + site_status.id, {
                            dataType: 'json',
                            success: function(re, status, xhr){
                                for (let proposal of re){
                                    if (proposal.proposalgeometry){
                                        try {
                                            let features = (new GeoJSON()).readFeatures(proposal.proposalgeometry)
                                            vm.proposalQuerySource.addFeatures(features)
                                            site_status.features.push(...features)
                                        } catch (err) {
                                            console.log(err)
                                        }
                                    }
                                }
                                site_status.loaded = true
                            },
                            error: function (jqXhr, textStatus, errorMessage) { // error callback 
                                console.log(errorMessage)
                            }
                        })
                    }
                } else {
                    // Hide
                    console.log('hide: ' + site_status.id)
                    for (let feature of site_status.features){
                        // Remove the apiary_site from the map.  There are no functions to show/hide a feature unlike the layer.
                        if (vm.proposalQuerySource.hasFeature(feature)){
                            try{
                                // Remove the feature from the map
                                vm.proposalQuerySource.removeFeature(feature)
                            } catch (err){
                                console.log(err)
                            }
                        }
                    }
                }
                site_status.shown = site_status.show
            } // END: loop for show_hide_instructions
        },
        fetchFilterLists: function(){
            let vm = this;

            // Application Types
            vm.$http.get(api_endpoints.application_types_dict + '?for_filter=true').then((response) => {
                vm.applySelect2ToApplicationTypes(response.body)
            },(error) => {
            })

            // Application Statuses
            vm.$http.get(api_endpoints.application_statuses_dict + '?for_filter=true').then((response) => {
                vm.applySelect2ToApplicationStatuses(response.body)
            },(error) => {
            })
        },
        addEventListeners: function(){
            let vm = this

            // Lodged From
            //$(vm.$refs.proposalDateFromPicker).datetimepicker(vm.datepickerOptions);
            //$(vm.$refs.proposalDateFromPicker).on('dp.change',function (e) {
            //    if ($(vm.$refs.proposalDateFromPicker).data('DateTimePicker').date()) {
            //        // DateFrom has been picked
            //        vm.filterProposalLodgedFrom = e.date.format('DD/MM/YYYY');
            //        $(vm.$refs.proposalDateToPicker).data("DateTimePicker").minDate(e.date);
            //    }
            //    else if ($(vm.$refs.proposalDateFromPicker).data('date') === "") {
            //        vm.filterProposalLodgedFrom = "";
            //        $(vm.$refs.proposalDateToPicker).data("DateTimePicker").minDate(false);
            //    }
            //});

            // Lodged To
            //$(vm.$refs.proposalDateToPicker).datetimepicker(vm.datepickerOptions);
            //$(vm.$refs.proposalDateToPicker).on('dp.change',function (e) {
            //    if ($(vm.$refs.proposalDateToPicker).data('DateTimePicker').date()) {
            //        // DateTo has been picked
            //        vm.filterProposalLodgedTo = e.date.format('DD/MM/YYYY');
            //        $(vm.$refs.proposalDateFromPicker).data("DateTimePicker").maxDate(e.date);
            //    }
            //    else if ($(vm.$refs.proposalDateToPicker).data('date') === "") {
            //        vm.filterProposalLodgedTo = "";
            //        $(vm.$refs.proposalDateFromPicker).data("DateTimePicker").maxDate(false);
            //    }
            //});
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
            vm.setBaseLayer('osm')
            vm.addOptionalLayers()
            vm.showHideProposals()
        });
    }
}
</script>
<style scoped>
    .map {
        width: 100%;
        height: 600px;
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
        padding: 4px;
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
    .filter_search_wrapper {
        position: relative;
        z-index: 10;
    }
    .table_apiary_site {
        position: relative;
        z-index: 10;
    }
    .button_row {
        display: flex;
        justify-content: flex-end;
    }
    .view_all_button {
        color: #03a9f4;
        cursor: pointer;
    }
    .status_filter_dropdown_wrapper {
        position: relative;
    }
    .status_filter_dropdown_button {
        cursor: pointer;
        width: 100%;
        position: relative;
    }
    .status_filter_dropdown {
        position: absolute;
        background: white;
        display: none;
        border-radius: 2px;
        min-width: max-content;
        padding: 0.5em;
        border: 3px solid rgba(5, 5, 5, .1);
    }
    .sub_option {
        margin-left: 1em;
    }
    .dropdown_arrow::after {
        content: "";
        width: 7px;
        height: 7px;
        border: 0px;
        border-bottom: solid 2px #909090;
        border-right: solid 2px #909090;
        -ms-transform: rotate(45deg);
        -webkit-transform: rotate(45deg);
        transform: rotate(45deg);
        position: absolute;
        top: 50%;
        right: 21px;
        margin-top: -4px;
    }
    /*
    .status_filter_dropdown {
        position: absolute;
        display: none;
        background: white;
        padding: 1em;
    }
    */
    .select2-container {
        z-index: 100000;
    }
    .select2-options {
        z-index: 100000;
    }
    .dataTables_filter {
        display: none !important;
    }
</style>
