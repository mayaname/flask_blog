"""
Program: Trans
Author: Maya Name
Creation Date: 02/08/2024
Revision Date: 
Description: Translations using Google Translate API

Revisions:

"""

from .extensions import translator


async def translate_text(text:str, src:str, dest:str) -> str:
    """
    Description: Asynchronous  wrapper for Google Translate API
    Param: text - Text to be translated
    Param: src - Language code of source text
    Param: desc - Language code of destination text
    Return: Translated text
    """

    translated = await translator.translate(text=text, src=src, dest=dest)
    
    return translated.text