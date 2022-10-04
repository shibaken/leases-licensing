<template>
    <template v-for="item in years_array">
        <div class="row mb-2">
            <div class="col-sm-3 text-end">
                Increment
            </div>
            <div class="col-sm-1 text-end">year</div>
            <div class="col-sm-2">
                <input 
                    type="number" 
                    :min="min_year" 
                    :max="max_year" 
                    :step="step_year" 
                    class="form-control"
                    v-model="item.year"
                />
            </div>
            <div class="col-sm-2 text-end">{{ value_title }}</div>
            <div class="col-sm-2">
                <input 
                    type="number" 
                    :min="min_increment" 
                    :max="max_increment" 
                    :step="step_increment" 
                    class="form-control"
                    v-model="item.increment_value"
                />
            </div>
        </div>
    </template>
    <div class="text-end">
        <a href="#" @click="addAnotherYearClicked">Add another year</a>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid'

export default {
    name: 'AnnualAmount',
    props: {
        increment_type: {
            type: String,
            required: true,
        },
        years_array: {
            type: Array,
            default: () => {return []},
        },
        min_year: {
            type: Number,
            default: 2021,
        },
        max_year: {
            type: Number,
            default: 2100,
        },
        step_year: {
            type: Number,
            default: 1,
        }
    },
    data: function() {
        let vm = this;
        return {

        }
    },
    created: function() {

    },
    mounted: function() {

    },
    computed: {
        value_title: function(){
            if (this.increment_type === 'amount')
                return 'amount [AU$]'
            else if (this.increment_type === 'percentage')
                return 'percentage [%]'
        },
        step_increment: function(){
            if (this.increment_type === 'amount')
                return 100
            else if (this.increment_type === 'percentage')
                return 0.1
        },
    },
    methods: {
        addAnotherYearClicked: function(e){
            console.log('addAnotherYearClicked')
            e.preventDefault()
            this.years_array.push({
                'id': uuid(),
                'year': null,
                'increment_value': null,
            })
            
        }
    },
}
</script>