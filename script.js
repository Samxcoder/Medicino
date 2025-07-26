// Configuration
const API_BASE_URL = 'http://localhost:5000'; // Change this to your backend URL

// DOM Elements
const symptomsInput = document.getElementById('symptomsInput');
const diagnoseBtn = document.getElementById('diagnoseBtn');
const voiceBtn = document.getElementById('voiceBtn');
const clearBtn = document.getElementById('clearBtn');
const diagnosisLoader = document.getElementById('diagnosisLoader');
const diagnosisResult = document.getElementById('diagnosisResult');

const medicineInput = document.getElementById('medicineInput');
const searchMedicineBtn = document.getElementById('searchMedicineBtn');
const showAllBtn = document.getElementById('showAllBtn');
const medicineLoader = document.getElementById('medicineLoader');
const medicineInfoResult = document.getElementById('medicineInfoResult');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    console.log('🏥 Medicino Frontend initialized successfully!');
    
    // Add welcome animation
    setTimeout(() => {
        document.body.style.animation = 'fadeIn 0.5s ease-in';
    }, 100);
}

function setupEventListeners() {
    // Symptom diagnosis
    diagnoseBtn.addEventListener('click', handleDiagnosis);
    
    // Voice input
    voiceBtn.addEventListener('click', handleVoiceInput);
    
    // Clear button
    clearBtn.addEventListener('click', () => {
        symptomsInput.value = '';
        hideElement(diagnosisResult);
    });
    
    // Medicine search
    searchMedicineBtn.addEventListener('click', handleMedicineSearch);
    showAllBtn.addEventListener('click', handleShowAllMedicines);
    
    // Enter key support
    symptomsInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            handleDiagnosis();
        }
    });
    
    medicineInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleMedicineSearch();
        }
    });
    
    // Quick actions
    document.getElementById('historyBtn').addEventListener('click', showHistory);
    document.getElementById('emergencyBtn').addEventListener('click', showEmergencyGuide);
    document.getElementById('aboutBtn').addEventListener('click', showAbout);
}

// Diagnosis Functions
async function handleDiagnosis() {
    const symptoms = symptomsInput.value.trim();
    
    if (!symptoms) {
        showNotification('Please enter your symptoms first.', 'warning');
        return;
    }
    
    showLoader(diagnosisLoader);
    hideElement(diagnosisResult);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/diagnose`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symptoms: symptoms })
        });
        
        const result = await response.json();
        
        hideLoader(diagnosisLoader);
        
        if (result.success) {
            displayDiagnosisResult(result.data);
        } else {
            showNotification('Diagnosis failed: ' + result.message, 'error');
        }
        
    } catch (error) {
        hideLoader(diagnosisLoader);
        console.error('Diagnosis error:', error);
        showNotification('Network error. Please check if the backend server is running.', 'error');
    }
}

function displayDiagnosisResult(data) {
    document.getElementById('diseaseOutput').textContent = data.disease;
    document.getElementById('ayurvedicOutput').textContent = data.ayurvedic;
    document.getElementById('medicineOutput').textContent = data.medicine;
    
    // Confidence score
    const confidenceText = document.getElementById('confidenceText');
    const confidenceFill = document.getElementById('confidenceFill');
    
    confidenceText.textContent = `${data.confidence}% confidence - AI analysis based on symptom matching`;
    
    // Animate confidence bar
    setTimeout(() => {
        confidenceFill.style.width = `${data.confidence}%`;
    }, 500);
    
    // Severity badge
    const severityBadge = document.getElementById('severityBadge');
    if (data.severity && data.severity !== 'unknown') {
        severityBadge.innerHTML = `
            <div class="severity-badge severity-${data.severity}">
                <i class="fas fa-exclamation-${data.severity === 'severe' ? 'triangle' : 'circle'}"></i>
                Severity: ${data.severity.toUpperCase()}
            </div>
        `;
    }
    
    showElement(diagnosisResult);
}

// Voice Input Function
function handleVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showNotification('Speech recognition is not supported in this browser. Please use Chrome or Edge.', 'warning');
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        voiceBtn.classList.add('listening');
        voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i> Listening...';
        showNotification('Listening... Please speak your symptoms clearly.', 'info');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        symptomsInput.value = transcript;
        showNotification('Voice input captured successfully!', 'success');
    };

    recognition.onend = () => {
        voiceBtn.classList.remove('listening');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Voice Input';
    };

    recognition.onerror = (event) => {
        voiceBtn.classList.remove('listening');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Voice Input';
        showNotification('Speech recognition error: ' + event.error, 'error');
    };

    recognition.start();
}

// Medicine Search Functions
async function handleMedicineSearch() {
    const medicineName = medicineInput.value.trim();
    
    if (!medicineName) {
        showNotification('Please enter a medicine name.', 'warning');
        return;
    }
    
    showLoader(medicineLoader);
    hideElement(medicineInfoResult);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/medicine/${encodeURIComponent(medicineName)}`);
        const result = await response.json();
        
        hideLoader(medicineLoader);
        
        if (result.success && result.data) {
            displayMedicineResult(result.data);
        } else {
            displayNoMedicineFound(medicineName);
        }
        
    } catch (error) {
        hideLoader(medicineLoader);
        console.error('Medicine search error:', error);
        showNotification('Network error. Please check if the backend server is running.', 'error');
    }
}

