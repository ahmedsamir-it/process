from flask import Flask, render_template, request, jsonify, send_file
import re
import openpyxl
from io import BytesIO
from googletrans import Translator
from hijri_converter import convert
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    input_words = request.form.get('inputWords', '')
    words_array = list(filter(None, input_words.splitlines()))
    processed_words = []

    for word in words_array:
        processed_word = word.strip().replace(' ', '')
        processed_words.append(processed_word)
    
    return jsonify(processed_words)

@app.route('/clear', methods=['POST'])
def clear_results():
    return jsonify([])

@app.route('/export', methods=['POST'])
def export_to_excel():
    data = request.json.get('data', [])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Processed Data"

    for row in data:
        ws.append([row])
    
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    
    return send_file(stream, as_attachment=True, download_name="ProcessedData.xlsx")

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text', '')
    lang_pair = data.get('langPair', '')

    if lang_pair == 'ar-en':
        target_lang = 'en'
    elif lang_pair == 'en-ar':
        target_lang = 'ar'
    else:
        return jsonify({'error': 'Invalid language pair'}), 400
    
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    
    return jsonify({'translated_text': translation.text})

@app.route('/convert-date', methods=['POST'])
def convert_date():
    date_to_convert = request.form.get('dateToConvert', '')
    conversion_type = request.form.get('conversionType', '')

    if not date_to_convert:
        return jsonify({'error': 'No date provided'}), 400

    try:
        if conversion_type == 'gregorian-hijri':
            date_obj = datetime.strptime(date_to_convert, '%Y-%m-%d')
            hijri_date = convert.Gregorian(date_obj.year, date_obj.month, date_obj.day).to_hijri()
            converted_date = f"{hijri_date.year}-{hijri_date.month:02d}-{hijri_date.day:02d}"
        elif conversion_type == 'hijri-gregorian':
            hijri_year, hijri_month, hijri_day = map(int, date_to_convert.split('-'))
            gregorian_date = convert.Hijri(hijri_year, hijri_month, hijri_day).to_gregorian()
            converted_date = gregorian_date.strftime('%Y-%m-%d')
        else:
            return jsonify({'error': 'Invalid conversion type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'converted_date': converted_date})

if __name__ == '__main__':
    app.run(debug=True)
