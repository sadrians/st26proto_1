
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

import util
import os

from forms import SequenceListingForm, TitleForm, SequenceForm, FeatureForm, QualifierForm, EditFeatureForm

from models import SequenceListing, Title, Sequence, Feature, Qualifier
from forms import MultipleFeatureForm
from django.utils.encoding import filepath_to_uri

import logging 

logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = 'sequencelistings/index.html'
    context_object_name = 'sequencelistings'
  
    def get_queryset(self):
        """Return all sequence listings."""
        
        return SequenceListing.objects.all()

# class DetailView(generic.DetailView):
#     model = SequenceListing
#     template_name = 'sequencelistings/detail.html'

def detail(request, pk): #good
    sl = get_object_or_404(SequenceListing, pk=pk)
        
    return render(request, 'sequencelistings/detail_w3.html', {'sequencelisting': sl})

# TODO: is this needed?

def edit_sequence_data(request, pk): #good
    sl = get_object_or_404(SequenceListing, pk=pk)
        
    return render(request, 'sequencelistings/edit_sequence_data_w3.html', {'sequencelisting': sl})

@login_required 
def add_sequencelisting(request):
    if request.method == 'POST':
        form = SequenceListingForm(request.POST)
        title_form = TitleForm(request.POST)

        if form.is_valid() and title_form.is_valid():
            filingDateFromForm = request.POST.get('filingDate')
#             set to None bc the model does not handle properly empty string from form
            fd = filingDateFromForm if filingDateFromForm else None
            
            sl_instance = SequenceListing.objects.create(
            fileName = request.POST.get('fileName'),
            dtdVersion = '1',
            softwareName = 'prototype',
            softwareVersion = '0.1',
            productionDate = timezone.now(), #should be overwritten upon xml export
            
            applicantFileReference = request.POST.get('applicantFileReference'),
     
            IPOfficeCode = request.POST.get('IPOfficeCode'),
            applicationNumberText = request.POST.get('applicationNumberText'),
#             filingDate = request.POST.get('filingDate'),
            filingDate = fd,
            
            earliestPriorityIPOfficeCode = request.POST.get('earliestPriorityIPOfficeCode'),
            earliestPriorityApplicationNumberText = request.POST.get('earliestPriorityApplicationNumberText'),
            earliestPriorityFilingDate = request.POST.get('earliestPriorityFilingDate'),
         
            applicantName = request.POST.get('applicantName'),
            applicantNameLanguageCode = request.POST.get('applicantNameLanguageCode'),
            applicantNameLatin = request.POST.get('applicantNameLatin'),
         
            inventorName = request.POST.get('inventorName'),
            inventorNameLanguageCode = request.POST.get('inventorNameLanguageCode'),
            inventorNameLatin = request.POST.get('inventorNameLatin'),
            )
            
            sl_instance.save()
            
            tcd = title_form.cleaned_data
            title_instance = Title(sequenceListing = sl_instance,
                inventionTitle = tcd['inventionTitle'],
                inventionTitleLanguageCode = tcd['inventionTitleLanguageCode']
                )
            
            title_instance.save()
            
            return HttpResponseRedirect(reverse('sequencelistings:detail', 
                                                args=(sl_instance.pk,)))
    else:
        form = SequenceListingForm()
        title_form = TitleForm()
        
    return render(request, 'sequencelistings/add_sequencelisting.html', 
                  {'form': form, 'title_form': title_form})

# TODO: is this needed?

def add_title(request, pk):
    if request.method == 'POST':
        form = TitleForm(request.POST)

        if form.is_valid():
            sl = SequenceListing.objects.get(pk=pk)
            cd = form.cleaned_data
            
            title_instance = Title(sequenceListing = sl,
                inventionTitle = cd['inventionTitle'].encode('utf-8'),
                inventionTitleLanguageCode = cd['inventionTitleLanguageCode']
                )
            title_instance.save()
            
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = TitleForm()
    return render(request, 'sequencelistings/add_title.html', {'form': form, 'pk': pk})

