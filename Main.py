import sys
import couchdb
import ctypes  # An included library with Python install.
from PyQt5 import uic, QtWidgets
import json
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget,QTableWidgetItem,QMessageBox,QPushButton
from PyQt5 import QtGui
# -------------------------------------------------------------------------------

qtCreatorFile = "GUI.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Conexion a la BASE DE DATOS
couch = couchdb.Server("http://127.0.0.1:5984")
db = couch['test2']
propietarios=[]
farmaceuticos=[]
productos=[]
productos_laboratorio=[]
productos_almacenes=[]
almacenes=[]


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        ##############
        ##############AGREGAR
        ##############
        # Agregar Farmaceutico
        self.bt_Farmaceutico_agregar_2.clicked.connect(self.agregarFarmaceutico)
        # Agregar Propietarios
        #self.bt_propietario_agregar.clicked.connect(self.agregarPropietario)
        # agregar Laboratorios
        self.bt_Laboratorio_agregar.clicked.connect(self.agregarLaboratorio)
        # Agregar Productos
        self.bt_Producto_agregar.clicked.connect(self.agregarProductos)
        # AgregarFarmacia
        self.bt_Farmacia_Agregar.clicked.connect(self.agregarFarmacia)
        ################
        ################  ELIMINAR
        ################
        # prueba eliminar

        # eliminar Farmaceutico
        self.bt_Farmaceutico_Eliminar_2.clicked.connect(self.AccionEliminarFarmaceutico)
        # eliminar Propietario
        #self.bt_propietario_Eliminar.clicked.connect(self.AccionEliminarPropietario)
        # eliminar Productos
        self.bt_Producto_Eliminar.clicked.connect(self.AccionEliminarProducto)
        # eliminar Laboratorio
        self.bt_Laboratorio_Eliminar.clicked.connect(self.AccionEliminarLaboratorio)
        # eliminar Farmacias
        self.bt_Farmacia_Eliminar.clicked.connect(self.AccionEliminarFarmacia)
        ################
        ################ ACTUALIZAR
        ################
        # Actualizar Farmaceutico
        self.bt_Farmaceutico_Modificar_2.clicked.connect(self.AccionModificarFarmaceutico)
        # Actualizar Propietario
        #self.bt_propietario_Modificar.clicked.connect(self.AccionModificarPropietario)
        # Actualizar Laboratorio
        self.bt_Laboratorio_Modificar.clicked.connect(self.AccionModificarLaboratorio)
        # Actualizar Producto
        self.bt_Producto_Modificar.clicked.connect(self.AccionModificarProducto)
        #Actualizar Farmacia
        self.bt_Farmacia_Modificar.clicked.connect(self.ModificarFarmacia)
        ################
        ################ BUSCAR
        ################
        self.bt_FindFarmacia.clicked.connect(self.BuscarFarmacia)
        self.bt_FindFarmaceutico_2.clicked.connect(self.BuscarFarmaceutico)
        #self.bt_FindPropietario.clicked.connect(self.BuscarPropietaraio)
        self.bt_FindLaboratorio.clicked.connect(self.BuscarLaboratorio)
        self.bt_FindProducto.clicked.connect(self.BuscarProducto)
        ################
        ############### TAB BAR CLICKED
        ################
        self.bt_Farmacia_BuscarProductos.clicked.connect(self.AccionBuscarProductos)
        self.bt_load.clicked.connect(self.loadComboboxes)
        self.bt_Farmacia_asigPropietarios.clicked.connect(self.asignarPropietario)
        self.bt_Farmacia_asigFarmaceuticos.clicked.connect(self.asignarFarmaceuticos)
        self.bt_agregarAlmacen.clicked.connect(self.agregarAlmacen)
        self.bt_asignaralmancen.clicked.connect(self.asignarAlamacen)
        self.bt_loadprodlab.clicked.connect(self.loadPro)
        self.bt_Farmacia_BuscarProductos.clicked.connect(self.loadAlmacenesfar)
        self.bt_almacen_farmacia.clicked.connect(self.loadProductosfar)
        self.bt_load_2.clicked.connect(self.loadProRES)
        self.bt_Laboratorio_AgregarProducto.clicked.connect(self.AgregarProductoALAb)
        self.bt_Laboratorio_AgregarProducto_3.clicked.connect(self.SetproductosLaboratorio)
        self.bt_Farmacia_BuscarProductos_3.clicked.connect(self.CargarTodosLabsConProductos)
        self.bt_Farmacia_BuscarProductos_6.clicked.connect(self.AgregarProductos_Cola)
        self.bt_Farmacia_BuscarProductos_7.clicked.connect(self.RealizarPedido)


    def RealizarPedido(self):
        almacen=self.tf_Farmacia_CodFarmaciaAlmacenBuscar_3.text()
        docalma=db[almacen]
        db.delete(docalma)
        for e in productos_almacenes:
            for pro in db.get(e[3]).get('productos'):
                if(e[0]==pro[0] and int(e[1])<int(pro[1]) and e[2]==pro[2]):
                    print('Primer if')
                    doc = db[e[3]]
                    db.delete(doc)
                    valor=int(pro[1])-int(e[1])
                    id = e[3]
                    nombre = doc.get('nombre')
                    temp=doc.get('productos')
                    array=[]
                    for l in temp:
                        if(l[0]==pro[0]):
                            l[1]=valor.__str__()
                        if(valor>0):
                            array.append(l)
                    doc = {
                    '_id': id,
                    'nombre': nombre,
                    'productos': array,
                    'tipo':'laboratorio'
                    }
                    db.save(doc)

        doc1 = {
            '_id': almacen,
            'productos':productos_almacenes,
            'tipo':'almacenes'
        }
        db.save(doc1)
        productos_almacenes.clear()
        self.tableWidget_9.setRowCount(0)
        self.tableWidget_9.setColumnCount(0)
        self.tableWidget_9.setHorizontalHeaderItem(0, QTableWidgetItem(""))
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setHorizontalHeaderItem(0, QTableWidgetItem(""))
        self.tf_Farmacia_CodFarmaciaAlmacenBuscar_4.setText("")
        self.tf_Farmacia_CodFarmaciaAlmacenBuscar_5.setText("")
        self.tf_Farmacia_CodFarmaciaAlmacenBuscar_6.setText("")
        self.tf_Farmacia_CodFarmaciaAlmacenBuscar_12.setText("")










    def modificarProductosEnLaboratorio(idlab,idpro,cantidadNueva):
        print('inicio')


    def AgregarProductos_Cola(self):
        codigo_lab=self.tf_Farmacia_CodFarmaciaAlmacenBuscar_4.text()
        codigo_pro=self.tf_Farmacia_CodFarmaciaAlmacenBuscar_5.text()
        precio_pro=self.tf_Farmacia_CodFarmaciaAlmacenBuscar_6.text()
        cant_pedir=self.tf_Farmacia_CodFarmaciaAlmacenBuscar_12.text()

        productos_almacenes.append([codigo_pro,cant_pedir,precio_pro,codigo_lab])

        self.tableWidget_9.setRowCount(len(productos_almacenes))
        self.tableWidget_9.setColumnCount(4)
        self.tableWidget_9.setHorizontalHeaderItem(0, QTableWidgetItem("Nombre"))
        self.tableWidget_9.setHorizontalHeaderItem(1, QTableWidgetItem("Codigo"))
        self.tableWidget_9.setHorizontalHeaderItem(2, QTableWidgetItem("Precio"))
        self.tableWidget_9.setHorizontalHeaderItem(3, QTableWidgetItem("Cantidad"))
        i=0
        for e in productos_almacenes:
            self.tableWidget_9.setItem(i,0, QtWidgets.QTableWidgetItem(db.get(e[0]).get('nombre')))
            self.tableWidget_9.setItem(i,1, QtWidgets.QTableWidgetItem(e[0]))
            self.tableWidget_9.setItem(i,2, QtWidgets.QTableWidgetItem(e[2]))
            self.tableWidget_9.setItem(i,3, QtWidgets.QTableWidgetItem(e[1]))
            i=i+1


    def CargarTodosLabsConProductos(self):
        torequest=requests.get('http://127.0.0.1:5984/test2/_design/list/_view/laboratorios')
        doc=torequest.json().get('rows')
        print(doc)
        self.tableWidget_2.setRowCount(1000)
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderItem(0, QTableWidgetItem("Laboratorio"))
        self.tableWidget_2.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        self.tableWidget_2.setHorizontalHeaderItem(2, QTableWidgetItem("Codigo"))
        self.tableWidget_2.setHorizontalHeaderItem(3, QTableWidgetItem("Cantidad"))
        self.tableWidget_2.setHorizontalHeaderItem(4, QTableWidgetItem("Precio"))
        i=0
        for labs in doc:
            for pro in db.get(labs.get('key')).get('productos'):
                self.tableWidget_2.setItem(i,0, QtWidgets.QTableWidgetItem(labs.get('key')))
                self.tableWidget_2.setItem(i,1, QtWidgets.QTableWidgetItem(db.get(pro[0]).get('nombre')))
                self.tableWidget_2.setItem(i,2, QtWidgets.QTableWidgetItem(pro[0]))
                self.tableWidget_2.setItem(i,3, QtWidgets.QTableWidgetItem(pro[1]))
                self.tableWidget_2.setItem(i,4, QtWidgets.QTableWidgetItem(pro[2]))
                i=i+1





            i=i+1

    def ModificarFarmacia(self):
        cod = self.tf_Farmacia_codigoFarm.text()
        ciudad = self.tf_Farmacia_Ciudad.text()
        departamento = self.tf_Farmacia_departamento.text()
        calle = self.tf_Farmacia_calle.text()
        alma=db.get(cod).get('almacenes')
        prop=db.get(cod).get('propietarios')
        farma=db.get(cod).get('farmaceuticos')
        doc = {
            '_id': cod,
            "direccion":{ "ciudad": ciudad,
                         "departamento": departamento,
                         "calle":calle
                         },
            "almacenes":alma,
            "propietarios":prop,
            "farmaceuticos":farma,
            "tipo":"farmacia"
        }
        doc = db[cod]
        db.delete(doc)
        db.save(doc)
        self.bt_load.setEnabled(True)
        self.tf_Farmacia_codigoFarm.settext('')
        self.tf_Farmacia_Ciudad.settext('')
        self.tf_Farmacia_departamento.settext('')
        self.tf_Farmacia_calle.settext('')

    def AgregarProductoALAb(self):
        codigo=self.tf_Laboratorio_IdProduct.text()
        cantidad=self.tf_Laboratorio_cantidadProduct.text()
        pre_venta=self.tf_Laboratorio_costoVentaProducto.text()
        productos_laboratorio.append([codigo,cantidad,pre_venta])
        print (productos_laboratorio)

        self.tb_lab_agregarproducto_2.setRowCount(len(productos_laboratorio))
        self.tb_lab_agregarproducto_2.setColumnCount(5)
        self.tb_lab_agregarproducto_2.setHorizontalHeaderItem(0, QTableWidgetItem("Codigo"))
        self.tb_lab_agregarproducto_2.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        self.tb_lab_agregarproducto_2.setHorizontalHeaderItem(2, QTableWidgetItem("Cantidad"))
        self.tb_lab_agregarproducto_2.setHorizontalHeaderItem(3, QTableWidgetItem("precio coste"))
        self.tb_lab_agregarproducto_2.setHorizontalHeaderItem(4, QTableWidgetItem("Precio Venta"))
        i=0
        for e in productos_laboratorio:
            if(i<len(productos_laboratorio)):
                self.tb_lab_agregarproducto_2.setItem(i,0, QtWidgets.QTableWidgetItem(e[0]))
                self.tb_lab_agregarproducto_2.setItem(i,1, QtWidgets.QTableWidgetItem(db.get(e[0]).get('nombre')))
                self.tb_lab_agregarproducto_2.setItem(i,2, QtWidgets.QTableWidgetItem(e[1]))
                self.tb_lab_agregarproducto_2.setItem(i,3, QtWidgets.QTableWidgetItem(db.get(e[0]).get('precioCosto')))
                self.tb_lab_agregarproducto_2.setItem(i,4, QtWidgets.QTableWidgetItem(e[2]))

            else:
                break
            i=i+1
        self.tf_Laboratorio_IdProduct.setText('')
        self.tf_Laboratorio_cantidadProduct.setText('')
        self.tf_Laboratorio_costoVentaProducto.setText('')

    def SetproductosLaboratorio(self):
        doc = db[self.tf_Laboratorio_IdProduct_3.text()]
        db.delete(doc)
        id = self.tf_Laboratorio_IdProduct_3.text()
        nombre = doc.get('nombre')
        temp=doc.get('productos')
        for e in temp:
            productos_laboratorio.append(e)
        doc = {
            '_id': id,
            'nombre': nombre,
            'productos': productos_laboratorio,
            'tipo':'laboratorio'

        }
        db.save(doc)
        self.tf_Laboratorio_id.setText("")
        self.tf_Laboratorio_nombre.setText("")
        self.tb_lab_agregarproducto_2.setRowCount(0)
        self.tb_lab_agregarproducto_2.setColumnCount(0)
        self.tb_lab_agregarproducto_2.setHorizontalHeaderItem(0, QTableWidgetItem(""))
        self.tb_lab_agregarproducto.setRowCount(0)
        self.tb_lab_agregarproducto.setColumnCount(0)
        self.tb_lab_agregarproducto.setHorizontalHeaderItem(0, QTableWidgetItem(""))
        productos_laboratorio.clear()

    def loadProductosfar(self):
        doc=db.get(self.tf_alamacenfarma.text())
        array=doc.get('productos')
        print(array)
        self.tableWidget.setRowCount(len(array))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Codigo"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Cantidad"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Precio Venta"))
        i=0
        for e in array:
            self.tableWidget.setItem(i,0, QtWidgets.QTableWidgetItem(e[0]))
            self.tableWidget.setItem(i,1, QtWidgets.QTableWidgetItem(db.get(e[0]).get('nombre')))
            self.tableWidget.setItem(i,2, QtWidgets.QTableWidgetItem(e[1]))
            self.tableWidget.setItem(i,3, QtWidgets.QTableWidgetItem(e[2]))
            i=i+1


    def loadAlmacenesfar(self):
        doc=db.get(self.tf_Farmacia_CodFarmaciaAlmacenBuscar.text())
        array=doc.get('almacenes')
        print (array)
        self.tb_almacenesfarma.setRowCount(len(array))
        self.tb_almacenesfarma.setColumnCount(3)
        self.tb_almacenesfarma.setHorizontalHeaderItem(0, QTableWidgetItem("Codigo"))

        i=0
        for e in doc:
            if(i<len(array)):
                self.tb_almacenesfarma.setItem(i,0, QtWidgets.QTableWidgetItem(array[i]))
            else:
                break
            i=i+1





    def loadPro(self):
        torequest=requests.get('http://127.0.0.1:5984/test2/_design/list/_view/productos')
        doc=torequest.json().get('rows')
        self.tb_lab_agregarproducto.setRowCount(len(doc))
        self.tb_lab_agregarproducto.setColumnCount(2)
        self.tb_lab_agregarproducto.setHorizontalHeaderItem(0, QTableWidgetItem("Codigo"))
        self.tb_lab_agregarproducto.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        i=0
        for e in doc:
            self.tb_lab_agregarproducto.setItem(i,0, QtWidgets.QTableWidgetItem(e.get('key')))
            self.tb_lab_agregarproducto.setItem(i,1, QtWidgets.QTableWidgetItem(db.get(e.get('key')).get('nombre')))
            i=i+1


    def agregarAlmacen(self):
        codigo= self.tf_codigo_almacenes.text()
        array=[]
        doc = {
            '_id': codigo,
            'productos':array,
            'tipo':'almacenes'
        }
        db.save(doc)
        self.tf_codigo_almacenes.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se agrego el almacen exitosamente!.")
        msgBox.exec_()

    def asignarAlamacen(self):
        almacenes.append(self.cb_almaneces.currentText())
        index=self.cb_almaneces.currentIndex()
        self.cb_almaneces.removeItem(index)
        self.bt_load.setEnabled(False)
        print (almacenes)
        msgBox = QMessageBox()
        msgBox.setText("Se asigno el almacen exitosamente!.")
        msgBox.exec_()

    def asignarPropietario(self):
        propietarios.append(self.cb_Farmacia_Propietarios.currentText())
        index=self.cb_Farmacia_Propietarios.currentIndex()
        self.cb_Farmacia_Propietarios.removeItem(index)
        self.bt_load.setEnabled(False)
        msgBox = QMessageBox()
        msgBox.setText("Se asigno el propietario exitosamente!.")
        msgBox.exec_()

    def asignarFarmaceuticos(self):
        farmaceuticos.append(self.cb_Farmacia_farmaceuticos.currentText())
        index=self.cb_Farmacia_farmaceuticos.currentIndex()
        self.cb_Farmacia_farmaceuticos.removeItem(index)
        self.bt_load.setEnabled(False)
        msgBox = QMessageBox()
        msgBox.setText("Se asigno el farmaceutico exitosamente!.")
        msgBox.exec_()

    def AccionBuscarProductos(self):
        torequest=requests.get('http://127.0.0.1:5984/test2/_design/List_productos/_view/view_list_productos')
        doc=torequest.json().get('rows')



    def AccionModificarProducto(self):
        doc = db[self.tf_Producto_id.text()]
        db.delete(doc)
        nombre = self.tf_Producto_nombre.text()
        fabricante = self.tf_Producto_Fabricante.text()
        seguro = self.cb_Producto_TieneProteccion.currentText()
        preciocoste=self.tf_Producto_precioCoste.text()
        categoria = self.tf_Producto_Categoria.text()
        descripcion = self.tf_Producto_DescripcionProducto.toPlainText()
        doc = {
            '_id': self.tf_Producto_id.text(),
            'nombre': nombre,
            'fabricante': fabricante,
            'precioCosto': preciocoste,
            'precioVenta': '',
            'cantidad': '',
            'seguro': seguro,
            'categoria': categoria,
            'descripcion': descripcion,
            'tipo':"producto"

        }
        print(doc)
        db.save(doc)
        self.tf_Producto_id.setText("")
        self.tf_Producto_nombre.setText("")
        self.tf_Producto_Fabricante.setText("")
        self.tf_Producto_precioCoste.setText("")
        self.tf_Producto_Categoria.setText("")
        self.tf_Producto_DescripcionProducto.setPlainText("")
        msgBox = QMessageBox()
        msgBox.setText("Se modifico el producto exitosamente!.")
        msgBox.exec_()

    def AccionModificarLaboratorio(self):
        doc = db[self.tf_Laboratorio_id.text()]
        db.delete(doc)
        id = self.tf_Laboratorio_id.text()
        nombre = self.tf_Laboratorio_nombre.text()
        temp=doc.get('productos')
        for e in temp:
            productos_laboratorio.append(e)
        doc = {
            '_id': id,
            'nombre': nombre,
            'productos':productos_laboratorio,
            'tipo':'laboratorio'

        }
        db.save(doc)
        self.tf_Laboratorio_id.setText("")
        self.tf_Laboratorio_nombre.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se modifico el laboratorio exitosamente!.")
        msgBox.exec_()


    def AccionModificarFarmaceutico(self):
        doc = db[self.tf_Farmaceutico_id_2.text()]
        db.delete(doc)
        id = self.tf_Farmaceutico_id_2.text()
        nombre = self.tf_Farmaceutico_nombre_2.text()
        direccion = self.tf_Farmaceutico_direccion_2.text()
        edad = self.tf_Farmaceutico_edad_2.text()
        persona = ("Farmaceutico")
        doc = {
            '_id': id,
            'nombre': nombre,
            'direccion': direccion,
            'edad': edad,
            'tipo': 'persona'
        }
        db.save(doc)
        self.tf_Farmaceutico_id_2.setText("")
        self.tf_Farmaceutico_nombre_2.setText("")
        self.tf_Farmaceutico_direccion_2.setText("")
        self.tf_Farmaceutico_edad_2.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se modifico el farmaceutico exitosamente!.")
        msgBox.exec_()

    def loadProRES(self):
        doc=db.get(self.codigo_farmacia.text())
        array=doc.get('propietarios')


        self.tableWidget_3.setRowCount(len(array))
        self.tableWidget_3.setColumnCount(2)
        self.tableWidget_3.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.tableWidget_3.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre"))
        i=0
        for e in array:
            self.tableWidget_3.setItem(i,0, QtWidgets.QTableWidgetItem(array[i]))
            self.tableWidget_3.setItem(i,1, QtWidgets.QTableWidgetItem(db.get(array[i]).get('nombre')))
            i=i+1

        doc=db.get(self.codigo_farmacia.text())
        array=doc.get('farmaceuticos')


        self.tableWidget_4.setRowCount(len(array))
        self.tableWidget_4.setColumnCount(2)
        self.tableWidget_4.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.tableWidget_4.setHorizontalHeaderItem(1, QTableWidgetItem("Nombre    "))
        i=0
        for e in array:
            self.tableWidget_4.setItem(i,0, QtWidgets.QTableWidgetItem(array[i]))
            self.tableWidget_4.setItem(i,1, QtWidgets.QTableWidgetItem(db.get(array[i]).get('nombre')))
            i=i+1

    def BuscarProducto(self):
       id=self.tf_Producto_id.text()
       doc=db.get(id)
       self.tf_Producto_nombre.setText(doc.get('nombre'))
       self.tf_Producto_Fabricante.setText(doc.get('fabricante'))
       self.tf_Producto_precioCoste.setText(doc.get('precioCosto'))
       self.tf_Producto_Categoria.setText(doc.get('categoria'))
       self.tf_Producto_DescripcionProducto.setPlainText(doc.get('descripcion'))

    def BuscarLaboratorio(self):
        doc=db.get(self.tf_Laboratorio_id.text())
        self.tf_Laboratorio_nombre.setText(doc.get('nombre'))

    def BuscarPropietaraio(self):
        doc=db.get(self.tf_propietario_id.text())
        print(doc)
        self.tf_propietario_nombre.setText(doc.get('nombre'))
        self.tf_propietario_direccion.setText(doc.get('direccion'))
        self.tf_propietario_edad.setText(doc.get('edad'))

    def BuscarFarmaceutico(self):
        doc=db.get(self.tf_Farmaceutico_id_2.text())
        print (doc)
        self.tf_Farmaceutico_nombre_2.setText(doc.get('nombre'))
        self.tf_Farmaceutico_direccion_2.setText(doc.get('direccion'))
        self.tf_Farmaceutico_edad_2.setText(doc.get('edad'))


    def BuscarFarmacia(self):
        doc=db.get(self.tf_Farmacia_codigoFarm.text())
        print (doc)
        self.tf_Farmacia_Ciudad.setText(doc.get('direccion').get('ciudad'))
        self.tf_Farmacia_departamento.setText(doc.get('direccion').get('departamento'))
        self.tf_Farmacia_calle.setText(doc.get('direccion').get('calle'))

    def AccionModificarPropietario(self):
        doc = db[self.tf_propietario_id.text()]
        db.delete(doc)
        id = self.tf_propietario_id.text()
        nombre = self.tf_propietario_nombre.text()
        direccion = self.tf_propietario_direccion.text()
        edad = self.tf_propietario_edad.text()
        persona = ("Propietario")
        doc = {
            '_id': id,
            'nombre': nombre,
            'direccion': direccion,
            'edad': edad,
            'tipo': persona

        }
        db.save(doc)
        self.tf_propietario_id.setText("")
        self.tf_propietario_nombre.setText("")
        self.tf_propietario_direccion.setText("")
        self.tf_propietario_edad.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se modifico el propietario exitosamente!.")
        msgBox.exec_()



    def AccionEliminarFarmaceutico(self):
        doc = db[self.tf_Farmaceutico_id_2.text()]
        db.delete(doc)
        self.tf_Farmaceutico_id_2.setText("")
        self.tf_Farmaceutico_nombre_2.setText("")
        self.tf_Farmaceutico_direccion_2.setText("")
        self.tf_Farmaceutico_edad_2.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se elimino el farmaceutico exitosamente!.")
        msgBox.exec_()

    def AccionEliminarPropietario(self):
        doc = db[self.tf_propietario_id.text()]
        db.delete(doc)
        self.tf_propietario_id.setText("")
        self.tf_propietario_nombre.setText("")
        self.tf_propietario_direccion.setText("")
        self.tf_propietario_edad.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se elimino el propietario exitosamente!.")
        msgBox.exec_()

    def AccionEliminarProducto(self):
        doc = db[self.tf_Producto_id.text()]
        db.delete(doc)
        self.tf_Producto_id.setText("")
        self.tf_Producto_nombre.setText("")
        self.tf_Producto_Fabricante.setText("")
        self.tf_Producto_precioCoste.setText("")
        self.tf_Producto_Categoria.setText("")
        self.tf_Producto_DescripcionProducto.setPlainText("")
        msgBox = QMessageBox()
        msgBox.setText("Se elimino el producto exitosamente!.")
        msgBox.exec_()

    def AccionEliminarLaboratorio(self):
        doc = db[self.tf_Laboratorio_id.text()]
        db.delete(doc)
        self.tf_Laboratorio_id.setText("")
        self.tf_Laboratorio_nombre.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se elimino el laboratorio exitosamente!.")
        msgBox.exec_()

    def AccionEliminarFarmacia(self):
        doc = db[self.tf_Farmacia_codigoFarm.text()]
        db.delete(doc)
        self.bt_load.setEnabled(True)
        self.tf_Farmacia_codigoFarm.settext('')
        self.tf_Farmacia_Ciudad.settext('')
        self.tf_Farmacia_departamento.settext('')
        self.tf_Farmacia_calle.settext('')
        msgBox = QMessageBox()
        msgBox.setText("Se elimino la farmacia exitosamente!.")
        msgBox.exec_()

    def agregarFarmacia(self):
        cod = self.tf_Farmacia_codigoFarm.text()
        ciudad = self.tf_Farmacia_Ciudad.text()
        departamento = self.tf_Farmacia_departamento.text()
        calle = self.tf_Farmacia_calle.text()
        doc = {
            '_id': cod,
            "direccion":{ "ciudad": ciudad,
                         "departamento": departamento,
                         "calle":calle
                         },
            "almacenes":almacenes,
            "propietarios":propietarios,
            "farmaceuticos":farmaceuticos,
            "tipo":"farmacia"
        }
        db.save(doc)
        self.bt_load.setEnabled(True)
        self.tf_Farmacia_codigoFarm.setText('')
        self.tf_Farmacia_Ciudad.setText('')
        self.tf_Farmacia_departamento.setText('')
        self.tf_Farmacia_calle.setText('')
        msgBox = QMessageBox()
        msgBox.setText("Se agrego la farmacia exitosamente!.")
        msgBox.exec_()

    def loadComboboxes(self):
        torequest=requests.get('http://127.0.0.1:5984/test2/_design/list/_view/personas')
        doc=torequest.json().get('rows')
        self.cb_Farmacia_Propietarios.clear()
        for e in doc:
            self.cb_Farmacia_Propietarios.addItem(e.get('key'))
        torequest=requests.get('http://127.0.0.1:5984/test2/_design/list/_view/personas')
        doc=torequest.json().get('rows')
        self.cb_Farmacia_farmaceuticos.clear()
        for e in doc:
            self.cb_Farmacia_farmaceuticos.addItem(e.get('key'))
        torequest=requests.get('http://127.0.0.1:5984/test2/_design/list/_view/almacenes')
        doc=torequest.json().get('rows')
        self.cb_almaneces.clear()
        for e in doc:
            self.cb_almaneces.addItem(e.get('key'))



    def loadPropietarios(self):
        self.cb_Farmacia_Propietarios.clear()
        for e in propietarios:
            self.cb_Farmacia_Propietarios.addItem(e)


    def agregarProductos(self):
        id = self.tf_Producto_id.text()
        nombre = self.tf_Producto_nombre.text()
        fabricante = self.tf_Producto_Fabricante.text()
        seguro = self.cb_Producto_TieneProteccion.currentText()
        preciocoste=self.tf_Producto_precioCoste.text()
        categoria = self.tf_Producto_Categoria.text()
        descripcion = self.tf_Producto_DescripcionProducto.toPlainText()
        doc = {
            '_id': id,
            'nombre': nombre,
            'fabricante': fabricante,
            'precioCosto': preciocoste,
            'precioVenta': '',
            'cantidad': '',
            'seguro': seguro,
            'categoria': categoria,
            'descripcion': descripcion,
            'tipo':"producto"

        }
        db.save(doc)
        self.tf_Producto_id.setText("")
        self.tf_Producto_nombre.setText("")
        self.tf_Producto_Fabricante.setText("")
        self.tf_Producto_precioCoste.setText("")
        self.tf_Producto_Categoria.setText("")
        self.tf_Producto_DescripcionProducto.setPlainText("")
        msgBox = QMessageBox()
        msgBox.setText("Se agrego el producto exitosamente!.")
        msgBox.exec_()

    def agregarLaboratorio(self):
        id = self.tf_Laboratorio_id.text()
        nombre = self.tf_Laboratorio_nombre.text()
        array=[]
        doc = {
            '_id': id,
            'nombre': nombre,
            'productos':array,
            'tipo':'laboratorio'

        }
        db.save(doc)
        self.tf_Laboratorio_id.setText("")
        self.tf_Laboratorio_nombre.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se agrego el laboratorio exitosamente!.")
        msgBox.exec_()

    def agregarPropietario(self):
        id = self.tf_propietario_id.text()
        nombre = self.tf_propietario_nombre.text()
        direccion = self.tf_propietario_direccion.text()
        edad = self.tf_propietario_edad.text()
        persona = ("Propietario")

        doc = {
            '_id': id,
            'nombre': nombre,
            'direccion': direccion,
            'edad': edad,
            'tipo': 'persona'

        }
        db.save(doc)
        self.tf_propietario_id.setText("")
        self.tf_propietario_nombre.setText("")
        self.tf_propietario_direccion.setText("")
        self.tf_propietario_edad.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se agrego el propietario exitosamente!.")
        msgBox.exec_()

    def agregarFarmaceutico(self):
        id = self.tf_Farmaceutico_id_2.text()
        nombre = self.tf_Farmaceutico_nombre_2.text()
        direccion = self.tf_Farmaceutico_direccion_2.text()
        edad = self.tf_Farmaceutico_edad_2.text()
        persona = ("Farmaceutico")
        doc = {
            '_id': id,
            'nombre': nombre,
            'direccion': direccion,
            'edad': edad,
            'tipo': 'persona'


        }
        db.save(doc)
        self.tf_Farmaceutico_id_2.setText("")
        self.tf_Farmaceutico_nombre_2.setText("")
        self.tf_Farmaceutico_direccion_2.setText("")
        self.tf_Farmaceutico_edad_2.setText("")
        msgBox = QMessageBox()
        msgBox.setText("Se agrego el farmaceutico exitosamente!.")
        msgBox.exec_()





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
