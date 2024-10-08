from loguru import logger
from data import config
import pyrogram
from data.config import USE_PROXY

async def create_sessions():
    while True:
        session_name = input('Введите название сессии (для выхода нажмите Enter)\n')
        if not session_name:
            return
        
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r',encoding='utf-8') as file:
                list = [i.strip().split() for i in file.readlines()]
                proxy = []
                for info in list:
                    if info!=[]:
                        proxy.append((info[0],''.join(info[1:]).replace('.session','')))
                for prox,name in proxy:
                    proxy_dict[name] = prox
            
            if session_name in proxy_dict:
                proxy = proxy_dict[session_name]
                proxy_client = {
                    "scheme": config.PROXY_TYPE,
                    "hostname": proxy.split(':')[0],
                    "port": int(proxy.split(':')[1]),
                    "username": proxy.split(':')[2],
                    "password": proxy.split(':')[3],
                }
                
                session = pyrogram.Client(
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    name=session_name,
                    workdir=config.WORKDIR,
                    proxy=proxy_client
                )

                async with session:
                    user_data = await session.get_me()

                logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY {proxy.split(":")[0]}')
            else:
                if config.CHECK_PROXY:
                    logger.error(f"{session_name}.session ПРОКСИ НЕ НАЙДЕН")
                    return False
                            
                session = pyrogram.Client(
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    name=session_name,
                    workdir=config.WORKDIR
                )

                async with session:
                    user_data = await session.get_me()

                logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY : NONE')
        else:
            
            session = pyrogram.Client(
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                name=session_name,
                workdir=config.WORKDIR
            )

            async with session:
                user_data = await session.get_me()

            logger.success(f'Добавлена сессия +{user_data.phone_number} @{user_data.username} PROXY : NONE')