# TODO: is this view used actually?
def sequence(request, pk, spk):
    seq = Sequence.objects.get(pk=spk)
    form = SequenceForm(instance=seq, initial={'organism': seq.getOrganism()})
    form.organism = seq.getOrganism()
    featureFormDic = {}
    qualifierFormDic = {}
    for f in seq.feature_set.all():
        featureFormDic[f] = FeatureForm(instance=f, mt=seq.moltype, initial={'featureKey': f.featureKey})

        qualifierFormList = []
        for q in f.qualifier_set.all():
            qualifierFormList.append(QualifierForm(feature=f, 
                                                   instance=q, 
                                                   initial={'qualifierName': q.qualifierName}))

        qualifierFormDic[f] = qualifierFormList
            
    return render(request, 'sequencelistings/sequence.html', {'form': form, 'seq': seq, 
                                                              'featureFormDic': featureFormDic, 
                                                              'qualifierFormDic': qualifierFormDic,})

def add_multiple_feature(request, pk, spk):
    seq = Sequence.objects.get(pk=spk)
    if request.method == 'POST':
        form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
 
        if form.is_valid():
            cd = form.cleaned_data
            
            fk = cd['featureKey']
            fl = cd['location']
            qn = cd['qualifierName']
            qv = cd['qualifierValue']
            
            if 'ra' in fl:
                locations = util.rangeFromString(fl) 
            else:
                locations = fl.split(',')
            for l in locations:
                f = Feature.objects.create(sequence=seq, featureKey=fk, location=l)
                f.save()
                q = Qualifier.objects.create(feature=f, 
                                             qualifierName = qn, 
                                             qualifierValue = qv)
                q.save()
             
            return HttpResponseRedirect(reverse('sequencelistings:edit_sequence_data', args=(seq.sequenceListing.pk,)))
    else:
        form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
    return render(request, 'sequencelistings/add_multiple_feature.html', {'form': form, 'seq': seq})

def add_sequence(request, pk):
    sl = SequenceListing.objects.get(pk=pk)
    if request.method == 'POST':
        organism = request.POST.get('organism')
        form = SequenceForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            raw_residues = cd['residues']
            
            sequence_instance = Sequence(sequenceListing = sl,
                length = len(cd['residues']),
                moltype = cd['moltype'],
                residues = cd['residues'] 
                )
            
            sequence_instance.save()
            feature_source_helper(sequence_instance, organism)
#             create a note qualifier to indicate the a formula if applicable
            if '(' in raw_residues:
                value_for_note = 'note'
                if cd['moltype'] == 'AA':
                    value_for_note = 'NOTE'
                
                feature_instance = Feature.objects.filter(sequence = sequence_instance)[0]
                note_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
                                                          qualifierName=value_for_note, 
                                                          qualifierValue=raw_residues)
                note_qualifier_instance.save()
            
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = SequenceForm()
    return render(request, 'sequencelistings/add_seq.html', {'form': form, 'pk': pk, 'seql': sl})

def feature_source_helper(seq, organism):
    '''
    Create automatically feature source for a given sequence and organism.
    '''
    value_for_source = 'source'
    value_for_organism = 'organism'
    value_for_moltype = 'mol_type'
    
    molType = seq.moltype
    
    if molType == 'AA':
        value_for_source = 'SOURCE'
        value_for_organism = 'ORGANISM'
        value_for_moltype = 'MOL_TYPE'
    
    feature_instance = Feature.objects.create(sequence=seq, 
                                              featureKey=value_for_source, 
                                              location='1..%s' % seq.length)
    feature_instance.save()
    
    organism_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
                                                  qualifierName=value_for_organism, 
                                                  qualifierValue=organism)
    organism_qualifier_instance.save()
    
    mol_type_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
                                                  qualifierName=value_for_moltype, 
                                                  qualifierValue=util.MOL_TYPE_QUALIFIER_VALUES[molType])
    mol_type_qualifier_instance.save()

