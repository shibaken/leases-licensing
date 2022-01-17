<template lang="html">
    <div>
        <div class="toggle_filters_wrapper">
            <div data-toggle="collapse" :data-target="'#' + target_elem_id" :id="button_elem_id" class="toggle_filters_button collapsed" @click="toggle_filters_button_clicked">
                <div class="toggle_filters_icon">
                    <!--
                    <span v-if="filters_expanded" class="text-right"><i class="fa fa-chevron-up"></i></span>
                    <span v-else class="text-right"><i class="fa fa-chevron-down"></i></span>
                    -->

                    <i :id="chevron_elem_id" class="rotate_icon fa fa-chevron-down"></i>
                </div>
                <i v-if="display_icon" title="filter(s) applied" class="fa fa-exclamation-circle fa-2x filter_warning_icon"></i>
            </div>

            <div class="collapse" :id="target_elem_id">
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
    watch: {
        filters_expanded: function(){
            let chevron_icon = $('#' + this.chevron_elem_id)
            if (this.filters_expanded){
                chevron_icon.addClass('chev_rotated')
            } else {
                chevron_icon.removeClass('chev_rotated')

            }
        }
    },
    data:function () {
        return {
            target_elem_id: 'target_elem_' + uuid(),
            button_elem_id: 'button_elem_' + uuid(),
            chevron_elem_id: 'chevron_elem_' + uuid(),
            display_icon: false,
            filters_expanded: false,
        }
    },
    computed:{

    },
    methods: {
        toggle_filters_button_clicked: function(e){
            // Bootstrap add a 'collapsed' class name to the element
            this.filters_expanded = $('#' + this.button_elem_id).hasClass('collapsed')
        },
        show_icon: function(show){
            this.display_icon = show
        },
    },
    created: function() {

    },
    mounted: function() {
        this.$nextTick(function(){
            this.$emit('created')
        })
    },
    updated:function () {

    },
}
</script>

<style lang="css">
.toggle_filters_wrapper {
    background: #efefee;
    padding: 0.5em;
    margin: 0 0 0.5em 0;
    display: grid;
}
.toggle_filters_button {
    cursor: pointer;
    display: flex;
    flex-direction: row-reverse;
}
.filter_warning_icon {
    color: #ffc107;
}
.toggle_filters_icon {
    margin: 0 0 0 0.5em;
}
.rotate_icon {
    transition: 0.5s;
}
.chev_rotated {
    transform: rotate(180deg);
}
</style>
