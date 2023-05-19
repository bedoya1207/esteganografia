import tkinter as tk
import cv2
import numpy as np

def has_watermark(image_path):
    # Abre la imagen utilizando OpenCV
    image = cv2.imread(pathmarca.get())

    # Divide los canales de la imagen en R, G y B
    red_channel, green_channel, blue_channel = cv2.split(image)

    # Extrae los bits menos significativos de cada canal
    red_bits = (red_channel & 0x01).flatten()
    green_bits = (green_channel & 0x01).flatten()
    blue_bits = (blue_channel & 0x01).flatten()

    # Comprueba si hay bits 1 en los canales R, G y B
    if np.any(red_bits) or np.any(green_bits) or np.any(blue_bits):
        mensaje="existe marca"
        mensajefunca.config(text=" " + mensaje)
        return True
    else:
        mensaje="no existe marca"
        mensajefunca.config(text=" " + mensaje)
        return False




def hide_watermark(image_path, text):
    # Abre la imagen utilizando OpenCV

    image = cv2.imread(txtpathentradamarca.get())
    text=txtmarca.get()
    # Convierte el texto en una lista de caracteres ASCII
    ascii_values = [ord(char) for char in text]

    # Verifica si el tamaño del texto es mayor que el número de píxeles en la imagen
    num_pixels = image.shape[0] * image.shape[1]
    if len(ascii_values) > num_pixels:
        raise ValueError("El texto es demasiado largo para ocultarlo en la imagen.")

    # Divide los canales de la imagen en R, G y B
    red_channel, green_channel, blue_channel = cv2.split(image)

    # Oculta cada carácter en el bit menos significativo de cada canal
    for i, ascii_value in enumerate(ascii_values):
        row = i // image.shape[1]
        col = i % image.shape[1]

        # Actualiza el canal rojo
        red_pixel = red_channel[row, col]
        new_red_pixel = (red_pixel & 0xFE) | ((ascii_value & 0x80) >> 7)
        red_channel[row, col] = new_red_pixel

        # Actualiza el canal verde
        green_pixel = green_channel[row, col]
        new_green_pixel = (green_pixel & 0xFE) | ((ascii_value & 0x40) >> 6)
        green_channel[row, col] = new_green_pixel

        # Actualiza el canal azul
        blue_pixel = blue_channel[row, col]
        new_blue_pixel = (blue_pixel & 0xFE) | ((ascii_value & 0x20) >> 5)
        blue_channel[row, col] = new_blue_pixel

    # Combina los canales R, G y B para obtener la imagen resultante
    result_image = cv2.merge((red_channel, green_channel, blue_channel))

    # Guarda la imagen con la marca de agua oculta
    cv2.imwrite("marcaimagen.png", result_image)





def encodef5(path, texto):
    path = entrada1.get()
    texto = entrada2.get()
    img = cv2.imread(path)
    height, width, _ = img.shape
    message_len = len(texto)
    if message_len * 8 > height * width:
        raise ValueError("El mensaje es demasiado largo para la imagen")

    binary_message = ''.join(format(ord(c), '08b') for c in texto)
    binary_message += '0' * (height * width - message_len * 8)

    np_message = np.array(list(binary_message)).astype(int)
    np_message = np_message.reshape(height, width)

    img[..., 0] = ((img[..., 0] & ~1) | np_message).astype(np.uint8)
    cv2.imwrite('imagen_ocultaF5.png', img)


def decodeF5(encoded_image_path):
    encoded_image_path=entradaDecript.get()
    img = cv2.imread(encoded_image_path)
    binary_message = ''
    for row in img:
        for pixel in row:
            binary_message += str(pixel[0] & 1)

    binary_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    mensaje = ''.join([chr(int(c, 2)) for c in binary_message])
    salida.config(text="texto recibido "+ mensaje)
    return salida
