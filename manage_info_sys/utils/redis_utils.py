import redis
import logging
import config


class CrawlerRedis:
    __redisPool = None

    def __init__(self, db=4):
        try:
            r = redis.ConnectionPool(host=config.get_config().CACHE_REDIS_HOST,
                                     port=config.get_config().CACHE_REDIS_PORT,
                                     password=config.get_config().CACHE_REDIS_PASSWORD, db=db)
            self.__redisPool = redis.Redis(connection_pool=r)
        except Exception as e:
            logging.error('init redis error: ' + str(e))

    def get_redis_pool(self):
        return self.__redisPool


mis_state_manage = CrawlerRedis(0)