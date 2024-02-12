from core.handler import PhotoHandler


async def get_photo(update, context):
    files = [photo.file_id for photo in update.message.photo]
    print(f'Фотографии: {files}')
    # await update.bot.get_file(files[0])


get_photo_handler = PhotoHandler(
    callback=get_photo, receive=True, path='photo')
