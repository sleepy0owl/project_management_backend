## Project Management APIs
This project uses Python3, Django REST framework and sqlite3.
### List of API endpoints
```
- api/project/user/create/ | POST | 

request body | JSON | 
{"first_name" :"sourav","last_name" :"mondal","username" : "sleepyowl","email_address" : "sourav.mondal@abcd.com","password" : "1234","subscription_type" : 1
}

here subscription_type = 1 is free and 2 is paid

```
```
- api/project/user/login/  | POST |

request body | JSON | 
{
    "email_address" : "sourav.mondal@abcd.com",
    "password" : "1234"
}

```

```
- api/project/board/create/ | POST |

request body | JSON | 
{
    "user_id" : <int>,
    "board_name" : "Golang projects",
    "board_description" : "Golang project management board"
}

```
```
- api/project/board/getbycustomer/ | POST |

request body | JSON | 
{
    "user_id" : <int>
}

```
```
- api/project/board/details | POST |

request body | JSON | 
{
     "board_id": <existing board id>
}
```

```
- api/project/list/create/ | POST |

request body | JSON | 
{
    "board_id" : <existing board id>,
    "list_name" : "doing"
}

```
```
- api/project/list/update/ | POST |

request body | JSON | 
{
    "list_id" : <existing list id>,
    "list_name" : <desired name>
}

```
```
- api/project/list/details/ | POST |

request body | JSON | 
{
    "list_id" : <existing list id>
}

```
```
- api/project/card/create/ | POST |

request body | JSON | 
 {
    "list_id" : <existing list id>,
    "card_name" : "code review",
    "card_description" : "code review of a github repo",
    "due_date" : "2021-06-20",
    "attachments" : ["http://google.com/],
    "priority" : 2
}
here higher value of priority represnts high priority task
```
```
- api/project/card/update/ | POST |

request body | JSON | 
 {
    "card_id": <existing card id>,
    "card_name": "Work on face recognition",
    "card_description": "Use OpenCv to build a face recognition API",
    "due_date": "2021-06-13",
    "priority": 1
}

```
```
- api/project/card/get/ | POST |
request body | JSON | 
{
    "card_id" : <existing card it>
}
```
```
- api/project/card/changelist/ | POST |

request body | JSON | 
{
    "card_id" : <existing card id>,
    "list_id" : <destination list id>
}

```
```
start development server using python3 manage.py runserver
```
**This will start a server at localhost[http://127.0.0.1:8000]**

**Use a API testing tool like postman to test the above APIs**