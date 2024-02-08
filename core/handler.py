class Handler:

    def __init__(self, callback, command: str = ''):
        self.callback = callback
        self.command = self._add_command(command)

    def respond(self, update):
        return True

    async def get_callback(self, update, context):
        await self.callback(update, context)

    def _add_command(self, command):
        return command


class MessageAnyHandler(Handler):
    pass


class MessageStrongHandler(Handler):

    def respond(self, update):
        if update.message.text == self.command:
            return True
        else:
            return False


class CommandHandler(MessageStrongHandler):

    def _add_command(self, command):
        if command.startswith('/'):
            return command
        return f'/{command}'
