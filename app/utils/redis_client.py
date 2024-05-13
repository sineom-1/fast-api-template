#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author sineom
@Date 2024/5/7-17:01
@Email h.sineom@gmail.com
@description  redis配置
@Copyright (c) 2022 by sineom, All Rights Reserved.
"""

import asyncio
import random
import uuid
from typing import Optional, Awaitable

import redis
from loguru import logger
from redis import Redis
from typing_extensions import Literal


class RedisClient:
    _instance = None
    _redis = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, host: str, port: int, db: int, username: str = None, password: str = None, pool_size: int = 10):
        self._redis: Optional[Redis] = None
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.pool_size = pool_size

    def get_redis(self):
        self._redis = self._redis or redis.Redis(
            host=self.host, port=self.port, db=self.db, password=self.password, max_connections=self.pool_size,
            decode_responses=True
        )
        return self._redis

    def set(self, key, value, expire=None):
        _redis = self.get_redis()
        if expire:
            _redis.set(key, value, ex=expire)
        else:
            _redis.set(key, value)

    def sadd(self, key, *value):
        """
        向set中添加元素
        """
        _redis = self.get_redis()
        _redis.sadd(key, *value)

    def smembers(self, key):
        """
        获取set中的所有元素
        """
        _redis = self.get_redis()
        return _redis.smembers(key)

    def srem(self, key, *value):
        """
        移除set中的元素
        """
        _redis = self.get_redis()
        _redis.srem(key, *value)

    def sismember(self, key, value) -> Literal[0, 1] | Awaitable[Literal[0, 1]]:
        """
        判断元素是否在set中
        """
        _redis = self.get_redis()
        return _redis.sismember(key, value)

    def get(self, key):
        _redis = self.get_redis()
        return _redis.get(key)

    def delete(self, key):
        _redis = self.get_redis()
        _redis.delete(key)

    class RedisLock:
        def __init__(self, redis_client, lock_key, token, expiration):
            self.redis_client = redis_client
            self.lock_key = lock_key
            self.token = token
            self.expiration = expiration

        async def __aenter__(self):
            await self.redis_client.acquire_lock(self.lock_key, self.token, self.expiration)
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            await self.redis_client.release_lock(self.lock_key, self.token)

    async def acquire_lock(self, lock_key: str, expiration: int = 10000, retry_delay: float = 0.1,
                           jitter: float = 0.01) -> Optional[RedisLock]:
        """
        尝试获取分布式锁
        lock_key: 锁的键名
        expiration: 锁的过期时间（毫秒）
        retry_delay: 如果锁被其他客户端持有，等待这么多秒后再次尝试获取锁
        """
        token = str(uuid.uuid4())
        _redis = self.get_redis()
        logger.debug(f"设置锁 {lock_key} {token}")
        while True:
            # 防止死锁
            if _redis.exists(lock_key):
                return None
            if _redis.set(lock_key, token, nx=True, px=expiration):
                return self.RedisLock(self, lock_key, token, expiration)
            else:
                await asyncio.sleep(retry_delay * (1 + random.uniform(-jitter, jitter)))

    def release_lock(self, lock_key: str, token: str):
        """
        释放分布式锁
        lock_key: 锁的键名
        token: 与锁对应的标识符，防止删除非本客户端持有的锁
        """
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        _redis = self.get_redis()
        logger.debug(f"释放锁 {lock_key} {token}")
        cmd = _redis.register_script(script)
        result = cmd(keys=[lock_key], args=[token])
        logger.debug(f"释放锁 {result}")
        return result == 1

    # 检测技能是否处于冷却时间
    def trigger_skill(self, skill_name: str, ex: int = None) -> bool:
        """
        触发技能A的函数
        :param skill_name: 技能名称
        :param ex: 冷却时间 毫秒
        :return: bool  true - 不处于冷却时间  false - 处于冷却时间
        """
        # 技能A的冷却时间键
        skill_key = f'{skill_name}:cooldown'
        # 用户请求的键
        user_request_key = f'{skill_name}:request'

        # 使用Redis事务来保证原子性
        with self.get_redis().pipeline() as pipe:
            # 检查技能是否处于冷却时间
            pipe.exists(skill_key)
            # 设置用户请求的键，如果技能不在冷却时间内 冷却时间随机1000-4000毫秒
            pipe.set(user_request_key, 1, nx=True, ex=ex or random.randint(1000, 4000))
            # 执行事务
            results = pipe.execute()
            # 如果技能不在冷却时间内，并且用户请求的键设置成功
            return not results[0] and results[1]
            # if not results[0] and results[1]:
            #     print(f"User {user_id} triggered skill A successfully!")
            #     # 模拟技能处理时间
            #     time.sleep(1)
            #     # 技能处理完成后，删除用户请求的键
            #     r.delete(user_request_key)
            # else:
            #     print(f"User {user_id} failed to trigger skill A due to cooldown.")
