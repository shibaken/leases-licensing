<template>
    <div>
        <div @click="clicked">Test Event</div>
        <table>
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
                </td>
            </tr>
        </table>
    </div>
</template>


<script>
export default {
    name: 'CustomRow',
    props: {
        party_full_data: null,
    },
    data() {
        let vm = this;
        return {
            //full_data: null,
        }
    },
    created: function(){
        //this.invited_at_data = this.invited_at
    },
    methods: {
        clicked: function(){
            this.$emit('aho', 123)
        }
    }
}
</script>