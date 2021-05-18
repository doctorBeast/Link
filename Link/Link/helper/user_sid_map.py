from Link import cache


def get_user_sid(user_id):
    return cache.get(user_id)


def set_user_sid(user_id, sid):
    return cache.set(user_id, sid, timeout=300)
