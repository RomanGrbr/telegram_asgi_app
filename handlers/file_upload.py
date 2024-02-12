from core.handler import PhotoHandler


async def get_photo(update, context):
    print(f'Фотографии: {[photo.file_id for photo in update.message.photo]}')
    # await update.reply_text(text=f'Привет {name}')


get_photo_handler = PhotoHandler(callback=get_photo)
