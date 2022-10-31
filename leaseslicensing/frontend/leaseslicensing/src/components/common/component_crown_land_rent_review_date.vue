<template>
    <div class="row mb-4">
        <div class="col-sm-3">
            Crown Land Rent Review Date
        </div>
        <div class="col-sm-9">
            <template v-for="item in review_dates" :key="item.key">
                <div class="row mb-2 row_wrapper">
                    <div class="col-sm-3">
                        <input type="date" class="form-control w-auto" placeholder="DD/MM/YYYY" v-model="item.review_date" :disabled="item.readonly"/>
                    </div>
                    <div v-if="deletable(item)" class="col-sm-1">
                        <span class="remove_a_row text-danger" @click="remove_a_row(item, $event)"><i class="bi bi-x-circle-fill"></i></span>
                    </div>
                </div>
            </template>
            <a href="#" @click="addAnotherDateClicked">Add review date</a>
        </div>
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid'

export default {
    name: 'CrownLandRentReviewDate',
    props: {
        review_dates: {
            type: Array,
            required: true,
        },
    },
    data: function() {
        let vm = this;
        return {
            temp_date: null,
        }
    },
    methods: {
        deletable: function(item){
            if (item.id === 0 || !item.readonly)
                // If the date is a newly added one, or not readonly, it is deletable.
                return true
            return false
        },
        addAnotherDateClicked: function(e){
            e.preventDefault()
            this.review_dates.push({
                'id': 0,
                'key': uuid(),
                'review_date': null,
                'readonly': false,
            })
        },
        remove_a_row: function(item, e){
            let vm = this
            let $elem = $(e.target)

            // Fade out a row
            $elem.closest('.row_wrapper').fadeOut(500, function(){
                if (item.id === 0){
                    // When a row is newly added one (not stored in the database yet), just remove it from the array
                    const index = vm.years_array.indexOf(item)
                    if (index > -1){
                        vm.years_array.splice(index, 1)
                    }
                } else {
                    // When a row is the one already stored in the database, flag it to be deleted.
                    item.to_be_deleted = true
                }
            })
        },
    }
}
</script>