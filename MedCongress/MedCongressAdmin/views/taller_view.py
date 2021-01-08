import json

from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect)
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from MedCongressAdmin.forms.congres_forms import (AsignarTallerForms,
                                                  ExportarTallerExelForm,
                                                  PonenteTallerForm,
                                                  TallerCategPagoForm,
                                                  TallerForms)
from MedCongressApp.models import (Bloque, Congreso, Ponente,
                                   RelTalleresCategoriaPago, RelTallerPonente,
                                   RelTallerUser, Taller, Ubicacion)
from openpyxl import Workbook
from openpyxl.styles import (Alignment, Border, Font, PatternFill, Protection,
                             Side)


class validarUser(UserPassesTestMixin):
    permission_denied_message = 'No tiene permiso para acceder a la administracion'
    login_url='/admin/login/'
    def test_func(self):
       
        if self.request.user.is_staff :
            return True
        else:
            return False
    

class TalleresListView(validarUser,ListView):
    model = Taller
    context_object_name = 'talleres'
    template_name = 'MedCongressAdmin/talleres.html'

class  TallerCreateView(validarUser,FormView):
    form_class = TallerForms
    success_url = reverse_lazy('MedCongressAdmin:talleres_list')
    template_name = 'MedCongressAdmin/taller_form.html'

    def form_valid(self, form):
        
        taller=form['taller'].save(commit=False)
        ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)

        if ubic.exists():
            taller.lugar=ubic.first()
        else:
            ubicacion=form['ubicacion'].save(commit=True)
            taller.lugar=ubicacion
        path=taller.titulo.replace("/","").replace(" ","-").replace("?","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        chars = '0123456789'
        secret_key = get_random_string(5, chars)
        taller.path=path+secret_key
        id_video=['']
        if taller.cod_video:
            id_video=taller.cod_video.split(sep='https://player.vimeo.com/video/')
            id_video=id_video[-1].split(sep='"')
        taller.id_video=id_video[0]
        taller.save()
        return super(TallerCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        
        context = super(TallerCreateView, self).get_context_data(**kwargs)
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
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_talleres',kwargs={'path': congreso.path} )
        if self.kwargs.get('pk_block'):
            block=Bloque.objects.get(pk=self.kwargs.get('pk_block'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Bloque_talleres',kwargs={'path': block.path} )
        return self.success_url 

########## Vista de las Categorias de Pago de un Congreso #############

class TallerCategPagosListView(TemplateView):
    template_name= 'MedCongressAdmin/taller_cat_pagos.html' 
    

    def get(self, request, **kwargs):
        taller=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if taller is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(TallerCategPagosListView, self).get_context_data(**kwargs)
        taller=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['congres']=taller
        context['cat_pagos']=RelTalleresCategoriaPago.objects.filter(taller=taller)
        return context        
        
class  TallerCategPagosCreateView(validarUser,CreateView):
    info_sended =Taller()
    form_class = TallerCategPagoForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/taller_cat_pago_form.html'
    def form_valid(self, form):
        congreso=form.save(commit=False)
  
        congreso.save()
        return super(TallerCategPagosCreateView, self).form_valid(form)

    def get_success_url(self):
           self.success_url =  reverse_lazy('MedCongressAdmin:Taller_pagos',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    def get_context_data(self, **kwargs):
        ctx = super(TallerCategPagosCreateView, self).get_context_data(**kwargs)
        pon=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        ctx['cong'] = pon
        return ctx

class TallerUpdateView(validarUser,FormView):
    form_class = TallerForms
    success_url = reverse_lazy('MedCongressAdmin:talleres_list')
    template_name = 'MedCongressAdmin/taller_form.html'

    def get_queryset(self, **kwargs):
        return Taller.objects.filter(pk=self.kwargs.get('pk'))
    
    def get_form_kwargs(self):
        taller=Taller.objects.get(pk=self.kwargs.get('pk'))
        self.object=taller
        kwargs = super(TallerUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'taller': self.object,
            'ubicacion': self.object.lugar,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        taller=Taller.objects.get(pk=self.kwargs.get('pk'))
        self.object=taller
        context=super().get_context_data(**kwargs)
        if self.object.meta_og_imagen:
            context['imagen_meta']='/static/%s'%(self.object.meta_og_imagen)
        if self.object.imagen:
            context['imagen_seg_url']='/static/%s'%(self.object.imagen)
        context['update']=self.object.bloque
        return context

    def form_valid(self, form):
        taller_update=Taller.objects.get(pk=self.kwargs.get('pk'))
        self.object=taller_update
        taller=form['taller'].save(commit=False)
        ubic=Ubicacion.objects.filter(direccion=form['ubicacion'].instance.direccion)

        if ubic.exists():
            taller.lugar=ubic.first()
        else:
            ubicacion=form['ubicacion'].save(commit=True)
            taller.lugar=ubicacion
        id_video=['']
        if taller.cod_video:
            id_video=taller.cod_video.split(sep='https://player.vimeo.com/video/')
            id_video=id_video[-1].split(sep='"')
        taller.id_video=id_video[0]
        taller_update=taller
        taller_update.save()
        return super(TallerUpdateView, self).form_valid(form)
    def get_success_url(self):
        if self.kwargs.get('pk'):
            congreso=Congreso.objects.get(pk=self.kwargs.get('pk'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Congres_talleres',kwargs={'path': congreso.path} )
        if self.kwargs.get('pk_block'):
            block=Bloque.objects.get(pk=self.kwargs.get('pk_block'))
            self.success_url =  reverse_lazy('MedCongressAdmin:Bloque_talleres',kwargs={'path': block.path} )
        return self.success_url  
class TallerPonenteListView(TemplateView):
    template_name= 'MedCongressAdmin/taller_ponentes.html' 
    def get(self, request, **kwargs):
        taller=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        if taller is None:
            return   HttpResponseRedirect(reverse('Error404'))
        return self.render_to_response(self.get_context_data())    
    def get_context_data(self, **kwargs):
        context = super(TallerPonenteListView, self).get_context_data(**kwargs)
        taller=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        context['taller']=taller
        context['ponentes']=RelTallerPonente.objects.filter(taller=taller)
        return context     

class  TallerPonenteCreateView(validarUser,CreateView):
    
    form_class = PonenteTallerForm
    # success_url = reverse_lazy('MedCongressAdmin:ponencias_list')
    template_name = 'MedCongressAdmin/taller_ponente_form.html'

    

    def form_valid(self, form):
        ponencia=form.save(commit=False)
  
        ponencia.save()
        return super(TallerPonenteCreateView, self).form_valid(form)

    def get_success_url(self):
        
           self.success_url =  reverse_lazy('MedCongressAdmin:Taller_ponentes',kwargs={'path': self.kwargs.get('path')} )
           return self.success_url

    # def form_invalid(self, form):
    #     for error in form.errors:
    #         print(error)
    #         form[error].field.widget.attrs['class'] += ' is-invalid'
    #     return super(PonenciaPonenteCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super(TallerPonenteCreateView, self).get_context_data(**kwargs)
        pon=Taller.objects.filter(path=self.kwargs.get('path'),published=True).first()
        ctx['pon'] = pon
        ponentes=RelTallerPonente.objects.filter(taller=pon)
        id=[]
        for ponente in ponentes:
            id.append(ponente.ponente.pk)
        ctx['ponentes']=Ponente.objects.exclude(id__in=id)
        return ctx

class TallerDeletedView(validarUser,DeleteView):
    model = Taller
    success_url = reverse_lazy('MedCongressAdmin:talleres_list')

class AsignarTalleresListView(validarUser,ListView,FormView):
    model = RelTallerUser
    context_object_name = 'talleres'
    template_name = 'MedCongressAdmin/asignar_taller.html'
    form_class=ExportarTallerExelForm

    def form_valid(self, form):
        return super().form_valid(form)


class AsignarTallerAddViews(validarUser,FormView):
    form_class = AsignarTallerForms
    success_url = reverse_lazy('MedCongressAdmin:asig_talleres_list')
    template_name = 'MedCongressAdmin/asig_taller_form.html'

    def form_valid(self, form):
        congress=form.save(commit=True)
        return super().form_valid(form)
def GetPagosT(request):
    if request.is_ajax():
        query = request.POST['taller_id']
        categoria=RelTalleresCategoriaPago.objects.filter(taller=Taller.objects.get(pk=query))
        
        results = []
        for cat in categoria:
            results.append({'nombre':cat.categoria.nombre,'id':cat.categoria.pk})
            data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype) 

class AsignarTallerDeletedViews(validarUser,DeleteView):
    model = RelTallerUser
    success_url = reverse_lazy('MedCongressAdmin:asig_talleres_list')

class TallerPonenteDeletedView(validarUser,DeleteView):
    model = RelTallerPonente
    success_url = reverse_lazy('MedCongressAdmin:talleres_list')



def TallerBloqueDeleted(request):
    if request.is_ajax():
        query = request.POST['taller_id']
        taller=Taller.objects.get(id=query)
        taller.bloque=None
        taller.save()
        data = json.dumps([{'titulo':taller.titulo}])
        
        mimetype = "application/json"
    return HttpResponse(data, mimetype)   
    
class ReporteRelTallerUserExcel(TemplateView):
    
    #Usamos el método get para generar el archivo excel 
    def post(self, request):
        #Obtenemos todas las personas de nuestra base de datos
        taller=self.request.POST['taller']
        query= RelTallerUser.objects.filter(taller=taller).values('user__usuario__first_name','user__usuario__last_name','user__usuario__email','taller__titulo','categoria_pago__nombre').annotate(Sum('cantidad'))

		#Creamos el libro de trabajo
        wb = Workbook()
		#Definimos como nuestra hoja de trabajo, la hoja activa, por defecto la primera del libro
        ws = wb.active
       
		#En la celda B1 ponemos el texto 'REPORTE DE PERSONAS'
        ws['B1'] = 'Usuarios que han comprado el Taller%s'%( query[0]['taller__titulo'])
        ws['B1'].font = Font(size=12,bold=True)
        ws['B1'].alignment = Alignment(mergeCell='center',horizontal='center') 
        
		#Juntamos las celdas desde la B1 hasta la E1, formando una sola celda
        ws.merge_cells('B1:E1')
		#Creamos los encabezados desde la celda B3 hasta la E3
        ws['A3'] = 'No.'
        ws['B3'] = 'Nombre'
        ws['C3'] = 'Email'
        ws['D3'] = 'Taller'
        ws['E3'] = 'Categoria de Pago'
        ws['F3'] = 'Cantidad'        
        cont=4
        #Recorremos el conjunto de personas y vamos escribiendo cada uno de los datos en las celdas
        for quer in query:
            ws.cell(row=cont,column=1).value = cont-3
            ws.cell(row=cont,column=2).value = '%s %s'%(quer['user__usuario__first_name'],quer['user__usuario__last_name'])
            ws.cell(row=cont,column=3).value = quer['user__usuario__email']
            ws.cell(row=cont,column=4).value = quer['taller__titulo']
            ws.cell(row=cont,column=5).value = quer['categoria_pago__nombre']
            ws.cell(row=cont,column=6).value = quer['cantidad__sum']
            cont = cont + 1
		
        response = HttpResponse(content_type="application/ms-excel") 
        response["Content-Disposition"] = "attachment; filename=RelTallerUser.xlsx"
        wb.save(response)
        return response
