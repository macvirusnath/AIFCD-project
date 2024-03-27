import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from sklearn.utils import resample
from sklearn.preprocessing import LabelEncoder
import re
from sklearn.ensemble import RandomForestClassifier

# arry = ['1', '2', '30', '24500.0', '400',	'3', '0', '1.0']

def fraud_detect(arrayInput):
    df=pd.read_csv('./fraud_oracle.csv')
    df.head()

    oversamp=resample(df[df['FraudFound_P']==1],
                 replace=True,
                 n_samples=len(df[df['FraudFound_P']==0]),
                 random_state=30)
    df1=pd.concat([oversamp, df[df['FraudFound_P']==0]])
    Months_list=['Nov','Jul','Dec','Oct','Sep','Aug','Apr','Jun','Feb','Jan','May','Mar']
    Days_list=[ 'Sunday', 'Saturday','Wednesday','Thursday','Tuesday', 'Friday', 'Monday']
    pd.DataFrame(df1.groupby('Make').count()['FraudFound_P'].sort_values()).index

    Make_list=['Lexus', 'Ferrari', 'Porche', 'Jaguar', 'Mecedes', 'BMW', 'Nisson',
       'Saturn', 'Dodge', 'Mercury', 'Saab', 'VW', 'Ford', 'Accura',
       'Chevrolet', 'Mazda', 'Honda', 'Toyota', 'Pontiac']
    df1.groupby('Make').count()['FraudFound_P'].sort_values()

    df2=df1[['Make', 'AccidentArea','Sex','MaritalStatus', 'Age', 'Fault', 'PolicyType', 'VehicleCategory',
         'VehiclePrice','Deductible', 'DriverRating','PastNumberOfClaims', 'AgeOfVehicle',
         'AgeOfPolicyHolder', 'PoliceReportFiled', 'WitnessPresent', 'AgentType','NumberOfSuppliments', 
         'AddressChange_Claim', 'NumberOfCars', 'Year','BasePolicy','FraudFound_P']]
    
    df2['Make']=df2['Make'].replace({'Lexus':0, 'Ferrari':1, 'Porche':2, 'Jaguar':3, 'Mecedes':4, 'BMW':5, 'Nisson':6,
       'Saturn':7, 'Dodge':8, 'Mercury':9, 'Saab':10, 'VW':11, 'Ford':12, 'Accura':13, 
       'Chevrolet':14, 'Mazda':15, 'Honda':16, 'Toyota':17, 'Pontiac':18})
    
    df2['Fault']=LabelEncoder().fit_transform(df2['Fault'])

    df2.AccidentArea=LabelEncoder().fit_transform(df2['AccidentArea'])
    df2.Sex=LabelEncoder().fit_transform(df2['Sex'])
    df2.AccidentArea=LabelEncoder().fit_transform(df2['AccidentArea'])
    df2.MaritalStatus=LabelEncoder().fit_transform(df2['MaritalStatus'])
    df2.PolicyType=LabelEncoder().fit_transform(df2['PolicyType'])
    df2.VehicleCategory=LabelEncoder().fit_transform(df2['VehicleCategory'])
    df2.PoliceReportFiled=LabelEncoder().fit_transform(df2['PoliceReportFiled'])
    df2.WitnessPresent=LabelEncoder().fit_transform(df2['WitnessPresent'])
    df2.AgentType=LabelEncoder().fit_transform(df2['AgentType'])
    df2.BasePolicy=LabelEncoder().fit_transform(df2['BasePolicy'])

    df2.NumberOfSuppliments=df2['NumberOfSuppliments'].replace('none',0)
    df2.NumberOfSuppliments=df2['NumberOfSuppliments'].str.replace('\D','',regex=True)
    df2.NumberOfSuppliments=df2.NumberOfSuppliments.fillna(0)

    df2.AddressChange_Claim=df2['AddressChange_Claim'].replace('no change',0)
    df2.AddressChange_Claim=df2['AddressChange_Claim'].str.replace('\D','',regex=True)
    df2.AddressChange_Claim=df2['AddressChange_Claim'].fillna(0)

    df2.AgeOfVehicle=df2['AgeOfVehicle'].replace('new',1)
    df2.AgeOfVehicle=df2['AgeOfVehicle'].str.replace('\D','',regex=True)
    df2.AgeOfVehicle=df2['AgeOfVehicle'].fillna(1)

    def strcon(a):
        number=re.findall(r'\d+',a)
        if len(number)==2:
            return (int(number[0])+int(number[1]))/2
        elif len(number)==1:
            return int(number[0])
        else:
            return 0
        
    df2.VehiclePrice=df2['VehiclePrice'].apply(strcon)
    df2.AgeOfPolicyHolder=round(df2['AgeOfPolicyHolder'].apply(strcon))
    df2.NumberOfCars=round(df2['NumberOfCars'].apply(strcon))

    df2.PastNumberOfClaims=df2['PastNumberOfClaims'].replace({'1':1, 'none':0, '2 to 4':2, 'more than 4':4})

    df2.AgeOfVehicle=df2['AgeOfVehicle'].astype('int')
    df2.NumberOfSuppliments=df2['NumberOfSuppliments'].astype('int')
    df2.AddressChange_Claim=df2['AddressChange_Claim'].astype('int')

    df2.NumberOfCars.unique()

    df2.drop(['BasePolicy','Fault','PolicyType','PastNumberOfClaims','Year','NumberOfSuppliments','AgentType',
         'PastNumberOfClaims', 'AgeOfVehicle','AgeOfPolicyHolder', 'PoliceReportFiled', 'WitnessPresent',
         'VehicleCategory','Make','AccidentArea'],axis='columns',inplace=True)
    
    x=df2.drop('FraudFound_P',axis='columns')
    y=df2.FraudFound_P
    from sklearn.model_selection import train_test_split
    x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=20,test_size=0.2)
    print(df2.shape)

    model=RandomForestClassifier()
    model.fit(x_train,y_train)

    print(model.score(x_test,y_test))
    arrr1 = np.array(arrayInput)
    x_pred = arrr1.reshape(1, -1)
    #x_pred = np.array([[1,2,30,24500.0,400,3,0,1.0], [1, 1, 42, 20000.0, 400, 1, 0, 1.0]])
    y_pred = model.predict(x_pred)
    print(y_pred)
    print("Hello")

    return y_pred


# fraud_detect(arry)