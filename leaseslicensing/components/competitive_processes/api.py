from datetime import datetime
from rest_framework import viewsets
from rest_framework import viewsets, views
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_datatables.filters import DatatablesFilterBackend

from leaseslicensing.components.competitive_processes.models import CompetitiveProcess
from leaseslicensing.components.competitive_processes.serializers import ListCompetitiveProcessSerializer
from leaseslicensing.helpers import is_internal


class CompetitiveProcessFilterBackend(DatatablesFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_status = request.GET.get("filter_status") if request.GET.get("filter_status") != "all" else ""
        filter_competitive_process_created_from = request.GET.get("filter_competitive_process_created_from")
        filter_competitive_process_created_to = request.GET.get("filter_competitive_process_created_to")

        if filter_status:
            queryset = queryset.filter(status=filter_status)
        if filter_competitive_process_created_from:
            filter_competitive_process_created_from = datetime.strptime(filter_competitive_process_created_from, "%Y-%m-%d")
            queryset = queryset.filter(created_at__gte=filter_competitive_process_created_from)
        if filter_competitive_process_created_to:
            filter_competitive_process_created_to = datetime.strptime(filter_competitive_process_created_to, "%Y-%m-%d")
            queryset = queryset.filter(created_at__lte=filter_competitive_process_created_to)

        fields = self.get_fields(request)
        ordering = self.get_ordering(request, view, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        queryset = super(CompetitiveProcessFilterBackend, self).filter_queryset(
            request, queryset, view
        )
        # setattr(view, "_datatables_total_count", total_count)
        return queryset

class CompetitiveProcessPaginatedViewSet(viewsets.ModelViewSet):
    queryset = CompetitiveProcess.objects.none()
    serializer_class = ListCompetitiveProcessSerializer
    filter_backends = (CompetitiveProcessFilterBackend,)

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


class GetCompetitiveProcessStatusesDict(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        data = [{"id": i[0], "text": i[1]} for i in CompetitiveProcess.STATUS_CHOICES]
        return Response(data)

