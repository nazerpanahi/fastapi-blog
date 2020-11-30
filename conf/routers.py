from routers import auth_router, post_router, user_post_like_router

ROUTERS = [
    {'router': auth_router, 'tags': ['Authentication']},
    {'router': post_router, 'prefix': '/post', 'tags': ['Post']},
    {'router': user_post_like_router}
]
