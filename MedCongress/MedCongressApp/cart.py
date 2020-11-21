

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
        if len(self.cart[1])>0:
            
            # for car in self.cart[1]:
            #     if relCongresoCategoriaPago.congreso.pk == car['id_congreso'] and car['tipo_evento']=='Congreso':
            #         exist=True
            if self.request.user.groups.filter(name='Laboratorio').exists():
                exist=False

            
            if exist is False:
                self.cart[1].append(
                    {
                        'mi_id':int(self.cart[1][-1]['mi_id'])+1,
                        'id':relCongresoCategoriaPago.pk,
                        'tipo_evento':'Congreso',
                        'id_congreso':relCongresoCategoriaPago.congreso.pk,
                        'nombre_congreso':relCongresoCategoriaPago.congreso.titulo,
                        'id_cat_pago':relCongresoCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relCongresoCategoriaPago.categoria.nombre,
                        'precio':relCongresoCategoriaPago.precio,
                        'pagar':float(relCongresoCategoriaPago.precio)*float(cant),
                        'moneda':relCongresoCategoriaPago.moneda,
                        'cantidad': cant
                    }
                )
                self.cart[0]['cant']=self.cart[0]['cant']+float(relCongresoCategoriaPago.precio)*float(cant)
                self.save()
                return True
            else:
                return False

        else:
            self.cart[1].append(
                    {
                        'mi_id':1,
                        'id':relCongresoCategoriaPago.pk,
                        'tipo_evento':'Congreso',
                        'id_congreso':relCongresoCategoriaPago.congreso.pk,
                        'nombre_congreso':relCongresoCategoriaPago.congreso.titulo,
                        'id_cat_pago':relCongresoCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relCongresoCategoriaPago.categoria.nombre,
                        'precio':relCongresoCategoriaPago.precio,
                        'pagar':float(relCongresoCategoriaPago.precio)*float(cant),
                        'moneda':relCongresoCategoriaPago.moneda,
                        'cantidad': cant
                    }
                )  
            self.cart[0]['cant']=self.cart[0]['cant']+float(relCongresoCategoriaPago.precio)*float(cant)
            self.save()
            return True


    def add_taller(self,relTallerCategoriaPago,cant):
        exist=False
        if len(self.cart[1])>0:
            
            # for car in self.cart[1]:
            #     if relTallerCategoriaPago.taller.pk == car['id_congreso'] and car['tipo_evento']=='Taller':
            #         exist=True
            if self.request.user.groups.filter(name='Laboratorio').exists():
                exist=False
            if exist is False:
                self.cart[1].append(
                    {
                        'mi_id':int(self.cart[1][-1]['mi_id'])+1,
                        'id':relTallerCategoriaPago.pk,
                        'tipo_evento':'Taller',
                        'id_congreso':relTallerCategoriaPago.taller.pk,
                        'nombre_congreso':relTallerCategoriaPago.taller.titulo,
                        'id_cat_pago':relTallerCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relTallerCategoriaPago.categoria.nombre,
                        'precio':relTallerCategoriaPago.precio,
                        'pagar':float(relTallerCategoriaPago.precio)*float(cant),
                        'moneda':relTallerCategoriaPago.moneda,
                        'cantidad': cant
                    }
                )
                self.cart[0]['cant']=self.cart[0]['cant']+float(relTallerCategoriaPago.precio)*float(cant)
                self.save()
                return True
            else:
                return False

        else:
            self.cart[1].append(
                    {
                        'mi_id':1,
                        'id':relTallerCategoriaPago.pk,
                        'tipo_evento':'Taller',
                        'id_congreso':relTallerCategoriaPago.taller.pk,
                        'nombre_congreso':relTallerCategoriaPago.taller.titulo,
                        'id_cat_pago':relTallerCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relTallerCategoriaPago.categoria.nombre,
                        'precio':relTallerCategoriaPago.precio,
                        'pagar':float(relTallerCategoriaPago.precio)*float(cant),
                        'moneda':relTallerCategoriaPago.moneda,
                        'cantidad': cant
                    }
                )
            self.cart[0]['cant']=self.cart[0]['cant']+float(relTallerCategoriaPago.precio)*float(cant)
            self.save()
            return True


    def confirmar(self,id,cant):
        cont=0
        for car in self.cart[1]:
            if str(car['mi_id'])==str(id) :
                self.cart[1][cont]['cantidad']=cant
                self.cart[0]['cant']=float(self.cart[0]['cant'])-float(car['pagar'])
                self.cart[1][cont]['pagar']=float(self.cart[1][cont]['precio'])*float(cant)
                self.cart[0]['cant']=float(self.cart[0]['cant'])+float(self.cart[1][cont]['pagar'])
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
            cont=cont+1
        self.save()
        return True

    def clear(self):
        self.session["cart"]=[{'cant':0},[]]
        self.session.modified=True