async function handleShowAllMedicines() {
    showLoader(medicineLoader);
    hideElement(medicineInfoResult);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/medicines`);
        const result = await response.json();
        
        hideLoader(medicineLoader);
        
        if (result.success) {
            displayAllMedicines(result.data);
        } else {
            showNotification('Failed to load medicines list.', 'error');
        }
        
    } catch (error) {
        hideLoader(medicineLoader);
        console.error('Medicines list error:', error);
        showNotification('Network error. Please check if the backend server is running.', 'error');
    }
}

function displayMedicineResult(medicine) {
    medicineInfoResult.innerHTML = `
        <h3 style="margin-bottom: 1.5rem; color: #f093fb;">
            <i class="fas fa-pill"></i>
            Medicine Details
        </h3>
        <div class="medicine-card">
            <div class="medicine-name">${medicine.name}</div>
            
            <div class="medicine-detail">
                <strong><i class="fas fa-info-circle"></i> Description:</strong>
                <span>${medicine.description}</span>
            </div>
            
            <div class="medicine-detail">
                <strong><i class="fas fa-clock"></i> Dosage:</strong>
                <span>${medicine.dosage}</span>
            </div>
            
            <div class="medicine-detail">
                <strong><i class="fas fa-exclamation-triangle"></i> Side Effects:</strong>
                <span>${medicine.side_effects}</span>
            </div>
            
            <div class="medicine-detail">
                <strong><i class="fas fa-ban"></i> Contraindications:</strong>
                <span>${medicine.contraindications}</span>
            </div>
            
            <div class="medicine-detail">
                <strong><i class="fas fa-tag"></i> Category:</strong>
                <span style="text-transform: capitalize;">${medicine.category || 'General'}</span>
            </div>
            
            <div style="margin-top: 1.5rem; text-align: center;">
                <div class="price-tag">
                    <i class="fas fa-rupee-sign"></i>
                    ${medicine.price}
                </div>
            </div>
        </div>
    `;
    
    showElement(medicineInfoResult);
}

function displayNoMedicineFound(medicineName) {
    medicineInfoResult.innerHTML = `
        <div class="medicine-card" style="text-align: center; border-color: rgba(255, 65, 108, 0.3);">
            <div style="font-size: 3rem; color: #ff416c; margin-bottom: 1rem;">
                <i class="fas fa-search-minus"></i>
            </div>
            <h3 style="color: #ff416c; margin-bottom: 1rem;">Medicine Not Found</h3>
            <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 1.5rem;">
                The medicine "<strong style="color: var(--text-primary);">${medicineName}</strong>" was not found in our database. 
                Please check the spelling or try searching with a different name.
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <button class="btn btn-primary" onclick="document.getElementById('medicineInput').focus()">
                    <i class="fas fa-search"></i>
                    Try Another Search
                </button>
                <button class="btn btn-secondary" onclick="handleShowAllMedicines()">
                    <i class="fas fa-list"></i>
                    Browse All Medicines
                </button>
            </div>
        </div>
    `;
    
    showElement(medicineInfoResult);
}

function displayAllMedicines(medicines) {
    if (!medicines || medicines.length === 0) {
        medicineInfoResult.innerHTML = `
            <div class="medicine-card" style="text-align: center;">
                <h3 style="color: #667eea;">No medicines found in the database.</h3>
            </div>
        `;
        showElement(medicineInfoResult);
        return;
    }

    let medicinesHTML = `
        <h3 style="margin-bottom: 1.5rem; color: #f093fb;">
            <i class="fas fa-pills"></i>
            All Medicines (${medicines.length} found)
        </h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1rem;">
    `;

    medicines.forEach(medicine => {
        medicinesHTML += `
            <div class="medicine-card">
                <div class="medicine-name">${medicine.name}</div>
                
                <div class="medicine-detail">
                    <strong>Description:</strong>
                    <span>${medicine.description.substring(0, 100)}${medicine.description.length > 100 ? '...' : ''}</span>
                </div>
                
                <div class="medicine-detail">
                    <strong>Category:</strong>
                    <span style="text-transform: capitalize;">${medicine.category || 'General'}</span>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                    <div class="price-tag">
                        <i class="fas fa-rupee-sign"></i>
                        ${medicine.price}
                    </div>
                    <button class="btn btn-primary" style="padding: 0.5rem 1rem; font-size: 0.9rem;" 
                            onclick="searchSpecificMedicine('${medicine.name}')">
                        <i class="fas fa-eye"></i>
                        View Details
                    </button>
                </div>
            </div>
        `;
    });

    medicinesHTML += '</div>';
    medicineInfoResult.innerHTML = medicinesHTML;
    showElement(medicineInfoResult);
}

function searchSpecificMedicine(medicineName) {
    medicineInput.value = medicineName;
    handleMedicineSearch();
}

// Quick Actions Functions
async function showHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/history`);
        const result = await response.json();
        
        if (result.success) {
            displayHistory(result.data);
        } else {
            showNotification('Failed to load diagnosis history.', 'error');
        }
    } catch (error) {
        console.error('History error:', error);
        showNotification('Network error. Please check if the backend server is running.', 'error');
    }
}

