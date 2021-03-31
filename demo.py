from flask import Flask
from flask import jsonify
import sqlite3
import pandas as pd
import numpy as np
import json
# flask restful api
from flask_restful import Api
from flask_restful import Resource
# CORS
from flask_cors import CORS


# flask setting
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False
# 跨域設定> 目前全開與前端溝通
CORS(app)
api = Api(app)

# test data
tpe = {
    "id": 0,
    "city_name": "TAIPEI",
    "country_name": "台灣",
    "longitude": 121.569,
    "latitude": 25.003,
}
city = [tpe]

# from sqlite3 to pandas
# 時間關係就沒有細寫 以下是處理其他SQLite 後做好的API
db_root = 'DPPATH'
conn = sqlite3.connect(db_root)
df = pd.read_sql_query("SELECT * FROM DetailUrlFile", conn)
conn.commit()
conn.close()

# dataframe to list for jsonify for api /realestate
data_list = []
df_rows = df.shape[0]
for i in range(df_rows):
    ser = df.loc[i, :]
    row_dict = {}
    for idx, val in zip(ser.index, ser.values):
        if type(val) is str:
            row_dict[idx] = val
        elif type(val) is np.int64:
            row_dict[idx] = int(val)
        elif type(val) is np.float64:
            row_dict[idx] = float(val)
    data_list.append(row_dict)

# dataframe insert new column to match google map api
df['LatiLong'] = pd.Series(dtype='object')
for j in range(df_rows):
    tmp_lati = df['Latitude'][j]
    tmp_long = df['Longitude'][j]
    input_data = [tmp_lati, tmp_long]
    df['LatiLong'][j] = input_data
change_to_json = df.to_json(orient="records")
estate_data = json.loads(change_to_json)

@app.route('/', methods=['GET'])
def hello_world():
    return "hello world"

@app.route('/cities/all', methods=['GET'])
def city_all():
    return jsonify(city)

@app.route('/realestate', methods=['GET'])
def cafe_land():
    return jsonify(data_list)


class Estate_Restful(Resource):
    def get(self):
        return estate_data

api.add_resource(Estate_Restful, "/estate/")

if __name__ == '__main__':
    app.run()