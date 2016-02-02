# Create your views here.

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.static import serve 
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

import util
import os


from forms import SequenceListingForm, TitleForm, SequenceForm, FeatureForm, QualifierForm, UserForm

from models import SequenceListing, Title, Sequence, Feature, Qualifier
from forms import MultipleFeatureForm
from django.utils.encoding import filepath_to_uri

detailTemplate = 'sequencelistings/detail.html'
# detailTemplate = 'sequencelistings/detail1.html'

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
        
    return render(request, detailTemplate, {'sequencelisting': sl})
@login_required 
def add_sequencelisting(request):
#     print 'add_sequencelisting invoked'
    if request.method == 'POST':
        form = SequenceListingForm(request.POST)
        title_form = TitleForm(request.POST)

        if form.is_valid() and title_form.is_valid():
            sl_instance = SequenceListing.objects.create(
            fileName = request.POST.get('fileName'),
            dtdVersion = '1',
            softwareName = 'prototype',
            softwareVersion = '0.1',
            productionDate = timezone.now(), #should be overwritten upon xml export
            
            applicantFileReference = request.POST.get('applicantFileReference'),
     
            IPOfficeCode = request.POST.get('IPOfficeCode'),
            applicationNumberText = request.POST.get('applicationNumberText'),
            filingDate = request.POST.get('filingDate'),
         
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

def add_title(request, pk):
#     print 'add_title invoked'
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
            
#     if request.method == 'POST':
         
 
#         if form.is_valid():
#             cd = form.cleaned_data
#             
#             fk = cd['featureKey']
#             fl = cd['location']
#             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
#             f.save()
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = FeatureForm(mt=seq.moltype)
    return render(request, 'sequencelistings/sequence.html', {'form': form, 'seq': seq, 
                                                              'featureFormDic': featureFormDic, 
                                                              'qualifierFormDic': qualifierFormDic,})
def add_multiple_feature(request, pk, spk):
    #     print 'add_multiple_feature invoked'
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
             
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(seq.sequenceListing.pk,)))
    else:
        form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
    return render(request, 'sequencelistings/add_multiple_feature.html', {'form': form})

# def add_multiple_feature(request, pk, spk):
#     #     print 'add_multiple_feature invoked'
#     seq = Sequence.objects.get(pk=spk)
#     if request.method == 'POST':
#         form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
#  
#         if form.is_valid():
#             cd = form.cleaned_data
#             
#             fk = cd['featureKey']
#             fl = cd['location']
#             qn = cd['qualifierName']
#             qv = cd['qualifierValue']
#             
#             locations = fl.split(',')
#             for l in locations:
#                 f = Feature.objects.create(sequence=seq, featureKey=fk, location=l)
#                 f.save()
#                 q = Qualifier.objects.create(feature=f, 
#                                              qualifierName = qn, 
#                                              qualifierValue = qv)
#                 q.save()
#              
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(seq.sequenceListing.pk,)))
#     else:
#         form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
#     return render(request, 'sequencelistings/add_multiple_feature.html', {'form': form})
    
def add_sequence(request, pk):
#     print 'add_sequence invoked'
    if request.method == 'POST':
        organism = request.POST.get('organism')
        form = SequenceForm(request.POST)

        if form.is_valid():
            sl = SequenceListing.objects.get(pk=pk)
            cd = form.cleaned_data
            
            sequence_instance = Sequence(sequenceListing = sl,
                length = len(cd['residues']),
                moltype = cd['moltype'],
                residues = cd['residues'] 
                )
            
            sequence_instance.save()
            
            value_for_source = 'source'
            if cd['moltype'] == 'AA':
                value_for_source = 'SOURCE'
                
            value_for_organism = 'organism'
            if cd['moltype'] == 'AA':
                value_for_organism = 'ORGANISM'
                
            value_for_moltype = 'mol_type'
            if cd['moltype'] == 'AA':
                value_for_moltype = 'MOL_TYPE'
            
            feature_instance = Feature.objects.create(sequence=sequence_instance, 
                                                      featureKey=value_for_source, 
                                                      location='1..%s' % sequence_instance.length)
            feature_instance.save()
            
            organism_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
                                                          qualifierName=value_for_organism, 
                                                          qualifierValue=organism)
            organism_qualifier_instance.save()
            
            mol_type_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
                                                          qualifierName=value_for_moltype, 
                                                          qualifierValue=util.MOL_TYPE_QUALIFIER_VALUES[cd['moltype']])
            mol_type_qualifier_instance.save()
            
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = SequenceForm()
    return render(request, 'sequencelistings/add_seq.html', {'form': form, 'pk': pk})

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
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = FeatureForm(mt=seq.moltype)
    return render(request, 'sequencelistings/add_feature.html', {'form': form})

