# mamaklimusic - Telegram bot for streaming audio in group calls
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
from DaisyXMusic.helpers.decorators import authorized_users_only, errors
from DaisyXMusic.services.callsmusic import callsmusic
from DaisyXMusic.services.queues import queues
from DaisyXMusic.config import que


@Client.on_message(
    filters.command(["kanaldur", "kdur"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def dur(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("sohbet bağlantılı mı")
        return
    chat_id = chid
    (
        await message.reply_text("▶️ durdum!")
    ) if (
        callsmusic.pause(chat_id)
    ) else (
        await message.reply_text("❗ BİŞEY ÇALMYOR OGLUM MALMISIN!")
    )


@Client.on_message(
    filters.command(["kanaldevam", "kdevam"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def devam(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("bağlımısın?")
        return
    chat_id = chid
    (
       await message.reply_text("⏸ devaaaaamkeeee!")
    ) if (
        callsmusic.resume(chat_id)
    ) else (
        await message.reply_text("❗ mal çalmıyor bişi!")
    )
        
    

@Client.on_message(
    filters.command(["kanalson", "kson"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def bitir(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("bağlı mısın ki")
        return
    chat_id = chid
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("❗ duramam çok hızlandım!")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        await callsmusic.stop(chat_id)
        await message.reply_text("❌durdum ya la!")


@Client.on_message(
    filters.command(["kanalatla", "katla"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def atla(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("baglı mısın")
        return
    chat_id = chid
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("❗ neyi atlayım la mal!")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            await callsmusic.stop(chat_id)
        else:
            await callsmusic.set_stream(chat_id, queues.get(chat_id)["file"])

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- atladım pu sana **{skip[0]}**\n- şimdi çalıyom **{qeue[0][0]}**")
    
    
@Client.on_message(
    filters.command(["kanalsus", "ksus"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def sus(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("baglı mısın")
        return 
    chat_id = chid
    result = await callsmusic.mute(chat_id)
    (
        await message.reply_text("✅ sustum")
    ) if (
        result == 0
    ) else (
        await message.reply_text("❌ susamam")
    ) if (
        result == 1
    ) else (
        await message.reply_text("❌ konuşmuyorum ki")
    )
        
        
@Client.on_message(
    filters.command(["kanalkonuş", "kkonuş"]) & filters.group & ~filters.edited
)
@errors
@authorized_users_only
async def konuş(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("baglı mısın")
        return 
    chat_id = chid
    result = await callsmusic.unmute(chat_id)
    (
        await message.reply_text("✅ aferin")
    ) if (
        result == 0
    ) else (
        await message.reply_text("❌ beceremedin mal")
    ) if (
        result == 1
    ) else (
        await message.reply_text("❌ gerizekalı")
    )


@Client.on_message(filters.command("channeladmincache"))
@errors
async def admincache(client, message: Message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("Is chat even linked")
        return
    set(
        chid,
        [
            member.user
            for member in await conchat.linked_chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ Admin cache refreshed!")
