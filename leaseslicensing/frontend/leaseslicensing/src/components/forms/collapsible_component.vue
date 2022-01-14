<template lang="html">
    <div>
        <div class="toggle_filters_wrapper">
            <div data-toggle="collapse" data-target="#target_id" class="toggle_filters_button">
                <div class="toggle_filters_icon">
                    <span v-if="filters_expanded" class="text-right"><i class="fa fa-chevron-up"></i></span>
                    <span v-else class="text-right"><i class="fa fa-chevron-down"></i></span>
                </div>
                <i v-if="show_icon" title="filter(s) applied" class="fa fa-exclamation-circle fa-2x filter-warning-icon"></i>
            </div>

            <!--
            <a data-toggle="collapse" data-target="#target_id">collapse button in collapsible_component</a>
            -->
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
            show_icon: false,
        }
    },
    computed:{
        filters_expanded: function(){
            // TODO
            return true
        }
    },
    methods: {
        toggle_panel: function(param){
            this.show_icon = param
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
