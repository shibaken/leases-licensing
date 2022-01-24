<template lang="html">
    <div class="accordion" :id="custom_id">
      <div class="accordion-item">
        <div class="accordion-header" :id="section_header_id">
          <h2 class="mb-0">
            <button id="mybutton" class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target="'#'+section_body_id" :aria-expanded="true" :aria-controls="section_body_id">
                {{ label }}
            </button>
          </h2>
        </div>
        <div :id="section_body_id" class="accordion-collapse collapse show" :aria-labelledby="section_header_id" :data-parent="'#'+custom_id">
          <div class="accordion-body">
              <slot></slot>
          </div>
        </div>
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
        /*
        noChevron: {
            default: false,
        },
        */
    },
    data:function () {
        return {
            custom_id: uuid(),
            /*
            title:"Section title",
            panel_chevron_class: null,
            chev_down_class_names: 'glyphicon glyphicon-chevron-down pull-right rotate_icon',
            chev_up_class_names:   'glyphicon glyphicon-chevron-down pull-right rotate_icon chev_rotated',
            */
        }
    },
    computed:{
        section_header_id: function () {
            return "section_header_"+this.Index;
        },
        section_body_id: function () {
            return "section_body_"+this.Index;
        },
        /*
        panel_collapse_class: function() {
            this.panel_chevron_class = this.chev_up_class_names
            return "panel-body collapse in";
        },
        */
    },
    methods: {
        /*
        switchPanelChevronClass: function() {
            if (this.panel_chevron_class == this.chev_down_class_names) {
                this.panel_chevron_class = this.chev_up_class_names
            } else {
                this.panel_chevron_class = this.chev_down_class_names
            }
        },
        */
    },
    mounted: function() {
        /*
        let vm = this;
        $('#' + vm.custom_id).on('click',function () {
            vm.switchPanelChevronClass();
        });
        $('#mybutton').on('click', function(e) {
            console.log(e);
        });
        */
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