function displayHistory(historyData) {
    if (!historyData || historyData.length === 0) {
        showModal('Diagnosis History', `
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem; color: #667eea; margin-bottom: 1rem;">
                    <i class="fas fa-history"></i>
                </div>
                <h3 style="color: #667eea; margin-bottom: 1rem;">No History Found</h3>
                <p style="color: var(--text-secondary);">You haven't made any diagnoses yet. Start by entering your symptoms above!</p>
            </div>
        `);
        return;
    }

    let historyHTML = `
        <div style="max-height: 400px; overflow-y: auto;">
            <h4 style="color: #667eea; margin-bottom: 1rem;">Recent Diagnoses (${historyData.length} records)</h4>
    `;

    historyData.slice(0, 10).forEach((record, index) => {
        const date = new Date(record.created_at).toLocaleDateString();
        const time = new Date(record.created_at).toLocaleTimeString();
        
        historyHTML += `
            <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 1rem; margin-bottom: 1rem; border-left: 4px solid #667eea;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong style="color: #667eea;">${record.diagnosed_condition}</strong>
                    <small style="color: var(--text-secondary);">${date} ${time}</small>
                </div>
                <div style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                    <strong>Symptoms:</strong> ${record.symptoms}
                </div>
                <div style="color: var(--text-secondary); font-size: 0.9rem;">
                    Confidence: ${record.confidence_score}%
                </div>
            </div>
        `;
    });

    historyHTML += '</div>';
    showModal('Diagnosis History', historyHTML);
}

function showEmergencyGuide() {
    const emergencyHTML = `
        <div style="color: #ff416c; text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">
                <i class="fas fa-ambulance"></i>
            </div>
            <h3>Emergency Medical Guide</h3>
        </div>
        
        <div style="background: rgba(255, 65, 108, 0.1); border: 2px solid rgba(255, 65, 108, 0.3); border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem;">
            <h4 style="color: #ff416c; margin-bottom: 1rem;">⚠️ When to Call Emergency Services</h4>
            <ul style="color: var(--text-secondary); line-height: 1.8;">
                <li>Difficulty breathing or shortness of breath</li>
                <li>Chest pain or pressure</li>
                <li>Severe allergic reaction</li>
                <li>Loss of consciousness</li>
                <li>Severe bleeding</li>
                <li>Signs of stroke (FAST: Face, Arms, Speech, Time)</li>
            </ul>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; color: #ff416c; margin-bottom: 0.5rem;">🚨</div>
                <strong>Emergency</strong><br>
                <span style="color: var(--text-secondary);">108 / 112</span>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; color: #43e97b; margin-bottom: 0.5rem;">🏥</div>
                <strong>Ambulance</strong><br>
                <span style="color: var(--text-secondary);">108</span>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; color: #667eea; margin-bottom: 0.5rem;">☎️</div>
                <strong>Police</strong><br>
                <span style="color: var(--text-secondary);">100</span>
            </div>
        </div>
        
        <div style="background: rgba(67, 233, 123, 0.1); border: 2px solid rgba(67, 233, 123, 0.3); border-radius: 10px; padding: 1rem; margin-top: 1.5rem;">
            <p style="color: var(--text-secondary); text-align: center; margin: 0;">
                <strong style="color: #43e97b;">Remember:</strong> This app is for informational purposes only. 
                Always consult healthcare professionals for serious symptoms.
            </p>
        </div>
    `;
    
    showModal('Emergency Medical Guide', emergencyHTML);
}

