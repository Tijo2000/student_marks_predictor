from flask import Flask, render_template, request
from flask import jsonify
import requests
import pickle
import numpy as np
import pandas as pd
import sklearn
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
#model = pickle.load(open("student_marks_prediction_using_linear_regression.pkl","rb"))
model = joblib.load("student_marks_prediction_using_linear_regression.pkl")

df=pd.DataFrame()

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    
    global df
    
    input_features = [float(x) for x in request.form.values()]
    features_value = np.array(input_features)
    
    if input_features[0] <0 or input_features[0] >24:
        return render_template('index.html', prediction_text="Please enter valid hours between 1 to 24 if you live on the Earth") 
       
    output = model.predict([features_value])[0].round(2)
    
    # input and predicted value store in df then save in csv file
    df= pd.concat([df,pd.DataFrame({'Study Hours':input_features,'Predicted Output':[output]})],ignore_index=True)
    print(df)   
    df.to_csv('smp_data_from_app.csv')

    return render_template('index.html', Prediction_text='You will get {}% marks, if you study {} hours per day '.format(output, int(features_value[0])))
    #return render_template('index.html', Prediction_text = f"you will get {output}% marks, when you study {input_features} hours per day")

if __name__ == '__main__':
    app.debug = True
    app.run()
