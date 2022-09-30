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
            <label for="once_off_charge_amount" class="control-label">Once-off charge (AU$)</label>
        </div>
        <div class="col-sm-2">
            <input type="number" id="once_off_charge_amount" class="form-control" v-model="invoicing_details.once_off_charge_amount">
        </div>
    </div>
    <div v-show="show_fixed_annual_increment || show_fixed_annual_percentage" class="row mb-2">
        <div class="col-sm-3">
            <label for="base_fee_amount" class="control-label">Base fee (AU$)</label>
        </div>
        <div class="col-sm-2">
            <input type="number" id="base_fee_amount" class="form-control" v-model="invoicing_details.base_fee_amount">
        </div>
    </div>
    <div v-show="show_fixed_annual_increment" class="row mb-2">
        TODO: Annual Increment Component
    </div>
    <div v-show="show_fixed_annual_percentage" class="row mb-2">
        TODO: Annual Percentage Component
    </div>
    <div v-show="show_review_of_base_fee" class="row mb-2">
        <div class="col-sm-3">
            <label class="control-label">Review of base fee</label>
        </div>
        <div class="col-sm-2">
            <label for="review_once_every" class="control-label">Once every</label>
        </div>
        <div class="col-sm-2">
            <input type="number" id="review_once_every" class="form-control" v-model="invoicing_details.review_once_every">
        </div>
        <div class="col-sm-2">
            <div v-for="repetition_type in repetition_types" :id="repetition_type.id">
                <input type="radio" :id="repetition_type.key" :value="repetition_type.key" v-model="invoicing_details.review_repetition_type" />
                <label :for="repetition_type.key">{{ repetition_type.display_name }}</label>
            </div>
        </div>
    </div>
    <div v-show="show_crown_land_rent_review_date" class="row mb-2">
        TODO: Cronw Land Component
    </div>
    <div v-show="show_invoicing_frequency" class="row mb-2">
        <div class="col-sm-3">
            <label for="invoicing_frequency" class="control-label">Invoicing Frequency</label>
        </div>
        <div class="col-sm-2">
            <label for="invoicing_once_every" class="control-label">Once every</label>
        </div>
        <div class="col-sm-2">
            <input type="number" id="invoicing_once_every" class="form-control" v-model="invoicing_details.invoicing_once_every">
        </div>
        <div class="col-sm-2">
            <div v-for="repetition_type in repetition_types" :id="repetition_type.id">
                <input type="radio" :id="repetition_type.key" :value="repetition_type.key" v-model="invoicing_details.invoicing_repetition_type" />
                <label :for="repetition_type.key">{{ repetition_type.display_name }}</label>
            </div>
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
            repetition_types: [],
            invoicing_details: {},
        }
    },
    components: {

    },
    created: function(){
        this.fetchChargeMethods()
        this.fetchRepetitionTypes()
    },
    mounted: function(){

    },
    computed: {
        show_once_off_charge_amount: function(){
            // TODO
            return true
        },
        show_fixed_annual_increment: function(){
            // TODO
            return true
        },
        show_fixed_annual_percentage: function(){
            // TODO
            return true
        },
        show_review_of_base_fee: function(){
            // TODO
            return true
        },
        show_crown_land_rent_review_date: function(){
            // TODO
            return true
        },
        show_invoicing_frequency: function(){
            // TODO
            return true
        },
    },
    methods: {
        fetchChargeMethods: async function(){
            let vm = this
            try {
                const res = await fetch('/api/charge_methods')
                if (!res.ok)
                    throw new Error(res.statusText)  // 400s or 500s error
                let charge_methods = await res.json()
                vm.charge_methods = charge_methods
            } catch(err){
                console.log({err})
            } finally {

            }
        },
        fetchRepetitionTypes: async function(){
            let vm = this
            try {
                const res = await fetch('/api/repetition_types')
                if (!res.ok)
                    throw new Error(res.statusText)  // 400s or 500s error
                let repetition_types = await res.json()
                vm.repetition_types= repetition_types
            } catch(err){
                console.log({err})
            } finally {

            }
        }
    },
}
</script>