<template lang="html">
    <div>
        <a data-toggle="collapse" data-target="#target_id">collapse button in collapsible_component</a>
        <div class="collapse" id="target_id">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import uuid from 'uuid';

export default {
    name:"CollapsibleComponent",
    props: {

    },
    data:function () {
        return {

        }
    },
    computed:{

    },
    methods: {
        toggle_panel: function(param){
            console.log('this function is in collapsible_component')
            console.log('param passed: ' + param)
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