def add_qualifier(request, pk, spk, fpk):
#     print 'add_qualifier invoked'
    f = Feature.objects.get(pk=fpk)
    if request.method == 'POST':
        form = QualifierForm(request.POST, feature=f)

        if form.is_valid():
            qn = request.POST.get('qualifierName')
            qv = request.POST.get('qualifierValue')
            q = Qualifier.objects.create(feature=f, qualifierName=qn, qualifierValue=qv)
            q.save()
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = QualifierForm(feature=f)
    return render(request, 'sequencelistings/add_qualifier.html', 
                  {'form': form, 
                   'pk': pk, 
                   'spk': spk, 
                   'fpk': fpk})

def generateXml(request, pk):
        sl = SequenceListing.objects.all().get(pk=pk)
        
        res = helper_generateXml(sl)
        
        return render(request, 'sequencelistings/xmloutput.html', 
                      {'filePath': res[1], 
                        'location': os.path.abspath(res[0]), 
                        'fileName': sl.fileName,
                        })
        
def helper_generateXml(sl):
        sl.productionDate = timezone.now()
        sl.save()
        sequences = sl.sequence_set.all()
     
        xml = render_to_string('xml_template.xml', {'sequenceListing': sl,
                                                    'sequences': sequences
                                                    }).encode('utf-8', 'strict')
 
        outf = os.path.join(util.PROJECT_DIRECTORY,
                            'sequencelistings',
                            'static',
                            'sequencelistings',
                            '%s.xml' % sl.fileName)

#         outf = os.path.join(util.PROJECT_DIRECTORY,
#                             'output_xml',
#                             '%s.xml' % sl.fileName)
         
        with open(outf, 'w') as gf:
            gf.write(xml) 
         
        xmlFilePath = 'sequencelistings/%s.xml' % sl.fileName
#         xmlFilePath = os.path.join(util.PROJECT_DIRECTORY, 'output_xml', '%s.xml' % sl.fileName)
         
#         return xmlFilePath
#         return sl.fileName 
        return (outf, xmlFilePath) 

@login_required
def render_xmlFile(request):
   # Take the user to the xml file.
#     return HttpResponseRedirect('sequencelistings/output_xml/%s/' % fileName)
    return HttpResponseRedirect('/sequencelistings/output_xml/')
#     return HttpResponse('test xml')

