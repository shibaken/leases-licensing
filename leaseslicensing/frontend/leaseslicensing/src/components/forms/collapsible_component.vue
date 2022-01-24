<template lang="html">
    <div>
        <div class="toggle_filters_wrapper">
            <div data-toggle="collapse" :data-target="'#' + target_elem_id" :id="button_elem_id" class="toggle_filters_button collapsed" @click="toggle_filters_button_clicked">
                <div class="toggle_filters_icon">
                    <i :id="chevron_elem_id" class="rotate_icon fa fa-chevron-down"></i>
                </div>
                <i :id="warning_icon_id" :title="warning_icon_title" class="fa fa-exclamation-circle fa-2x filter_warning_icon"></i>
            </div>

            <div class="collapse" :id="target_elem_id">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
import uuid from 'uuid';

export default {
    name:"CollapsibleComponent",
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
            warning_icon_id: 'warning_elem_' + uuid(),
            warning_icon_title: '',
            display_icon: false,
            filters_expanded: false,
        }
    },
    methods: {
        toggle_filters_button_clicked: function(e){
            // Bootstrap add a 'collapsed' class name to the element
            this.filters_expanded = $('#' + this.button_elem_id).hasClass('collapsed')
        },
        show_warning_icon: function(show){
            let warning_icon = $('#' + this.warning_icon_id)
            if (show){
                warning_icon.css('opacity', 1)
                this.warning_icon_title = 'filter(s) applied'
            } else {
                warning_icon.css('opacity', 0)
                this.warning_icon_title = ''
            }
        },
    },
    mounted: function() {
        this.$nextTick(function(){
            this.$emit('created')
        })
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
    transition: 0.5s;
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
