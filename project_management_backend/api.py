from django.urls import path
from user_management.views import test_get, create_user, login_user
from workflow.views import create_board, get_all_boards, create_list, update_list
urls = [
    path('test/get/', test_get),
    path('user/create/', create_user),
    path('user/login/', login_user),
    path('board/create/', create_board),
    path('board/getbycustomer/', get_all_boards),
    path('list/create/', create_list),
    path('list/update/', update_list)
]