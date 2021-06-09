from rest_framework import serializers
from .models import BoardList, WorkflowBoard, Card, Attachments


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowBoard
        fields = '__all__'


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardList
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachments
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer(many=True)
    class Meta:
        model = Card
        fields = '__all__'

class CardDetailSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer(many=True)
    class Meta:
        model = Card
        fields = ['card_id', "card_name", "card_description",
                  "updated_on", 'due_date', 'priority', 'attachment']


class ListDetailSerializer(serializers.ModelSerializer):
    # card = CardDetailSerializer(many=True)
    card = serializers.SerializerMethodField()

    class Meta:
        model = BoardList
        fields = ['list_id', 'list_name', 'updated_on', 'card']

    def get_card(self, instance):
        cards = instance.card.all().order_by('-priority')
        return CardDetailSerializer(cards, many=True).data


class BoardDetailSerializer(serializers.ModelSerializer):
    board_list = ListDetailSerializer(many=True)

    class Meta:
        model = WorkflowBoard
        fields = ['board_id', 'board_name', 'board_description', 'board_list']
