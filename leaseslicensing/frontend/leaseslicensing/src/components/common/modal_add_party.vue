<template lang="html">
    <div id="recordSale">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" title="Add Party" large>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-sm-3">
                        Add party
                    </div>
                    <div class="col-sm-9">
                        radio buttons here
                    </div>
                    <div class="col-sm-3">
                        Person
                    </div>
                    <div class="col-sm-9">
                        <input type="text" /> Create New
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
import {helpers,api_endpoints} from "@/utils/hooks.js"

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
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                /*
                keepInvalid:true,
                allowInputToggle:true
                */
            },
            saving: false,
            saleDate: null,
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
            $(this.$refs.sale_date).data('DateTimePicker').clear();
            this.$emit('closeModal');
        },
        sendData: async function(){
            try {
                this.saving = true;
                const url = `${api_endpoints.vesselownership}${this.recordSaleId}/record_sale/`;
                const res = await this.$http.post(url, {
                    "sale_date": this.saleDate,
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
                    this.saleDate = res.body.end_date;
                }
            } catch(error) {
                this.errors = true;
                this.errorString = helpers.apiVueResourceError(error);
            }
        },
        eventListeners:function () {

        },
    },
    mounted:function async () {
        this.$nextTick(async ()=>{
            await this.fetchSaleDate();
            this.eventListeners();
        });
    },
    created: async function() {
    },
}
</script>

<style lang="css">
</style>
