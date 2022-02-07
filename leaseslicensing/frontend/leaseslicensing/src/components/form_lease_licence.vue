<template lang="html">
    <div>
    <div v-if="debug">components/form_lease_licence.vue</div>
    <FormSection label="Proposal Details" Index="application_details" v-if="proposal">
        <slot name="slot_proposal_details_checklist_questions"></slot>
        <div class="col-sm-12 inline-details-text">
            <div class="col-sm-3">
                <label for="details_text" class="control-label pull-left">Provide a description of your proposal</label>
            </div>
            <div class="col-sm-8">
                <RichText
                id="details_text"
                :proposalData="proposal.details_text"
                ref="details_text"
                label="Rich text in here" 
                :readonly="readonly" 
                :can_view_richtext_src=true
                v-bind:key="proposal.id"
                />
            </div>
            <div class="col-sm-3">
                <label for="supporting_documents">Attach any supporting documents</label>
            </div>
            <div class="col-sm-9">
                <FileField 
                    :readonly="readonly"
                    ref="supporting_documents"
                    name="supporting_documents"
                    id="supporting_documents"
                    :isRepeatable="true"
                    :documentActionUrl="supportingDocumentsUrl"
                    :replace_button_by_text="true"
                />
            </div>
        </div>

        <div class="col-sm-12">
            <div class="col-sm-3 question-title">
                <label class="control-label pull-left">Is the proposal consistent with the purpose of the park or reserve?</label>
            </div>
            <div class="col-sm-9">
                <ul  class="list-inline col-sm-6">
                    <li class="list-inline-item">
                        <input class="form-check-input" v-model="proposal.consistent_purpose" type="radio" name="consistent_purpose_yes" id="consistent_purpose_yes" :value="true" data-parsley-required :disabled="readonly"/>
                        <label for="consistent_purpose_yes">Yes</label>
                    </li>
                    <li class="list-inline-item">
                        <input  class="form-check-input" v-model="proposal.consistent_purpose" type="radio" name="consistent_purpose_no" id="consistent_purpose_no" :value="false" data-parsley-required :disabled="readonly"/> 
                        <label for="consistent_purpose_no">No</label>
                    </li>
                    <li class="list-inline-item">
                        <input  class="form-check-input" v-model="proposal.consistent_purpose" type="radio" name="consistent_purpose_null" id="consistent_purpose_null" :value="null" data-parsley-required :disabled="readonly"/> 
                        <label for="consistent_purpose_null">Unsure</label>
                    </li>
                </ul>

            </div>
        </div>
        <div class="col-sm-12 inline-details-text" v-show="proposal.consistent_purpose">
            <div class="col-sm-3 question-title">
                <label for="consistent_purpose_text" class="control-label pull-left">Provide details</label>
            </div>
            <div class="col-sm-8 question-title">
                <RichText
                :proposalData="proposal.consistent_purpose_text"
                ref="consistent_purpose_text"
                id="consistent_purpose_text"
                :readonly="readonly" 
                :can_view_richtext_src=true
                v-bind:key="proposal.id"
                />
            </div>
            <div class="col-sm-3 question-title">
                <label for="consistent_purpose_documents">Attach any supporting documents</label>
            </div>
            <div class="col-sm-9 question-title">
                <FileField 
                    :readonly="readonly"
                    ref="consistent_purpose_documents"
                    name="consistent_purpose_documents"
                    id="consistent_purpose_documents"
                    :isRepeatable="true"
                    :documentActionUrl="consistentPurposeDocumentsUrl"
                    :replace_button_by_text="true"
                />
            </div>
        </div>

    </FormSection>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue'
import RichText from '@/components/forms/richtext.vue'
import FileField from '@/components/forms/filefield_immediate.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'

    export default {
        name: 'LeaseLicenceForm',
        props:{
            proposal:{
                type: Object,
                required:true
            },
            readonly:{
                type: Boolean,
                default: true,
            },
        },
        data:function () {
            return{
            }
        },
        components: {
            FormSection,
            RichText,
            FileField,
        },
        computed:{
            proposalId: function() {
                return this.proposal ? this.proposal.id : null;
            },
            deedPollDocumentUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_deed_poll_document/'
                    )
            },
            supportingDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_supporting_document/'
                    )
            },
            exclusiveUseDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_exclusive_use_document/'
                    )
            },
            longTermUseDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_long_term_use_document/'
                    )
            },
            consistentPurposeDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_consistent_purpose_document/'
                    )
            },
            consistentPlanDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_consistent_plan_document/'
                    )
            },
            clearingVegetationDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_clearing_vegetation_document/'
                    )
            },
            groundDisturbingWorksDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_ground_disturbing_works_document/'
                    )
            },
            heritageSiteDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_heritage_site_document/'
                    )
            },
            environmentallySensitiveDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_environmentally_sensitive_document/'
                    )
            },
            wetlandsImpactDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_wetlands_impact_document/'
                    )
            },
            buildingRequiredDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_building_required_document/'
                    )
            },
            significantChangeDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_significant_change_document/'
                    )
            },
            aboriginalSiteDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_aboriginal_site_document/'
                    )
            },
            nativeTitleConsultationDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_native_title_consultation_document/'
                    )
            },
            miningTenementDocumentsUrl: function() {
                return helpers.add_endpoint_join(
                    api_endpoints.proposal,
                    this.proposal.id + '/process_mining_tenement_document/'
                    )
            },
        },
        methods:{
            debug: function(){
                if (this.$route.query.debug){
                    return this.$route.query.debug === 'true'
                }
                return false
            },
        },
        mounted: function() {
        }
 
    }
</script>

<style lang="css" scoped>
    .inline-details-text{
        margin-bottom: 20px;
    }
    .details-text{
        padding-left: 15px;
    }
    .question-title{
        padding-left: 15px;
    }
    .section-style{
        padding-left: 15px;
        margin-bottom: 20px;
    }
    .list-inline-item{
        padding-right: 15px;
    }
    .section{
        text-transform: capitalize;
    }
    .list-group{
        margin-bottom: 0;
    }
    .fixed-top{
        position: fixed;
        top:56px;
    }

    .nav-item {
        background-color: rgb(200,200,200,0.8) !important;
        margin-bottom: 2px;
    }

    .nav-item>li>a {
        background-color: yellow !important;
        color: #fff;
    }

    .nav-item>li.active>a, .nav-item>li.active>a:hover, .nav-item>li.active>a:focus {
      color: white;
      background-color: blue;
      border: 1px solid #888888;
    }

	.admin > div {
	  display: inline-block;
	  vertical-align: top;
	  margin-right: 1em;
	}
</style>

