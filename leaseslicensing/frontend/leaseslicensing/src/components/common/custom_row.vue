<template>
        <div @click="clicked">Test Event</div>
        <table class="party_detail_table">
            <tr>
                <th>Invited to competitive process</th>
                <td>
                    <input type="date" class="form-control" placeholder="DD/MM/YYYY" v-model="party_full_data.invited_at">
                </td>
            </tr>
            <tr>
                <th>Removed from competitive process</th>
                <td>
                    <input type="date" class="form-control" placeholder="DD/MM/YYYY" v-model="party_full_data.removed_at">
                </td>
            </tr>
            <tr>
                <th>Details</th>
                <td>
                    <template v-for="party_detail in party_full_data.party_details" :key="party_detail.id">
                        <div>
                            <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="party_detail.detail">
                        </div>
                    </template>
                    <table class="party_detail_table">
                        <tr>
                            <th>New detail</th>
                            <td>
                                <input type="text" class="form-control">
                            </td>
                        </tr>
                        <tr>
                            <th>Documents</th>
                            <td>
                                <FileField
                                    :readonly="readonly"
                                    ref="temp_document"
                                    name="temp_document"
                                    isRepeatable="true"
                                    :documentActionUrl="detailDocumentUrl"
                                    :replace_button_by_text="true"
                                    :temporaryDocumentCollectionId="temporary_document_collection_id"
                                    @update-temp-doc-coll-id="addToTemporaryDocumentCollectionList"
                                />
                            </td>
                        </tr>
                    </table>
                    <!-- <div class="row modal-input-row">
                        <div class="col-sm-3">
                            <label class="form-label">New detail</label>
                        </div>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" placeholder="">
                        </div>
                    </div> -->
                </td>
            </tr>
        </table>
</template>

<script>
import { api_endpoints, helpers } from '@/utils/hooks'
import FileField from '@/components/forms/filefield_immediate.vue'

export default {
    name: 'CustomRow',
    props: {
        party_full_data: null,
        competitive_process_id: '',
    },
    components: {
        FileField,
    },
    data() {
        let vm = this;
        return {
            temporary_document_collection_id: null,
        }
    },
    created: function(){

    },
    computed: {
        readonly: function(){
            return false
        },
        existingDetail: function() {
            return false
        },
        detailDocumentUrl: function() {
            let url = '';
            if (this.existingDetail) {
                // url = helpers.add_endpoint_join(
                //     api_endpoints.vesselownership,
                //     this.vessel.vessel_ownership.id + '/process_vessel_registration_document/'
                // )
            } else {
                url = 'temporary_document';
            }
            return url;
        },
    },
    methods: {
        addToTemporaryDocumentCollectionList(temp_doc_id) {
            this.temporary_document_collection_id = temp_doc_id;
        },
        clicked: function(){
            this.$emit('aho', 123)
        }
    }
}
</script>
<style scoped>
.party_detail_table {
    width: 100%;
}
.party_detail_table th, td {
    border: none;
}

</style>