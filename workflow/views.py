import logging

from rest_framework.settings import APISettings

from user_management.models import Users
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db import connection
from .models import Card, Users, WorkflowBoard, BoardList
from .serializers import BoardDetailSerializer, BoardSerializer, BoardListSerializer, CardSerializer
from .serializers import ListDetailSerializer
from .errors import MaxBoardLimitReachedException
from constants import FAILRESPONSE, SUCCESSCODE
# Create your views here.
logger = logging.getLogger(__name__)


@api_view(['GET'])
def test_get(request):
    try:
        return Response({"message": "all ok"})
    except Exception as e:
        return Response({"message": "not all ok"})


@api_view(['POST'])
def create_board(request):
    """ takes user id check's subscription type and creates a board """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        user_id = data['user_id']
        board_name = data['board_name']
        board_description = data['board_description']

        #! check user's subscription type
        with transaction.atomic():
            user = Users.objects.get(pk=user_id)
            logger.info("user's subscription type %s", user.subscription_type)
            if user.subscription_type == 1:
                logger.info("check current board count")
                board_count = WorkflowBoard.objects.filter(
                    user_id=user_id).count()
                logger.info("user's board count %s", board_count)
                #! subscription type free
                if board_count < 10:
                    board_data = {
                        "board_name": board_name,
                        "board_description": board_description
                    }
                    current_board = WorkflowBoard.objects.create(
                        **board_data, user=user)
                    board_serializer = BoardSerializer(current_board)
                    response = {
                        "code": SUCCESSCODE,
                        "exception": False,
                        "data": {
                            "board": board_serializer.data
                        }
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    raise MaxBoardLimitReachedException(
                        "customer has reached max board limit")
            else:
                #! subscription type paid
                board_data = {
                    "board_name": board_name,
                    "board_description": board_description
                }
                current_board = WorkflowBoard.objects.create(
                    **board_data, user=user)
                board_serializer = BoardSerializer(current_board)
                response = {
                    "code": SUCCESSCODE,
                    "exception": False,
                    "data": {
                        "board": board_serializer.data
                    }
                }
                logger.info("================================= end  - ==============================")
                return Response(response, status=status.HTTP_201_CREATED)
    except MaxBoardLimitReachedException as m:
        logger.exception(m)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_all_boards(request):
    """ takes user'id and returns all boards """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        user_id = data['user_id']
        with transaction.atomic():
            user = Users.objects.get(pk=user_id)
            boards = WorkflowBoard.objects.filter(user=user)
            board_serializers = BoardSerializer(boards, many=True)
            response = {
                "code" : SUCCESSCODE,
                "exception" : False,
                "data" : {
                    "boards" : board_serializers.data
                }
            }
            logger.info("================================= end  - ==============================")
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def get_board_details(request):
    """ takes board's id and returns all information associated with it """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        board_id = data['board_id']
        
        with transaction.atomic():
            current_board = WorkflowBoard.objects.get(pk=board_id)
            board_serializer = BoardDetailSerializer(current_board)

            logger.info("board details %s", board_serializer.data)
            response = {
                "code" : SUCCESSCODE,
                "exception" : False,
                "data" : {
                    "board_details" : board_serializer.data
                }
            }
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def create_list(request):
    """ creates a list for a board """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        board_id = data['board_id']
        list_name = data['list_name']

        with transaction.atomic():
            board = WorkflowBoard.objects.get(board_id=board_id)
            list_data = {
                "list_name": list_name
            }
            current_list = BoardList.objects.create(**list_data, board=board)
            list_serializer = BoardListSerializer(current_list)
            response = {
                "code": SUCCESSCODE,
                "exception": False,
                "data": {
                    "board_list": list_serializer.data
                }
            }
            logger.info("list is created successfully")
            return Response(response, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_list(request):
    """ updates a lists property """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        list_id = data['list_id']
        list_name = data['list_name']
        with transaction.atomic():
            list_data = {"list_name": list_name}
            BoardList.objects.filter(list_id=list_id).update(**list_data)
            current_list = BoardList.objects.get(pk=list_id)
            list_serializer = BoardListSerializer(current_list)
            response = {
                "code": SUCCESSCODE,
                "exception": False,
                "data": {
                    "board_list": list_serializer.data
                }
            }
            logger.info("list is updated successfully")
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_list_details(request):
    """ takes list id and returns all the cards associated with it  """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        list_id = data['list_id']

        with transaction.atomic():
            current_list = BoardList.objects.get(pk=list_id)
            list_serializer = ListDetailSerializer(current_list)

            logger.info("list +card %s", list_serializer.data)
            response = {
                "code" : SUCCESSCODE,
                "exception" : False,
                "data" : {
                    "list_details" : list_serializer.data
                }
            }
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def create_card(request):
    """ creates a card for a list """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        card_name = data['card_name']
        card_desciption = data['card_description']
        due_date = data['due_date']
        list_id = data['list_id']
        priority = data['priority']
        with transaction.atomic():
            current_list = BoardList.objects.get(pk=list_id)
            card_data = {
                "card_name": card_name,
                "card_desciption": card_desciption,
                "due_date" : due_date,
                "priority" : priority
            }
            current_card = Card.objects.create(
                **card_data, board_list=current_list)
            card_serializer = CardSerializer(current_card)
            response = {
                "code": SUCCESSCODE,
                "exception": False,
                "data": {
                    "card": card_serializer.data
                }
            }
            logger.info("card is creadted successfully")
            return Response(response, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_card(request):
    """ updates a cards name and description """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        card_name = data['card_name']
        card_desciption = data['card_description']
        card_id = data['card_id']
        due_date = data['due_date']
        priority = data['priority']
        with transaction.atomic():
            card_data = {
                "card_name": card_name,
                "card_desciption": card_desciption,
                "due_date" : due_date,
                "priority" : priority
            }
            Card.objects.filter(card_id=card_id).update(**card_data)
            current_card = Card.objects.get(pk=card_id)
            card_serializer = CardSerializer(current_card)
            response = {
                "code": SUCCESSCODE,
                "exception": False,
                "data": {
                    "card": card_serializer.data
                }
            }
            logger.info("card is creadted successfully")
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def get_card(request):
    """ takes card's id and returns it;s details """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        card_id = data['card_id']

        with transaction.atomic():
            card = Card.objects.get(pk=card_id)
            card_serializer = CardSerializer(card)

            response = {
                "code": SUCCESSCODE,
                "exception": False,
                "data": {
                    "card": card_serializer.data
                }
            }
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def change_card_list(request):
    """ takes a card from one list and assign it to other """
    try:
        logger.info("================================= start - ==============================")
        data = request.data
        logger.info("request data %s", data)
        card_id = data['card_id']
        destination_list = data['list_id']

        with transaction.atomic():
            new_list = BoardList.objects.get(pk=destination_list)
            Card.objects.filter(card_id=card_id).update(board_list=new_list)

            updated_list = BoardList.objects.get(pk=destination_list)
            list_serializer = ListDetailSerializer(updated_list) 
            response = {
                "code": SUCCESSCODE,
                "exception": False,
                "data": {
                    "card": list_serializer.data
                }
            }
            return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        logger.info("================================= end  - ==============================")
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

