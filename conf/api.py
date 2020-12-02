auth_apis = {
    'register': {'path': '/register', 'methods': ['POST', ], 'name': 'register'},
    'login': {'path': '/login', 'methods': ['POST', ], 'name': 'login'},
    'logout': {'path': '/logout', 'methods': ['POST', ], 'name': 'logout'},
    'delete_account': {'path': '/delete-account', 'methods': ['POST', ], 'name': 'delete_account'},
}

post_apis = {
    'new': {'path': '/new', 'methods': ['POST', ], },
    'all': {'path': '/all', 'methods': ['GET', ], },
    'me_all': {'path': '/me/all', 'methods': ['GET', ], },
    'get': {'path': '/get', 'methods': ['GET', ], },
    'delete': {'path': '/delete/{post_id}', 'methods': ['GET', ], },
    'edit': {'path': '/edit/{post_id}', 'methods': ['POST', ], },
}

like_apis = {
    'like': {'path': '/like', 'methods': ['GET', ], },
    'unlike': {'path': '/unlike', 'methods': ['GET', ], },
    'liked': {'path': '/liked', 'methods': ['GET', ], },
    'likes': {'path': '/likes', 'methods': ['GET', ], },
}
