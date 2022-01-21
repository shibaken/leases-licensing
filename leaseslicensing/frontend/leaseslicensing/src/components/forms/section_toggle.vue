<template lang="html">
    <div class="panel panel-default" >
        <div v-if="!hideHeader" class="panel-heading">
            <h3 class="panel-title">{{label}} <span class="subtitle">{{ subtitle }}</span>
                <a :href="'#'+section_id" class="panelClicker" :id="custom_id" data-toggle="collapse" expanded="true" :aria-controls="section_id">
                    <span v-if="!noChevron" :class="panel_chevron_class"></span>
                </a>
            </h3>
        </div>
        <div :class="panel_collapse_class" :id="section_id">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import uuid from 'uuid';

export default {
    name:"FormSection",
    props: {
        label: {}, 
        subtitle: {
            type: String,
            default: '',
        },
        Index: {}, 
        hideHeader: {},
        noChevron: {
            default: false,
        },
    },
    data:function () {
        return {
            title:"Section title",
            panel_chevron_class: null,
            custom_id: uuid(),
            chev_down_class_names: 'glyphicon glyphicon-chevron-down pull-right rotate_icon',
            chev_up_class_names:   'glyphicon glyphicon-chevron-down pull-right rotate_icon chev_rotated',
        }
    },
    computed:{
        section_id: function () {
            return "section_"+this.Index
        },
        panel_collapse_class: function() {
            this.panel_chevron_class = this.chev_up_class_names
            return "panel-body collapse in";
        },
    },
    methods: {
        switchPanelChevronClass: function() {
            if (this.panel_chevron_class == this.chev_down_class_names) {
                this.panel_chevron_class = this.chev_up_class_names
            } else {
                this.panel_chevron_class = this.chev_down_class_names
            }
        },
    },
    mounted: function() {
        let vm = this;
        $('#' + vm.custom_id).on('click',function () {
            vm.switchPanelChevronClass();
        });
    },
}
</script>

<style lang="css">
    h3.panel-title{
        font-weight: bold;
        font-size: 25px;
        padding:20px;
    }
    .flex-container {
        display: flex;
        flex-direction: column;
        min-height: 325px;
    }
    .subtitle {
        font-size: 0.6em;
    }
    .rotate_icon {
        transition: 0.5s;
    }
    .chev_rotated {
        transform: rotate(180deg);
    }
</style>
