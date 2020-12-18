import json
from django import forms
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView,TemplateView,FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressApp.models import Ponencia,RelPonenciaPonente,Ubicacion,Congreso,Bloque,Ponente
from MedCongressAdmin.forms.congres_forms import PonenciaForms,PonentePonenciaForm
from django.utils.crypto import get_random_string
class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class PonenciaListView(validarUser,ListView):
    model = Ponencia
    context_object_name = 'ponencias'
    template_name = 'MedCongressAdmin/ponencias.html'

class  PonenciaCreateView(validarUser,FormView):
    form_class = PonenciaForms
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/ponencia_form.html'
    def form_valid(self, form):
        
        ponencia=form['ponencia'].save(commit=False)
        ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)

        if ubic.exists():
            ponencia.lugar=ubic.first()
        else:
            ubicacion=form['ubicacion'].save(commit=True)
            ponencia.lugar=ubicacion
        path=ponencia.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        ponencia.path=path+secret_key
        ponencia.save()
        return super(PonenciaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        
        context = super(PonenciaCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('pk'):
            context['con']=Congreso.objects.get(pk=self.kwargs.get('pk'))
            context['blo']=Bloque.objects.filter(congreso=context['con'])
        if self.kwargs.get('pk_block'):
            context['bloque']=Bloque.objects.get(pk=self.kwargs.get('pk_block'))
            context['con']=context['bloque'].congreso
            context['blo']= None
        return context 
    
    def get_success_url(self):
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_ponencias',kwargs={'path': congreso.path} )
        if self.kwargs.get('pk_block'):
            block=Bloque.objects.get(pk=self.kwargs.get('pk_block'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Bloque_ponencias',kwargs={'path': block.path} )
        return self.success_url   
 
########## Vista de las Categorias de Pago de un Congreso #############

class PonenciaPonenteListView(TemplateView):
    template_name= 'MedCongressAdmin/ponencia_ponentes.html' 
    def get(self, request, **kwargs):
        ponencia=Ponencia.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if ponencia is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(PonenciaPonenteListView, self).get_context_data(**kwargs)
        ponencia=Ponencia.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['ponencia']=ponencia
        context['ponentes']=RelPonenciaPonente.objects.filter(ponencia=ponencia)
        return context        

class  PonenciaPonenteCreateView(validarUser,CreateView):
    info_sended =Ponencia()
    form_class = PonentePonenciaForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/ponencia_ponente_form.html'

    

    def form_valid(self, form):
        ponencia=form.save(commit=False)
  
        ponencia.save()
        return super(PonenciaPonenteCreateView, self).form_valid(form)

    def get_success_url(self):
        
           self.success_url =  reverse_lazy('MedCongressAdmin:Ponencia_ponentes',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    # def form_invalid(self, form):
    #     for error in form.errors:
    #         print(error)
    #         form[error].field.widget.attrs['class'] += ' is-invalid'
    #     return super(PonenciaPonenteCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super(PonenciaPonenteCreateView, self).get_context_data(**kwargs)
        pon=Ponencia.objects.filter(path=self.kwargs.get('path'),published=True).first()
        ctx['pon'] = pon
        ponentes=RelPonenciaPonente.objects.filter(ponencia=pon)
        id=[]
        for ponente in ponentes:
            id.append(ponente.ponente.pk)
        ctx['ponentes']=Ponente.objects.exclude(id__in=id)
        return ctx


class PonencicaUpdateView(validarUser,UpdateView):
    form_class = PonenciaForms
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/ponencia_form.html'

    def get_queryset(self, **kwargs):
        return Ponencia.objects.filter(pk=self.kwargs.get('pk'))
    
    def get_form_kwargs(self):
        kwargs = super(PonencicaUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'ponencia': self.object,
            'ubicacion': self.object.lugar,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['imagen_seg_url']='/static/%s'%(self.object.imagen)
        if self.object.meta_og_imagen:
            context['imagen_meta']='/static/%s'%(self.object.meta_og_imagen)
        context['update']=self.object.bloque
        return context

class PonenciaDeletedView(validarUser,DeleteView):
    model = Ponencia
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')

class PonenciaPonenteDeletedView(validarUser,DeleteView):
    model = RelPonenciaPonente
    success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
   
def PonenciaBloqueDeleted(request):
    if request.is_ajax():
        query = request.POST['ponencia_id']
        ponencia=Ponencia.objects.get(id=query)
        ponencia.bloque=None
        ponencia.save()
        data = json.dumps([{'titulo':ponencia.titulo}])
        
        mimetype = "application/json"
    return HttpResponse(data, mimetype)  





