from fastapi.middleware.cors import CORSMiddleware

from configs import configure_app

from routes import transaction_v1_router, coins_v1_router, interest_v1_router, history_v1_router, sockets_v1_router

from utils import configure_logging

configure_logging()

app = configure_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sockets_v1_router)
app.include_router(coins_v1_router)
app.include_router(transaction_v1_router)
app.include_router(history_v1_router)
app.include_router(interest_v1_router)


