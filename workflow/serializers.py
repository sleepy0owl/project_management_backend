from rest_framework import serializers
from .models import BoardList, WorkflowBoard, Card
class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowBoard
        fields = '__all__'

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardList
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class CardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_id', "card_name", "card_desciption", "updated_on", 'due_date']


class ListDetailSerializer(serializers.ModelSerializer):
    card = CardDetailSerializer(many=True)
    class Meta:
        model = BoardList
        fields = ['list_id', 'list_name', 'updated_on', 'card']

class BoardDetailSerializer(serializers.ModelSerializer):
    board_list = ListDetailSerializer(many=True)
    class Meta:
        model = WorkflowBoard
        fields = ['board_id', 'board_name', 'board_description', 'board_list']
