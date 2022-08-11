<template lang="html">
    <div class="container" v-if="competitive_process">
        <div class="row">
            <h3>Competitive Process: {{ competitive_process.lodgement_number }}</h3>
        </div>
    </div>
</template>

<script>
import { api_endpoints, helpers } from '@/utils/hooks'
import { v4 as uuid } from 'uuid'

export default {
    name: 'CompetitiveProcess',
    data: function() {
        let vm = this;
        return {
            competitive_process: null
        }
    },
    created: function(){
        this.fetchCompetitiveProcess()
    },
    mounted: function(){

    },
    methods: {
        fetchCompetitiveProcess: async function(){
            let vm = this
            try {
                const res = await fetch('/api/competitive_process/' + vm.$route.params.competitive_process_id)
                if (!res.ok)
                    throw new Error(res.statusText)  // 400s or 500s error
                let competitive_process = await res.json()
                vm.competitive_process = competitive_process
            } catch(err){
                console.log({err})
            } finally {

            }
        }
    }
}
</script>

<style>
</style>