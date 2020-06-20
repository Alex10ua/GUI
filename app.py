
from tkinter import *
from tkinter import filedialog, Text, Image, Label, messagebox
import os
from PIL import Image, ImageTk
import numpy as np
import matplotlib as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import cv2

root = Tk()
root.geometry("600x600")
canvas = Canvas(width=350, height=400, bg='black')
imag_e = Label(image='')
#opened_model = ''
def take_image():

    image_path = filedialog.askopenfilename(initialdir="/", title='Вибір зображення',
                                          filetypes=([("Image File", '.jpg')]))
    if image_path =="":
        messagebox.showerror("Помилка", "Зобараження не було вибрано.")
    else:
        get_result(image_path)

def get_result(image_path):

    new_model = load_model("covid_model.h5")


    new_model.summary()
    img_width, img_height = 224, 224
    img = image.load_img(image_path,
                         target_size=(img_width, img_height))
    x = image.img_to_array(img)
    img = np.expand_dims(x, axis=0)

    pred = new_model.predict(img)
    print(pred)# норм тут
    print(np.argmax(pred, axis=1))
    prediction=np.argmax(pred, axis=1)

    im = Image.open(image_path)
    resized = im.resize((350, 400), Image.ANTIALIAS)
    resized.save("result.jpg")
    print_on_image = ''
    if prediction == 0:
        print_on_image = 'Covid-19'
    else:
        print_on_image = 'Non_Covid-19'

    image_cv=cv2.imread("result.jpg")
    output=image_cv.copy()
    cv2.putText(output, print_on_image, (10, 390), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.imwrite("result_name.jpg",output)

    #gif1 = PhotoImage(file="result_name.gif")
    #canvas.create_image(244, 244, image=gif1, anchor=NW)


    new_image=Image.open("result_name.jpg")
    tkimage = ImageTk.PhotoImage(new_image)

    imag_e.config(image=tkimage)
    imag_e.image = tkimage
    imag_e.pack(side = "bottom", fill = "both", expand = "yes")


def clear_canvas():
    #canvas.delete('all')
    imag_e.config(image='')

#def take_model():
#    opened_model=filedialog.askopenfilename(initialdir="/", title='Вибір моделі',
#                                          filetypes=([("HDF", '.h5')]))
#    print(opened_model)
#    if opened_model =='':
#        messagebox.showerror("Помилка", "Модель не була вибрана. Повторіть спробу")
#    else:messagebox.showinfo("Вибрана модель","Шлях до моделі: "+opened_model)


openFile = Button(root, text="Get image", command=take_image)
openFile.pack()
clear_field=Button(root,text='Clear', command=clear_canvas)
clear_field.pack()
#openModel= Button(root, text="Open model", command=take_model)
#openModel.pack()

root.mainloop()