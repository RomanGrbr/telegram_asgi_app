from typing import Sequence, Union, List


class KeyboardButton:
    __slots__ = 'text', 'request_contact', 'request_location'

    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location

    def to_dict(self):
        data = {}
        for key in self.__slots__:
            value = getattr(self, key, None)
            if value is not None:
                data[key] = value
        return data


class InlineKeyboardButton:
    __slots__ = (
        'text',
        'url',
        'callback_data',
        'callback_game',
        'switch_inline_query',
        'switch_inline_query_current_chat',
    )

    def __init__(
            self,
            text: str,
            url: str = None,
            callback_data: object = None,
            switch_inline_query: str = None,
            switch_inline_query_current_chat: str = None,
            callback_game=None
    ):
        self.text = text
        self.url = url
        self.callback_data = callback_data
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game


class ReplyKeyboardMarkup:
    def __init__(
            self,
            keyboard: Sequence[Sequence[Union[str, KeyboardButton]]],
            resize_keyboard: bool = False,
            one_time_keyboard: bool = False,
            selective: bool = False,
    ):
        self.keyboard = keyboard
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective
        self.keyboard = []
        for row in keyboard:
            button_row = []
            for button in row:
                if isinstance(button, KeyboardButton):
                    button_row.append(button.to_dict())
                else:
                    button_row.append(KeyboardButton(button))
            self.keyboard.append(button_row)


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: List[List[InlineKeyboardButton]]):
        self.inline_keyboard = inline_keyboard

    # def to_dict(self) -> JSONDict:
    #     """See :meth:`telegram.TelegramObject.to_dict`."""
    #     data = super().to_dict()
    #
    #     data['inline_keyboard'] = []
    #     for inline_keyboard in self.inline_keyboard:
    #         data['inline_keyboard'].append([x.to_dict() for x in inline_keyboard])
    #
    #     return data
