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

            // For expander
            td_expand_class_name: 'expand-icon',
            td_collapse_class_name: 'collapse-icon',
        }
    },
    components: {
        datatable,
    },
    created: function(){
    },
    mounted: function(){
        let vm = this
        vm.$nextTick(() => {
            vm.addEventListeners();
        });
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
                createdRow: function(row, data, index){
                    let $row = this.api().row(row)

                    // $(row).child($('<div>aho</div>')).show()
                    // console.log({row})
                    // let row_jq = $(row)
                    // console.log({row_jq})
                    // let $row = vm.$refs.competitive_process_datatable.vmDataTable.row(row_jq)

                    console.log({$row})
                    // $row.child('aho').show()
                },
                rowCallback: function (row, competitive_process){
                    // console.log({row})
                    // let row_jq = $(row)
                    // row_jq.children().first().addClass(vm.td_expand_class_name)
                    //row_jq.child('aho')
                    // console.log(vm.$refs.competitive_process_datatable.vmDataTable)

                    // let $row = vm.$refs.competitive_process_datatable.vmDataTable.row($row)
                    // if($row.child.isShown()){
                    //     console.log('shown')
                    // } else {
                    //     console.log('not shown')
                    // }
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
        add_party_clicked: function (){

        },
        addEventListeners: function (){
            let vm = this

            vm.$refs.competitive_process_datatable.vmDataTable.on('click', 'td', function(e) {
                console.log('clicked')

                let td_link = $(this)
                let tr = td_link.closest('tr')
                let first_td = tr.children().first()

                // Get full data of this row
                let $row = vm.$refs.competitive_process_datatable.vmDataTable.row(tr)
                let full_data = $row.data()

                if($row.child.isShown()){
                    $row.child.hide();
                    first_td.removeClass(vm.td_collapse_class_name).addClass(vm.td_expand_class_name)
                } else {
                    first_td.removeClass(vm.td_expand_class_name).addClass(vm.td_collapse_class_name)
                    $row.child('id: ' + full_data.id).show();
                }
            })
        },
    }
}
</script>

<style>
.collapse-icon {
    cursor: pointer;
}
.collapse-icon::before {
    top: 5px;
    left: 4px;
    height: 14px;
    width: 14px;
    border-radius: 14px;
    line-height: 14px;
    border: 2px solid white;
    line-height: 14px;
    content: '-';
    color: white;
    background-color: #d33333;
    display: inline-block;
    box-shadow: 0px 0px 3px #444;
    box-sizing: content-box;
    text-align: center;
    text-indent: 0 !important;
    font-family: 'Courier New', Courier monospace;
    margin: 5px;
}
.expand-icon {
    cursor: pointer;
}
.expand-icon::before {
    top: 5px;
    left: 4px;
    height: 14px;
    width: 14px;
    border-radius: 14px;
    line-height: 14px;
    border: 2px solid white;
    line-height: 14px;
    content: '+';
    color: white;
    background-color: #337ab7;
    display: inline-block;
    box-shadow: 0px 0px 3px #444;
    box-sizing: content-box;
    text-align: center;
    text-indent: 0 !important;
    font-family: 'Courier New', Courier monospace;
    margin: 5px;
}

</style>