from aiogram import Router


def setup_routers() -> Router:
    from handlers import start_command
   
    router = Router()
    router.include_router(start_command.router)

    
    return router