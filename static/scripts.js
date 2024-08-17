function processInput() {
    const inputWords = document.getElementById('inputWords').value;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ inputWords: inputWords })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultBox').innerHTML = data.map(item => `<div>${item}</div>`).join('');
    })
    .catch(error => console.error('Error:', error));
}

function clearResults() {
    document.getElementById('inputWords').value = '';
    document.getElementById('resultBox').innerHTML = '';
}

function exportToExcel() {
    const data = Array.from(document.querySelectorAll('#resultBox div')).map(div => div.textContent);

    fetch('/export', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: data })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ProcessedData.xlsx';
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error:', error));
}

function setLanguage(langPair) {
    document.getElementById('languageDropdown').innerText = langPair === 'ar-en' ? 'Arabic to English' : 'English to Arabic';
    document.getElementById('languageDropdown').setAttribute('data-langpair', langPair);
}

function translateText() {
    const text = document.getElementById('inputText').value;
    const langPair = document.getElementById('languageDropdown').getAttribute('data-langpair');

    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text, langPair: langPair })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('translationResult').innerText = data.translated_text;
    })
    .catch(error => console.error('Error:', error));
}

function clearTranslation() {
    document.getElementById('inputText').value = '';
    document.getElementById('translationResult').innerText = '';
}

function convertDate() {
    const dateToConvert = document.getElementById('dateInput').value;
    const conversionType = document.getElementById('conversionType').value;

    fetch('/convert-date', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ dateToConvert: dateToConvert, conversionType: conversionType })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('dateConversionResult').innerText = data.converted_date;
    })
    .catch(error => console.error('Error:', error));
}
