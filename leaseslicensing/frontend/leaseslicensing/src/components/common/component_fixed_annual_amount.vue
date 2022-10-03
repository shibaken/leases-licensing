<template>
    <template v-for="item in years_array">
        <div class="row mb-2">
            <div class="col-sm-3 text-end">
                <label for="" class="form-label">Increment</label>
            </div>
        </div>
    </template>
</template>

<script>
export default {
    name: 'AnnualAmount',
    props: {
        amount_type: {
            type: String,
            required: true,
        },
        years_array: [],
    },
    data: function() {
        let vm = this;
        return {

        }
    }
}
</script>