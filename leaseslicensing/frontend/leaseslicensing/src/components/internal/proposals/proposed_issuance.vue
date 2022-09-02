<template lang="html">
    <div id="proposedIssuanceApproval">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="title" large>
            <ProposedIssuanceForm
                v-if="proposal"
                :proposal="proposal"
                ref="proposed_approval_form"
                :processing_status="proposal.processing_status"
                :proposal_id="proposal.id"
                :proposal_type='proposal.proposal_type.code'
                :submitter_email="submitter_email"
                :applicant_email="applicant_email"
                :key="proposedApprovalKey"
                :proposedApprovalKey="proposedApprovalKey"
            />
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
import modal from '@vue-utils/bootstrap-modal.vue'
import VueAlert from '@vue-utils/alert.vue'
import RichText from '@/components/forms/richtext.vue'
import { helpers, api_endpoints } from "@/utils/hooks.js"
import FileField from '@/components/forms/filefield_immediate.vue'
import ProposedIssuanceForm from '@/components/internal/proposals/proposed_issuance_form.vue'
export default {
    name:'Proposed-Approval',
    components:{
        modal,
        VueAlert,
        RichText,
        FileField,
        ProposedIssuanceForm,
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
            approvalSubTypes: [],
            selectedApprovalSubType: {},
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
        submitter_email: function(){
            if (this.proposal.submitter){
                return this.proposal.submitter.email
            } else {
                return this.proposal.applicant_obj.email
            }
        },
        applicant_email:function(){
            return this.proposal && this.proposal.applicant.email ? this.proposal.applicant.email : '';
        },
        selectedApprovalTypeExists: function() {
            if (this.selectedApprovalType && this.selectedApprovalType.id) {
                return true;
            }
        },
        leaseLicenceApprovalDocumentsUrl: function() {
            return helpers.add_endpoint_join(
                api_endpoints.proposal,
                this.proposal.id + '/process_lease_licence_approval_document/'
                )
        },
        proposedApprovalDocumentsUrl: function() {
            return helpers.add_endpoint_join(
                api_endpoints.proposal,
                this.proposal.id + '/process_proposed_approval_document/'
                )
        },
        selectedApprovalDocumentTypes: function() {
            if (this.selectedApprovalType) {
                return this.selectedApprovalType.approval_type_document_types;
            }
        },
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
        withApprover: function(){
            return this.processing_status == 'With Approver' ? true : false;
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
            //await this.$router.push({ path: '/internal' });
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
        fetchApprovalSubTypes: async function(){
            this.approvalSubTypes = []
            const response = await fetch(api_endpoints.approval_sub_types_dict);
            const returnedApprovalSubTypes = await response.json()
            for (let approvalSubType of returnedApprovalSubTypes) {
                this.approvalSubTypes.push(approvalSubType)
            }
        },
        sendData: async function(){
            this.errors = false;
            this.issuingApproval = true;
            //let approval = JSON.parse(JSON.stringify(vm.approval));
            if (this.registrationOfInterest) {
                this.approval.details = this.$refs.registration_of_interest_details.detailsText;
                this.approval.decision = this.selectedDecision;
            } else if (this.leaseLicence) {
                this.approval.details = this.$refs.lease_licence_details.detailsText;
                this.approval.approval_type = this.selectedApprovalType ? this.selectedApprovalType.id : null;
                this.approval.approval_sub_type = this.selectedApprovalSubType ? this.selectedApprovalSubType.id : null;
            }
            this.$nextTick(async () => {
                if (this.state == 'proposed_approval'){
                    const response = await fetch(helpers.add_endpoint_json(api_endpoints.proposals,this.proposal_id+'/proposed_approval'),{ 
                        body: JSON.stringify(this.approval),
                        method: 'POST',
                    })
                    if (response.ok) {
                        this.issuingApproval = false;
                        this.close();
                        this.$router.push({ path: '/internal' }); //Navigate to dashboard page after Propose issue.
                    } else {
                        this.errors = true;
                        this.issuingApproval = false;
                        this.errorString = await helpers.parseFetchError(response)
                    }
                } else if (this.state == 'final_approval'){
                    const response = await fetch(helpers.add_endpoint_json(api_endpoints.proposals,this.proposal_id+'/final_approval'),{ 
                        body: JSON.stringify(this.approval),
                        method: 'POST',
                    })
                    if (response.ok) {
                        this.issuingApproval = false;
                        this.close();
                        this.$router.push({ path: '/internal' }); //Navigate to dashboard page after Propose issue.
                    } else {
                        this.errors = true;
                        this.issuingApproval = false;
                        this.errorString = await helpers.parseFetchError(response)
                    }
                }
            });
        },
   },
   created: async function () {
        let vm =this;
        vm.form = document.forms.approvalForm;
        this.approval = Object.assign({}, this.proposal.proposed_issuance_approval);
        await this.fetchApprovalTypes();
        await this.fetchApprovalSubTypes();
        //vm.addFormValidations();
        this.$nextTick(()=>{
            if (this.approval.decision) {
                this.selectedDecision = this.approval.decision;
            }
            // Approval Type
            if (this.approval.approval_type) {
                for (let atype of this.approvalTypes) {
                    if (atype.id === this.approval.approval_type) {
                        this.selectedApprovalType = atype;
                    }
                }
            }
            // Approval Sub Type
            if (this.approval.approval_sub_type) {
                for (let atype of this.approvalSubTypes) {
                    if (atype.id === this.approval.approval_sub_type) {
                        this.selectedApprovalSubType = atype;
                    }
                }
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
