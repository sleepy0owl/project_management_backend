from rest_framework import serializers
from .models import BoardList, WorkflowBoard
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
        model = BoardList
        fields = '__all__'

