from __future__ import absolute_import
from pprint import pprint
import os
from flask import Flask, render_template, request, session, abort, flash, url_for, send_file
from detect_intent_texts import detect_intent_texts, line_manipulator
from read_attributes import get_columns, get_file_name
from werkzeug.utils import secure_filename, redirect
from API_manager import enter_new_entity
import DB_Manager
from entities import create_attribute_dict

app = Flask(__name__)

app.secret_key = "AS9UjjJI0J0JS9j"

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'session_pc'
# UPLOAD_FOLDER = '/home/madusha/'
UPLOAD_FOLDER = '/media/madusha/DA0838CA0838A781/PC_Interface/Resources'
ALLOWED_EXTENSIONS = set(['csv', 'txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
url_ds_attributes = 'https://api.dialogflow.com/v1/entities/ds_attributes'
url_ds_name = 'https://api.dialogflow.com/v1/entities/Dataset_Name'
data_set_name = ''


@app.route('/payload', methods=['POST'])
def payload():
    if not request.json:
        abort(400)
    if request.json:
        response = request.json
        pprint(response)

    try:
        content = request.json['queryResult']
        print("_" * 20)
        pprint(content)

    except:
        print("JSON not found")

    return 'none'


@app.route('/send_message', methods=['POST'])
def send_message():
    message = "Hi, Name please"
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text}
    print(response_text)


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/find/<string:name>/")
def hello(name):
    return render_template('found_wim_phone.html', name=name)


@app.route('/home', methods=['GET'])
def search():
    try:
        phone_price = request.form['price']

        users = findUsersByPrice(phone_price)
        return render_template('home.html', ph_price=phone_price, users_list=users)
    except:
        return render_template('home.html')


@app.route('/pc', methods=['GET'])
def receive_pseudo_code():
    try:
        pseudocode = request.form['pcode']
        lines_raw = pseudocode.split('\n')
        lines = []
        for l in lines_raw:
            if l is not '' and l is not '\r':
                lines.append(l)
        DB_Manager.insert_pseudocode_into_db(lines)
        return render_template('result1.html', statements=lines)
    except:
        return render_template('input_form1.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/ds', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            global data_set_name
            data_set_name = filename
            create_attribute_dict.find_filename(data_set_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            columns = get_columns(UPLOAD_FOLDER + '/' + filename)
            file_names = get_file_name(filename)
            enter_new_entity(file_names, url_ds_name, 'Dataset_Name')
            enter_new_entity(columns, url_ds_attributes, 'ds_attributes')
            return render_template('pseudocode_input.html', filename=filename)
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return render_template('input_form1.html')


@app.route('/intermediate', methods=['GET', 'POST'])
def generate_intermediate_code():
    lines = DB_Manager.get_pseudocode_from_db()[0]
    # full_pc = ""
    full_pc = line_manipulator(lines, data_set_name)
    # for line in lines:
    #     pc = detect_intent_texts(PROJECT_ID, SESSION_ID, line, 'en-US')
    #     full_pc = full_pc + '\n' + pc

    print(full_pc[0])
    f = open("ipc.txt", "w+")
    f.write(full_pc[0])
    DB_Manager.delete_all_documents("pseudocodes_temp")
    DB_Manager.insert_standard_pc_into_db(full_pc[1])
    return render_template('result1.html', statements=full_pc[1])


@app.route('/sc', methods=['GET'])
def generate_source_code():
    try:
        pseudocode = request.form['pcode']
        print(pseudocode)
        return render_template('result2.html', name=user_name, phone_cs_list=set(phones))
    except:
        return render_template('input_form2.html')


@app.route('/evl', methods=['GET'])
def evaluate_results():
    try:
        user_name = request.form['username']
        agegroup = request.form['age']
        phones = teenPhone(agegroup)
        print(phones)

        return render_template('result3.html', name=user_name, phone_age_list=phones)
    except:
        return render_template('input_form3.html')


@app.route('/about', methods=['GET'])
def about():
    try:
        user_name = request.form['username']
        brand_name = request.form['brandname']
        os = request.form['os']

        return render_template('result4.html', name=user_name)
    except:
        return render_template('input_form4.html')


app.add_url_rule('/pc', 'pc', receive_pseudo_code, methods=['GET', 'POST'])
app.add_url_rule('/ds', 'ds', upload_file, methods=['GET', 'POST'])
app.add_url_rule('/intermediate', 'intermediate', generate_intermediate_code, methods=['GET', 'POST'])
app.add_url_rule('/sc', 'sc', generate_source_code, methods=['GET', 'POST'])
app.add_url_rule('/eval', 'eval', evaluate_results, methods=['GET', 'POST'])
app.add_url_rule('/about', 'about', about, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(host='localhost', port=3550, debug=True)
