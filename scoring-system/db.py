import sqlite3
import discord
from discord.ext import tasks
from datetime import datetime, timedelta
import os
import json
import random


async def create_db(bot, channel_ids):
    print(f"Creating databases...")
    with sqlite3.connect("discord_rpg.db") as connection:
        cursor = connection.cursor()

        # Create the 'users' table if it does not exist
        print(f"building users...")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                nickname TEXT,
                messages INTEGER,
                text_only_messages INTEGER,
                hyperlink_messages INTEGER,
                image_messages INTEGER,
                video_messages INTEGER,
                reply_messages INTEGER,
                sticker_messages INTEGER,
                emoji_reactions INTEGER,
                experience INTEGER
            )
        """
        )

        connection.commit()

        # Create the 'channels' table if it does not exist
        print(f"Building channels table...")
        channel_columns = ", ".join(
            f"channel_{channel_id} INTEGER" for channel_id in channel_ids
        )
        with sqlite3.connect("discord_rpg.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS channels (
                    user_id INTEGER PRIMARY KEY,
                    {channel_columns}
                )
            """
            )
            connection.commit()

        # Iterate through all members in the server and insert or ignore their data
        for guild in bot.guilds:
            for member in guild.members:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO users (user_id, username, nickname, messages, text_only_messages, hyperlink_messages, image_messages, video_messages, reply_messages, sticker_messages, emoji_reactions, experience)
                    VALUES (?, ?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                """,
                    (member.id, member.name, member.display_name),
                )

        connection.commit()

        print(f"Databases created!")
        # await fetch_random_event()


async def update_user_experience(user_id, experience):
    with sqlite3.connect("discord_rpg.db") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT experience FROM users WHERE user_id = ?", (user_id,))
        current_experience = cursor.fetchone()[0]
        new_experience = current_experience + experience

        cursor.execute(
            """
            UPDATE users
            SET experience = ?
            WHERE user_id = ?
            """,
            (new_experience, user_id),
        )

        connection.commit()


async def update_channel(user_id, channel_id):
    # Connect to the database
    with sqlite3.connect("discord_rpg.db") as connection:
        cursor = connection.cursor()

        # Check if the user exists in the 'channels' table
        cursor.execute("SELECT * FROM channels WHERE user_id = ?", (user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            # User exists, update the row
            cursor.execute(
                f"""
                UPDATE channels
                SET channel_{channel_id} = channel_{channel_id} + 1
                WHERE user_id = ?
                """,
                (user_id,),
            )
        else:
            # User does not exist, insert a new row
            cursor.execute(
                f"""
                INSERT INTO channels (user_id, channel_{channel_id})
                VALUES (?, 1)
                """,
                (user_id,),
            )

        # Commit the changes to the database
        connection.commit()


async def update_user(user_id, stat_type):
    # Connect to the database
    with sqlite3.connect("discord_rpg.db") as connection:
        cursor = connection.cursor()

        # Increment the specified stat for the given user
        cursor.execute(
            f"""
            UPDATE users
            SET {stat_type} = {stat_type} + 1
            WHERE user_id = ?
            """,
            (user_id,),
        )

        # Commit the changes to the database
        connection.commit()


async def fetch_user_info(user_id):
    with sqlite3.connect("discord_rpg.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT user_id, username, nickname, messages, experience
            FROM users
            WHERE user_id = ?
        """,
            (user_id,),
        )
        user_info = cursor.fetchone()

        return user_info


async def fetch_user_experience(user_id):
    with sqlite3.connect("discord_rpg.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT experience
            FROM users
            WHERE user_id = ?
        """,
            (user_id,),
        )
        user_info = cursor.fetchone()

        return user_info[0] if user_info else None


async def fetch_all_users_experience():
    with sqlite3.connect("discord_rpg.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT experience
            FROM users
        """
        )
        all_users_experience = [row[0] for row in cursor.fetchall()]

    return all_users_experience
