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
                    ref="parties_datatable"
                    :id="datatable_id"
                    :dtHeaders="datatable_headers"
                    :dtOptions="datatable_options"
                />
            </div>
        </div>

        <AddParty 
            ref="add_party" 
            :recordSaleId="recordSaleId"
            :key="recordSaleKey"
            @closeModal="closeModal"
            @refreshDatatable="refreshFromResponse"
        />
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid'
import { api_endpoints, helpers } from '@/utils/hooks'
import datatable from '@/utils/vue/datatable.vue'
import CustomRow from '@/components/common/custom_row.vue'
import { createApp, h } from 'vue';
import AddParty from '@/components/common/modal_add_party.vue';

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
            expandable_row_class_name: 'expandable_row_class_name',
        }
    },
    components: {
        datatable,
        AddParty,
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
                columnDefs: [
                    {responsivePriority: 1, targets: 1},
                    {responsivePriority: 2, targets: 2},
                    {responsivePriority: 6, targets: 3},
                    {responsivePriority: 5, targets: 4},
                    {responsivePriority: 4, targets: 5},
                    {responsivePriority: 3, targets: 6},
                ],
                createdRow: function(row, full_data, dataIndex){
                    full_data.expanded = false
                },
                rowCallback: function (row, aho){
                    let $row = $(row)
                    $row.children().first().addClass(vm.td_expand_class_name)
                },
                responsive: true,
                serverSide: false,
                data: vm.competitive_process_parties,
                searching: search,
                dom: "<'d-flex align-items-center'<'me-auto'l>f>" +
                     "<'row'<'col-sm-12'tr>>" +
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
        openAddPartyModal: function() {
            this.$nextTick(() => {
                this.$refs.add_party.isModalOpen = true;
            });
        },
        closeModal: function() {
            this.uuid++;
        },
        refreshFromResponse: async function(){
            // await this.$refs.vessels_datatable.vmDataTable.ajax.reload();
            console.log('TODO: update table')
        },
        number_of_columns: function() {
            // Return the number of visible columns
            let num =  this.$refs.parties_datatable.vmDataTable.columns(':visible').nodes().length;
            return num
        },
        updateCustomRowColSpan: function(){
            // Set colspan to the manually added table row
            $('tr.' + this.expandable_row_class_name + ' td').attr('colspan', this.number_of_columns())
        },
        add_party_clicked: function (){
            this.openAddPartyModal()
        },
        addClickEventHandler: function(){
            let vm = this
            vm.$refs.parties_datatable.vmDataTable.on('click', 'td', function(e) {
                let td_link = $(this)
                if (!(td_link.hasClass(vm.td_expand_class_name) || td_link.hasClass(vm.td_collapse_class_name))){
                    // This row is not configured as expandable row (at the rowCallback)
                    return
                }
                let tr = td_link.closest('tr')
                let first_td = tr.children().first()

                // Get full data of this row
                let $row = vm.$refs.parties_datatable.vmDataTable.row(tr)
                let full_data = $row.data()

                if(full_data.expanded){
                    // Collapse
                    let siblings = tr.siblings('tr.' + vm.expandable_row_class_name)
                    siblings.fadeOut(500, function(){
                        siblings.remove()
                    })

                    if (full_data.custom_row_app){
                        // Component mounted once cannot be remount easily.  Therefore unmount and delete it completely here and then when required, create it again.
                        full_data.custom_row_app.unmount()
                        full_data.custom_row_app = undefined
                    }

                    // Change icon
                    first_td.removeClass(vm.td_collapse_class_name).addClass(vm.td_expand_class_name)
                    // Hide child row, where hidden columns are
                    $row.child.hide()
                    // Toggle flag
                    full_data.expanded = false
                } else {
                    // Expand
                    let details_elem = $('<tr class="' + vm.expandable_row_class_name +'"><td id="custom_row_' + full_data.id + '"></td></tr>')
                    details_elem.hide()
                    details_elem.insertAfter(tr)
                    vm.updateCustomRowColSpan()

                    // -----------------------
                    // Add vue component dynamically
                    // -----------------------
                    // Configure event listener (Ref: https://stackoverflow.com/questions/67516974/vue3-listen-to-event-from-dynamically-created-child-component-on-replacement)
                    const comp = h(CustomRow, {
                        onAho: e => console.log('onAho: ', e),  // 'aho' is the event name configured in CustomRow component.
                    })
                    let custom_row_app = createApp(comp, {
                        // props
                        party_full_data: full_data
                    })
                    custom_row_app.mount('#custom_row_' + full_data.id)

                    // Store custom_row_app to unmount when hide
                    full_data.custom_row_app = custom_row_app
                    // -----------------------

                    details_elem.fadeIn(1000)

                    // Change icon
                    first_td.removeClass(vm.td_expand_class_name).addClass(vm.td_collapse_class_name)
                    // Show child row, where hidden columns are
                    $row.child.show()
                    // Toggle flag
                    full_data.expanded = true
                }
            })
        },
        addResponsiveResizeHandler: function(){
            // When columns are shown/hidden, expand/collapse the child row according to the current expand-collapse status of each row
            let vm = this
            vm.$refs.parties_datatable.vmDataTable.on('responsive-resize', function(e, datatable, columns) {
                // This event can be used to inform external libraries and controls that Responsive has changed the visibility of columns in the table in response to a resize or recalculation event.
                vm.updateCustomRowColSpan()
                datatable.rows().every(function(rowIdx, tableLoop, rowLoop){
                    // Work on each row
                    let full_data = this.data()
                    if (full_data.expanded){
                        this.child.show()
                    } else {
                        this.child.hide()
                    }
                })
            })
        },
        addEventListeners: function (){
            this.addClickEventHandler()
            this.addResponsiveResizeHandler()
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