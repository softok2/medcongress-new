

class Cart:
    def __init__(self,request):
        self.request=request
        self.session=request.session
        cart=self.session.get("cart")
        if not cart:
            cart=self.session["cart"]=[{'cant':0},[]]
        self.cart=cart

    def add_evento(self,relCongresoCategoriaPago):
        exist=False
        if len(self.cart[1])>0:
            
            for car in self.cart[1]:
                if relCongresoCategoriaPago.congreso.pk == car['id_congreso'] and car['tipo_evento']=='Congreso':
                    exist=True
            
            if exist is False:
                self.cart[1].append(
                    {
                        'id':relCongresoCategoriaPago.pk,
                        'tipo_evento':'Congreso',
                        'id_congreso':relCongresoCategoriaPago.congreso.pk,
                        'nombre_congreso':relCongresoCategoriaPago.congreso.titulo,
                        'id_cat_pago':relCongresoCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relCongresoCategoriaPago.categoria.nombre,
                        'precio':relCongresoCategoriaPago.precio,
                        'moneda':relCongresoCategoriaPago.moneda,
                        'cantidad': "1"
                    }
                )
                self.cart[0]['cant']=self.cart[0]['cant']+relCongresoCategoriaPago.precio
                self.save()
                return True
            else:
                return False

        else:
            self.cart[1].append(
                    {
                        'id':relCongresoCategoriaPago.pk,
                        'tipo_evento':'Congreso',
                        'id_congreso':relCongresoCategoriaPago.congreso.pk,
                        'nombre_congreso':relCongresoCategoriaPago.congreso.titulo,
                        'id_cat_pago':relCongresoCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relCongresoCategoriaPago.categoria.nombre,
                        'precio':relCongresoCategoriaPago.precio,
                        'moneda':relCongresoCategoriaPago.moneda,
                        'cantidad': "1"
                    }
                )  
            self.cart[0]['cant']=self.cart[0]['cant']+relCongresoCategoriaPago.precio
            self.save()
            return True


    def add_taller(self,relTallerCategoriaPago):
        exist=False
        if len(self.cart[1])>0:
            
            for car in self.cart[1]:
                if relTallerCategoriaPago.taller.pk == car['id_congreso'] and car['tipo_evento']=='Taller':
                    exist=True
            
            if exist is False:
                self.cart[1].append(
                    {
                        'id':relTallerCategoriaPago.pk,
                        'tipo_evento':'Taller',
                        'id_congreso':relTallerCategoriaPago.taller.pk,
                        'nombre_congreso':relTallerCategoriaPago.taller.titulo,
                        'id_cat_pago':relTallerCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relTallerCategoriaPago.categoria.nombre,
                        'precio':relTallerCategoriaPago.precio,
                        'moneda':relTallerCategoriaPago.moneda,
                        'cantidad': "1"
                    }
                )
                self.cart[0]['cant']=self.cart[0]['cant']+relTallerCategoriaPago.precio
                self.save()
                return True
            else:
                return False

        else:
            self.cart[1].append(
                    {
                        'id':relTallerCategoriaPago.pk,
                        'tipo_evento':'Taller',
                        'id_congreso':relTallerCategoriaPago.taller.pk,
                        'nombre_congreso':relTallerCategoriaPago.taller.titulo,
                        'id_cat_pago':relTallerCategoriaPago.categoria.pk,
                        'nombre_cat_pago':relTallerCategoriaPago.categoria.nombre,
                        'precio':relTallerCategoriaPago.precio,
                        'moneda':relTallerCategoriaPago.moneda,
                        'cantidad': "1"
                    }
                )
            self.cart[0]['cant']=self.cart[0]['cant']+relTallerCategoriaPago.precio
            self.save()
            return True

    def save(self):
        self.session["cart"]=self.cart
        self.session.modified=True

    def remove(self,id,evento):
        cont=0
        for car in self.cart[1]:
            if str(car['id'])==str(id) and str(car['tipo_evento']) == str(evento):
                self.cart[0]['cant']=self.cart[0]['cant']-car['precio']
                self.cart[1].pop(cont)
            cont=cont+1
        self.save()
        return True

    def clear(self):
        self.session["cart"]=[{'cant':0},[]]
        self.session.modified=True