# def download(request, fileName):
#     dir = os.path.join(util.PROJECT_DIRECTORY, 
#                        'sequencelistings', 'static', 
#                        'sequencelistings')
#     return serve(request, '%s.xml' % fileName, dir)
# 
# def show_bare_xml(request, fileName):
#     filePath = dir = os.path.join(util.PROJECT_DIRECTORY, 
#                        'sequencelistings', 'static', 
#                        'sequencelistings', 
#                        '%s.xml' % fileName)
#     with open(filePath, 'r') as f:
#         s = f.read()
#         s = s.replace('<?xml-stylesheet type="text/xsl" href="st26.xsl"?>', '')
#         
#         return HttpResponse(s)
# def register(request):
# 
#     # A boolean value for telling the template whether the registration was successful.
#     # Set to False initially. Code changes value to True when registration succeeds.
#     registered = False
# 
#     # If it's a HTTP POST, we're interested in processing form data.
#     if request.method == 'POST':
#         # Attempt to grab information from the raw form information.
#         user_form = UserForm(data=request.POST)
#         
#         # If the form is valid...
#         if user_form.is_valid():
#             # Save the user's form data to the database.
#             user = user_form.save()
# 
#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()
# 
#             # Update our variable to tell the template registration was successful.
#             registered = True
# 
#         # Invalid form or forms - mistakes or something else?
#         # Print problems to the terminal.
#         # They'll also be shown to the user.
#         else:
#             print user_form.errors
# 
#     # Not a HTTP POST, so we render our form using two ModelForm instances.
#     # These forms will be blank, ready for user input.
#     else:
#         user_form = UserForm()
#         
#     # Render the template depending on the context.
#     return render(request,
#             'sequencelistings/register.html',
#             {'user_form': user_form, 'registered': registered} )
# 
# 
# def user_login(request):
# 
#     # If the request is a HTTP POST, try to pull out the relevant information.
#     if request.method == 'POST':
#         # Gather the username and password provided by the user.
#         # This information is obtained from the login form.
#                 # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
#                 # because the request.POST.get('<variable>') returns None, if the value does not exist,
#                 # while the request.POST['<variable>'] will raise key error exception
#         username = request.POST.get('username')
#         password = request.POST.get('password')
# 
#         # Use Django's machinery to attempt to see if the username/password
#         # combination is valid - a User object is returned if it is.
#         user = authenticate(username=username, password=password)
# 
#         # If we have a User object, the details are correct.
#         # If None (Python's way of representing the absence of a value), no user
#         # with matching credentials was found.
#         if user:
#             # Is the account active? It could have been disabled.
#             if user.is_active:
#                 # If the account is valid and active, we can log the user in.
#                 # We'll send the user back to the homepage.
#                 login(request, user)
#                 return HttpResponseRedirect('/sequencelistings/')
#             else:
#                 # An inactive account was used - no logging in!
#                 return HttpResponse("Your sequencelistings account is disabled.")
#         else:
#             # Bad login details were provided. So we can't log the user in.
#             print "Invalid login details: {0}, {1}".format(username, password)
#             return HttpResponse("Invalid login details supplied.")
# 
#     # The request is not a HTTP POST, so display the login form.
#     # This scenario would most likely be a HTTP GET.
#     else:
#         # No context variables to pass to the template system, hence the
#         # blank dictionary object...
#         return render(request, 'sequencelistings/login.html', {})
# 
# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)
# 
#     # Take the user back to the homepage.
#     return HttpResponseRedirect('/sequencelistings/')

@login_required
def restricted(request):
    return HttpResponse("This is a test page. You see this text because you're logged in.")

def about(request):
    return render_to_response('sequencelistings/about.html', {}, {})
#     return HttpResponse("This is a test for about page.")
    
# @login_required
# def render_xmlFile(request, fileName):
#    # Take the user to the xml file.
#     return HttpResponseRedirect('sequencelistings/output_xml/%s/' % fileName)
# #     return HttpResponseRedirect('/sequencelistings/')


# def add_feature(request, pk, spk):
#     seq = Sequence.objects.get(pk=spk)
#     
#     if request.method == 'POST':
#         form = FeatureForm(request.POST)
# 
#         if form.is_valid():
#             cd = form.cleaned_data
#             
#             fk = cd['featureKey']
#             fl = cd['location']
#             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
#             f.save()
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = FeatureForm()
#     return render(request, 'sequencelistings/add_feature.html', {'form': form})


# def sequence(request, pk, spk):
#     seq = Sequence.objects.get(pk=spk)
#     form = SequenceForm(instance=seq)
#     form.organism = seq.getOrganism()
#     featureFormList = []
#     for f in seq.feature_set.all():
#         featureFormList.append(FeatureForm(instance=f))
#         
# #     if request.method == 'POST':
#         
# 
# #         if form.is_valid():
# #             cd = form.cleaned_data
# #             
# #             fk = cd['featureKey']
# #             fl = cd['location']
# #             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
# #             f.save()
# #             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
# #     else:
# #         form = FeatureForm(mt=seq.moltype)
#     return render(request, 'sequencelistings/sequence.html', {'form': form, 'seq': seq, 
#                                                               'featureFormList': featureFormList})



# def edit_feature(request, fpk):
#     feature = get_object_or_404(Feature, id=fpk)
#     print feature
#     form = FeatureForm(request.POST or None, mt=feature.sequence.moltype, instance=feature)
#     print form
#     if form.is_valid():
#         form.save()
#         
#         return HttpResponseRedirect(reverse('sequencelistings:detail', 
#                                             args=(feature.sequence.sequenceListing.pk,)))
#     else:
#         form = FeatureForm(mt=feature.sequence.moltype)
#     return render(request, 'sequencelistings/edit_feature.html', {'form': form})




