# -*- coding: utf-8 -*-
import logging
import discord
from commands import commandregex, commands
from event_manager import event_manager


class Client(discord.Client):
    def __init__(self):
        super(Client, self)
        self.channel_whitelist = []

main_client = discord.Client()

@main_client.event
def on_ready():
    print('Connected!')
    print('Username: ' + main_client.user.name)
    print('ID: ' + main_client.user.id)
    logging.info("Connected to Discord as %s (ID: %s)", main_client.user.name, main_client.user.id)


@main_client.event
def on_message(message):
    if message.content[0] == "!":
        if len(main_client.channel_whitelist) > 0 and message.channel.id not in main_client.channel_whitelist:
            return

        logging.info("#%s (%s) : %s", message.channel.name, message.author.name, message.content)
        event_manager.handle_message(main_client)
        cmdline = commandregex.search(message.content.lower())
        logging.debug("Command : %s(%s)", cmdline.group('command'), cmdline.group('args'))
        msg = commands[cmdline.group('command')](message, cmdline.group('args'))
        if msg is not None:
            main_client.send_message(message.channel, msg)