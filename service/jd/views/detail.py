from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_detail
import random

async def detail(link: str):
    """
    搜索京东商品
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res = await request_detail(link, account.get('cookie', ''))
        logger.info(f'search success, account: {account_id}, link: {link}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'search failed, account: {account_id}, link: {link}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')