from flask import Flask, render_template, request, send_file
import os
from utils.converter import convert_csv_to_vcf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    csv_file = request.files['csv_file']
    contact_name = request.form['contact_name']
    country_code = request.form['country_code']

    if csv_file:
        filepath = os.path.join('temp.csv')
        csv_file.save(filepath)
        vcf_data = convert_csv_to_vcf(filepath, contact_name, country_code)
        os.remove(filepath)
        return (
            vcf_data,
            200,
            {
                'Content-Type': 'text/vcard',
                'Content-Disposition': f'attachment; filename={contact_name}.vcf'
            }
        )
    return "No file uploaded", 400

if __name__ == '__main__':
    app.run(debug=True)