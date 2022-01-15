<template lang="html">
    <div>
        <div class="toggle_filters_wrapper">
            <div data-toggle="collapse" data-target="#target_id" class="toggle_filters_button collapsed" @click="toggle_filters_button_clicked($event)">
                <div class="toggle_filters_icon">
                    <span v-if="filters_expanded" class="text-right"><i class="fa fa-chevron-up"></i></span>
                    <span v-else class="text-right"><i class="fa fa-chevron-down"></i></span>
                </div>
                <i v-if="display_icon" title="filter(s) applied" class="fa fa-exclamation-circle fa-2x filter-warning-icon"></i>
            </div>

            <div class="collapse" id="target_id">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
import uuid from 'uuid';
import '@/components/common/filters.css'

export default {
    name:"CollapsibleComponent",
    props: {

    },
    data:function () {
        return {
            display_icon: false,
            filters_expanded: false,
        }
    },
    computed:{

    },
    methods: {
        toggle_filters_button_clicked: function(e){
            this.filters_expanded = $('.toggle_filters_button').hasClass('collapsed')
        },
        show_icon: function(show){
            this.display_icon = show
        },
    },
    mounted: function() {

    },
    updated:function () {

    },
}
</script>

<style lang="css">

</style>
