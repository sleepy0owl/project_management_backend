from django.urls import path
from user_management.views import test_get, create_user, login_user
from workflow.views import create_board, get_all_boards, create_list, update_card, update_list, create_card, get_card, get_list_details, get_board_details, change_card_list
urls = [
    path('test/get/', test_get),
    path('user/create/', create_user),
    path('user/login/', login_user),
    path('board/create/', create_board),
    path('board/getbycustomer/', get_all_boards),
    path('board/details/', get_board_details),
    path('list/create/', create_list),
    path('list/update/', update_list),
    path('list/details/', get_list_details),
    path('card/create/', create_card),
    path('card/update/', update_card),
    path('card/get/', get_card),
    path('card/changelist/', change_card_list)
]