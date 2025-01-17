import { RouterView } from 'vue-router'
import ExternalDashboard from '@/components/external/dashboard.vue'
import Proposal from '@/components/external/proposal.vue'
import ProposalApply from '@/components/external/proposal_apply.vue'
import ProposalSubmit from '@/components/external/proposal_submit.vue'
import Organisation from '@/components/external/organisations/manage.vue'
import Compliance from '../compliances/access.vue'
import ComplianceSubmit from '../compliances/submit.vue'
/*
import Compliance from '../compliances/access.vue'
import ComplianceSubmit from '../compliances/submit.vue'
import Approval from '../approvals/approval.vue'
*/
export default
{
    path: '/external',
    component: RouterView,
    name: 'external-dashboard',
    children: [
        {
            path: '/external/',
            component: ExternalDashboard,
            name: 'external-dashboard'
        },
        {
            path: 'organisations/manage/:org_id',
            component: Organisation
        },
        {
            path: 'compliance/:compliance_id',
            component: Compliance
        },
        {
            path: 'compliance/submit/:compliance_id',
            component: ComplianceSubmit,
            name:"submit_compliance",
            //props: (route) => ({ query: route.query.compliance }),
        },
        {
            path: 'proposal/',
            component: ProposalApply,
            name:"apply_proposal"
        },
        {
            path: 'proposal/submit/:proposal_id',
            component: ProposalSubmit,
            name:"submit-proposal",
            //props: (route) => ({ query: route.query.proposal }),
            //props: true,
        },
        {
            path: 'proposal/:proposal_id',
            component: Proposal,
            name:"draft_proposal"
        },
    ]
}
