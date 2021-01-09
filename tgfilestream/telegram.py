# tgfilestream - A Telegram bot that can stream Telegram files to users over HTTP.
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.'
import logging
import requests

from telethon import TelegramClient, Button, events
from telethon.sessions import StringSession

from .paralleltransfer import ParallelTransferrer
from .config import (
    session_name,
    api_id,
    api_hash,
    public_url,
    start_message,
    group_chat_message
)
from .util import pack_id, get_file_name, get_file_size, convert_size, get_file_type, get_duration, convert_time

log = logging.getLogger(__name__)

client = TelegramClient(StringSession(session_name), api_id, api_hash)
transfer = ParallelTransferrer(client)
api_key = "01300e2c9748234447e8bf581c6e012b20c35"

@client.on(events.NewMessage)
async def handle_message(evt: events.NewMessage.Event) -> None:
    if not evt.is_private:
        await evt.reply(group_chat_message)
        return
    if not evt.file:
        await evt.reply(start_message)
        return

    url = public_url / str(pack_id(evt)) / (get_file_name(evt))
    file_name = (get_file_name(evt))
    # file_size = (get_file_size(evt))
    file_size = convert_size(get_file_size(evt))
    file_type = get_file_type(evt)
    duration = convert_time(get_duration(evt))
    # [{file_name}]({url})")


    api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
    data = requests.get(api_url).json()["url"]
    if data["status"] == 7:
    shortened_url = data["shortLink"]
    await evt.reply(f"📋 **File name :** ```{file_name}```\n\n⚖️ **File size :** ```{file_size}```\n📂 **File type :** ```{file_type}```\n\n**If you send PORN You will be BANNED!!**\n**Join to our Telegram Channel** @MovieSquad\n\n", 
    buttons = [
        [Button.url('🔗 Download Link', f"{shortened_url}")],
        [Button.url('📝 Contact Me', 'https://t.me/TharinduX')],
        [Button.url('🎬 MovieSquad', 'https://t.me/MovieSquad')]
    ])

    else:
    await evt.reply(f"📋 **File name :** ```{file_name}```\n\n⚖️ **File size :** ```{file_size}```\n📂 **File type :** ```{file_type}```\n\n**If you send PORN You will be BANNED!!**\n**Join to our Telegram Channel** @MovieSquad\n\n", 
    buttons = [
        [Button.url('🔗 Download Link', f"{url}")],
        [Button.url('📝 Contact Me', 'https://t.me/TharinduX')],
        [Button.url('🎬 MovieSquad', 'https://t.me/MovieSquad')]
    ])


    log.info(
        f"Replied with link for {evt.id} to {evt.from_id} in {evt.chat_id}")
    log.debug(f"Link to {evt.id} in {evt.chat_id}: {url}")
