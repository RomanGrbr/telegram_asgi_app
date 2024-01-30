class BaseFromChat:
    """Base class for Chat and From.
    Get dict, return attr.
    """

    __slots__ = 'id', 'first_name', 'last_name', 'username'

    def __init__(self, data: dict) -> None:
        self.id: int = data.get('id')
        self.first_name: str = data.get('first_name')
        self.last_name: str = data.get('last_name')
        self.username: str = data.get('username')


class From(BaseFromChat):
    """Class for form.
    Get dict, return attr.
    """

    __slots__ = 'is_bot', 'language_code'

    def __init__(self, mess_from: dict) -> None:
        super().__init__(mess_from)
        self.is_bot: bool = mess_from.get('is_bot')
        self.language_code: str = mess_from.get('language_code')


class Chat(BaseFromChat):
    """Class for chat.
    Get dict, return attr.
    """

    __slots__ = 'type'

    def __init__(self, chat: dict) -> None:
        super().__init__(chat)
        self.type: str = chat.get('type')


class BaseFile:
    __slots__ = 'file_id', 'file_unique_id', 'file_size'

    def __init__(self, data: dict) -> None:
        self.file_id: str = data.get('file_id')
        self.file_unique_id: str = data.get('file_unique_id')
        self.file_size: int = data.get('file_size')


class Photo(BaseFile):
    __slots__ = 'width', 'height'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.width: int = data.get('width')
        self.height: int = data.get('height')


class Document(BaseFile):
    __slots__ = 'file_name', 'mime_type'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.mime_type: str = data.get('mime_type')
        self.file_name: str = data.get('file_name')


class Voice(BaseFile):
    __slots__ = 'duration', 'mime_type'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.mime_type: str = data.get('mime_type')
        self.duration: str = data.get('duration')


class Audio(Voice):
    __slots__ = 'title', 'performer'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.title: str = data.get('title')
        self.performer: str = data.get('performer')


class Location:
    __slots__ = 'latitude', 'longitude'

    def __init__(self, data: dict) -> None:
        self.latitude: int = data.get('latitude')
        self.longitude: int = data.get('longitude')


class PollOptions:
    __slots__ = 'text', 'voter_count'

    def __init__(self, data: dict) -> None:
        self.text: str = data.get('text')
        self.voter_count: int = data.get('voter_count')


class Poll:
    __slots__ = (
        'id', 'question', 'options', 'total_voter_count', 'is_closed',
        'is_anonymous', 'type', 'allows_multiple_answers'
    )

    def __init__(self, data) -> None:
        self.id: str = data.get('id')
        self.question: str = data.get('question')
        self.options: list[PollOptions] = [
            PollOptions(option) for option in data.get('options')
        ]
        self.total_voter_count: int = data.get('total_voter_count')
        self.is_closed: bool = data.get('is_closed')
        self.is_anonymous: bool = data.get('is_anonymous')
        self.type: str = data.get('type')
        self.allows_multiple_answers: bool = data.get('allows_multiple_answers')


class Contact:
    __slots__ = 'phone_number', 'first_name', 'vcard'

    def __init__(self, data) -> None:
        self.phone_number: str = data.get('phone_number')
        self.first_name: str = data.get('first_name')
        self.vcard: str = data.get('vcard')


class BaseMessage:
    """Class for message.
    Get dict, return attr.
    """

    __slots__ = 'message_id', 'mess_from', 'chat', 'date'

    def __init__(self, message: dict) -> None:
        self.message_id: int = message.get('message_id')
        self.mess_from: From = From(message.get('from'))
        self.chat: Chat = Chat(message.get('chat'))
        self.date: int = message.get('date')


class Message(BaseMessage):
    __slots__ = 'text'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.text: str = data.get('text')


class PhotoMessage(BaseMessage):
    __slots__ = 'photo'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.photo: list[Photo] = [Photo(photo) for photo in data.get('photo')]


class DocumentMessage(BaseMessage):
    __slots__ = 'document'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.document: Document = Document(data.get('document'))


class VoiceMessage(BaseMessage):
    __slots__ = 'voice'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.voice: Voice = Voice(data.get('voice'))


class LocationMessage(BaseMessage):
    __slots__ = 'location'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.location: Location = Location(data.get('location'))


class PollMessage(BaseMessage):
    __slots__ = 'poll'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.poll: Poll = Poll(data.get('poll'))


class ContactMessage(BaseMessage):
    __slots__ = 'contact'

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.contact: Contact = Contact(data.get('contact'))


class AudioMessage(BaseMessage):
    __slots__ = 'caption', 'audio'

    def __init__(self, data) -> None:
        super().__init__(data)
        self.caption: str = data.get('caption')
        self.audio: Audio = Audio(data.get('audio'))


class ReplyKeyboard(Message):
    pass

# class CallbackQuery:
#     __slots__ = 'id'
#
#     def __init__(self, callback_query: dict) -> None:
#         self.id = callback_query.get('id')
