<template lang="html">
    <div class="container" >
        <div class="row d-flex justify-content-center">
            <div v-if="isProposal" class="col-sm-6 borderDecoration">
              <div class="form-para">
                  <strong>Confirmation</strong>
              </div>
              <div class="form-para">
                  <strong>Your application for a {{ applicationType }} has been successfully submitted.</strong>
              </div>
                <!-- <strong>Your application for a commercial operations licence has been successfully submitted.</strong>
                <br/> -->
              <div class="form-para">
                <table>
                    <tr>
                        <td><strong>Reference number:</strong></td>
                        <td>{{ proposal.lodgement_number }}</td>
                    </tr>
                    <tr>
                        <td><strong>Date / Time:</strong></td>
                        <!--td> {{proposal.lodgement_date|formatDate}}</td-->
                        <td> {{ proposal.lodgement_date_display }}</td>
                    </tr>
                </table>
              </div>
                <!--label>You will receive a notification email if there is any incomplete information or documents missing from the application.</label-->
                <!--router-link :to="{name:'external-dashboard'}" style="margin-top:15px;" class="btn btn-primary pull-right">Back to Dashboard</router-link-->
                <a href="/external/" class="router-link-active btn btn-primary pull-right" data-v-5da83b51="" style="margin-top: 15px;">Back to Dashboard</a>
            </div>
            <div v-else class="col-sm-offset-3 col-sm-6 borderDecoration">
                <strong>Sorry it looks like there isn't any application currently in your session.</strong>
                <br />
                <a href="/external/" class="router-link-active btn btn-primary pull-right" data-v-5da83b51="" style="margin-top: 15px;">Back to Dashboard</a>
            </div>
        </div>
    </div>
</template>
<script>
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
export default {
  data: function() {
    return {
        "proposal": {},
    }
  },
    /*
  props: {
      proposal: {
          type: Object,
      },
  },
  */

  components: {
  },
  computed: {
    applicationType: function() {
      //return this.proposal && this.proposal.id ? this.proposal.application_type.name_display : '';
      //return this.proposal && this.proposal.id ? this.proposal.application_type.confirmation_text : '';
      return this.proposal.application_type_text;
    },
    isProposal: function(){
      return this.proposal && this.proposal.id ? true : false;
    },
  },
  methods: {
  },
    /*
  filters:{
        formatDate: function(data){
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss'): '';
        }
  },
  */
  mounted: function() {
    //let vm = this;
    //vm.form = document.forms.new_proposal;
  },
  beforeRouteEnter: function(to, from, next) {
    if (to.params.proposal_id) {
      fetch(`/api/proposal/${to.params.proposal_id}.json`).then(res => {
          next(async (vm) => {
              console.log(vm)
              const proposalData = await res.json()
              console.log(proposalData)
              vm.proposal = proposalData;
              });
          },
        err => {
          console.log(err);
        });
    }
  }
}
</script>

<style lang="css" scoped>
.borderDecoration {
    border: 1px solid;
    border-radius: 5px;
    padding: 50px;
    margin-top: 70px;
}
.form-para {
    margin-bottom: 20px;
}
</style>
