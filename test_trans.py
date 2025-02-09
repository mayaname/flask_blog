# Test of the Google Translate API

import asyncio
from googletrans import Translator

src_lang = 'en'
dest_lang = 'de'
trans_text = 'Configure the PythonAnywhere WSGI file'

async def translate_text(text, src, dest):

    translator = Translator()
    translated = await translator.translate(text=text, src=src, dest=dest)
    
    print(translated.text)

# Run the async function
asyncio.run(translate_text(text=trans_text, src=src_lang, dest=dest_lang))
