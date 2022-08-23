<template>
    <div>
        <div v-if="is_internal" class="row">
            <div class="text-end mb-2">
                <button type="button" class="btn btn-primary pull-right" @click="add_party_clicked"><i class="fa-solid fa-circle-plus"></i>Add Party</button>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-12">
                <datatable
                    ref="competitive_process_datatable"
                    :id="datatable_id"
                    :dtHeaders="datatable_headers"
                    :dtOptions="datatable_options"
                    :key="datatable_key"
                />
            </div>
        </div>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid'
import { api_endpoints, helpers } from '@/utils/hooks'
import datatable from '@/utils/vue/datatable.vue'

export default {
    name: 'TableParties',
    props: {
        level: '',
        competitive_process_parties: [],
    },
    data() {
        let vm = this;
        return {
            datatable_id: uuid(),
            datatable_key: uuid(),
        }
    },
    components: {
        datatable,
    },
    created: function(){
    },
    computed: {
        column_id: () => {
            return {
                data: "id",
                name: 'id',
                orderable: false,
                searchable: false,
                visible: false,
                'render': function(row, type, full){
                    console.log(full)
                    return full.id
                }
            }
        },
        column_name: () => {
            return {
                data: null,
                'render': function(row, type, full){
                    if (full.is_person)
                        return full.person.fullname
                    return ''
                }
            }
        },
        column_organisation: () => {
            return {
                data: null,
                'render': function(row, type, full){
                    if (full.is_organisation)
                        return full.organisation.name
                    return ''
                }
            }
        },
        column_phone: () => {
            return {
                data: null,
                'render': function(row, type, full){
                    return '(phone)'
                }
            }
        },
        column_mobile: () => {
            return {
                data: null,
                'render': function(row, type, full){
                    return '(mobile)'
                }
            }

        },
        column_email: () => {
            return {
                data: null,
                'render': function(row, type, full){
                    return '(email)'
                }
            }
        },
        column_action: () => {
            return {
                data: null,
                'render': function(row, type, full){
                    return '(action)'
                }
            }
        },
        is_external: function() {
            return this.level == 'external'
        },
        is_internal: function() {
            return this.level == 'internal'
        },
        datatable_headers: function(){
            if (this.is_internal){
                return ['id', 'Name', 'Organisation', 'Phone', 'Mobile', 'Email', 'Action']
            }
            return []
        },
        datatable_options: function(){
            let vm = this

            let columns = []
            let search = null
            if(vm.is_internal){
                columns = [
                    vm.column_id,
                    vm.column_name,
                    vm.column_organisation,
                    vm.column_phone,
                    vm.column_mobile,
                    vm.column_email,
                    vm.column_action,
                ]
                search = true
            }

            return {
                autoWidth: false,
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                rowCallback: function (row, competitive_process){
                    let row_jq = $(row)
                    row_jq.children().first().addClass(vm.td_expand_class_name)
                },
                responsive: true,
                serverSide: false,
                data: vm.competitive_process_parties,
                searching: search,
                // ajax: {
                //     "url": api_endpoints.competitive_process + '?format=datatables',
                //     "dataSrc": 'data',
                // },
                dom: "<'d-flex align-items-center'<'me-auto'l>f>" +
                     "<'row'<'col-sm-12'tr>>" +
                    //  "<'d-flex align-items-center'<'me-auto'i>p>",
                     "<'d-flex align-items-center'<'me-auto'i>>",
                columns: columns,
                processing: true,
                initComplete: function() {
                    console.log('in initComplete')
                },
            }
        }
    },
    methods: {
        add_party_clicked: () => {

        },
    }
}
</script>