function showAbout() {
    const aboutHTML = `
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 3rem; background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;">
                <i class="fas fa-user-md"></i>
            </div>
            <h3 style="background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">About Medicino</h3>
        </div>
        
        <div style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 1.5rem;">
            <p style="margin-bottom: 1rem;">
                Medicino is an AI-powered medical assistant designed to provide intelligent symptom analysis 
                and medicine information. Our platform combines modern technology with traditional Ayurvedic 
                wisdom to offer comprehensive healthcare guidance.
            </p>
            
            <h4 style="color: #667eea; margin: 1.5rem 0 1rem 0;">🚀 Features:</h4>
            <ul style="margin-left: 1rem;">
                <li>AI-powered symptom diagnosis with confidence scoring</li>
                <li>Comprehensive medicine database with pricing</li>
                <li>Ayurvedic treatment recommendations</li>
                <li>Voice input support for accessibility</li>
                <li>Diagnosis history tracking</li>
                <li>Emergency medical guidance</li>
            </ul>
            
            <h4 style="color: #f093fb; margin: 1.5rem 0 1rem 0;">🛡️ Technology Stack:</h4>
            <ul style="margin-left: 1rem;">
                <li>Frontend: HTML5, CSS3, Vanilla JavaScript</li>
                <li>Backend: Flask/Django with Python</li>
                <li>Database: SQLite with optimized queries</li>
                <li>APIs: RESTful architecture</li>
            </ul>
        </div>
        
        <div style="background: rgba(102, 126, 234, 0.1); border: 2px solid rgba(102, 126, 234, 0.3); border-radius: 10px; padding: 1rem;">
            <p style="color: var(--text-secondary); text-align: center; margin: 0;">
                <strong style="color: #667eea;">Disclaimer:</strong> This application is for educational and informational purposes only. 
                It is not intended to replace professional medical advice, diagnosis, or treatment.
            </p>
        </div>
    `;
    
    showModal('About Medicino', aboutHTML);
}

// Utility Functions
function showElement(element) {
    element.classList.remove('hidden');
    element.style.animation = 'slideInUp 0.5s ease-out';
}

function hideElement(element) {
    element.classList.add('hidden');
}

function showLoader(loader) {
    loader.classList.remove('hidden');
}

function hideLoader(loader) {
    loader.classList.add('hidden');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: 500;
        max-width: 400px;
        animation: slideInDown 0.3s ease-out;
    `;
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideInUp 0.3s ease-out reverse';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

function getNotificationColor(type) {
    const colors = {
        'success': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'error': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'warning': 'linear-gradient(135deg, #ff9a56 0%, #ff6b95 100%)',
        'info': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    };
    return colors[type] || colors.info;
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || icons.info;
}

function showModal(title, content) {
    // Create modal backdrop
    const backdrop = document.createElement('div');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        animation: fadeIn 0.3s ease-out;
    `;
    
    // Create modal content
    const modal = document.createElement('div');
    modal.style.cssText = `
        background: var(--bg-secondary);
        border-radius: 20px;
        padding: 2rem;
        max-width: 600px;
        width: 100%;
        max-height: 80vh;
        overflow-y: auto;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-glass);
        animation: slideInDown 0.3s ease-out;
    `;
    
    modal.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color);">
            <h3 style="color: var(--text-primary); margin: 0;">${title}</h3>
            <button id="closeModal" style="background: none; border: none; color: var(--text-secondary); font-size: 1.5rem; cursor: pointer; padding: 0.5rem;">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div>${content}</div>
    `;
    
    backdrop.appendChild(modal);
    document.body.appendChild(backdrop);
    
    // Close modal functionality
    const closeModal = () => {
        backdrop.style.animation = 'fadeIn 0.3s ease-out reverse';
        setTimeout(() => {
            document.body.removeChild(backdrop);
        }, 300);
    };
    
    document.getElementById('closeModal').addEventListener('click', closeModal);
    backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) {
            closeModal();
        }
    });
    
    // ESC key to close
    const handleEsc = (e) => {
        if (e.key === 'Escape') {
            closeModal();
            document.removeEventListener('keydown', handleEsc);
        }
    };
    document.addEventListener('keydown', handleEsc);
}

// Performance optimization - debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add smooth scrolling behavior
document.documentElement.style.scrollBehavior = 'smooth';

// Add loading states for better UX
window.addEventListener('beforeunload', () => {
    document.body.style.opacity = '0.7';
});

// Initialize tooltips and help text
document.addEventListener('DOMContentLoaded', () => {
    // Add help tooltips
    const helpElements = document.querySelectorAll('[data-help]');
    helpElements.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            // Show tooltip (implementation can be expanded)
            console.log('Help:', e.target.getAttribute('data-help'));
        });
    });
});