# def add_sequence(request, pk):
# #     print 'add_sequence invoked'
#     if request.method == 'POST':
#         organism = request.POST.get('organism')
#         form = SequenceForm(request.POST)
# 
#         if form.is_valid():
#             sl = SequenceListing.objects.get(pk=pk)
#             cd = form.cleaned_data
#             
#             sequence_instance = Sequence(sequenceListing = sl,
#                 length = len(cd['residues']),
#                 moltype = cd['moltype'],
#                 residues = cd['residues'] 
#                 )
#             
#             sequence_instance.save()
#             
#             
#             feature_instance = Feature.objects.create(sequence=sequence_instance, 
#                                                       featureKey='source', 
#                                                       location='1..%s' % sequence_instance.length)
#             feature_instance.save()
#             
#             organism_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
#                                                           qualifierName='organism', 
#                                                           qualifierValue=organism)
#             organism_qualifier_instance.save()
#             
#             mol_type_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
#                                                           qualifierName='mol_type', 
#                                                           qualifierValue=util.MOL_TYPE_QUALIFIER_VALUES[cd['moltype']])
#             mol_type_qualifier_instance.save()
#             
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = SequenceForm()
#     return render(request, 'sequencelistings/add_seq.html', {'form': form, 'pk': pk})


# def index(request): #good
#     sls = SequenceListing.objects.all()
#     print sls
#     return render(request, 'sequencelistings/index.html', {'sequencelistings': sls})
#  
# def detail(request, sequenceListing_id): #good
#     print 'detail invoked'
#     sl = get_object_or_404(SequenceListing, pk=sequenceListing_id)
#        
#     return render(request, 'sequencelistings/detail.html', {'sequencelisting': sl})
# def index(r):
#     return HttpResponse('Hello world. You are at the sequence listing index.')
   
# def detail(request, sequenceListing_id):
#     return HttpResponse("You're looking at poll %s." % sequenceListing_id)


# def add_feature(request, pk, spk): #good
#     print 'add_feature invoked'
#     seq = Sequence.objects.get(pk=spk)
#     print 'sequenceIdNo: ', seq.sequenceIdNo
#     print 'moltype: ', seq.moltype
#     
#     if request.method == 'POST':
#         form = FeatureForm(request.POST)
# #         assert False
#         if form.is_valid():
#             cd = form.cleaned_data
#             
#             fk = cd['featureKey']
#             fl = cd['location']
#             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
#             f.save()
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = FeatureForm()
#     return render(request, 'sequencelistings/add_feature.html', {'form': form})

# def add_feature(request, pk, spk):
#     print 'add_feature invoked'
# #     s = Sequence.objects.all().get(pk=int(spk))
#     if request.method == 'POST':
#         
#         form = FeatureForm(request.POST, s.moltype)
# 
#         if form.is_valid():
#             cd = form.cleaned_data
#             seq = Sequence.objects.get(pk=spk)
#             fk = cd['featureKey']
#             fl = cd['location']
# 
# #             fk = request.POST.get('featureKey')
# #             fl = request.POST.get('location')
#             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
#             f.save()
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = FeatureForm(s.moltype)
#     return render(request, 'sequencelistings/add_feature.html', {'form': form})
    # {% url 'sequencelistings:add_feature' %}
    
# def generateXml(request, pk):
# #     print 'generateXml invoked'
#     sl = SequenceListing.objects.all().get(pk=pk)
#     sl.productionDate = timezone.now()
#     sl.save()
#     o = 'sequencelistings/%s' % sl.generateXml()
#     location = os.path.abspath(o)
#     return render(request, 'sequencelistings/xmloutput.html', 
#                   {'outputfilepath': o, 
#                    'location': location})
# 
# def generateXml1(request, pk):
#         sl = SequenceListing.objects.all().get(pk=pk)
#         sl.productionDate = timezone.now()
#         sl.save()
#         sequences = sl.sequence_set.all()
#     
#         xml = render_to_string('xml_template.xml', {'sequenceListing': sl,
#                                                     'sequences': sequences
#                                                     })
# 
#         outf = os.path.join(util.PROJECT_DIRECTORY,
#                             'sequencelistings',
#                             'static',
#                             'sequencelistings',
#                             'generated1_%s.xml' % sl.fileName)
#         
#         with open(outf, 'w') as gf:
#             gf.write(xml) 
#         
#         o = 'sequencelistings/generated1_%s.xml' % sl.fileName
#         
#         location = os.path.abspath(o)
#         return render(request, 'sequencelistings/xmloutput.html', 
#                       {'outputfilepath': o, 
#                        'location': location})