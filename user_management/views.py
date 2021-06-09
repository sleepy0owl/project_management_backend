import logging
import hashlib
from user_management.models import Users
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from constants import SUCCESSCODE, FAILURECODE, FAILRESPONSE
from .utils import check_email, check_existing_user, get_password, convert_password_md5
from .errors import WrongEmailFormatException, UserAlreadyExistsException, UserDoesntExistsException, WrongPasswordException
# Create your views here.
logger = logging.getLogger(__name__)

@api_view(['GET'])
def test_get(request):
    try:
        return Response({"message" : "all ok"})
    except Exception as e:
        return Response({"message" : "not all ok"})


@api_view(['POST'])
def create_user(request):
    try:
        data = request.data
        logger.info("request data %s", data)
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email_address = data['email_address']
        password = data['password']
        subscription_type = data['subscription_type'] 
        #! subscription_type = 1 = free max 10 boards 
        #! subscription_type = 2 = paid max unlimited

        with transaction.atomic():
            #! check email validity
            email_check = check_email(email_address)
            logger.info("check email address ")
            if email_check:
                logger.info("email address format is correct")
                #! check email or username alreadyy in db
                new_customer_check = check_existing_user(
                    email_address, username)
                logger.info("check if the user exists or not ")
                if new_customer_check:
                    logger.info("user doesnt exist")
                    logger.info("create new user")
                    md5_password = convert_password_md5(password)
                    user_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email_address": email_address,
                        "subscription_type": subscription_type,
                        "password": md5_password,
                        "username" : username
                    }
                    Users.objects.create(**user_data)
                    response = {
                        "code": SUCCESSCODE,
                        "exception": False,
                        "data": None
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    logger.info("already has an account")
                    raise UserAlreadyExistsException("already has an account")
            else:
                raise WrongEmailFormatException(
                    'email address format is correct')
    except UserAlreadyExistsException as u:
        logger.exception(u)
        response = FAILRESPONSE
        response['data'] = "user already exists"
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except WrongEmailFormatException as w:
        logger.exception(w)
        response = FAILRESPONSE
        response['data'] = "wrong email format"
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        response['data'] = 'exception occured'
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_user(request):
    try:
        data = request.data
        logger.info("request data %s", data)
        email_address = data['email_address']
        password = data['password']

        with transaction.atomic():
            email_check = check_email(email_address)
            logger.info("check email address ")
            if email_check:
                user_existance_check = check_existing_user(email=email_address, username="", both=False)
                if user_existance_check:
                    password_from_db = get_password(email=email_address)
                    md5_password = convert_password_md5(password)
                    if password_from_db == md5_password:
                        logger.info("password matched login successful")
                        response = {
                        "code": SUCCESSCODE,
                        "exception": False,
                        "data": None
                        }
                        return Response(response, status=status.HTTP_200_OK)
                    else:
                        WrongPasswordException("password is wrong")
                else:
                    raise UserDoesntExistsException("user does not exists")
            else:
                raise WrongEmailFormatException("email for is wrong")
    except WrongPasswordException as w:
        logger.exception(w)
        response = FAILRESPONSE
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except UserDoesntExistsException as u:
        logger.exception(u)
        response = FAILRESPONSE
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except WrongEmailFormatException as e:
        logger.exception(e)
        response = FAILRESPONSE
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.exception(e)
        response = FAILRESPONSE
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
