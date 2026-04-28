# # app.py 
# from flask import Flask, render_template, request
# import pandas as pd
# import pickle

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/process_file', methods=['POST'])

# def process_file():
#     if 'file' not in request.files:
#         return "No file part"

#     file = request.files['file']

#     if file.filename == '':
#         return "No selected file"

#     if file:
#         file_data = file.read()
#         df = pd.read_excel(file_data)
#         # labels_and_values = list(zip(df.columns, df.iloc[0]))     
#         labels_and_values = [row.to_dict() for _, row in df.iterrows()]
#         h = labels_and_values
#         s = []
#         for row in h:
#             for i,j in row:
#                 s.append(j)
            
#                 mdvp_fo=s[4]
#                 mdvp_fhi=s[5]
#                 mdvp_flo=s[6]
#                 mdvp_jitper=s[7]
#                 mdvp_jitabs=s[8]
#                 mdvp_rap=s[9]
#                 mdvp_ppq=s[10]
#                 jitter_ddp=s[11]
#                 mdvp_shim=s[12]
#                 mdvp_shim_db=s[13]
#                 shimm_apq3=s[14]
#                 shimm_apq5=s[15]
#                 mdvp_apq=s[16]
#                 shimm_dda=s[17]
#                 nhr=s[18]
#                 hnr=s[19]
#                 rpde=s[20]
#                 dfa=s[21]
#                 spread1=s[22]
#                 spread2=s[23]
#                 d2=s[24]
#                 ppe=s[25]
#                 filename = 'modelForPrediction.sav'
#                 loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
#                 # predictions using the loaded model file
#                 scaler = pickle.load(open('standardScalar.sav', 'rb'))
#                 prediction=loaded_model.predict(scaler.transform([[mdvp_fo,mdvp_fhi,mdvp_flo,mdvp_jitper, mdvp_jitabs,
#                     mdvp_rap,mdvp_ppq, jitter_ddp, mdvp_shim, mdvp_shim_db,shimm_apq3,shimm_apq5,mdvp_apq,shimm_dda,nhr,hnr,rpde,dfa,spread1,spread2,d2,ppe]]))
#                 print('prediction is', prediction)
#                 if prediction == 1:
#                     pred = "You have Supranuclear Palsy Disease. Please consult a specialist."
#                 else:
#                     pred = "You are Healthy Person."
#                 return render_template('results.html', labels_and_values=labels_and_values,s=pred)


# if __name__ == '__main__':
#     app.run(debug=True)    

# =================================================================================================================

# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import pandas as pd
import pickle
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def add_basic_info_in_processed_data(processed_data, result):
    for i in range(len(processed_data)):
        processed_data[i]["basic_info"] = {}
        for key, value in result[i].items():
            processed_data[i]["basic_info"][key] = value       
        processed_data[i]["basic_info"]["prediction"] = processed_data[i]["prediction"]

