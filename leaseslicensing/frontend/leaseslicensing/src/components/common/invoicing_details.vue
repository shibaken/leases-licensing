<template>
    <div class="row mb-2">
        <div class="col-sm-3">
            <label for="" class="control-label">Rent or licence charge method</label>
        </div>
        <div class="col-sm-9">
            <div v-for="charge_method in charge_methods" class="form-check" :id="charge_method.id">
                <input 
                    type="radio" 
                    class="form-check-input"
                    name="charge_method"
                    :id="charge_method.key" 
                    :value="charge_method.key" 
                    v-model="invoicing_details.charge_method"
                />
                <label :for="charge_method.key" class="form-check-label">{{ charge_method.display_name }}</label>
            </div>
        </div>
    </div>
    <div v-show="show_once_off_charge_amount" class="row mb-2">
        <div class="col-sm-3">
            <label for="once_off_charge_amount" class="control-label">Once-off charge [AU$]</label>
        </div>
        <div class="col-sm-2">
            <input type="number" min="0" step="100" id="once_off_charge_amount" class="form-control" v-model="invoicing_details.once_off_charge_amount">
        </div>
    </div>
    <div v-show="show_fixed_annual_increment || show_fixed_annual_percentage" class="row mb-2">
        <div class="col-sm-3">
            <label for="base_fee_amount" class="control-label">Base fee [AU$]</label>
        </div>
        <div class="col-sm-2">
            <input type="number" min="0" step="100" id="base_fee_amount" class="form-control" v-model="invoicing_details.base_fee_amount">
        </div>
    </div>
    <div v-show="show_fixed_annual_increment">
        <AnnualIncrement
            increment_type="amount"
            :years_array="years_array_increment"
        />
    </div>
    <div v-show="show_fixed_annual_percentage">
        <AnnualIncrement
            increment_type="percentage"
            :years_array="years_array_percentage"
        />
    </div>
    <div v-show="show_review_of_base_fee" class="row mb-2">
        <div class="col-sm-3">
            <label class="control-label">Review of base fee</label>
        </div>
        <div class="col-sm-2">
            <label for="review_once_every" class="control-label">Once every</label>
        </div>
        <div class="col-sm-2">
            <input type="number" min="0" max="5" step="1" id="review_once_every" class="form-control" v-model="invoicing_details.review_once_every">
        </div>
        <div class="col-sm-2">
            <div v-for="repetition_type in repetition_types" class="form-check" :id="repetition_type.id">
                <input 
                    type="radio" 
                    name="repetition_type_review"
                    class="form-check-input"
                    :id="'review_' + repetition_type.key" 
                    :value="repetition_type.key" 
                    v-model="invoicing_details.review_repetition_type"
                />
                <label :for="'review_' + repetition_type.key" class="form-check-label">{{ repetition_type.display_name }}</label>
            </div>
        </div>
    </div>
    <div v-show="show_crown_land_rent_review_date">
        <CrownLandRentReviewDate />
    </div>
    <div v-show="show_invoicing_frequency" class="row mb-2">
        <div class="col-sm-3">
            <label for="invoicing_frequency" class="control-label">Invoicing Frequency</label>
        </div>
        <div class="col-sm-2">
            <label for="invoicing_once_every" class="control-label">Once every</label>
        </div>
        <div class="col-sm-2">
            <input type="number" min="0" max="5" step="1" id="invoicing_once_every" class="form-control" v-model="invoicing_details.invoicing_once_every">
        </div>
        <div class="col-sm-2">
            <div v-for="repetition_type in repetition_types" class="form-check" :id="repetition_type.id">
                <input 
                    type="radio" 
                    name="repetition_type_invoicing"
                    class="form-check-input"
                    :id="'invoicing_' + repetition_type.key" 
                    :value="repetition_type.key" 
                    v-model="invoicing_details.invoicing_repetition_type"
                />
                <label :for="'invoicing_' + repetition_type.key" class="form-check-label">{{ repetition_type.display_name }}</label>
            </div>
        </div>
    </div>
</template>

<script>
import { none } from 'ol/centerconstraint';
import { v4 as uuid } from 'uuid'
import AnnualIncrement from '@/components/common/component_fixed_annual_amount.vue'
import CrownLandRentReviewDate from '@/components/common/component_crown_land_rent_review_date.vue'

export default {
    name: 'InvoicingDetails',
    data: function() {
        let vm = this;
        return {
            charge_methods: [],
            repetition_types: [],
            invoicing_details: {},

            years_array_increment: [],
            years_array_percentage: [],
        }
    },
    components: {
        AnnualIncrement,
        CrownLandRentReviewDate,
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