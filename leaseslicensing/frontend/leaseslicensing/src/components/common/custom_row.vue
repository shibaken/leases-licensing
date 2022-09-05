<template>
    <div @click="clicked">Test Event</div>
    <table class="party_detail_table">
        <tr>
            <th>Invited to competitive process</th>
            <td><input type="date" class="form-control w-auto" placeholder="DD/MM/YYYY" v-model="party_full_data.invited_at"></td>
        </tr>
        <tr>
            <th>Removed from competitive process</th>
            <td><input type="date" class="form-control w-auto" placeholder="DD/MM/YYYY" v-model="party_full_data.removed_at"></td>
        </tr>
        <tr>
            <th>Details</th>
            <td>
                <div class="details_box p-2">
                    <div v-for="(party_detail, index) in party_full_data.party_details" :key="party_detail.id">
                        <template v-if="index!=0">
                            <hr class="m-1">
                        </template>
                        <template v-if="party_detail.id">
                            <!-- This is an entry already saved in the database -->
                            <div>{{ party_detail.created_by.fullname }}, {{ formatDatetime(party_detail.created_at) }}</div>
                            <div>{{ party_detail.detail }}</div>
                            <div>(Files here)</div> 
                        </template>
                        <template v-else>
                            <!-- This entry is the one added just now, and not saved into the database yet -->
                            <div>{{ party_detail.temporary_data.accessing_user.full_name }} {{ formatDatetime(party_detail.temporary_data.created_at) }}</div>
                            <div>{{ party_detail.temporary_data.detail }}</div>
                            <template v-for="document in party_detail.temporary_data.documents">
                                <div><a href="document.file">{{ document.name }}</a></div>
                            </template>
                        </template>
                    </div>
                </div>
                <div class="new_detail_div mt-2 p-2">
                    <table class="party_detail_table">
                        <tr>
                            <th>New detail</th>
                            <td>
                                <input type="text" class="form-control detail_text" v-model="new_detail_text">
                            </td>
                        </tr>
                        <tr>
                            <th>Documents</th>
                            <td>
                                <FileField
                                    :readonly="readonly"
                                    ref="temp_document"
                                    name="temp_document"
                                    :isRepeatable="true"
                                    :documentActionUrl="detailDocumentUrl"
                                    :replace_button_by_text="true"
                                    :temporaryDocumentCollectionId="temporary_document_collection_id"
                                    @update-temp-doc-coll-id="addToTemporaryDocumentCollectionList"
                                />
                            </td>
                        </tr>
                        <tr>
                            <th></th>
                            <td class="text-end"><button class="btn btn-primary" @click="addDetailClicked"><i class="fa-solid fa-circle-plus"></i> Add</button></td>
                        </tr>
                        
                    </table>
                </div>
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
        accessing_user: null,
    },
    components: {
        FileField,
    },
    data() {
        let vm = this;
        return {
            temporary_document_collection_id: null,
            new_detail_text: '',
            datetimeFormat: 'DD/MM/YYYY HH:mm:ss',
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
        formatDatetime: function(dt){
            return moment(dt).format(this.datetimeFormat);
        },
        addDetailClicked: function(){
            this.party_full_data.party_details.push({
                'temporary_data': {
                    'detail': this.new_detail_text,
                    'temporary_document_collection_id': this.temporary_document_collection_id,
                    'documents': this.$refs.temp_document.documents,
                    'accessing_user': this.accessing_user,
                    'created_at': new Date(),
                }
            })
            this.new_detail_text = ''
        },
        addToTemporaryDocumentCollectionList(temp_doc_id) {
            console.log({temp_doc_id})
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
.new_detail_div {
    border: 1px solid lightgray;
    border-radius: 0.25em;
}
.details_box {
    border: 1px solid lightgray;
    border-radius: 0.25em;
}
.detail_text {
    width: 100%;
}

</style>