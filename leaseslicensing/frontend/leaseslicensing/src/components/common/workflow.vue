<template>
    <div class="">
        <div class="card card-default">
            <div class="card-header">
                Workflow
            </div>
            <div class="card-body card-collapse">
                <div class="row">
                    <div class="col-sm-12">
                        <strong>Status</strong><br/>
                        {{ proposal.processing_status }}
                    </div>
                    <div class="col-sm-12">
                        <div class="separator"></div>
                    </div>
                    <div v-if="!isFinalised" class="col-sm-12">
                        <strong>Currently assigned to</strong><br/>
                        <div class="form-group">
                            <template v-if="proposal.processing_status == 'With Approver'">
                                <select
                                    ref="assigned_officer"
                                    :disabled="!canAction"
                                    class="form-control"
                                    v-model="proposal.assigned_approver"
                                    @change="assignTo()">
                                    <option v-for="member in proposal.allowed_assessors" :value="member.id">{{ member.first_name }} {{ member.last_name }}</option>
                                </select>
                                <a v-if="canAssess && proposal.assigned_approver != proposal.current_assessor.id" @click.prevent="assignRequestUser()" class="actionBtn pull-right">Assign to me</a>
                            </template>
                            <template v-else>
                                <select
                                    ref="assigned_officer"
                                    :disabled="!canAction"
                                    class="form-control"
                                    v-model="proposal.assigned_officer"
                                    @change="assignTo()">
                                    <option v-for="member in proposal.allowed_assessors" :value="member.id">{{ member.first_name }} {{ member.last_name }}</option>
                                </select>
                                <a v-if="canAssess && proposal.assigned_officer != proposal.current_assessor.id" @click.prevent="assignRequestUser()" class="actionBtn pull-right">Assign to me</a>
                            </template>
                        </div>
                    </div>

                    <template v-if="show_toggle_proposal">
                        <div class="col-sm-12">
                            <strong>Proposal</strong><br/>
                            <a class="actionBtn" v-if="!showingProposal" @click.prevent="toggleProposal()">Show Application</a>
                            <a class="actionBtn" v-else @click.prevent="toggleProposal()">Hide Application</a>
                        </div>
                        <div class="col-sm-12">
                            <div class="separator"></div>
                        </div>
                    </template>
                    <template v-if="show_toggle_requirements">
                        <div class="col-sm-12">
                            <strong>Requirements</strong><br/>
                            <a class="actionBtn" v-if="!showingRequirements" @click.prevent="toggleRequirements()">Show Requirements</a>
                            <a class="actionBtn" v-else @click.prevent="toggleRequirements()">Hide Requirements</a>
                        </div>
                        <div class="col-sm-12">
                            <div class="separator"></div>
                        </div>
                    </template>

                    <div class="col-sm-12">
                        <div class="separator"></div>
                    </div>
                            <template v-if="proposal.processing_status == 'With Assessor' || proposal.processing_status == 'With Referral'">
                                <div class="col-sm-12">
                                    <strong>Referrals</strong><br/>
                                    <div class="form-group">
                                        <select :disabled="!canLimitedAction" ref="department_users" class="form-control">
                                            <option value="null"></option>
                                            <option v-for="user in department_users" :value="user.email">{{user.name}}</option>
                                        </select>
                                        <template v-if='!sendingReferral'>
                                            <template v-if="selected_referral">
                                                <label class="control-label pull-left"  for="Name">Comments</label>
                                                <textarea class="form-control comments_to_referral" name="name" v-model="referral_text"></textarea>
                                                <a v-if="canLimitedAction" @click.prevent="sendReferral()" class="actionBtn pull-right">Send</a>
                                            </template>
                                        </template>
                                        <template v-else>
                                            <span v-if="canLimitedAction" @click.prevent="sendReferral()" disabled class="actionBtn text-primary pull-right">
                                                Sending Referral&nbsp;
                                                <i class="fa fa-circle-o-notch fa-spin fa-fw"></i>
                                            </span>
                                        </template>
                                    </div>
                                    <table class="table small-table">
                                        <tr>
                                            <th>Referral</th>
                                            <th>Status/Action</th>
                                        </tr>
                                        <tr v-for="r in proposal.latest_referrals">
                                            <td>
                                                <small><strong>{{r.referral}}</strong></small><br/>
                                                <small><strong>{{r.lodged_on | formatDate}}</strong></small>
                                            </td>
                                            <td>
                                                <small><strong>{{r.processing_status}}</strong></small><br/>
                                                <template v-if="r.processing_status == 'Awaiting'">
                                                    <small v-if="canLimitedAction"><a @click.prevent="remindReferral(r)" href="#">Remind</a> / <a @click.prevent="recallReferral(r)"href="#">Recall</a></small>
                                                </template>
                                                <template v-else>
                                                    <small v-if="canLimitedAction"><a @click.prevent="resendReferral(r)" href="#">Resend</a></small>
                                                </template>
                                            </td>
                                        </tr>
                                    </table>
                                    <template>

                                    </template>
                                    <MoreReferrals @refreshFromResponse="refreshFromResponse" :proposal="proposal" :canAction="canLimitedAction" :isFinalised="isFinalised" :referral_url="referralListURL"/>
                                </div>
                                <div class="col-sm-12">
                                    <div class="separator"></div>
                                </div>
                            </template>


                    <div v-if="display_actions">
                        <div class="d-flex justify-content-center">
                            <strong>Action</strong>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_enter_conditions">
                            <button
                                class="btn btn-primary w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="switchStatus('with_assessor_conditions')"
                            >Enter Conditions</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_complete_referral">
                            <button
                                class="btn btn-primary w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="completeReferral()"
                            >Complete Referral</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_request_amendment">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="amendmentRequest()"
                            >Request Amendment</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_propose_decline">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="proposedDecline()"
                            >Propose Decline</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_require_das">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="requireDas()"
                            >Require DAS</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_complete_editing">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="completeEditing()"
                            >Complete Editing</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_back_to_application">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="switchStatus('with_assessor')"
                            >Back To Application</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_propose_approve">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="proposedApproval()"
                            >Propose Approve</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_back_to_assessor">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                :disabled="can_user_edit"
                                @click.prevent="switchStatus('with_assessor')"
                            >Back To Assessor</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_approve">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                @click.prevent="issueProposal()"
                            >Approve</button>
                        </div>

                        <div class="d-flex justify-content-center" v-if="display_action_decline">
                            <button
                                class="btn btn-primary  w-75 my-1"
                                @click.prevent="declineProposal()"
                            >Decline</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { api_endpoints, helpers, constants } from '@/utils/hooks'
