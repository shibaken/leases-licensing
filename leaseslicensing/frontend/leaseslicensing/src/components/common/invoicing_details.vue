<template>
    <div class="row mb-2">
        <div class="col-sm-3">
            <label for="" class="control-label">Rent or licence charge method</label>
        </div>
        <div class="col-sm-4">
            <div v-for="charge_method in charge_methods" :id="charge_method.id">
                <input type="radio" :id="charge_method.key" :value="charge_method.key" v-model="invoicing_details.charge_method" />
                <label :for="charge_method.key">{{ charge_method.display_name }}</label>
            </div>
        </div>
    </div>
    <div v-show="show_once_off_charge_amount" class="row mb-2">
        <div class="col-sm-3">
            <label for="once_off_charge_amount" class="control-label">Once-off charge</label>
        </div>
        <div class="col-sm-9">
            <input type="text" id="once_off_charge_amount" class="form-control" v-model="invoicing_details.once_off_charge_amount">
        </div>
    </div>
    <div v-show="show_base_fee_amount" class="row mb-2">
        <div class="col-sm-3">
            <label for="base_fee_amount" class="control-label">Base fee</label>
        </div>
        <div class="col-sm-9">
            <input type="text" id="base_fee_amount" class="form-control" v-model="invoicing_details.base_fee_amount">
        </div>
    </div>
</template>

<script>
import { none } from 'ol/centerconstraint';
import { v4 as uuid } from 'uuid'

export default {
    name: 'InvoicingDetails',
    data: function() {
        let vm = this;
        return {
            charge_methods: [],
            invoicing_details: {},
        }
    },
    components: {

    },
    created: function(){
        this.fetchChargeMethods()
    },
    mounted: function(){

    },
    computed: {
        show_once_off_charge_amount: function(){
            // TODO
            return true
        },
        show_base_fee_amount: function(){
            // TODO
            return true
        }
    },
    methods: {
        fetchChargeMethods: async function(){
            let vm = this
            try {
                const res = await fetch('/api/charge_methods')
                if (!res.ok)
                    throw new Error(res.statusText)  // 400s or 500s error
                let charge_methods = await res.json()
                console.log(charge_methods)
                vm.charge_methods = charge_methods
            } catch(err){
                console.log({err})
            } finally {

            }
        }
    },
}
</script>