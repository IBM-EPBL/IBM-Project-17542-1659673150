from flask import Flask, render_template, request, redirect, url_for, session, redirect, Response,flash
import requests
import ibm_db
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder  
from flask_mail import Mail,Message
import numpy as np 
import matplotlib.pyplot as plt 

# from flask_session import Session

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="2k19cse075@kiot.ac.in"
app.config['MAIL_PASSWORD']="2k075cse19"
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)

app.secret_key='r'

global email

@app.route('/')
@app.route("/entry",methods=["POST"])
def entry():
    return render_template("main.html")

@app.route("/login",methods=["POST"])
def login():
    return render_template("main.html")


##prediction code
filename ='resales.sav'
model_rand=pickle.load(open(filename,'rb'))

@app.route('/result', methods = ['GET','POST'])
def result():       
    flash('You were successfully logged in')
    vehicleage = int(request.form['vehicle_age'])
    Km = int(request.form['Km_driven'])
    mileage1 = float(request.form['mileage'])
    engine1 = int(request.form['engine'])
    seats1 = int(request.form['seats'])
    maxpower = float(request.form['max_power'])
    ownertype = int(request.form['owner_type'])
    brand1 = request.form['slct1']
    model1 = request.form['slct2']
    fuel = request.form['fuel_type']
    transmissiontype =request.form['transmission_type']
   
    new_row = {'brand': brand1, 'model':model1,'vehicle_age':vehicleage,'km_driven':Km,'fuel_type':fuel,'transmission_type':transmissiontype,'mileage':mileage1,'engine':engine1,'max_power':maxpower,'seats':seats1,'Owner_type':ownertype}
    print(new_row)
    colunm= ['brand','model','vehicle_age','km_driven','fuel_type','transmission_type','mileage','engine','max_power','seats','Owner_type']
    new_df=pd.DataFrame(colunm) 
    print(new_df) 
    new_df = new_df.append(new_row,ignore_index=True)
    print()
    labels = ['brand','model','fuel_type','transmission_type']
    mapper={}
    for i in labels:
        mapper[i] = LabelEncoder()
        mapper[i].classes = np.load(str('classes' +i+'.npy'),allow_pickle = True)
        tr=mapper[i].fit_transform(new_df[i])
        # print(tr)
        new_df.loc[:,i + '_labels'] = pd.Series(tr,index=new_df.index)
        # print(new_df)

    new_df.dropna(subset=["brand","model"],inplace=True)
    print(new_df)
    print("*******************************************")
    labeled=new_df[['vehicle_age','km_driven','mileage','engine','max_power','seats','Owner_type']+[x+"_labels" for x in labels]]
    X= labeled.values
    print(X)
    print("------------------------------------")
    y_prediction = model_rand.predict(X)
    print(y_prediction)
    output = round(y_prediction[0],2)

    ##chart code
    if request.method=="POST":
        X = ['mileage','engine','max_power']
        user = [mileage1,engine1,maxpower]
        X_axis = np.arange(len(X))

        if(brand1=='Maruti'):
            max=[23.649,82.11,1202]
        elif(brand1=='Hyundai'):
            max=[18.77,103.36,1307]
        elif(brand1=='Ford'):
            max=[19.37,103.34,1421]
        elif(brand1=='Renault'):
            max=[18.03,81.02,1165]
        elif(brand1=='Mercedes-Benz'):
            max=[13.35,196.45,1743]
        elif(brand1=='Volkswagen'):
            max=[17.57,91.81,999]
        elif(brand1=='Honda'):
            max=[20.15,109.04,1581]
        elif(brand1=='Mahindra'):
            max=[17.39,114.32,1609]
        elif(brand1=='Datsun'):
            max=[20.76,65.83,995]
        elif(brand1=='Tata'):
            max=[21.13,112.83,1530]
        elif(brand1=='Kia'):
            max=[18,113.43,1495]
        elif(brand1=='Audi'):
            max=[16,214.52,1991]
        elif(brand1=='Skoda'):
            max=[16.60,161.37,1655]
        elif(brand1=='Bmw'):
            max=[15.66,272.67,2330]
        elif(brand1=='Toyota'):
            max=[13.34,108.05,1563]
        elif(brand1=='Nissan'):
            max=[14.33,123.28,1746]
        elif(brand1=='Jeep'):
            max=[14.9,167.67,1956]
        elif(brand1=='Volvo'):
            max=[11.2,246.74,1998]
        elif(brand1=='Volvo'):
            max=[15.6,120.76,1598]
        else:
            max=[0,0,0,]
        plt.bar(X_axis - 0.2, max, 0.4, label = 'Average_value')
        plt.bar(X_axis + 0.2, user, 0.4, label = 'User_value')

        
  
        plt.xticks(X_axis, X)
        plt.xlabel("user")
        plt.ylabel("values")
        plt.legend()
        plt.savefig('png.png')
        print("saved successfully")
        message=Message('Chart',sender="2k19cse075@kiot.ac.in",recipients=["2k19cse075@kiot.ac.in"])
        with app.open_resource("png.png") as fp:
            message.attach("png.png", "png/png", fp.read())
        mail.send(message)

    return render_template('main.html',prediction="{} Rupees".format(output))

if __name__ =='__main__':
    app.run()