import logging
import re
from user_management.errors import UserDoesntExistsException
from .models import Users

logger = logging.getLogger(__name__)

def check_email(email: str) -> bool:
    if re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email):
        return True
    else:
        return False

def check_existing_user(email: str, username: str, both: bool = True) -> bool:
    #! check email 
    if both:
        email_count = Users.objects.filter(email_address=email).count()
        username_count = Users.objects.filter(username=username).count()
        logger.info("email count %s", email_count)
        logger.info("username count %s", username_count)
        if email_count == 0 and username_count == 0:
            return True
        else:
            return False
    else:
        email_count = Users.objects.filter(email_address=email).count()
        logger.info("email count %s", email_count)
        if email_count == 1:
            return True
def get_password(email : str) -> str:
    user = Users.objects.get(email_address=email)
    password_from_db = user.password
    return password_from_db