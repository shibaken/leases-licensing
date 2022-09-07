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
                <div v-if="party_full_data.party_details.length > 0" class="details_box p-2">
                    <template v-for="(party_detail, index) in party_full_data.party_details" :key="party_detail.id">
                        <template v-if="index!=0">
                            <hr class="m-1">
                        </template>

                        <template v-if="party_detail.id">
                            <!-- This is an entry already saved in the database -->
                            <div>{{ party_detail.created_by.fullname }}, {{ formatDatetime(party_detail.created_at) }}</div>
                        </template>
                        <template v-else>
                            <!-- This entry is the one added just now, and not saved into the database yet -->
                            <div>{{ party_detail.accessing_user.full_name }} {{ formatDatetime(party_detail.created_at) }}</div>
                        </template>

                        <div>{{ party_detail.detail }}</div>

                        <template v-for="document in party_detail.party_detail_documents">
                            <div><a :href="document.file" target="_blank"><i :class="getFileIconClass(document.file)"></i> {{ document.name }}</a></div>
                        </template>
                    </template>
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
                                    :key="filefield_id"
                                ></FileField>
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
import { v4 as uuid } from 'uuid';

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
            filefield_id: uuid(),
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
        getFileIconClass: function(filepath){
            let ext = filepath.split('.').pop().toLowerCase()
            let classname = ['bi', 'fa-lg',]
            if (['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif',].includes(ext)){
                classname.push('bi-file-image-fill')
            } else if (['pdf',].includes(ext)){
                classname.push('bi-file-pdf-fill')
            } else if (['doc', 'docx',].includes(ext)){
                classname.push('bi-file-word-fill')
            } else if (['xls', 'xlsx',].includes(ext)){
                classname.push('bi-file-excel-fill')
            } else if (['txt', 'text',].includes(ext)){
                classname.push('bi-file-text-fill')
            } else if (['rtf',].includes(ext)){
                classname.push('bi-file-richtext-fill')
            } else if (['mp3', 'mp4'].includes(ext)){
                classname.push('bi-file-play-fill')
            } else {
                classname.push('bi-file_fill')
            }
            return classname.join(' ')
        },
        formatDatetime: function(dt){
            return moment(dt).format(this.datetimeFormat);
        },
        addDetailClicked: function(){
            let now = new Date()
            this.party_full_data.party_details.push({
                'id': 0,  // Should be 0, which is used to determine this as a new entry at the backend
                'created_at': now,
                'detail': this.new_detail_text,
                'temporary_document_collection_id': this.temporary_document_collection_id,
                'created_by_id': this.accessing_user.id,
                'accessing_user': this.accessing_user,
                'party_detail_documents': this.$refs.temp_document.documents,
            })
            this.new_detail_text = ''
            this.filefield_id = uuid()
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
    background-color: white;
}
.details_box {
    /* border: 1px solid lightgray; */
    border-radius: 0.25em;
    background-color: whitesmoke;
}
.detail_text {
    width: 100%;
}

</style>