def add_feature(request, pk, spk):
    seq = Sequence.objects.get(pk=spk)
     
    if request.method == 'POST':
        form = FeatureForm(request.POST, mt=seq.moltype)
 
        if form.is_valid():
            cd = form.cleaned_data
             
            fk = cd['featureKey']
            fl = cd['location']
            f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
            f.save()
            return HttpResponseRedirect(reverse('sequencelistings:edit_sequence_data', args=(pk,)))
    else:
        form = FeatureForm(mt=seq.moltype)
    return render(request, 'sequencelistings/add_feature.html', {'form': form, 'seq': seq})

def edit_feature(request, pk, spk, fpk):
    seq = Sequence.objects.get(pk=spk)
    f = Feature.objects.all().get(pk=fpk)
    
    featureForm = FeatureForm(instance=f, mt=seq.moltype, initial={'featureKey': f.featureKey})

    if request.method == 'POST':
        form = FeatureForm(request.POST, mt=seq.moltype)
  
        if form.is_valid():
            cd = form.cleaned_data
              
            f.featureKey = cd['featureKey']
            f.location = cd['location']
            f.save()
            return HttpResponseRedirect(reverse('sequencelistings:edit_sequence_data', args=(pk,)))
    else:
        form = FeatureForm(mt=seq.moltype)
    return render(request, 'sequencelistings/edit_feature.html', {'form': featureForm, 'seq': seq})

def add_qualifier(request, pk, spk, fpk):
    f = Feature.objects.get(pk=fpk)
    if request.method == 'POST':
        form = QualifierForm(request.POST, feature=f)

        if form.is_valid():
            qn = request.POST.get('qualifierName')
            qv = request.POST.get('qualifierValue')
            q = Qualifier.objects.create(feature=f, qualifierName=qn, qualifierValue=qv)
            q.save()
            return HttpResponseRedirect(reverse('sequencelistings:edit_sequence_data', args=(pk, )))

    else:
        form = QualifierForm(feature=f)
    return render(request, 'sequencelistings/add_qualifier.html', 
                  {'form': form, 
                   'pk': pk, 
                   'spk': spk, 
                   'fpk': fpk, 
                   'feature': f})

def generateXml(request, pk):
        sl = SequenceListing.objects.all().get(pk=pk)
        sl.productionDate = timezone.now()
        sl.save()
        
#         generate xml and write it to file system
        util.helper_generateXml(sl)
        
        xmlFilePath = 'sequencelistings/output/%s.xml' % sl.fileName
        
        logger.info('Generated xml seql at %s.' %xmlFilePath)
        
        return render(request, 'sequencelistings/xmloutput.html', 
                      {'filePath': xmlFilePath, 
                        'location': util.OUTPUT_DIR, 
                        'fileName': sl.fileName,
                        }) 
#         this version of xml root uses xsd schema file
#         <!-- <ST26SequenceListing dtdVersion="{{sequenceListing.dtdVersion}}" 
#                     fileName="{{sequenceListing.fileName}}"
#                     softwareName="{{sequenceListing.softwareName}}" 
#                     softwareVersion="{{sequenceListing.softwareVersion}}"
#                     productionDate="{{sequenceListing.productionDate}}"
#                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#                     xsi:noNamespaceSchemaLocation="st26.xsd"> -->
        
@login_required
def render_xmlFile(request):
#     Take the user to the xml file.
    return HttpResponseRedirect('/sequencelistings/output_xml/')

# TODO: refactor first line of this function ...
# TODO: TEST IT!!!
def download(request, fileName):
    s = '%s has not been found.' % fileName 
    filePath = os.path.join(util.PROJECT_DIRECTORY, 'sequencelistings', 'static', 'sequencelistings', 'output', '%s.xml' % fileName)
    with open(filePath, 'r') as f:
        s = f.read()
    response = HttpResponse(s, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; '
    
    return response 

@login_required
def restricted(request):
    return HttpResponse("This is a test page. You see this text because you're logged in.")

def about(request):
    return render_to_response('sequencelistings/about.html', {}, {})

