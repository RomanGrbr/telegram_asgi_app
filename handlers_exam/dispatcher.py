from .comands import buttons_handler, start_handler, inline_handler
from .messages import (any_message_handler, strong_message_handler,
                       lower_message_handler, regex_message_handler)
from .file_upload import (get_photo_handler, get_document_handler,
                          get_voice_handler, get_audio_handler)


def setup_dispatcher(dp):
    """Добавляет хендлеры вызывающие соответствующие функции в обработку."""
    dp.add_handler(buttons_handler)
    dp.add_handler(start_handler)
    dp.add_handler(inline_handler)

    dp.add_handler(strong_message_handler)
    dp.add_handler(lower_message_handler)
    dp.add_handler(regex_message_handler)

    dp.add_handler(get_photo_handler)
    dp.add_handler(get_document_handler)
    dp.add_handler(get_voice_handler)
    dp.add_handler(get_audio_handler)

    dp.add_handler(any_message_handler)
