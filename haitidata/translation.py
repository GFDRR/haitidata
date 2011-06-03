from modeltranslation.translator import translator, TranslationOptions
from flatblocks.models import FlatBlock
from geonode.maps.models import Layer


class FlatBlockTO(TranslationOptions):
    fields = ('content',)


class LayerTO(TranslationOptions):
    fields = (
             'title',
             'edition',
             'abstract',
             'purpose',
             'constraints_other',
             'distribution_description',
             'data_quality_statement',
             'supplemental_information',
             )


translator.register(FlatBlock, FlatBlockTO)
translator.register(Layer, LayerTO)