def ocultar_lsb(imagen, mensaje):
    # Convertir mensaje a binario

    imagen = cv2.imread(entradapath.get())
    mensaje = entradatxt.get()
    mensaje_bin = ''.join(format(ord(i), '08b') for i in mensaje)
    mensaje_bin += '11111111'  # Agregar marca de fin de mensaje

    # Obtener dimensiones de la imagen
    filas, columnas, _ = imagen.shape

    # Ocultar mensaje en el LSB del canal azul de la imagen
    idx_mensaje = 0
    for fila in range(filas):
        for col in range(columnas):
            # Obtener valor del pixel
            pixel = imagen[fila, col]

            # Obtener valor en binario del canal azul del pixel
            azul_bin = format(pixel[0], '08b')

            # Cambiar último bit del canal azul por el bit del mensaje
            azul_bin = azul_bin[:-1] + mensaje_bin[idx_mensaje]

            # Convertir nuevo valor binario a decimal
            azul_dec = int(azul_bin, 2)

            # Crear nuevo pixel con el canal azul modificado
            nuevo_pixel = (azul_dec, pixel[1], pixel[2])

            # Asignar nuevo pixel a la imagen
            imagen[fila, col] = nuevo_pixel

            # Incrementar índice del mensaje
            idx_mensaje += 1

            # Salir del bucle si se ha ocultado todo el mensaje
            if idx_mensaje == len(mensaje_bin):
                break

        if idx_mensaje == len(mensaje_bin):
            break
    cv2.imwrite("imagen_ocultaLSB.png", imagen)

    return imagen

def extraer_lsb(imagen):
    # Obtener dimensiones de la imagen
    imagen= cv2.imread(Entradalsb.get())
    filas, columnas, _ = imagen.shape

    # Extraer mensaje del LSB del canal azul de la imagen
    mensaje_bin = ''
    for fila in range(filas):
        for col in range(columnas):
            # Obtener valor del pixel
            pixel = imagen[fila, col]

            # Obtener valor en binario del canal azul del pixel
            azul_bin = format(pixel[0], '08b')

            # Obtener último bit del canal azul y añadirlo al mensaje
            mensaje_bin += azul_bin[-1]

            # Si se ha encontrado la marca de fin de mensaje, decodificar el mensaje y salir del bucle
            if mensaje_bin[-8:] == '11111111':
                mensaje_bin = mensaje_bin[:-8]
                mensaje = bytearray(int(mensaje_bin[i:i+8], 2) for i in range(0, len(mensaje_bin), 8)).decode()
                salidalsb.config(text="texto recibido"+mensaje)
                return salidalsb

    # Si no se ha encontrado la marca de fin de mensaje, devolver mensaje vacío
    return ''

def main():
 global ventana
 ventana = tk.Tk()
 ventana.title("Algoritmos de Esteganografia")
 ventana.geometry("350x200")
 label_1= tk.Label(ventana, text="Algoritmos de Estagnografia")
 label_1.pack()
 botonF5=tk.Button(ventana,text="Algoritmo F5",command=pantalla_F5)
 botonF5.pack()
 botonLSB=tk.Button(ventana, text="algoritmo LSB", command=pantalla_LSB)
 botonLSB.pack()
 botonMarca=tk.Button(ventana, text="marca de agua", command=pantalla_marca)
 botonMarca.pack()
 ventana.mainloop()



def pantalla_F5():
  global pantalla_F
  global entrada1
  global entrada2
  global entradaDecript
  global salida
  ventana.withdraw()
  pantalla_F=tk.Toplevel()
  pantalla_F.title("Algoritmo F5")
  pantalla_F.geometry("700x700")
  labelT=tk.Label(pantalla_F,text="algoritmo de encriptacion y desencriptacion F5")
  labelT.pack()
  def regresar():
   pantalla_F.destroy()
   ventana.deiconify()
  etiqueta1 = tk.Label(pantalla_F, text="path de la imagen :")
  etiqueta1.pack()
  entrada1 = tk.Entry(pantalla_F)
  entrada1.pack()
  etiqueta2 = tk.Label(pantalla_F, text="texto :")
  etiqueta2.pack()
  entrada2 = tk.Entry(pantalla_F)
  entrada2.pack()

  btnEncriptar = tk.Button(pantalla_F, text="encriptar", command=lambda:encodef5(entrada1,entrada2))
  btnEncriptar.pack()
  entradaDecript= tk.Entry(pantalla_F)
  entradaDecript.pack()
  btndesencriptar= tk.Button(pantalla_F,text="desencriptar",command=lambda:decodeF5(entradaDecript))
  btndesencriptar.pack()
  salida=tk.Label(pantalla_F,text="texto recibido")
  salida.pack()
  btnRegresar=tk.Button(pantalla_F,text="Regresar", command=regresar)
  btnRegresar.pack()
  pantalla_F.mainloop()


