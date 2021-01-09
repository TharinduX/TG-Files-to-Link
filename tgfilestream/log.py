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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import requests
from logging import Handler, Formatter
import logging
import datetime
from .config import log_config, debug


TELEGRAM_TOKEN = '1078276956:AAGfyOjbH3WpaxcRDaoEpQTct9up2lVC22U'
TELEGRAM_CHAT_ID = '-447499775'


class RequestsHandler(Handler):
	def emit(self, record):
		log_entry = self.format(record)
		payload = {
			'chat_id': TELEGRAM_CHAT_ID,
			'text': log_entry,
			'parse_mode': 'HTML'
		}
		return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN),
							 data=payload).content


class LogstashFormatter(Formatter):
	def __init__(self):
		super(LogstashFormatter, self).__init__()

	def format(self, record):
		t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

		return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)


def main():

 if log_config:
    logging.basicConfig(filename=log_config)
 else:
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    logging.getLogger("telethon").setLevel(logging.INFO if debug else logging.ERROR)

 log = logging.getLogger("tgfilestream")

	handler = RequestsHandler()
	formatter = LogstashFormatter()
	handler.setFormatter(formatter)
	logging.addHandler(handler)


if __name__ == '__main__':
	main()


# import logging
