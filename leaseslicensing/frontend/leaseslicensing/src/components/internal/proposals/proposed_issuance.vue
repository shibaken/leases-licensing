<template lang="html">
    <div id="proposedIssuanceApproval">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <!--template v-if="is_local">
                proposed_issuance.vue
            </template-->
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="approvalForm">
                        <VueAlert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></VueAlert>
                        <div class="col-sm-12" v-if="registrationOfInterest">
                            <div class="form-group">
                                <div class="row modal-input-row">
                                    <div class="col-sm-3">
                                        <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Decision</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Decision</label>
                                    </div>
                                    <div class="form-check col-sm-5">
                                        <input 
                                        type="radio" 
                                        class="form-check-input"
                                        name="approve_lease_licence" 
                                        id="approve_lease_licence" 
                                        value="approve_lease_licence" 
                                        v-model="selectedDecision"
                                        />
                                        <label class="form-check-label" for="approve_lease_licence" style="font-weight:normal">Invite applicant to apply for a lease or licence</label>
                                    </div>
                                    <div class="form-check col-sm-4">
                                        <input 
                                        type="radio" 
                                        class="form-check-input"
                                        name="approve_competitive_process" 
                                        id="approve_competitive_process" 
                                        value="approve_competitive_process" 
                                        v-model="selectedDecision"
                                        />
                                        <label class="form-check-label" for="approve_competitive_process" style="font-weight:normal">Start Competitive process</label>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row modal-input-row">
                                    <div class="col-sm-3">
                                        <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Details</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Details</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <!--textarea name="approval_details" class="form-control" style="width:70%;" v-model="approval.details"></textarea-->
                                        <RichText
                                        :proposalData="approval.details"
                                        ref="approval_details"
                                        id="approval_details"
                                        :can_view_richtext_src=true
                                        :key="proposedApprovalKey"
                                        />

                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row modal-input-row">
                                    <div class="col-sm-3">
                                        <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">BCC email</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed BCC email</label>
                                    </div>
                                    <div class="col-sm-9">
                                            <input type="text" class="form-control" name="approval_cc" style="width:70%;" ref="bcc_email" v-model="approval.cc_email">
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row modal-input-row">
                                    <div class="col-sm-12">
                                        <label v-if="submitter_email && applicant_email" class="control-label pull-left"  for="Name">After approving this proposal, approval will be emailed to {{submitter_email}} and {{applicant_email}}.</label>
                                        <label v-else class="control-label pull-left"  for="Name">After approving this proposal, approval will be emailed to {{submitter_email}}.</label>
                                    </div>
                                    
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-12" v-if="leaseLicence">
                            <div class="form-group">
                                <div class="row modal-input-row">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left" for="approvalType">Approval Type</label>
                                    </div>
                                    <div class="col-sm-9" v-if="processing_status == 'With Approver'">
                                        Approval Type
                                    </div>
                                    <div class="col-sm-9" v-else>
                                        <select 
                                            ref="approvalType"
                                            class="form-control"
                                            v-model="selectedApprovalType"
                                        >
                                            <option value="null"></option>
                                            <option v-for="atype in approvalTypes" :value="atype" :key="atype.name">{{atype.name}}</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row modal-input-row">
                                    <div class="col-sm-3">
                                        <label v-if="processing_status == 'With Approver'" class="control-label pull-left"  for="Name">Details</label>
                                        <label v-else class="control-label pull-left"  for="Name">Proposed Details</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <!--textarea name="approval_details" class="form-control" style="width:70%;" v-model="approval.details"></textarea-->
                                        <RichText
                                        :proposalData="approval.details"
                                        ref="approval_details"
                                        id="approval_details"
                                        :can_view_richtext_src=true
                                        :key="selectedApprovalTypeName"
                                        :placeholder_text="selectedApprovalTypeDetailsPlaceholder"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <p v-if="can_preview">Click <a href="#" @click.prevent="preview">here</a> to preview the approval letter.</p>

            <div slot="footer">
                <!--button type="button" v-if="issuingApproval" disabled class="btn btn-light" @click="ok"><i class="fa fa-spinner fa-spin"></i> Processing</button>
                <button type="button" v-else class="btn btn-light" @click="ok">Ok</button>
                <button type="button" class="btn btn-light" @click="cancel">Cancel</button-->
            </div>
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
import modal from '@vue-utils/bootstrap-modal.vue'
import VueAlert from '@vue-utils/alert.vue'
import RichText from '@/components/forms/richtext.vue'
import {helpers, api_endpoints} from "@/utils/hooks.js"
export default {
    name:'Proposed-Approval',
    components:{
        modal,
        VueAlert,
        RichText,
    },
    props:{
        proposal_id: {
            type: Number,
            required: true
        },
        processing_status: {
            type: String,
            required: true
        },
        proposal_type: {
            type: String,
            required: true
        },
        isApprovalLevelDocument: {
            type: Boolean,
            required: true
        },
        submitter_email: {
            type: String,
            required: true
        },
        applicant_email: {
            type: String,
            //default: ''
        },
        proposedApprovalKey: {
            type: String,
            //default: ''
        },
        proposal: {
            type: Object,
            required: true,
        },
    },
    data:function () {
        return {
            selectedDecision: null,
            isModalOpen:false,
            form:null,
            approval: {},
            approvalTypes: [],
            selectedApprovalType: {},
            state: 'proposed_approval',
            issuingApproval: false,
            validation_form: null,
            errors: false,
            toDateError:false,
            startDateError:false,
            errorString: '',
            toDateErrorString:'',
            startDateErrorString:'',
            successString: '',
            success:false,
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },
            warningString: 'Please attach Level of Approval document before issuing Approval',
            uuid: 0,
            //is_local: helpers.is_local(),
        }
    },
    computed: {
        selectedApprovalTypeName: function() {
            if (this.selectedApprovalType) {
                return this.selectedApprovalType.name
            }
        },
        selectedApprovalTypeDetailsPlaceholder: function() {
            if (this.selectedApprovalType) {
                return this.selectedApprovalType.details_placeholder
            }
        },
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        showtoDateError: function() {
            var vm = this;
            return vm.toDateError;
        },
        showstartDateError: function() {
            var vm = this;
            return vm.startDateError;
        },
        title: function(){
            return this.processing_status == 'With Approver' ? 'Issue Approval' : 'Propose to approve';
        },
        is_amendment: function(){
            return this.proposal_type == 'Amendment' ? true : false;
        },
        csrf_token: function() {
          return helpers.getCookie('csrftoken')
        },
        can_preview: function(){
            return this.processing_status == 'With Approver' ? true : false;
        },
        preview_licence_url: function() {
          return (this.proposal_id) ? `/preview/licence-pdf/${this.proposal_id}` : '';
        },
        registrationOfInterest: function(){
            if (this.proposal && this.proposal.application_type.name === 'registration_of_interest') {
                return true;
            }
        },
        leaseLicence: function(){
            if (this.proposal && this.proposal.application_type.name === 'lease_licence') {
                return true;
            }
        },
    },
    methods:{
        preview:function () {
            let vm =this;
            let formData = new FormData(vm.form)
            // convert formData to json
            let jsonObject = {};
            for (const [key, value] of formData.entries()) {
                jsonObject[key] = value;
            }
            vm.post_and_redirect(vm.preview_licence_url, {'csrfmiddlewaretoken' : vm.csrf_token, 'formData': JSON.stringify(jsonObject)});
        },
        post_and_redirect: function(url, postData) {
            /* http.post and ajax do not allow redirect from Django View (post method),
               this function allows redirect by mimicking a form submit.
               usage:  vm.post_and_redirect(vm.application_fee_url, {'csrfmiddlewaretoken' : vm.csrf_token});
            */
            var postFormStr = "<form method='POST' target='_blank' name='Preview Licence' action='" + url + "'>";
            for (var key in postData) {
                if (postData.hasOwnProperty(key)) {
                    postFormStr += "<input type='hidden' name='" + key + "' value='" + postData[key] + "'>";
                }
            }
            postFormStr += "</form>";
            var formElement = $(postFormStr);
            $('body').append(formElement);
            $(formElement).submit();
        },
        ok: async function() {
            await this.sendData();
            await this.$router.push({ path: '/internal' });
            /*
            let vm =this;
            if($(vm.form).valid()){
                vm.sendData();
                //vm.$router.push({ path: '/internal' });
            }
            */
        },
        cancel:function () {
            this.close()
        },
        close:function () {
            this.isModalOpen = false;
            this.approval = {};
            this.errors = false;
            /*
            this.toDateError = false;
            this.startDateError = false;
            $('.has-error').removeClass('has-error');
            $(this.$refs.due_date).data('DateTimePicker').clear();
            $(this.$refs.start_date).data('DateTimePicker').clear();
            this.validation_form.resetForm();
            */
        },
        fetchContact: async function(id){
            const response = await fetch(api_endpoints.contact(id));
            this.contact = await response.json(); 
            this.isModalOpen = true;
        },
        fetchApprovalTypes: async function(){
            this.approvalTypes = []
            const response = await fetch(api_endpoints.approval_types_dict);
            const returnedApprovalTypes = await response.json()
            for (let approvalType of returnedApprovalTypes) {
                this.approvalTypes.push(approvalType)
            }
        },

        sendData: async function(){
            this.errors = false;
            //let approval = JSON.parse(JSON.stringify(vm.approval));
            this.approval.details = this.$refs.approval_details.detailsText;
            this.approval.decision = this.selectedDecision;
            this.issuingApproval = true;
            this.$nextTick(async () => {
                if (this.state == 'proposed_approval'){
                    try {
                        await fetch(helpers.add_endpoint_json(api_endpoints.proposals,this.proposal_id+'/proposed_approval'),{ 
                            body: JSON.stringify(this.approval),
                            method: 'POST',
                        })
                        this.issuingApproval = false;
                        this.close();
                        //this.$emit('refreshFromResponse',response);
                        this.$router.push({ path: '/internal' }); //Navigate to dashboard page after Propose issue.
                    } catch (error) {
                        this.errors = true;
                        this.issuingApproval = false;
                        this.errorString = helpers.apiVueResourceError(error);
                    }
                } else if (this.state == 'final_approval'){
                    try {
                        await fetch(helpers.add_endpoint_json(api_endpoints.proposals,this.proposal_id+'/final_approval'),{ 
                        body: JSON.stringify(this.approval),
                        method: 'POST',
                            //emulateJSON:true,
                        })
                        this.issuingApproval = false;
                        this.close();
                        //this.$emit('refreshFromResponse',response);
                        this.$router.push({ path: '/internal' }); //Navigate to dashboard page after Propose issue.
                    } catch (error) {
                        this.errors = true;
                        this.issuingApproval = false;
                        this.errorString = helpers.apiVueResourceError(error);
                    }
                }
            });
        },
   },
   created:function () {
        let vm =this;
        vm.form = document.forms.approvalForm;
        this.approval = Object.assign({}, this.proposal.proposed_issuance_approval);
        this.fetchApprovalTypes()
        //vm.addFormValidations();
        this.$nextTick(()=>{
            if (this.approval.decision) {
                this.selectedDecision = this.approval.decision;
            }
        });
   }
}
</script>

<style lang="css">
.modal-input-row {
    margin-bottom: 20px;
}
.btn-light:hover {
    background-color: lightgrey;
}
</style>