def pantalla_LSB():
  global pantalla_LSB
  global entradatxt
  global entradapath
  global Entradalsb
  global salidalsb
  ventana.withdraw()
  pantalla_LSB=tk.Toplevel()
  pantalla_LSB.title("Algoritmo LSB")
  pantalla_LSB.geometry("700x700")
  labelT2=tk.Label(pantalla_LSB,text="algoritmo de encriptacion y desencriptacion LSB")
  labelT2.pack()
  labeltxt=tk.Label(pantalla_LSB,text="ingrese el texto")
  labeltxt.pack()
  entradatxt=tk.Entry(pantalla_LSB)
  entradatxt.pack()
  labelpath=tk.Label(pantalla_LSB,text="ingrese path de la imagen")
  labelpath.pack()
  entradapath=tk.Entry(pantalla_LSB)
  entradapath.pack()
  btnencriptar=tk.Button(pantalla_LSB,text="encriptar",command=lambda:ocultar_lsb(entradapath,entradatxt))
  btnencriptar.pack()
  labelsalida=tk.Label(pantalla_LSB,text="ingrese path de imagen oculta")
  labelsalida.pack()
  Entradalsb=tk.Entry(pantalla_LSB)
  Entradalsb.pack()
  btndesencriptar=tk.Button(pantalla_LSB,text="desencriptar",command=lambda:extraer_lsb(Entradalsb))
  btndesencriptar.pack()
  salidalsb=tk.Label(pantalla_LSB,text="texto recibido")
  salidalsb.pack()
  def regresar():
   pantalla_LSB.destroy()
   ventana.deiconify()
  btnRegresar1 = tk.Button(pantalla_LSB, text="Regresar", command=regresar)
  btnRegresar1.pack()
  pantalla_LSB.mainloop()
def pantalla_marca():
  global pantalla_marca
  global txtpathentradamarca
  global txtmarca
  global txtguardaren
  global pathmarca
  global mensajefunca
  ventana.withdraw()
  pantalla_marca=tk.Toplevel()
  pantalla_marca.title("Marca de Agua")
  pantalla_marca.geometry("700x700")
  labelT3=tk.Label(pantalla_marca,text="Marca de agua")
  labelT3.pack()
  labelpathimagen=tk.Label(pantalla_marca,text="ingresar path de la imagen de entrada")
  labelpathimagen.pack()
  txtpathentradamarca=tk.Entry(pantalla_marca)
  txtpathentradamarca.pack()
  labeltextomarca=tk.Label(pantalla_marca,text="ingrese texto para la marca de agua")
  labeltextomarca.pack()
  txtmarca=tk.Entry(pantalla_marca)
  txtmarca.pack()
  btncrearmarca=tk.Button(pantalla_marca,text="crear marca de agua",command=lambda:hide_watermark(txtpathentradamarca
                                                                                              ,txtmarca))
  btncrearmarca.pack()
  labelverifica=tk.Label(pantalla_marca,text="VERIFICACION")
  labelverifica.pack()
  labelpathfin=tk.Label(pantalla_marca,text="ingrese path imagen ")
  labelpathfin.pack()
  pathmarca=tk.Entry(pantalla_marca)
  pathmarca.pack()
  btnverify=tk.Button(pantalla_marca,text="verificar",command=lambda:has_watermark(pathmarca))
  btnverify.pack()
  mensajefunca=tk.Label(pantalla_marca,text="existe marca: ")
  mensajefunca.pack()
  def regresar():
   pantalla_marca.destroy()
   ventana.deiconify()
  btnRegresar2=tk.Button(pantalla_marca,text="regresar", command=regresar)
  btnRegresar2.pack()
  pantalla_marca.mainloop()


if __name__=="__main__":
  main()
