<template>
    <div class="container" id="externalDash">
        <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
            <li class="nav-item">
                <a class="nav-link" id="pills-applications-tab" data-toggle="pill" href="#pills-applications" role="tab" aria-controls="pills-applications" aria-selected="true">Applications</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="pills-competitive-processes-tab" data-toggle="pill" href="#pills-competitive-processes" role="tab" aria-controls="pills-competitive-processes" aria-selected="false">Competitive Processes</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" id="pills-map-tab" data-toggle="pill" href="#pills-map" role="tab" aria-controls="pills-map" aria-selected="false" @click="toggleComponentMapOn">Map</a>
            </li>
        </ul>

        <div class="tab-content" id="pills-tabContent">
            <div class="tab-pane fade" id="pills-applications" role="tabpanel" aria-labelledby="pills-applications-tab">
                <FormSection :formCollapse="false" label="Applications" Index="applications">
                    <ApplicationsTable
                        level="internal"
                    />
                </FormSection>
                <FormSection :formCollapse="false" label="Applications referred to me" Index="leases_and_licences">

                </FormSection>
            </div>
            <div class="tab-pane fade" id="pills-competitive-processes" role="tabpanel" aria-labelledby="pills-competitive-processes-tab">
                <FormSection :formCollapse="false" label="Competitive Processes" Index="competitive_processes">

                </FormSection>
            </div>
            <div class="tab-pane fade" id="pills-map" role="tabpanel" aria-labelledby="pills-map-tab">
                <FormSection :formCollapse="false" label="Map" Index="map">

                </FormSection>
            </div>
        </div>
    </div>
</template>

<script>
import datatable from '@/utils/vue/datatable.vue'
import FormSection from "@/components/forms/section_toggle.vue"
import ApplicationsTable from "@/components/common/table_proposals"
//import WaitingListTable from "@/components/common/table_approval_waiting_list"
//import LicencesAndPermitsTable from "@/components/common/table_approval_licences_and_permits"
//import CompliancesTable from "@/components/common/table_compliances"
//import AuthorisedUserApplicationsTable from "@/components/common/table_approval_to_be_endorsed"
import { api_endpoints, helpers } from '@/utils/hooks'

export default {
    name: 'InternalDashboard',
    data() {
        let vm = this;
        return {
            empty_list: '/api/empty_list',
            //proposals_url: helpers.add_endpoint_json(api_endpoints.proposals,'user_list'),
            //approvals_url: helpers.add_endpoint_json(api_endpoints.approvals,'user_list'),
            //compliances_url: helpers.add_endpoint_json(api_endpoints.compliances,'user_list'),

            proposals_url: api_endpoints.proposals_paginated_external,
            approvals_url: api_endpoints.approvals_paginated_external,
            compliances_url: api_endpoints.compliances_paginated_external,

            system_name: api_endpoints.system_name,
        }
    },
    components:{
        FormSection,
        ApplicationsTable,
        //WaitingListTable,
        //LicencesAndPermitsTable,
        //CompliancesTable,
        //AuthorisedUserApplicationsTable,
    },
    watch: {

    },
    computed: {
        is_external: function() {
            return this.level == 'external'
        },
        is_internal: function() {
            return this.level == 'internal'
        }
    },
    methods: {
        toggleComponentMapOn: function(){

        },
        set_tabs: function(){
            let aho = $('#pills-tab a[href="#pills-applications"]').tab('show');
        },
    },
    mounted: function () {
        this.set_tabs();
    },
    created: function() {

    },
}
</script>

<style lang="css" scoped>
    .section{
        text-transform: capitalize;
    }
    .list-group{
        margin-bottom: 0;
    }
    .fixed-top{
        position: fixed;
        top:56px;
    }

    .nav-item {
        background-color: rgb(200,200,200,0.8) !important;
        margin-bottom: 2px;
    }

    .nav-item>li>a {
        background-color: yellow !important;
        color: #fff;
    }

    .nav-item>li.active>a, .nav-item>li.active>a:hover, .nav-item>li.active>a:focus {
      color: white;
      background-color: blue;
      border: 1px solid #888888;
    }

	.admin > div {
	  display: inline-block;
	  vertical-align: top;
	  margin-right: 1em;
	}
</style>

