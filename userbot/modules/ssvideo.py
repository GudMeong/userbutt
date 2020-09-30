# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import os

from telethon.tl.types import DocumentAttributeFilename
from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.ssvideo(?: |$)(.*)")
async def ssvideo(framecap):
    if not framecap.reply_to_msg_id:
        await framecap.edit("`Reply to any media..`")
        return
    reply_message = await framecap.get_reply_message()
    if not reply_message.media:
        await framecap.edit("`reply to a video..`")
        return
    try:
        frame = int(framecap.pattern_match.group(1))
        if frame > 10:
            return await framecap.edit("`hey..dont put that much`")
    except BaseException:
        return await framecap.edit("`Please input number of frame!`")
    if reply_message.photo:
        return await framecap.edit("`Hey..this is an image!`")
    if (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        return await framecap.edit("`Unsupported files..`")
    elif (
        DocumentAttributeFilename(file_name="sticker.webp")
        in reply_message.media.document.attributes
    ):
        return await framecap.edit("`Unsupported files..`")
    await framecap.edit("`Downloading media..`")
    ss = await bot.download_media(
        reply_message,
        "anu.mp4",
    )
    try:
        await framecap.edit("`Proccessing..`")
        command = f"vcsi -g {frame}x{frame} {ss} -o ss.png "
        os.system(command)
        await framecap.client.send_file(
            framecap.chat_id,
            "ss.png",
            reply_to=framecap.reply_to_msg_id,
        )
        await framecap.delete()
        os.system("rm -rf *.png")
        os.system("rm -rf *.mp4")
    except BaseException as e:
        os.system("rm -rf *.png")
        os.system("rm -rf *.mp4")
        return await framecap.edit(f"{e}")


CMD_HELP.update({
    "ssvideo":
    "`.ssvideo` <frame>"
    "\nUsage: to ss video frame per frame."
})
