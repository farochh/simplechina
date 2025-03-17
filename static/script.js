function handleFileUpload(action) {
    console.log('Файл загружается...');

    let fileInput;
    switch (action) {
        case 'addHieroglyphs':
            fileInput = document.getElementById('addFileInputHieroglyphs');
            break;
        case 'addTranslation':
            fileInput = document.getElementById('addTranslationInput');
            break;
		case 'deleteHieroglyphs':
			fileInput = document.getElementById('deleteFileInput');
			break;
		case 'deleteTranslation':
			fileInput = document.getElementById('deleteTranslationInput');
			break;
        default:
            updateStatusMessage('Неизвестное действие');
            return;
    }

    if (!fileInput.files.length) {
        updateStatusMessage('Выберите файл перед отправкой.');
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        try {
            const fileContent = JSON.parse(e.target.result); 
            console.log("Файл JSON:", fileContent);
            sendDataToServer(fileContent, action); 
        } catch (error) {
            console.error('Ошибка парсинга JSON:', error);
            updateStatusMessage('Ошибка: Неверный формат JSON.');
        }
    };

    reader.readAsText(file);
}

function sendDataToServer(data, action) {
    let apiUrl;
    switch (action) {
        case 'addHieroglyphs':
            apiUrl = 'https://cm41785.tw1.ru/api/add';  // Укажите ваш хостинг-домен
            break;
        case 'addTranslation':
            apiUrl = 'https://cm41785.tw1.ru/api/upload_translations';
            break;
        case 'deleteHieroglyphs':
            apiUrl = 'https://cm41785.tw1.ru/api/delete';
            break;
        case 'deleteTranslation':
            apiUrl = 'https://cm41785.tw1.ru/api/delete_translation';
            break;
        default:
            updateStatusMessage('Неизвестное действие');
            return;
    }

    console.log("Отправляемые данные JSON:", JSON.stringify({ data }));
    
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data }) 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        console.log("Ответ сервера:", result);
        updateStatusMessage(`Операция ${action} завершена: ${result.message}`);
    })
    .catch(error => {
        console.error("Ошибка выполнения:", error);
        updateStatusMessage(`Ошибка выполнения: ${error}`);
    });
}

function uploadTranslations() {
    const fileInput = document.getElementById('uploadTranslationsInput');
    const statusDiv = document.getElementById('uploadStatus');

    if (!fileInput.files.length) {
        statusDiv.textContent = 'Выберите файл перед отправкой.';
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        const fileContent = e.target.result;
        try {
            const jsonData = JSON.parse(fileContent);

            fetch('https://cm41785.tw1.ru/api/upload_translations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ data: jsonData })
            })
                .then((response) => response.json())
                .then((result) => {
                    statusDiv.textContent = `Результат: ${result.message}`;
                })
                .catch((error) => {
                    statusDiv.textContent = `Ошибка: ${error}`;
                });
        } catch (error) {
            statusDiv.textContent = 'Неверный формат JSON.';
        }
    };

    reader.readAsText(file);
}

function handleTranslationsDelete() {
    const fileInput = document.getElementById('deleteTranslationsFileInput');

    if (!fileInput.files.length) {
        updateStatusMessage('Выберите файл перед отправкой.');
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const fileContent = e.target.result;

        fetch('https://cm41785.tw1.ru/api/delete_translations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: JSON.parse(fileContent) })
        })
        .then(response => response.json())
        .then(result => {
            updateStatusMessage(`Операция ${action} завершена: ${result.message}`);
        })
        .catch(error => {
            updateStatusMessage(`Ошибка удаления переводов: ${error}`);
        });
    };

    reader.readAsText(file);
}

function updateStatusMessage(message) {
    document.getElementById('statusMessage').textContent = message;
}