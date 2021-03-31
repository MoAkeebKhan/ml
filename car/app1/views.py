from django.shortcuts import render,redirect
import pickle
import datetime
model = pickle.load(open("RandomForestModel.pkl", "rb"))
scaled = pickle.load(open("Scaler.sav", "rb"))
ManufaturerDict = {
                    'Ford':1,'Maruti':2,'Honda':3,'Audi':4,'Nissan':5,'Hyundai':6,'Mahindra':7,'Tata':8,'BMW':9,'Skoda':10,
                    'Porsche':11,'Toyota':12,'Chevrolet':13,'Mercedes-Benz':14,'Land':15,'Force':16,'Volkswagen':17,
                    'Renault':18,'Jaguar':19,'Volvo':20,'Mini':21,'Mitsubishi':22,'Fiat':23,'Ambassador':24,'Datsun':25,
                    'ISUZU':26,'Jeep':27,'Bentley':28,'Smart':29,'Lamborghini':30
                    }
FuelTypeDict = {
                    'Diesel':1,'Petrol':2,'CNG':3,'LPG':4,'Electric':5
}
OwnerTypeDict = {
                    'First':1,'Second':2,'Third':3,'Fourth and above':4
}
TransmissionDict = {
                    'Mannual':1,'Automatic':0
}

def home(request):
    return render(request,'index.html')

def usedCarEvaluation(request):
    return render(request,'pred.html')

def predict(request):
    if request.method == 'POST':
        Year = request.POST.get('Year')
        Kilometers_Driven = request.POST.get('Kilometers_Driven')
        Mileage = request.POST.get('Mileage')
        Engine = request.POST.get('Engine')
        Power = request.POST.get('Power')
        Seats = request.POST.get('Seats')
        Manufacturer = request.POST.get('Manufacturer')
        Fuel_Type = request.POST.get('Fuel_Type')
        Transmission = request.POST.get('Transmission')
        Owner_Type = request.POST.get('Owner_Type')
        Model = request.POST.get('Model')

        curr_time = datetime.datetime.now()
        Year1 = curr_time.year - int(Year)

        if Manufacturer in ManufaturerDict:
            Manufacturer1 = ManufaturerDict[Manufacturer]
        else:
            print("Not found")

        if Fuel_Type in FuelTypeDict:
            Fuel_Type1 = FuelTypeDict[Fuel_Type]
        else:
            print("Not found")

        if Transmission in TransmissionDict:
            Transmission1 = TransmissionDict[Transmission]
        else:
            print("Not found") 

        if Owner_Type in OwnerTypeDict:
            Owner_Type1 = OwnerTypeDict[Owner_Type]
        else:
            print("Not found")
        prediction = model.predict(scaled.transform([[Year1,Kilometers_Driven,Mileage,Engine,Power,Seats,Manufacturer1,Fuel_Type1,Transmission1,Owner_Type1]]))
        error = (prediction[0]/100) * 15

        answer = round((prediction[0]-error), 2)
        good_condition = round(answer - 0.40,2)
        print(answer)
        print(abs(good_condition))
        context = {"Year":Year,"Kilometers_Driven":Kilometers_Driven,"Mileage":Mileage,"Engine":Engine,"Power":Power,
                    "Seats":Seats,"Manufacturer":Manufacturer,"Fuel_Type":Fuel_Type,"Transmission":Transmission,
                    "Owner_Type":Owner_Type,"Model":Model,"Answer":answer,"Good":good_condition,
                }
    return render(request,'results.html',context)



#         prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
#         output=round(prediction[0],2)
#         if output<0:
#             return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
#         else:
#             return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
#     else:
#         return render_template('index.html')



