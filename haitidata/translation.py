from modeltranslation.translator import translator, TranslationOptions
from flatblocks.models import FlatBlock
from django.contrib.flatpages.models import FlatPage

class FlatBlockTO(TranslationOptions):
    fields = ('content',)

class FlatPageTO(TranslationOptions):
    fields = ('title', 'content')

translator.register(FlatBlock, FlatBlockTO)
translator.register(FlatPage, FlatPageTO)
