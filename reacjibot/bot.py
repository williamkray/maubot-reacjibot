from typing import Awaitable, Type, Optional, Tuple
import emoji
import json
import re
import time
import random
import urllib.parse

from mautrix.client import Client
from mautrix.types import (Event, MessageType, EventID, UserID, FileInfo, EventType, RoomID,
                            MediaMessageEventContent, TextMessageEventContent, ContentURI,
                            ReactionEvent, RedactionEvent, ImageInfo, RelationType)
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command, event

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("restrict_users")
        helper.copy("allowed_users")
        helper.copy("mapping")

class ReacjiBot(Plugin):
    async def start(self) -> None:
        self.config.load_and_update()

    @command.passive(regex=re.compile(r"[^A-Za-z0-9]"), field=lambda evt: evt.content.relates_to.key, event_type=EventType.REACTION, msgtypes=None)
    async def generic_react(self, evt: ReactionEvent, key: Tuple[str]) -> None:
        print(self.config["mapping"], file=sys.stderr)
        reacjis = {"train":"public_transportation"}
        source_evt = await self.client.get_event(evt.room_id, evt.content.relates_to.event_id)
        symbol = evt.content.relates_to.key
        for key in reacjis:
           if re.match(emoji.emojize(":"+key+":"),symbol):
              message = evt.sender + ": " + source_evt.content.body + ' [' + emoji.emojize(":"+key+":") + '](' + 'https://matrix.to/#/' + evt.room_id + '/' + evt.content.relates_to.event_id + '?via=' + self.config["domain"] + ')'
              target = await self.client.resolve_room_alias('#' + reacjis[key] + ':' + self.config["domain"])
              target_id = target.room_id
              await self.client.send_markdown(target_id,message)

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config