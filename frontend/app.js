// API Gateway URL
const API_URL = 'http://localhost:8000/api';

// Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const uploadLoader = document.getElementById('uploadLoader');
const uploadProcessing = document.getElementById('uploadProcessing');
const uploadStatus = document.getElementById('uploadStatus');
const processSection = document.getElementById('processSection');
const fileId = document.getElementById('fileId');
const processBtn = document.getElementById('processBtn');
const processLoader = document.getElementById('processLoader');
const processProcessing = document.getElementById('processProcessing');
const processStatus = document.getElementById('processStatus');
const resultBox = document.getElementById('resultBox');
const processingTypeSelect = document.getElementById('processingType');
const typeDescription = document.getElementById('typeDescription');

// Step indicators
const step1 = document.getElementById('step1');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');

let selectedFile = null;
let currentFileId = null;
let processingTypes = [];

// Update step indicator
function updateStep(stepNumber) {
    [step1, step2, step3].forEach((step, index) => {
        if (index + 1 < stepNumber) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (index + 1 === stepNumber) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    });
}

// Upload area click
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFile(e.dataTransfer.files[0]);
});

// Handle file selection
function handleFile(file) {
    if (!file) return;

    // Validate file type
    const validTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel'
    ];

    if (!validTypes.includes(file.type) && !file.name.match(/\.(xlsx|xls)$/i)) {
        showStatus(uploadStatus, 'error', '❌ Please select a valid Excel file (.xlsx or .xls)');
        return;
    }

    // Check file size (50MB)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        showStatus(uploadStatus, 'error', '❌ File too large. Maximum size is 50MB');
        return;
    }

    selectedFile = file;
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    fileName.textContent = `${file.name} (${fileSizeMB} MB)`;
    fileInfo.classList.add('show');
    uploadBtn.disabled = false;
    uploadStatus.classList.remove('show');
}

// Upload button click
uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    uploadBtn.disabled = true;
    uploadLoader.classList.add('show');
    uploadProcessing.style.display = 'block';
    uploadStatus.classList.remove('show');
    processSection.style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || response.statusText);
        }

        const data = await response.json();
        currentFileId = data.file_id;

        showStatus(uploadStatus, 'success', `✅ File uploaded successfully! File ID: ${data.file_id.substring(0, 8)}...`);
        fileId.textContent = data.file_id;
        processSection.style.display = 'block';

        // Update to step 2
        updateStep(2);

        // Smooth scroll to process section
        setTimeout(() => {
            processSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 300);

    } catch (error) {
        showStatus(uploadStatus, 'error', `❌ Upload failed: ${error.message}`);
        uploadBtn.disabled = false;
    } finally {
        uploadLoader.classList.remove('show');
        uploadProcessing.style.display = 'none';
    }
});

// Load processing types on page load
async function loadProcessingTypes() {
    try {
        const response = await fetch(`${API_URL}/process/types`);
        if (response.ok) {
            const data = await response.json();
            processingTypes = data.processing_types;
            console.log('✅ Processing types loaded:', processingTypes.length);
        }
    } catch (error) {
        console.error('❌ Failed to load processing types:', error);
    }
}

// Processing type change
processingTypeSelect.addEventListener('change', (e) => {
    const selectedType = e.target.value;
    if (selectedType) {
        const typeInfo = processingTypes.find(t => t.type === selectedType);
        if (typeInfo && typeInfo.config) {
            const config = typeInfo.config;
            let description = `📋 Collections: ${config.collections ? config.collections.join(', ') : 'N/A'}`;
            if (config.description) {
                description += ` | ${config.description}`;
            }
            typeDescription.textContent = description;
        } else {
            typeDescription.textContent = `Processing type: ${selectedType}`;
        }
        typeDescription.style.color = '#475569';
    } else {
        typeDescription.textContent = 'Select a processing type to see details';
        typeDescription.style.color = '#64748b';
    }
});

// Process button click
processBtn.addEventListener('click', async () => {
    if (!currentFileId) return;

    const processingType = processingTypeSelect.value;
    if (!processingType) {
        showStatus(processStatus, 'error', '❌ Please select a processing type');
        return;
    }

    processBtn.disabled = true;
    processLoader.classList.add('show');
    processProcessing.style.display = 'block';
    processStatus.classList.remove('show');
    resultBox.style.display = 'none';

    // Update to step 3
    updateStep(3);

    try {
        const response = await fetch(`${API_URL}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_id: currentFileId,
                processing_type: processingType
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || response.statusText);
        }

        const data = await response.json();

        const successMessage = `✅ ${data.message || 'Processing completed!'}
📊 Records: ${data.records_processed}
🔑 Join Key: ${data.join_key_used}
📁 Collections: ${data.collection_used}`;

        showStatus(processStatus, 'success', successMessage);

        // Show result details with syntax highlighting
        resultBox.style.display = 'block';
        resultBox.innerHTML = `<pre>${syntaxHighlight(JSON.stringify(data, null, 2))}</pre>`;

        // Mark step 3 as completed
        step3.classList.add('completed');
        step3.classList.remove('active');

        // Smooth scroll to results
        setTimeout(() => {
            resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 300);

    } catch (error) {
        showStatus(processStatus, 'error', `❌ Processing failed: ${error.message}`);
        // Stay on step 3 but not completed
    } finally {
        processLoader.classList.remove('show');
        processProcessing.style.display = 'none';
        processBtn.disabled = false;
    }
});

// Show status message with auto-hide for success messages
function showStatus(element, type, message) {
    element.className = `status show ${type}`;
    element.textContent = message;

    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            element.classList.remove('show');
        }, 5000);
    }
}

// Syntax highlighting for JSON
function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        let cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
                return '<span style="color: #a78bfa; font-weight: 600;">' + match + '</span>';
            } else {
                cls = 'string';
                return '<span style="color: #86efac;">' + match + '</span>';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
            return '<span style="color: #fbbf24;">' + match + '</span>';
        } else if (/null/.test(match)) {
            cls = 'null';
            return '<span style="color: #ef4444;">' + match + '</span>';
        }
        return '<span style="color: #60a5fa;">' + match + '</span>';
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + U to trigger upload
    if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
        e.preventDefault();
        if (!uploadBtn.disabled && selectedFile) {
            uploadBtn.click();
        }
    }

    // Ctrl/Cmd + P to trigger process
    if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
        e.preventDefault();
        if (!processBtn.disabled && processingTypeSelect.value) {
            processBtn.click();
        }
    }
});

// Show welcome message
console.log('%c🚀 Data Processing Platform', 'font-size: 20px; font-weight: bold; color: #667eea;');
console.log('%cKeyboard Shortcuts:', 'font-size: 14px; font-weight: bold; color: #64748b;');
console.log('%c  Ctrl/Cmd + U: Upload file', 'font-size: 12px; color: #94a3b8;');
console.log('%c  Ctrl/Cmd + P: Process data', 'font-size: 12px; color: #94a3b8;');

// Load processing types when page loads
loadProcessingTypes();

// Add smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';
