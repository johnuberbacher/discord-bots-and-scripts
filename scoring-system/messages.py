# messages.py
import discord
from discord import File
from discord.ui import Button, View
import os
import sqlite3
import requests
from db import (
    update_user,
    update_channel,
)
from io import BytesIO


async def on_reaction_received(reaction, user):

    print(f"{user.name} reacted with {reaction.emoji} to a message.")

    # Update the Users stats
    await update_user(user.id, "emoji_reactions")
    print(f"...")


async def on_message_received(message):

    # Check if the message has attachments
    if message.attachments:
        image_extensions = [".bmp", ".png", ".jpg", ".jpeg", ".gif", ".webp"]
        video_extensions = [
            ".mov",
            ".mp4",
            ".wmv",
            ".avi",
            ".flv",
            ".avchd",
            ".webm",
            ".mkv",
            ".m4v",
            ".m4p",
            ".m4b",
            ".mpg",
            ".mpeg",
            ".mpg",
            ".3gp",
        ]
        for attachment in message.attachments:
            if any(
                attachment.filename.lower().endswith(ext) for ext in image_extensions
            ):
                print(f"{message.author} sent a message with an image attachment.")
                await update_user(message.author.id, "image_messages")
                break
            elif any(
                attachment.filename.lower().endswith(ext) for ext in video_extensions
            ):
                print(f"{message.author} sent a message with a video attachment.")
                await update_user(message.author.id, "video_messages")
                break
    elif all(keyword in message.content.lower() for keyword in "https://youtube.com"):
        print(f"{message.author} sent a message with a YouTube URL.")
        await update_user(message.author.id, "hyperlink_messages")
    elif any(url in message.content.lower() for url in ("http://", "https://")):
        print(f"{message.author} sent a message with a website URL.")
        await update_user(message.author.id, "hyperlink_messages")
    elif message.stickers:
        print(f"{message.author} sent a message with a sticker.")
    else:
        await update_user(message.author.id, "text_only_messages")
        print(f"{message.author} sent a message.")

    # Check if the message is a reply
    if message.reference is not None and message.reference.message_id is not None:
        replied_message_id = message.reference.message_id
        await update_user(message.author.id, "reply_messages")
        print(f"{message.author} replied to another message.")

    # Update the Users stats
    await update_user(message.author.id, "messages")
    await update_channel(message.author.id, message.channel.id)
    print(f"...")
    print(f"...")
