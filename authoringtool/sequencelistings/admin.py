from django.contrib import admin
from models import SequenceListing, Title, Sequence, Feature, Qualifier

# Register your models here.

class QualifierInline(admin.TabularInline):
    model = Qualifier
    extra = 1

# class FeatureInline(admin.StackedInline):
#     model = Feature
#     extra = 1

# class QualifierInline(admin.StackedInline):
#     model = Qualifier
#     extra = 1

class FeatureAdmin(admin.ModelAdmin):
    # fieldsets = [
#         ('File information',        {'fields': ['fileName', 'productionDate', 'dtdVersion', 'softwareName', 'softwareVersion'], 'classes': ['collapse']}),
#         ]
    inlines = [QualifierInline]
    list_display = ('sequence', 'featureKey', 'location',)

class TitleInline(admin.StackedInline):
    model = Title
    extra = 1

class SequenceInline(admin.StackedInline):
    model = Sequence
    extra = 1

class MyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('File information',        {'fields': ['fileName', 
                                                'productionDate', 
                                                'dtdVersion', 
                                                'softwareName', 
                                                'softwareVersion',
                                                'isEditable'
                                                ], 
                                     'classes': ['collapse']
                                     }), 
         ('General information',     {'fields': ['applicantFileReference',
                                                'IPOfficeCode',
                                                'applicationNumberText',
                                                'filingDate',
                                                'earliestPriorityIPOfficeCode',
                                                'earliestPriorityApplicationNumberText',
                                                'earliestPriorityFilingDate',
                                                'applicantName',
                                                'applicantNameLanguageCode',
                                                'applicantNameLatin',
                                                'inventorName',
                                                'inventorNameLanguageCode',
                                                'inventorNameLatin',
#                                                 'inventionTitle',
#                                                 'inventionTitleLanguageCode',
#                                                 'inventionTitleLatin',
                                                'sequenceTotalQuantity'
                                                ], 
                                      'classes': ['collapse']
                                      })
                 ]
    inlines = [TitleInline, SequenceInline]
    list_display = ('fileName', 
#                     'inventionTitle', 
                    'productionDate',)

admin.site.register(SequenceListing, MyAdmin)
admin.site.register(Feature, FeatureAdmin)
# admin.site.register(Qualifier, QualifierInline)