import MoreReferrals from '@common-utils/more_referrals.vue'

export default {
    name: 'Workflow',
    data: function() {
        let vm = this;
        
        let PS = constants.PROPOSAL_STATUS
        let conf_buttons = [ // List the statuses for which the button is to be displayed
            {
                'enter_conditions': {
                    'registration_of_interest': [],  // No conditions for registration_of_interest
                    'lease_licence': [PS.WITH_ASSESSOR, PS.WITH_REFERRAL,],
                },
                'complete_referral': {
                    'registration_of_interest': [PS.WITH_REFERRAL,],
                    'lease_licence': [PS.WITH_REFERRAL,],
                },
                'request_amendment': {
                    'registration_of_interest': [PS.WITH_ASSESSOR,],
                    'lease_licence': [PS.WITH_ASSESSOR,],
                },
                'propose_decline': {
                    'registration_of_interest': [PS.WITH_ASSESSOR,],
                    'lease_licence': [PS.WITH_ASSESSOR,],
                },
                'back_to_application': {
                    'registration_of_interest': [],  // No conditions for the registration_of_interest
                    'lease_licence': [PS.WITH_ASSESSOR_CONDITIONS,],
                },
                'propose_approve': {
                    'registration_of_interest': [PS.WITH_ASSESSOR,],
                    'lease_licence': [PS.WITH_ASSESSOR_CONDITIONS,],
                },
                'back_to_assessor': {
                    'registration_of_interest': [PS.WITH_APPROVER,],
                    'lease_licence': [PS.WITH_APPROVER,],
                },
                'approve': {
                    'registration_of_interest': [PS.WITH_APPROVER,],
                    'lease_licence': [PS.WITH_APPROVER,],
                },
                'decline': {
                    'registration_of_interest': [PS.WITH_APPROVER],
                    'lease_licence': [PS.WITH_APPROVER,],
                },
                'require_das': {
                    'registration_of_interest': [],
                    'lease_licence': [PS.WITH_ASSESSOR],
                },
                'complete_editing': {
                    'registration_of_interest': [],
                    'lease_licence': [PS.APPROVED_EDITING_INVOICING,],
                },
            },
        ]

        class Button{
            constructor(id, condition){
                this._id = id
                this._condition = condition
            }

            displayable(application_type, processing_status_id){
                let me = this
                if (vm.debug)
                    return true

                // Absorb type difference
                let displayable_statuses = me._condition[application_type].map(a_status => {
                    if (a_status.hasOwnProperty('ID'))
                        return a_status.ID
                    else if (a_status.hasOwnProperty('id'))
                        return a_status.id
                    else if (a_status.hasOwnProperty('Id'))
                        return a_status.Id
                    else
                        return a_status
                })
                processing_status_id = (function(){
                    if(processing_status_id.hasOwnProperty('ID'))
                        return processing_status_id.ID
                    else if(processing_status_id.hasOwnProperty('id'))
                        return processing_status_id.id
                    else if(processing_status_id.hasOwnProperty('Id'))
                        return processing_status_id.Id
                    else
                        return processing_status_id
                })()

                return displayable_statuses.includes(processing_status_id)
            }
        }

        return {
            showingProposal: false,
            showingRequirements: false,

            "loading": [],

            department_users : [],
            selected_referral: [],
            referral_text: '',
            sendingReferral: false,
            buttons: (function(){
                let button_array = {} 
                conf_buttons.forEach(dict => {
                    for (let [key, value] of Object.entries(dict)) {
                        button_array[key] = new Button(key, value)
                    }
                })
                return button_array
            })()
        }
    },
    props: {
        proposal: {
            type: Object,
            default: null,
        },
        isFinalised: {
            type: Boolean,
            default: false,
        },
        canAction: {
            type: Boolean,
            default: false,
        },
        canAssess: {
            type: Boolean,
            default: false,
        },
        can_user_edit: {
            type: Boolean,
            default: false,
        },
        //proposed_decline_status: {
        //    type: Boolean,
        //    default: false,
        //},
    },
    components: {
        MoreReferrals,
    },
    computed: {
        proposal_form_url: function() {
            return (this.proposal) ? `/api/proposal/${this.proposal.id}/assessor_save.json` : '';
        },
        referralListURL: function(){
            return this.proposal!= null ? helpers.add_endpoint_json(api_endpoints.referrals,'datatable_list')+'?proposal='+this.proposal.id : '';
        },
        canLimitedAction:function(){
            // TOOD: refer to proposal_apiary.vue
            return true
        },
        show_toggle_proposal: function(){
            if(this.proposal.processing_status == constants.WITH_ASSESSOR_CONDITIONS || this.proposal.processing_status == constants.WITH_APPROVER || this.isFinalised){
                return true
            } else {
                return false
            }
        },
        show_toggle_requirements: function(){
            if(this.proposal.processing_status == constants.WITH_APPROVER || this.isFinalised){
                return true
            } else {
                return false
            }
        },
        debug: function(){
            return (this.$route.query.debug && this.$route.query.debug == 'true') ? true : false
        },
        display_referrals: function(){
            return true
        },
        display_actions: function(){
            if (this.debug) return true

            return !this.isFinalised && this.canAction
        },
        display_action_complete_referral: function(){
            return this.buttons['complete_referral'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_request_amendment: function(){
            return this.buttons['request_amendment'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_enter_conditions: function(){
            return this.buttons['enter_conditions'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_propose_decline: function(){
            return this.buttons['propose_decline'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_back_to_application: function(){
            return this.buttons['back_to_application'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_propose_approve: function(){
            return this.buttons['propose_approve'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_require_das: function(){
            return this.buttons['require_das'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_complete_editing: function(){
            return this.buttons['complete_editing'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_back_to_assessor: function(){
            return this.buttons['back_to_assessor'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_approve: function(){
            return this.buttons['approve'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
        display_action_decline: function(){
            return this.buttons['decline'].displayable(this.proposal.application_type.name, this.proposal.processing_status_id)
        },
    },
    filters: {
        formatDate: function(data){
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss'): '';
        }
    },
    methods: {
        completeEditing: function(){
        },
        requireDas: function(){
        },
        checkAssessorData: function(){
            //check assessor boxes and clear value of hidden assessor boxes so it won't get printed on approval pdf.

            //select all fields including hidden fields
            var all_fields = $('input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required')

            all_fields.each(function() {
                var ele=null;
                //check the fields which has assessor boxes.
                ele = $("[name="+this.name+"-Assessor]");
                if(ele.length>0){
                    var visiblity=$("[name="+this.name+"-Assessor]").is(':visible')
                    if(!visiblity){
                        if(ele[0].value!=''){
                            ele[0].value=''
                        }
                    }
                }
            });
        },
        initialiseSelects: function(){
            let vm = this;
            $(vm.$refs.department_users).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder:"Select Referral"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.selected_referral = selected.val();
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.selected_referral = ''
            });
            vm.initialiseAssignedOfficerSelect();
        },
        initialiseAssignedOfficerSelect:function(reinit=false){
            let vm = this;
            if (reinit){
                $(vm.$refs.assigned_officer).data('select2') ? $(vm.$refs.assigned_officer).select2('destroy'): '';
            }
            // Assigned officer select
            $(vm.$refs.assigned_officer).select2({
                "theme": "bootstrap-5",
                allowClear: true,
                placeholder:"Select Officer"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                if (vm.proposal.processing_status == 'With Approver'){
                    vm.proposal.assigned_approver = selected.val();
                }
                else{
                    vm.proposal.assigned_officer = selected.val();
                }
                vm.assignTo();
            }).on("select2:unselecting", function(e) {
                var self = $(this);
                setTimeout(() => {
                    self.select2('close');
                }, 0);
            }).on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                if (vm.proposal.processing_status == 'With Approver'){
                    vm.proposal.assigned_approver = null;
                }
                else{
                    vm.proposal.assigned_officer = null;
                }
                vm.assignTo();
            });
        },
        updateAssignedOfficerSelect:function(){
            let vm = this;
            if (vm.proposal.processing_status == 'With Approver'){
                $(vm.$refs.assigned_officer).val(vm.proposal.assigned_approver);
                $(vm.$refs.assigned_officer).trigger('change');
            }
            else{
                $(vm.$refs.assigned_officer).val(vm.proposal.assigned_officer);
                $(vm.$refs.assigned_officer).trigger('change');
            }
        },
        refreshFromResponse:function(response){
            let vm = this;
            vm.original_proposal = helpers.copyObject(response.body);
            vm.proposal = helpers.copyObject(response.body);
            vm.proposal.applicant.address = vm.proposal.applicant.address != null ? vm.proposal.applicant.address : {};
            vm.$nextTick(() => {
                vm.initialiseAssignedOfficerSelect(true);
                vm.updateAssignedOfficerSelect();
            });
        },
        fetchDeparmentUsers: function(){
            let vm = this;
            vm.loading.push('Loading Department Users');
            vm.$http.get(api_endpoints.department_users).then((response) => {
                vm.department_users = response.body
                vm.loading.splice('Loading Department Users',1);
            },(error) => {
                console.log(error);
                vm.loading.splice('Loading Department Users',1);
            })
        },
        sendReferral: function(){
            let vm = this;
            vm.checkAssessorData();
            let formData = new FormData(vm.form);
            vm.sendingReferral = true;
            //vm.$http.post(vm.proposal_form_url, formData).then(
            vm.$http.post(vm.proposal_form_url, {'proposal': this.proposal}).then(
                res => {
                    let data = {'email':vm.selected_referral, 'text': vm.referral_text}
                    vm.sendingReferral = true;

                    vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposals, (vm.proposal.id + '/assesor_send_referral')), JSON.stringify(data), { emulateJSON:true }).then(
                        response => {

                            vm.sendingReferral = false;
                            vm.original_proposal = helpers.copyObject(response.body);
                            vm.proposal = response.body;
                            vm.proposal.applicant.address = vm.proposal.applicant.address != null ? vm.proposal.applicant.address : {};
                            swal(
                                'Referral Sent',
                                'The referral has been sent to ' + vm.department_users.find(d => d.email == vm.selected_referral).name,
                                'success'
                            )
                            $(vm.$refs.department_users).val(null).trigger("change");
                            vm.selected_referral = '';
                            vm.referral_text = '';
                        }, 
                        error => {
                            console.error(error);
                            swal(
                                'Referral Error',
                                helpers.apiVueResourceError(error),
                                'error'
                            )
                            vm.sendingReferral = false;
                        }
                    )  // END 2nd vm.$http.post
                },
                err=>{

                }
            )  // END 1st vm.$http.post
        },
        remindReferral:function(r){
            let vm = this;

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.referrals,r.id+'/remind')).then(response => {
                vm.original_proposal = helpers.copyObject(response.body);
                vm.proposal = response.body;
                vm.proposal.applicant.address = vm.proposal.applicant.address != null ? vm.proposal.applicant.address : {};
                swal(
                    'Referral Reminder',
                    'A reminder has been sent to '+r.referral,
                    'success'
                )
            },
            error => {
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        resendReferral:function(r){
            let vm = this;

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.referrals,r.id+'/resend')).then(response => {
                vm.original_proposal = helpers.copyObject(response.body);
                vm.proposal = response.body;
                vm.proposal.applicant.address = vm.proposal.applicant.address != null ? vm.proposal.applicant.address : {};
                swal(
                    'Referral Resent',
                    'The referral has been resent to '+r.referral,
                    'success'
                )
            },
            error => {
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        recallReferral:function(r){
            let vm = this;
            swal({
                    title: "Loading...",
                    //text: "Loading...",
                    allowOutsideClick: false,
                    allowEscapeKey:false,
                    onOpen: () =>{
                        swal.showLoading()
                    }
            })

            vm.$http.get(helpers.add_endpoint_json(api_endpoints.referrals,r.id+'/recall')).then(response => {
                swal.hideLoading();
                swal.close();
                vm.original_proposal = helpers.copyObject(response.body);
                vm.proposal = response.body;
                vm.proposal.applicant.address = vm.proposal.applicant.address != null ? vm.proposal.applicant.address : {};
                swal(
                    'Referral Recall',
                    'The referall has been recalled from '+r.referral,
                    'success'
                )
            },
            error => {
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        assignRequestUser: function(){
            this.$emit('assignRequestUser')
        },
        assignTo: function(){
            this.$emit('assignTo')
        },
        toggleProposal:function(){
            this.showingProposal = !this.showingProposal;
            this.$emit('toggleProposal', this.showingProposal)
        },
        toggleRequirements:function(){
            this.showingRequirements = !this.showingRequirements;
            this.$emit('toggleRequirements', this.showingRequirements)
        },
        switchStatus: function(value){
            this.$emit('switchStatus', value)
        },
        amendmentRequest: function(){
            this.$emit('amendmentRequest')
        },
        completeReferral: function(){
            this.$emit('completeReferral')
        },
        proposedDecline: function(){
            this.$emit('proposedDecline')
        },
        proposedApproval: function(){
            this.$emit('proposedApproval')
        },
        issueProposal: function(){
            this.$emit('issueProposal')
        },
        declineProposal: function(){
            this.$emit('declineProposal')
        },
    },
    created: function(){
        this.fetchDeparmentUsers()
    },
    mounted: function(){
        let vm = this
        this.$nextTick(() => {
            vm.initialiseSelects();
        })
    },
}
</script>

<style scoped>
.actionBtn {
    cursor: pointer;
}
.separator {
    border: 1px solid;
    margin-top: 15px;
    margin-bottom: 10px;
    width: 100%;
}
.referral_comment_textarea {
    resize: vertical;
}
.comments_to_referral {
    resize: vertical;
}
</style>
