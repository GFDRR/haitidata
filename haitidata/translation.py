from modeltranslation.translator import translator, TranslationOptions
from flatblocks.models import FlatBlock

class FlatBlockTO(TranslationOptions):
    fields = ('content',)

translator.register(FlatBlock, FlatBlockTO)
