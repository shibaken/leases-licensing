<template lang="html">
    <div id="recordSale">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" title="Add Party" okText="Add" large>
            <div class="container-fluid">
                <div class="row modal-input-row">
                    <div class="col-sm-3">
                        <label class="form-label">Add party</label>
                    </div>
                    <div class="col-sm-9">
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="person" v-model="type_to_add">
                            <label class="form-check-label" for="inlineRadio1">Person</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="organisation" v-model="type_to_add">
                            <label class="form-check-label" for="inlineRadio2">Organisation</label>
                        </div>
                    </div>
                </div>
                <div class="row modal-input-row">
                    <div v-show="type_to_add=='person'">
                        <div class="col-sm-3">
                            <label class="form-label">Person</label>
                        </div>
                        <div class="col-sm-9">
                            <select 
                                class="form-select" 
                                aria-label="Select person to add"
                                :disabled="false"
                                ref="email_users"
                            >
                                <option value="null"></option>
                                <option v-for="user in email_users" :value="user.email" :key="user.id">{{user.name}}</option>
                            </select>
                        </div>
                    </div>
                    <div v-show="type_to_add=='organisation'">
                        <div class="col-sm-3">
                            <label class="form-label">Organisation</label>
                        </div>
                        <div class="col-sm-9">
                            <select 
                                class="form-select" 
                                aria-label="Select organisation to add"
                                :disabled="false"
                                ref="organisations"
                            >
                                <option value="null"></option>
                                <option v-for="organisation in organisations" :value="organisation.email" :key="organisation.id">{{ organisation.name }}</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <!-- <div slot="footer">
                <button type="button" v-if="saving" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Saving</button>
                <button type="button" v-else class="btn btn-default" @click="ok">OK</button>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
            </div> -->
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
import modal from '@vue-utils/bootstrap-modal.vue'
import {helpers, api_endpoints} from "@/utils/hooks.js"

export default {
    name:'Add Party',
    components:{
        modal,
    },
    props:{
            recordSaleId:{
                type:Number,
                required: true
            },
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            errors: false,
            errorString: '',
            successString: '',
            success:false,
            saving: false,
            
            type_to_add: '',
            // Person
            email_users: [],
            selected_email_user: '',

            // Organisation
            organisations: [],
            selected_organisation: '',
        }
    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
    },
    /*
    watch: {
        due_date: function(){
            this.validDate = moment(this.requirement.due_date,'DD/MM/YYYY').isValid();
        },
    },
    */
    methods:{
        initialiseSelectPerson: function(){
            let vm = this;
            $(vm.$refs.email_users).select2({
                minimumInputLength: 2,
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder:"Select Person",
                ajax: {
                    url: api_endpoints.users_api + '/',
                    dataType: 'json',
                    data: function(params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                        }
                        return query;
                    },
                },
            })
            .on("select2:select", function (e) {
                let data = e.params.data.id;
                vm.selected_email_user = data;
            })
            .on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.selected_email_user = null;
            })
        },
        initialiseSelectOrganisation: function(){
            let vm = this;
            $(vm.$refs.organisations).select2({
                minimumInputLength: 2,
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder:"Select Organisation",
                ajax: {
                    url: api_endpoints.organisations + '/',
                    dataType: 'json',
                    data: function(params) {
                        var query = {
                            term: params.term,
                            type: 'public',
                        }
                        return query;
                    },
                },
            })
            .on("select2:select", function (e) {
                let data = e.params.data.id;
                vm.selected_organisation = data;
            })
            .on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.selected_organisation = null;
            })
        },
        ok:function () {
            this.$nextTick(()=>{
                this.sendData();
            });
        },
        cancel:function () {
            this.close()
        },
        close:function () {
            this.isModalOpen = false;
            this.errors = false;
            $('.has-error').removeClass('has-error');
            this.$emit('closeModal');
        },
        sendData: async function(){
            try {
                this.saving = true;
                const url = `${api_endpoints.vesselownership}${this.recordSaleId}/record_sale/`;
                const res = await this.$http.post(url, {
                    // "sale_date": this.saleDate,
                });
                if (res.ok) {
                    await swal(
                        'Saved',
                        'Your sale date has been saved',
                        'success'
                    );
                }
                this.close()
                this.saving = false;
                this.$emit('refreshDatatable');
            } catch(error) {
                this.errors = true;
                this.saving = false;
                this.errorString = helpers.apiVueResourceError(error);
            }
        },
        fetchSaleDate: async function(){
            try {
                const url = `${api_endpoints.vesselownership}${this.recordSaleId}/fetch_sale_date/`;
                const res = await this.$http.get(url);
                if (res.ok && res.body.end_date) {
                    console.log(res.body)
                    // this.saleDate = res.body.end_date;
                }
            } catch(error) {
                this.errors = true;
                this.errorString = helpers.apiVueResourceError(error);
            }
        },
        addEventListeners:function () {

        },
    },
    mounted:function async () {
        let vm = this
        vm.$nextTick(async ()=>{
            vm.initialiseSelectPerson()
            vm.initialiseSelectOrganisation()
            // await this.fetchSaleDate();
            // this.addeventlisteners();
        });
    },
    created: async function() {

    },
}
</script>

<style lang="css">
.modal-input-row {
    margin-bottom: 1em;
}
.select2-container--bootstrap-5 {
    /* this is required for the select2 in a modal */
    z-index: 99999;
}
</style>
