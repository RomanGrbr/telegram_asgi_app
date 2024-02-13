from core.handler import (PhotoHandler, DocumentHandler, VoiceHandler,
                          AudioHandler)


async def get_photo(update, context):
    files = [photo for photo in update.message.files]
    print(f'Фотографии: {files}')
    # await update.bot.get_file(files[0])


async def get_document(update, context):
    files = update.message.files
    print(f'Документы: {files}')
    # await update.bot.get_file(files[0])


async def get_voice(update, context):
    files = update.message.files
    print(f'Голос: {files}')
    # await update.bot.get_file(files[0])


async def get_audio(update, context):
    files = update.message.files
    print(f'Музыка: {files}')
    # await update.bot.get_file(files[0])


get_photo_handler = PhotoHandler(
    callback=get_photo, receive=True, path='photo')
get_document_handler = DocumentHandler(
    callback=get_document, receive=True, path='document')
get_voice_handler = VoiceHandler(
    callback=get_voice, receive=True, path='voice')
get_audio_handler = AudioHandler(
    callback=get_audio, receive=True, path='audio')
