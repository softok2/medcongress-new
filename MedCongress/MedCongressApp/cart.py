from .models import Carrito

class Cart:
    def __init__(self,request):
        self.request=request
        self.session=request.session
        cart=self.session.get("cart")
        if not cart:
            cart=self.session["cart"]=[{'cant':0},[]]
        self.cart=cart

    def add_evento(self,relCongresoCategoriaPago,cant):
        exist=False
       
            
        # for car in self.cart[1]:
        #     if relCongresoCategoriaPago.congreso.pk == car['id_congreso'] and car['tipo_evento']=='Congreso':
        #         exist=True
        # if self.request.user.groups.filter(name='Laboratorio').exists():
        #     exist=False

        
        if exist is False:
            esta=False
            cont=0
            for car in self.cart[1]:
                if car['id_congreso']==relCongresoCategoriaPago.congreso.pk and car['id_cat_pago']==relCongresoCategoriaPago.categoria.pk and car['tipo_evento']=='Congreso':
                    self.cart[1][cont]['cantidad']= int(self.cart[1][cont]['cantidad'])+int(cant)
                    self.cart[1][cont]['pagar']= float(self.cart[1][cont]['pagar'])+round(float(relCongresoCategoriaPago.precio)*float(cant),2)
                    esta=True
                    carrito=Carrito.objects.get(pk=self.cart[1][cont]['mi_id'])
                    carrito.cantidad= int(carrito.cantidad)+int(cant)
                    carrito.pagar=float(carrito.pagar)+round(float(relCongresoCategoriaPago.precio)*float(cant),2)
                    carrito.save()
                cont=cont+1   
            if not esta: 
                carrito=Carrito(id_congreso_cat_pago=relCongresoCategoriaPago.pk,tipo_evento='Congreso'
                    ,id_evento=relCongresoCategoriaPago.congreso.pk,nombre_congreso=relCongresoCategoriaPago.congreso.titulo,id_cat_pago=relCongresoCategoriaPago.categoria.pk,
                    nombre_cat_pago=relCongresoCategoriaPago.categoria.nombre,precio=relCongresoCategoriaPago.precio,pagar=round(float(relCongresoCategoriaPago.precio)*float(cant),2),
                    moneda=relCongresoCategoriaPago.moneda,cantidad=cant,usuario=self.request.user)
                carrito.save()  
                self.cart[1].append(
                    {
                        'mi_id':carrito.pk,
                        'id':relCongresoCategoriaPago.pk,
                        'tipo_evento':'Congreso',
                        'id_congreso':relCongresoCategoriaPago.congreso.pk,
                        'nombre_congreso':relCongresoCategoriaPago.congreso.titulo,
                        'id_cat_pago':relCongresoCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relCongresoCategoriaPago.categoria.nombre,
                        'precio':relCongresoCategoriaPago.precio,
                        'pagar':round(float(relCongresoCategoriaPago.precio)*float(cant),2),
                        'moneda':relCongresoCategoriaPago.moneda,
                        'cantidad': cant
                    }
                )
                
            self.cart[0]['cant']=round(self.cart[0]['cant']+float(relCongresoCategoriaPago.precio)*float(cant),2)
            self.save()
            return True
        else:
            return False

    def add_taller(self,relTallerCategoriaPago,cant):
        exist=False
       
            
        # for car in self.cart[1]:
        #     if relTallerCategoriaPago.taller.pk == car['id_congreso'] and car['tipo_evento']=='Taller':
        #         exist=True
        # if self.request.user.groups.filter(name='Laboratorio').exists():
        #     exist=False
        if exist is False:
            esta=False
            cont=0
            for car in self.cart[1]:
                if car['id_congreso']==relTallerCategoriaPago.taller.pk and car['id_cat_pago']==relTallerCategoriaPago.categoria.pk and car['tipo_evento']=='Taller':
                    self.cart[1][cont]['cantidad']= int(self.cart[1][cont]['cantidad'])+int(cant)
                    self.cart[1][cont]['pagar']= float(self.cart[1][cont]['pagar'])+round(float(relTallerCategoriaPago.precio)*float(cant),2)
                    esta=True
                    carrito=Carrito.objects.get(pk=self.cart[1][cont]['mi_id'])
                    carrito.cantidad= int(carrito.cantidad)+int(cant)
                    carrito.pagar=float(carrito.pagar)+round(float(relTallerCategoriaPago.precio)*float(cant),2)
                    carrito.save()
                cont=cont+1   
                
            if not esta: 
                carrito=Carrito(id_congreso_cat_pago=relTallerCategoriaPago.pk,tipo_evento='Taller'
                ,id_evento=relTallerCategoriaPago.taller.pk,nombre_congreso=relTallerCategoriaPago.taller.titulo,id_cat_pago=relTallerCategoriaPago.categoria.pk,
                nombre_cat_pago=relTallerCategoriaPago.categoria.nombre,precio=relTallerCategoriaPago.precio,pagar=round(float(relTallerCategoriaPago.precio)*float(cant),2),
                moneda=relTallerCategoriaPago.moneda,cantidad=cant,usuario=self.request.user)
                carrito.save()
                self.cart[1].append(
                    {
                        'mi_id':carrito.pk,
                        'id':relTallerCategoriaPago.pk,
                        'tipo_evento':'Taller',
                        'id_congreso':relTallerCategoriaPago.taller.pk,
                        'nombre_congreso':relTallerCategoriaPago.taller.titulo,
                        'id_cat_pago':relTallerCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relTallerCategoriaPago.categoria.nombre,
                        'precio':relTallerCategoriaPago.precio,
                        'pagar':round(float(relTallerCategoriaPago.precio)*float(cant),2),
                        'moneda':relTallerCategoriaPago.moneda,
                        'cantidad': cant
                    }
                )
            
            self.cart[0]['cant']=round(self.cart[0]['cant']+float(relTallerCategoriaPago.precio)*float(cant),2)
            self.save()
            return True
        else:
            return False

       

    def confirmar(self,id,cant):
        cont=0
        for car in self.cart[1]:
            if str(car['mi_id'])==str(id) :
                self.cart[1][cont]['cantidad']=cant
                self.cart[0]['cant']=round(float(self.cart[0]['cant'])-float(car['pagar']),2)
                self.cart[1][cont]['pagar']=round(float(self.cart[1][cont]['precio'])*float(cant),2)
                self.cart[0]['cant']=round(float(self.cart[0]['cant'])+float(self.cart[1][cont]['pagar']),2)
                carrito=Carrito.objects.get(pk=car['mi_id'])
                carrito.cantidad= cant
                carrito.pagar=round(float(self.cart[1][cont]['precio'])*float(cant),2)
                carrito.save()    
            cont=cont+1
        self.save()
        
        return True
    def save(self):
        self.session["cart"]=self.cart
        self.session.modified=True

    def remove(self,id):
        cont=0
        for car in self.cart[1]:
            if str(car['mi_id'])==str(id) :
                self.cart[0]['cant']=self.cart[0]['cant']-car['pagar']
                self.cart[1].pop(cont)
                carrito=Carrito.objects.get(pk=car['mi_id'])
                carrito.delete()
            cont=cont+1
        self.save()
        return True

    def clear(self):
        self.session["cart"]=[{'cant':0},[]]
        carrito=Carrito.objects.filter(usuario=self.request.user)
        carrito.delete()
        self.session.modified=True
