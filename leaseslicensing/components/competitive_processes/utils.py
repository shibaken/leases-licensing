from leaseslicensing.components.competitive_processes.serializers import CompetitiveProcessSerializer, \
    CompetitiveProcessPartySerializer


def format_data(competitive_process):
    for party in competitive_process.get('competitive_process_parties', []):
        for party_detail in party.get('party_details', []):
            if 'temporary_data' in party_detail:
                party_detail['detail'] = party_detail['temporary_data']['detail']
                party_detail['created_by_id'] = party_detail['temporary_data']['accessing_user']['id']
    return competitive_process
