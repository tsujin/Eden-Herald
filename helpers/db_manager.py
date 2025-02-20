""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

import aiosqlite


async def add_channel(server_id: int, channel_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("INSERT INTO channels(server_id, channel_id) VALUES (?, ?)", (server_id,channel_id))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM channels")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def update_channel(server_id: int, channel_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("UPDATE channels SET channel_id=? WHERE server_id=?", (channel_id, server_id))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM channels")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def get_channel(server_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        rows = await db.execute("SELECT channel_id FROM channels WHERE server_id=?", (server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()

        return result[0] if result else None


async def add_boss_kill(boss_name, killed_at):
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("INSERT INTO boss_kills(boss_name, last_killed) VALUES (?, ?)", (boss_name, killed_at))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM boss_kills")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def update_boss_kill(boss_name, killed_at):
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("UPDATE boss_kills SET last_killed = ? WHERE boss_name = ?", (killed_at, boss_name))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM boss_kills")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def get_boss_data():
    async with aiosqlite.connect("database/database.db") as db:
        rows = await db.execute("SELECT * FROM boss_kills")
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute("SELECT * FROM blacklist WHERE user_id=?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def add_warn(user_id: int, server_id: int, moderator_id: int, reason: str) -> int:
    """
    This function will add a warn to the database.

    :param user_id: The ID of the user that should be warned.
    :param reason: The reason why the user should be warned.
    """
    async with aiosqlite.connect("database/database.db") as db:
        rows = await db.execute("SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await db.execute("INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)", (warn_id, user_id, server_id, moderator_id, reason,))
            await db.commit()
            return warn_id


async def remove_warn(warn_id: int, user_id: int, server_id: int) -> int:
    """
    This function will remove a warn from the database.

    :param warn_id: The ID of the warn.
    :param user_id: The ID of the user that was warned.
    :param server_id: The ID of the server where the user has been warned
    """
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?", (warn_id, user_id, server_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def get_warnings(user_id: int, server_id: int) -> list:
    """
    This function will get all the warnings of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :return: A list of all the warnings of the user.
    """
    async with aiosqlite.connect("database/database.db") as db:
        rows = await db.execute("SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?", (user_id, server_id,))
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list