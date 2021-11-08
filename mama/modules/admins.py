# Calls Music 1 - Telegram bot for streaming audio in group calls
# Copyright (C) 2021  Roj Serbest

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from asyncio import QueueEmpty

from pyrogram import Client, filters
from pyrogram.types import Message

from DaisyXMusic.function.admins import set
from DaisyXMusic.helpers.channelmusic import get_chat_id
from DaisyXMusic.helpers.decorators import authorized_users_only, errors
from DaisyXMusic.helpers.filters import command, other_filters
from DaisyXMusic.services.callsmusic import callsmusic
from DaisyXMusic.services.queues import queues
from DaisyXMusic.config import que


@Client.on_message(filters.command("adminreset"))
async def update_admin(client, message: Message):
    chat_id = get_chat_id(message.chat)
    set(
        chat_id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ Admin cache refreshed!")


@Client.on_message(command("dur") & other_filters)
@errors
@authorized_users_only
async def dur(_, message: Message):
    chat_id = get_chat_id(message.chat)
    (
      await message.reply_text("▶️ durdum la!")
    ) if (
        callsmusic.pause(chat_id)
    ) else (
        await message.reply_text("❗ OGLUM BİŞEY ÇALMIYOR LA!")
    )
        


@Client.on_message(command("devam") & other_filters)
@errors
@authorized_users_only
async def devam(_, message: Message):
    chat_id = get_chat_id(message.chat)
    (
        await message.reply_text("⏸DEVAM BEBEĞİM!")
    ) if (
        callsmusic.resume(chat_id)
    ) else (
        await message.reply_text("❗ OGLUM BİŞEY ÇALMIYOR LA!")
    )
        


@Client.on_message(command("son") & other_filters)
@errors
@authorized_users_only
async def son(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("❗ OGLUM BİŞEY ÇALMIYOR LA!")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        await callsmusic.stop(chat_id)
        await message.reply_text("❌ TAMAM LA DURDUK")


@Client.on_message(command("atla") & other_filters)
@errors
@authorized_users_only
async def atla(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("❗ GECİLECEK BİŞEY OLURSA SÖYLE YOKSA BOŞ YAPMA!")
    else:
        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await callsmusic.son(chat_id)
        else:
            await callsmusic.set_stream(chat_id, queues.get(chat_id)["file"])

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- ATLADIM **{skip[0]}**\n- ŞİMDİ ÇALIYOM **{qeue[0][0]}**")
    

@Client.on_message(command('sus') & other_filters)
@errors
@authorized_users_only
async def sus(_, message: Message):
    chat_id = get_chat_id(message.chat)
    result = await callsmusic.mute(chat_id)
    (
        await message.reply_text("✅ Muted")
    ) if (
        result == 0
    ) else (
        await message.reply_text("❌ sustum la")
    ) if (
        result == 1
    ) else (
        await message.reply_text("❌ konuşmadım ki")
    )

        
@Client.on_message(command('konuş') & other_filters)
@errors
@authorized_users_only
async def konuş(_, message: Message):
    chat_id = get_chat_id(message.chat)
    result = await callsmusic.unmute(chat_id)
    (
        await message.reply_text("✅ aferin")
    ) if (
        result == 0
    ) else (
        await message.reply_text("❌ konusamıyorum")
    ) if (
        result == 1
    ) else (
        await message.reply_text("❌ sesim çıkmıyor")
    )


@Client.on_message(filters.command("admincache"))
@errors
async def admincache(client, message: Message):
    set(
        message.chat.id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ Admin cache refreshed!")