@app.route('/process_file', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        file_data = file.read()
        df = pd.read_excel(file_data)

        # SELECTING THE 4 COLUMNS
        dff = pd.read_excel(file_data)
        columns = dff.iloc[:, :4]
        result = columns.to_dict(orient='records')

        labels_and_values = [row.to_dict() for _, row in df.iterrows()]

        processed_data = []
        pre1 = []

        for row in labels_and_values:
            s = []
            pre2 = {}
            for i, j in row.items():
                s.append(j)
                
            mdvp_fo=s[4]
            mdvp_fhi=s[5]
            mdvp_flo=s[6]
            mdvp_jitper=s[7]
            mdvp_jitabs=s[8]
            mdvp_rap=s[9]
            mdvp_ppq=s[10]
            jitter_ddp=s[11]
            mdvp_shim=s[12]
            mdvp_shim_db=s[13]
            shimm_apq3=s[14]
            shimm_apq5=s[15]
            mdvp_apq=s[16]
            shimm_dda=s[17]
            nhr=s[18]
            hnr=s[19]
            rpde=s[20]
            dfa=s[21]
            spread1=s[22]
            spread2=s[23]
            d2=s[24]
            ppe=s[25]

            # Loading the model and making a prediction
            filename = 'modelForPrediction.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            scaler = pickle.load(open('standardScalar.sav', 'rb'))
            prediction=loaded_model.predict(scaler.transform([[mdvp_fo,mdvp_fhi,mdvp_flo,mdvp_jitper, mdvp_jitabs,
                mdvp_rap,mdvp_ppq, jitter_ddp, mdvp_shim, mdvp_shim_db,shimm_apq3,shimm_apq5,mdvp_apq,shimm_dda,nhr,hnr,rpde,dfa,spread1,spread2,d2,ppe]]))

            # Assigning the prediction result
            if prediction == 1:
                pred = "You have Supranuclear Palsy Disease. Please consult a specialist."
            else:
                pred = "You are a Healthy Person."
            pre2["prediction"] = pred
            pre1.append(pre2)
            processed_data.append({'labels_and_values': row, 'prediction': pred})

        add_basic_info_in_processed_data(processed_data, result)

        for_visualize = [data["basic_info"] for data in processed_data]
        csv_file_path = 'macxi.csv'
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Name ', 'Age', 'Gender', 'Year', 'prediction']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write the data
            for row in for_visualize:
                writer.writerow(row)

        # Corrected redirection to 'results' endpoint
        return render_template('results.html', processed_data=processed_data)
        


csv_file_path = 'C:/Users/admin/Desktop/PSP/macxi.csv'
df = pd.read_csv(csv_file_path)

@app.route('/viz')
def viz():
    years = df['Year'].unique()
    return render_template('viz.html', years=sorted(years))

@app.route('/ins', methods=['POST'])
def ins():
    selected_year = int(request.form['selected_year'])
    filtered_df = df[df['Year'] == selected_year]

    chart_data = {
        'labels': filtered_df['Gender'].unique().tolist(),
        'datasets': [
            {
                'label': 'PSP',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'data': filtered_df[filtered_df['prediction'] == 'You have Supranuclear Palsy Disease. Please consult a specialist.']['Gender'].value_counts().tolist(),
            },
            {
                'label': 'No PSP',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'data': filtered_df[filtered_df['prediction'] == 'You are a Healthy Person.']['Gender'].value_counts().tolist(),
            },
        ],
    }

    return jsonify(chart_data)


if __name__ == '__main__':
    app.run(debug=True)


















# =============================================================================
#                      DON'T TOUCH THE CODE BELOW
# =============================================================================

# app.py 
# from flask import Flask, render_template, request
# import pandas as pd
# import pickle

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/process_file', methods=['POST'])
# def process_file():
#     if 'file' not in request.files:
#         return "No file part"

#     file = request.files['file']

#     if file.filename == '':
#         return "No selected file"

#     if file:
#         file_data = file.read()
#         df = pd.read_excel(file_data)
#         labels_and_values = [row.to_dict() for _, row in df.iterrows()]
#         processed_data = []
#         for row in labels_and_values:
#             s = []
#             for i,j in row.items():
#                 s.append(j)
            
#             mdvp_fo=s[4]
#             mdvp_fhi=s[5]
#             mdvp_flo=s[6]
#             mdvp_jitper=s[7]
#             mdvp_jitabs=s[8]
#             mdvp_rap=s[9]
#             mdvp_ppq=s[10]
#             jitter_ddp=s[11]
#             mdvp_shim=s[12]
#             mdvp_shim_db=s[13]
#             shimm_apq3=s[14]
#             shimm_apq5=s[15]
#             mdvp_apq=s[16]
#             shimm_dda=s[17]
#             nhr=s[18]
#             hnr=s[19]
#             rpde=s[20]
#             dfa=s[21]
#             spread1=s[22]
#             spread2=s[23]
#             d2=s[24]
#             ppe=s[25]
#             filename = 'modelForPrediction.sav'
#             loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
#             scaler = pickle.load(open('standardScalar.sav', 'rb'))
#             prediction=loaded_model.predict(scaler.transform([[mdvp_fo,mdvp_fhi,mdvp_flo,mdvp_jitper, mdvp_jitabs,
#                 mdvp_rap,mdvp_ppq, jitter_ddp, mdvp_shim, mdvp_shim_db,shimm_apq3,shimm_apq5,mdvp_apq,shimm_dda,nhr,hnr,rpde,dfa,spread1,spread2,d2,ppe]]))
#             print('prediction is', prediction)
#             if prediction == 1:
#                 pred = "You have Supranuclear Palsy Disease. Please consult a specialist."
#             else:
#                 pred = "You are Healthy Person."
#             processed_data.append({'labels_and_values': row, 'prediction': pred})
#         return render_template('results.html', processed_data=processed_data)


# if __name__ == '__main__':
#     app.run(debug=True)   

        
        # dom = {}
        # for i, inner_list in enumerate(pre1,start=1):
        #     value = inner_list[0]
        #     key = f"Prediction"
        #     dom[key] = value



# ===============================================================
#                               CHART
# ===============================================================

# @app.route('/get_chart_data', methods=['POST'])
# def get_chart_data():
#     selected_year = int(request.form['selected_year'])
#     df = pd.read_csv('macxi.csv')
#     filtered_df = df[df['Year'] == selected_year]

#     chart_data = {
#         'labels': filtered_df['Gender'].unique().tolist(),
#         'datasets': [
#             {
#                 'label': 'Supranuclear Palsy Disease',
#                 'backgroundColor': 'rgba(75, 192, 192, 0.2)',
#                 'borderColor': 'rgba(75, 192, 192, 1)',
#                 'data': filtered_df[filtered_df['prediction'] == 'You have Supranuclear Palsy Disease. Please consult a specialist.']['Gender'].value_counts().tolist(),
#             },
#             {
#                 'label': 'Healthy Person',
#                 'backgroundColor': 'rgba(255, 99, 132, 0.2)',
#                 'borderColor': 'rgba(255, 99, 132, 1)',
#                 'data': filtered_df[filtered_df['prediction'] == 'You are Healthy Person.']['Gender'].value_counts().tolist(),
#             },
#         ],
#     }

#     return jsonify(chart_data)




# ===========================================================
#                           FINAL CODE STEP 1
# ===========================================================

# app.py
# from flask import Flask, render_template, request, redirect, url_for
# import pandas as pd
# import pickle
# import csv

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# def add_basic_info_in_processed_data(processed_data, result):
#     for i in range(len(processed_data)):
#         processed_data[i]["basic_info"] = {}
#         for key, value in result[i].items():
#             processed_data[i]["basic_info"][key] = value       
#         processed_data[i]["basic_info"]["prediction"] = processed_data[i]["prediction"]

# @app.route('/process_file', methods=['POST'])
# def process_file():
#     if 'file' not in request.files:
#         return "No file part"

#     file = request.files['file']

#     if file.filename == '':
#         return "No selected file"

#     if file:
#         file_data = file.read()
#         df = pd.read_excel(file_data)

#         # SELECTING THE 4 COLUMNS
#         dff = pd.read_excel(file_data)
#         columns = dff.iloc[:, :4]
#         result = columns.to_dict(orient='records')

#         labels_and_values = [row.to_dict() for _, row in df.iterrows()]

#         processed_data = []
#         pre1 = []

#         for row in labels_and_values:
#             s = []
#             pre2 = {}
#             for i, j in row.items():
#                 s.append(j)
                
#             mdvp_fo=s[4]
#             mdvp_fhi=s[5]
#             mdvp_flo=s[6]
#             mdvp_jitper=s[7]
#             mdvp_jitabs=s[8]
#             mdvp_rap=s[9]
#             mdvp_ppq=s[10]
#             jitter_ddp=s[11]
#             mdvp_shim=s[12]
#             mdvp_shim_db=s[13]
#             shimm_apq3=s[14]
#             shimm_apq5=s[15]
#             mdvp_apq=s[16]
#             shimm_dda=s[17]
#             nhr=s[18]
#             hnr=s[19]
#             rpde=s[20]
#             dfa=s[21]
#             spread1=s[22]
#             spread2=s[23]
#             d2=s[24]
#             ppe=s[25]

#             # Loading the model and making a prediction
#             filename = 'modelForPrediction.sav'
#             loaded_model = pickle.load(open(filename, 'rb'))
#             scaler = pickle.load(open('standardScalar.sav', 'rb'))
#             prediction=loaded_model.predict(scaler.transform([[mdvp_fo,mdvp_fhi,mdvp_flo,mdvp_jitper, mdvp_jitabs,
#                 mdvp_rap,mdvp_ppq, jitter_ddp, mdvp_shim, mdvp_shim_db,shimm_apq3,shimm_apq5,mdvp_apq,shimm_dda,nhr,hnr,rpde,dfa,spread1,spread2,d2,ppe]]))

#             # Assigning the prediction result
#             if prediction == 1:
#                 pred = "You have Supranuclear Palsy Disease. Please consult a specialist."
#             else:
#                 pred = "You are a Healthy Person."
#             pre2["prediction"] = pred
#             pre1.append(pre2)
#             processed_data.append({'labels_and_values': row, 'prediction': pred})

#         add_basic_info_in_processed_data(processed_data, result)

#         for_visualize = [data["basic_info"] for data in processed_data]
#         csv_file_path = 'macxi.csv'
#         with open(csv_file_path, 'w', newline='') as csvfile:
#             fieldnames = ['Name ', 'Age', 'Gender', 'Year', 'prediction']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#             # Write the header
#             writer.writeheader()

#             # Write the data
#             for row in for_visualize:
#                 writer.writerow(row)

#         # Corrected redirection to 'results' endpoint
#         return render_template('results.html', processed_data=processed_data)
#         # return redirect(url_for('results'))

# @app.route('/viz')
# def viz():
#     return render_template('viz.html')


# @app.route('/get_chart_data', methods=['POST'])
# def get_chart_data():
#     selected_year = int(request.form['selected_year'])
#     df = pd.read_csv('macxi.csv')
#     filtered_df = df[df['Year'] == selected_year]

#     chart_data = {
#         'labels': filtered_df['Gender'].unique().tolist(),
#         'datasets': [
#             {
#                 'label': 'Yes',
#                 'backgroundColor': 'rgba(75, 192, 192, 0.2)',
#                 'borderColor': 'rgba(75, 192, 192, 1)',
#                 'data': filtered_df[filtered_df['Prediction'] == 'Yes']['Gender'].value_counts().tolist(),
#             },
#             {
#                 'label': 'No',
#                 'backgroundColor': 'rgba(255, 99, 132, 0.2)',
#                 'borderColor': 'rgba(255, 99, 132, 1)',
#                 'data': filtered_df[filtered_df['Prediction'] == 'No']['Gender'].value_counts().tolist(),
#             },
#         ],
#     }

#     return chart_data


# if __name__ == '__main__':
#     app.run(debug=True)