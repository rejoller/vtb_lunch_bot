from aiogram import Router


def setup_routers() -> Router:
    from handlers import start_command, subscribe
    from vtb_tg_bot.callbacks import subscribe_cb
   
    router = Router()
    router.include_router(start_command.router)
    router.include_router(subscribe.router)
    router.include_router(subscribe_cb.router)

    
    return router