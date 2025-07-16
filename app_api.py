from fastapi import FastAPI, Request, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel


app = FastAPI()

#загрузка модели
with open('best_rf.pkl', 'rb') as f:
    model = pickle.load(f)

#счетчик запросов

request_count = 0

#модель для валидации входных данных
class PredictionInput(BaseModel):
    ЛСК_донора: float
    ОК_донора: float
    Возраст: int
    Диам_донора_х_10: int
    

@app.get('/stats')
def stats():
    return {'request count': request_count}

@app.get('/health')
def health():
    return {'status': 'OK'}

@app.post('/predict_model')
def predict_model(input_data: PredictionInput):
    global request_count
    request_count +=1

    new_data = pd.DataFrame({
        'ЛСК_донора': [input_data.ЛСК_донора],
        'ОК_донора': [input_data.ОК_донора],
        'Возраст': [input_data.Возраст],
        'Диам_донора х 10': [input_data.Диам_донора_х_10],
        
    })

    proba = model.predict_proba(new_data)[0][1]  # вероятность класса 1 (несостоятельность)
    percent = round(proba * 100, 2)  # округляем до сотых

    return {'probability': percent}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5000)