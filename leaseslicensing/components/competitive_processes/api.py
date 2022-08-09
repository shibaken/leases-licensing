from rest_framework import viewsets

from leaseslicensing.components.competitive_processes.models import CompetitiveProcess
from leaseslicensing.components.competitive_processes.serializers import ListCompetitiveProcessSerializer
from leaseslicensing.helpers import is_internal


class CompetitiveProcessPaginatedViewSet(viewsets.ModelViewSet):
    queryset = CompetitiveProcess.objects.none()
    serializer_class = ListCompetitiveProcessSerializer

    def get_queryset(self):
        if is_internal(self.request):
            return CompetitiveProcess.objects.all()
        else:
            return CompetitiveProcess.objects.none()
    
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        qs = qs.distinct()
        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListCompetitiveProcessSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)