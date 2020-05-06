import pandas as pd
from keras.models import model_from_json
from pickle import load
import json
import datetime

class LoanModel:
    def __init__(self):
        self.__model = None
        with open('D:\\Workspace\\VisualStudioProj\\WindowsToPythonAI\\python_model\\model.json', 'r') as json_file:
            loaded_model_json = json_file.read()
            self.__model = model_from_json(loaded_model_json)
            self.__model.load_weights("D:\\Workspace\\VisualStudioProj\\WindowsToPythonAI\\python_model\\model.h5")
            self.__model.compile(optimizer ='adam',loss='binary_crossentropy', metrics =['accuracy'])
        
        self.__scaler = load(open('D:\\Workspace\\VisualStudioProj\\WindowsToPythonAI\\python_model\\scaler.pkl', 'rb'))
        self.__grade_encoder = load(open('D:\\Workspace\\VisualStudioProj\\WindowsToPythonAI\\python_model\\grade_encoder.pkl', 'rb'))
        self.__ownership_encoder = load(open('D:\\Workspace\\VisualStudioProj\\WindowsToPythonAI\\python_model\\ownership_encoder.pkl', 'rb'))
        self.__purpose_encoder = load(open('D:\\Workspace\\VisualStudioProj\\WindowsToPythonAI\\python_model\\purpose_encoder.pkl', 'rb'))

    def predict_this(self, json_arguments):
        de_serialized_args = json.loads(json_arguments)
        pd_input = self.get_input_params( de_serialized_args["model_input"] )
        
        prediction = self.__model.predict(pd_input)
        result = "GRANTED" if prediction[0][0] > 0.8 else "REJECTED"
        return_obj = {
            "prediction" : result,
            "timestamp" : str(datetime.datetime.now())
        }

        
        return json.dumps(return_obj)
        
    def get_input_params(self, input_obj):
        grade = pd.Series(input_obj['grade'])
        home_ownership = pd.Series(input_obj['home_ownership'])
        purpose = pd.Series(input_obj['purpose'])
    
        pd_input = pd.DataFrame({
            'loan_amnt': [ input_obj['loan_amnt'] ],
            'int_rate': [ input_obj['int_rate'] ],
            'installment': [ input_obj['installment'] ],
            'grade': [ self.__grade_encoder.transform( grade ) ],
            'emp_length': [ input_obj['emp_length'] ],
            'home_ownership': [ self.__ownership_encoder.transform( home_ownership ) ],
            'annual_inc': [ input_obj['annual_inc'] ],
            'purpose': [ self.__purpose_encoder.transform( purpose ) ],
            'inq_last_12m': [ input_obj['inq_last_12m'] ],
            'delinq_2yrs': [ input_obj['delinq_2yrs'] ]
        })

        pd_input = self.__scaler.transform( pd_input )
        return pd_input
        
if ( __name__ == '__main__' ):
    print("Testing Keras model from Windows Forms application")
