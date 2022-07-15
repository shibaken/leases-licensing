from rest_framework import serializers


class RelatedItem:
    def __init__(self, model_name='', identifier='', descriptor='',
            action_url='', weak_link=False, second_object_id=None, second_content_type=None, comment=None):
        self.model_name = model_name
        self.identifier = identifier
        self.descriptor = descriptor
        self.action_url = action_url
        # self.weak_link = weak_link
        # self.second_object_id = second_object_id
        # self.second_content_type = second_content_type
        # self.comment = comment


class RelatedItemsSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    identifier = serializers.CharField()
    descriptor = serializers.CharField()
    action_url = serializers.CharField(allow_blank=True)
    # second_object_id = serializers.IntegerField(allow_null=True)
    # second_content_type = serializers.CharField(allow_blank=True)
    # weak_link = serializers.BooleanField()
    # comment = serializers.CharField()


def get_related_items(entity, **kwargs):
    related_item = RelatedItem(
        model_name='model_name1',
        identifier='identifier1',
        descriptor='descriptor1',
        action_url='action_url1',
    )
    related_item2 = RelatedItem(
        model_name='model_name2',
        identifier='identifier2',
        descriptor='descriptor2',
        action_url='action_url2',
    )
    # serializer = RelatedItemsSerializer(return_list, many=True)
    # return serializer.data
    return [related_item, related_item2,]
