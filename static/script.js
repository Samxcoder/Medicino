// Medicino Web Application - Complete JavaScript Implementation
// Author: AI Assistant
// Version: 1.0

// Global Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000/api',
    FLASK_BASE_URL: 'http://localhost:5000',
    DJANGO_BASE_URL: 'http://localhost:8000',
    CURRENT_BACKEND: 'flask', // 'flask' or 'django'
    VOICE_RECOGNITION_TIMEOUT: 10000,
    API_TIMEOUT: 10000
};

// Global State Management
const AppState = {
    isListening: false,
    currentDiagnosis: null,
    diagnosisHistory: [],
    allMedicines: [],
    isLoading: false
};

// Utility Functions
const Utils = {
    // Show/hide elements with animation
    show: (element) => {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) {
            element.classList.remove('hidden');
            element.style.animation = 'fadeIn 0.5s ease-out';
        }
    },

    hide: (element) => {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) {
            element.classList.add('hidden');
        }
    },

    // Show loading state
    showLoader: (loaderId) => {
        Utils.show(loaderId);
    },

    hideLoader: (loaderId) => {
        Utils.hide(loaderId);
    },

    // Format text for display
    formatText: (text) => {
        if (!text) return 'Not available';
        return text.charAt(0).toUpperCase() + text.slice(1);
    },

    // Clean and validate symptoms input
    cleanSymptoms: (symptoms) => {
        return symptoms
            .toLowerCase()
            .trim()
            .replace(/[^\w\s,.-]/g, '') // Remove special characters except common ones
            .replace(/\s+/g, ' '); // Remove extra spaces
    },

    // Show notification
    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            ${message}
        `;

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
            font-weight: 500;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    },

    // Validate symptoms input
    validateSymptoms: (symptoms) => {
        const cleaned = Utils.cleanSymptoms(symptoms);
        if (!cleaned || cleaned.length < 3) {
            return { valid: false, message: 'Please enter at least 3 characters describing your symptoms' };
        }
        if (cleaned.length > 500) {
            return { valid: false, message: 'Symptoms description is too long (max 500 characters)' };
        }
        return { valid: true, cleaned: cleaned };
    }
};

// API Service
const ApiService = {
    // Get current API base URL
    getApiUrl: () => {
        return CONFIG.CURRENT_BACKEND === 'django' ?
            `${CONFIG.DJANGO_BASE_URL}/api` :
            CONFIG.API_BASE_URL;
    },

    // Generic API request function
    request: async (endpoint, options = {}) => {
        const url = `${ApiService.getApiUrl()}${endpoint}`;
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: CONFIG.API_TIMEOUT
        };

        const requestOptions = { ...defaultOptions, ...options };

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), requestOptions.timeout);

            const response = await fetch(url, {
                ...requestOptions,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API Request Error:', error);
            if (error.name === 'AbortError') {
                throw new Error('Request timeout. Please check your connection and try again.');
            }
            throw error;
        }
    },

    // Diagnose symptoms
    diagnose: async (symptoms) => {
        const endpoint = CONFIG.CURRENT_BACKEND === 'django' ? '/diagnose/' : '/diagnose';
        return await ApiService.request(endpoint, {
            method: 'POST',
            body: JSON.stringify({ symptoms: symptoms })
        });
    },

    // Get medicine information
    getMedicine: async (medicineName) => {
        const endpoint = CONFIG.CURRENT_BACKEND === 'django' ?
            `/medicine/${encodeURIComponent(medicineName)}/` :
            `/medicine/${encodeURIComponent(medicineName)}`;
        return await ApiService.request(endpoint);
    },



    // Get diagnosis history
    getHistory: async () => {
        const endpoint = CONFIG.CURRENT_BACKEND === 'django' ? '/history/' : '/history';
        return await ApiService.request(endpoint);
    }
};

// Voice Recognition Service
const VoiceService = {
    recognition: null,
    isSupported: false,

    init: () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            VoiceService.recognition = new SpeechRecognition();
            VoiceService.recognition.continuous = false;
            VoiceService.recognition.interimResults = false;
            VoiceService.recognition.lang = 'en-US';
            VoiceService.isSupported = true;

            VoiceService.recognition.onstart = () => {
                AppState.isListening = true;
                const voiceBtn = document.getElementById('voiceBtn');
                voiceBtn.classList.add('listening');
                voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i> Listening...';
                Utils.showNotification('Listening... Please speak your symptoms clearly', 'info');
            };

            VoiceService.recognition.onend = () => {
                AppState.isListening = false;
                const voiceBtn = document.getElementById('voiceBtn');
                voiceBtn.classList.remove('listening');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Voice Input';
            };

            VoiceService.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                AppState.isListening = false;
                const voiceBtn = document.getElementById('voiceBtn');
                voiceBtn.classList.remove('listening');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i> Voice Input';

                let errorMessage = 'Voice recognition error. ';
                switch (event.error) {
                    case 'no-speech':
                        errorMessage += 'No speech detected. Please try again.';
                        break;
                    case 'network':
                        errorMessage += 'Network error. Please check your connection.';
                        break;
                    case 'not-allowed':
                        errorMessage += 'Microphone access denied. Please enable microphone permissions.';
                        break;
                    default:
                        errorMessage += 'Please try again.';
                }
                Utils.showNotification(errorMessage, 'error');
            };

            VoiceService.recognition.onresult = (event) => {
                const result = event.results[0][0].transcript;
                document.getElementById('symptomsInput').value = result;
                Utils.showNotification(`Voice input received: "${result}"`, 'success');
            };
        } else {
            console.warn('Speech recognition not supported in this browser');
        }
    },

    start: () => {
        if (VoiceService.isSupported && VoiceService.recognition && !AppState.isListening) {
            try {
                VoiceService.recognition.start();
            } catch (error) {
                console.error('Error starting voice recognition:', error);
                Utils.showNotification('Could not start voice recognition. Please try again.', 'error');
            }
        } else if (!VoiceService.isSupported) {
            Utils.showNotification('Voice recognition is not supported in your browser', 'error');
        }
    },

    stop: () => {
        if (VoiceService.recognition && AppState.isListening) {
            VoiceService.recognition.stop();
        }
    }
};

// Diagnosis Handler
const DiagnosisHandler = {
    diagnose: async () => {
        const symptomsInput = document.getElementById('symptomsInput');
        const symptoms = symptomsInput.value.trim();

        // Validate input
        const validation = Utils.validateSymptoms(symptoms);
        if (!validation.valid) {
            Utils.showNotification(validation.message, 'error');
            symptomsInput.focus();
            return;
        }

        const cleanedSymptoms = validation.cleaned;

        // Show loading state
        Utils.showLoader('diagnosisLoader');
        Utils.hide('diagnosisResult');

        const diagnoseBtn = document.getElementById('diagnoseBtn');
        const originalBtnText = diagnoseBtn.innerHTML;
        diagnoseBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        diagnoseBtn.disabled = true;

        try {
            const response = await ApiService.diagnose(cleanedSymptoms);

            if (response.success && response.data) {
                AppState.currentDiagnosis = response.data;
                DiagnosisHandler.displayResults(response.data);
                Utils.showNotification('Diagnosis completed successfully!', 'success');
            } else {
                throw new Error(response.message || 'Diagnosis failed');
            }
        } catch (error) {
            console.error('Diagnosis error:', error);
            Utils.showNotification(`Diagnosis failed: ${error.message}`, 'error');
            Utils.hide('diagnosisResult');
        } finally {
            Utils.hideLoader('diagnosisLoader');
            diagnoseBtn.innerHTML = originalBtnText;
            diagnoseBtn.disabled = false;
        }
    },

    displayResults: (data) => {
        // Update disease output
        document.getElementById('diseaseOutput').textContent = Utils.formatText(data.disease);

        // Update severity badge
        const severityBadge = document.getElementById('severityBadge');
        const severity = data.severity || 'unknown';
        severityBadge.innerHTML = `<span class="severity-badge severity-${severity}">
            <i class="fas fa-${DiagnosisHandler.getSeverityIcon(severity)}"></i>
            ${Utils.formatText(severity)} Severity
        </span>`;

        // Update Ayurvedic remedy
        document.getElementById('ayurvedicOutput').textContent = data.ayurvedic || 'No Ayurvedic remedy available';

        // Update medicine suggestion
        document.getElementById('medicineOutput').textContent = data.medicine || 'No medicine suggestion available';

        // Update confidence score
        const confidence = Math.min(Math.max(data.confidence || 0, 0), 100);
        document.getElementById('confidenceText').textContent = `${confidence.toFixed(1)}%`;

        // Animate confidence bar
        const confidenceFill = document.getElementById('confidenceFill');
        setTimeout(() => {
            confidenceFill.style.width = `${confidence}%`;
        }, 300);

        // Show results
        Utils.show('diagnosisResult');

        // Scroll to results
        document.getElementById('diagnosisResult').scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    },

    getSeverityIcon: (severity) => {
        switch (severity.toLowerCase()) {
            case 'mild': return 'smile';
            case 'moderate': return 'meh';
            case 'severe': return 'frown';
            case 'critical': return 'exclamation-triangle';
            default: return 'question-circle';
        }
    },

    clear: () => {
        document.getElementById('symptomsInput').value = '';
        Utils.hide('diagnosisResult');
        Utils.hide('diagnosisLoader');
        AppState.currentDiagnosis = null;

        // Reset confidence bar
        document.getElementById('confidenceFill').style.width = '0%';
    }
};

// Medicine Handler
const MedicineHandler = {
    search: async () => {
        const medicineInput = document.getElementById('medicineInput');
        const medicineName = medicineInput.value.trim();

        if (!medicineName) {
            Utils.showNotification('Please enter a medicine name', 'error');
            medicineInput.focus();
            return;
        }

        if (medicineName.length < 2) {
            Utils.showNotification('Please enter at least 2 characters', 'error');
            return;
        }

        // Show loading state
        Utils.showLoader('medicineLoader');
        Utils.hide('medicineInfoResult');

        const searchBtn = document.getElementById('searchMedicineBtn');
        const originalBtnText = searchBtn.innerHTML;
        searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
        searchBtn.disabled = true;

        try {
            const response = await ApiService.getMedicine(medicineName);

            if (response.success && response.data) {
                MedicineHandler.displayMedicineInfo([response.data]);
                Utils.showNotification('Medicine found successfully!', 'success');
            } else {
                Utils.showNotification('Medicine not found. Try a different name or check spelling.', 'error');
                document.getElementById('medicineInfoResult').innerHTML = `
                    <div class="medicine-card" style="text-align: center; color: var(--text-secondary);">
                        <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                        <h3>Medicine Not Found</h3>
                        <p>We couldn't find "${medicineName}" in our database.</p>
                        <p>Try searching with a different name or check the spelling.</p>
                    </div>
                `;
                Utils.show('medicineInfoResult');
            }
        } catch (error) {
            console.error('Medicine search error:', error);
            Utils.showNotification(`Search failed: ${error.message}`, 'error');
        } finally {
            Utils.hideLoader('medicineLoader');
            searchBtn.innerHTML = originalBtnText;
            searchBtn.disabled = false;
        }
    },



    displayMedicineInfo: (medicines) => {
        const resultDiv = document.getElementById('medicineInfoResult');

        if (!medicines || medicines.length === 0) {
            resultDiv.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No medicines found.</p>';
            Utils.show('medicineInfoResult');
            return;
        }

        let html = '';

        if (medicines.length > 1) {
            html += `<h3 style="margin-bottom: 1.5rem; color: #f093fb;">
                <i class="fas fa-pills"></i> Found ${medicines.length} Medicines
            </h3>`;
        }

        medicines.forEach(medicine => {
            html += `
                <div class="medicine-card">
                    <div class="medicine-name">
                        <i class="fas fa-capsules"></i>
                        ${Utils.formatText(medicine.name)}
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-info-circle"></i> Description:</strong>
                        <span>${medicine.description || 'Not available'}</span>
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-prescription-bottle-alt"></i> Dosage:</strong>
                        <span>${medicine.dosage || 'Consult healthcare provider'}</span>
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-exclamation-triangle"></i> Side Effects:</strong>
                        <span>${medicine.side_effects || 'Not specified'}</span>
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-ban"></i> Contraindications:</strong>
                        <span>${medicine.contraindications || 'Not specified'}</span>
                    </div>

                    <div class="medicine-detail">
                        <strong><i class="fas fa-tag"></i> Category:</strong>
                        <span class="category-tag">${Utils.formatText(medicine.category || 'general')}</span>
                    </div>

                    <div class="medicine-detail" style="align-items: center; margin-top: 1rem;">
                        <strong><i class="fas fa-rupee-sign"></i> Price:</strong>
                        <span class="price-tag">
                            <i class="fas fa-rupee-sign"></i>
                            ${medicine.price ? parseFloat(medicine.price).toFixed(2) : 'N/A'}
                        </span>
                    </div>
                </div>
            `;
        });

        resultDiv.innerHTML = html;
        Utils.show('medicineInfoResult');

        // Scroll to results if showing all medicines
        if (medicines.length > 3) {
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
};

// History Handler
const HistoryHandler = {
    show: async () => {
        try {
            Utils.showNotification('Loading diagnosis history...', 'info');
            const response = await ApiService.getHistory();

            if (response.success && response.data) {
                AppState.diagnosisHistory = response.data;
                HistoryHandler.displayHistory(response.data);
            } else {
                Utils.showNotification('No history found', 'error');
            }
        } catch (error) {
            console.error('Error loading history:', error);
            Utils.showNotification(`Failed to load history: ${error.message}`, 'error');
        }
    },

    displayHistory: (history) => {
        if (!history || history.length === 0) {
            Utils.showNotification('No diagnosis history available', 'info');
            return;
        }

        // Create modal for history display
        const modal = document.createElement('div');
        modal.className = 'history-modal';
        modal.innerHTML = `
            <div class="modal-overlay" onclick="HistoryHandler.closeModal()"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i class="fas fa-history"></i> Diagnosis History</h2>
                    <button class="close-btn" onclick="HistoryHandler.closeModal()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    ${history.map((record, index) => `
                        <div class="history-item">
                            <div class="history-header">
                                <strong>Diagnosis #${history.length - index}</strong>
                                <span class="history-date">${new Date(record.created_at).toLocaleString()}</span>
                            </div>
                            <div class="history-content">
                                <p><strong>Symptoms:</strong> ${record.symptoms}</p>
                                <p><strong>Condition:</strong> ${record.diagnosed_condition}</p>
                                <p><strong>Confidence:</strong> ${record.confidence_score}%</p>
                                <p><strong>Ayurvedic Remedy:</strong> ${record.ayurvedic_remedy}</p>
                                <p><strong>Medicine:</strong> ${record.medicine_suggestion}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        // Add modal styles
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        document.body.appendChild(modal);

        // Modal styles are now handled by CSS

        Utils.showNotification(`Loaded ${history.length} diagnosis records`, 'success');
    },

    closeModal: () => {
        const modal = document.querySelector('.history-modal');
        if (modal) {
            modal.remove();
        }
    }
};

// Emergency Guide Handler
const EmergencyHandler = {
    show: () => {
        const emergencyInfo = `
            <div class="emergency-modal">
                <div class="modal-overlay" onclick="EmergencyHandler.close()"></div>
                <div class="modal-content">
                    <div class="modal-header emergency-header">
                        <h2><i class="fas fa-exclamation-triangle"></i> Emergency Guidelines</h2>
                        <button class="close-btn" onclick="EmergencyHandler.close()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="emergency-section">
                            <h3><i class="fas fa-phone"></i> Emergency Numbers (India)</h3>
                            <ul>
                                <li><strong>108</strong> - Emergency Ambulance</li>
                                <li><strong>102</strong> - Medical Emergency</li>
                                <li><strong>100</strong> - Police</li>
                                <li><strong>101</strong> - Fire Department</li>
                            </ul>
                        </div>

                        <div class="emergency-section">
                            <h3><i class="fas fa-heart"></i> When to Seek Immediate Medical Attention</h3>
                            <ul>
                                <li>Chest pain or pressure</li>
                                <li>Difficulty breathing</li>
                                <li>Severe allergic reactions</li>
                                <li>High fever (above 103°F/39.4°C)</li>
                                <li>Severe head injury</li>
                                <li>Unconsciousness</li>
                                <li>Severe bleeding</li>
                                <li>Signs of stroke (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency)</li>
                            </ul>
                        </div>

                        <div class="emergency-section">
                            <h3><i class="fas fa-first-aid"></i> Basic First Aid</h3>
                            <ul>
                                <li><strong>For cuts:</strong> Apply pressure with clean cloth</li>
                                <li><strong>For burns:</strong> Cool with cold water for 10-20 minutes</li>
                                <li><strong>For choking:</strong> Perform Heimlich maneuver</li>
                                <li><strong>For unconsciousness:</strong> Check breathing, place in recovery position</li>
                            </ul>
                        </div>

                        <div class="emergency-disclaimer">
                            <p><strong>⚠️ Disclaimer:</strong> This app is for informational purposes only and should not replace professional medical advice. In case of emergency, always call emergency services immediately.</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const modalDiv = document.createElement('div');
        modalDiv.innerHTML = emergencyInfo;
        modalDiv.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        // Emergency modal styles are now handled by CSS

        document.body.appendChild(modalDiv);
    },

    close: () => {
        const modal = document.querySelector('.emergency-modal');
        if (modal && modal.parentElement) {
            modal.parentElement.remove();
        }
    }
};

// About Handler
const AboutHandler = {
    show: () => {
        const aboutInfo = `
            <div class="about-modal">
                <div class="modal-overlay" onclick="AboutHandler.close()"></div>
                <div class="modal-content">
                    <div class="modal-header">
                        <h2><i class="fas fa-info-circle"></i> About Medicino</h2>
                        <button class="close-btn" onclick="AboutHandler.close()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="about-section">
                            <h3><i class="fas fa-brain"></i> What is Medicino?</h3>
                            <p>Medicino is an AI-powered medical assistant that helps you understand your symptoms and provides intelligent health recommendations. Our system combines modern medical knowledge with traditional Ayurvedic wisdom to offer comprehensive health guidance.</p>
                        </div>

                        <div class="about-section">
                            <h3><i class="fas fa-cogs"></i> Features</h3>
                            <ul>
                                <li><strong>Smart Symptom Analysis:</strong> AI-powered diagnosis with confidence scoring</li>
                                <li><strong>Dual Treatment Approach:</strong> Modern medicine + Ayurvedic remedies</li>
                                <li><strong>Medicine Database:</strong> Comprehensive information on medications</li>
                                <li><strong>Voice Input:</strong> Speak your symptoms naturally</li>
                                <li><strong>History Tracking:</strong> Keep track of your consultations</li>
                                <li><strong>Emergency Guidelines:</strong> Quick access to emergency information</li>
                            </ul>
                        </div>

                        <div class="about-section">
                            <h3><i class="fas fa-shield-alt"></i> Technology Stack</h3>
                            <ul>
                                <li><strong>Frontend:</strong> HTML5, CSS3, JavaScript (ES6+)</li>
                                <li><strong>Backend:</strong> Flask/Django Python Framework</li>
                                <li><strong>Database:</strong> SQLite with optimized indexing</li>
                                <li><strong>AI Engine:</strong> Custom symptom matching algorithm</li>
                                <li><strong>Voice Recognition:</strong> Web Speech API</li>
                            </ul>
                        </div>

                        <div class="about-section">
                            <h3><i class="fas fa-users"></i> How It Works</h3>
                            <ol>
                                <li>Enter your symptoms via text or voice input</li>
                                <li>Our AI analyzes your symptoms against medical database</li>
                                <li>Receive diagnosis with confidence score</li>
                                <li>Get both modern medicine and Ayurvedic recommendations</li>
                                <li>Access detailed medicine information from our database</li>
                            </ol>
                        </div>

                        <div class="about-disclaimer">
                            <h4><i class="fas fa-exclamation-triangle"></i> Important Disclaimer</h4>
                            <p>Medicino is designed for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns. In case of emergency, contact emergency services immediately.</p>
                        </div>

                        <div class="about-footer">
                            <p><strong>Version:</strong> 1.0.0</p>
                            <p><strong>Last Updated:</strong> ${new Date().toLocaleDateString()}</p>
                            <p><strong>Support:</strong> For technical support or feedback, please contact our development team.</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const modalDiv = document.createElement('div');
        modalDiv.innerHTML = aboutInfo;
        modalDiv.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        `;

        // About modal styles are now handled by CSS

        document.body.appendChild(modalDiv);
    },

    close: () => {
        const modal = document.querySelector('.about-modal');
        if (modal && modal.parentElement) {
            modal.parentElement.remove();
        }
    }
};

// Backend Switcher (for testing different backends)
const BackendSwitcher = {
    switch: (backend) => {
        if (backend === 'flask' || backend === 'django') {
            CONFIG.CURRENT_BACKEND = backend;
            Utils.showNotification(`Switched to ${backend.toUpperCase()} backend`, 'success');
            console.log(`Backend switched to: ${backend}`);
        }
    },

    detectAvailableBackend: async () => {
        // Try Flask first
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/medicines`, {
                method: 'GET',
                timeout: 3000
            });
            if (response.ok) {
                CONFIG.CURRENT_BACKEND = 'flask';
                console.log('Flask backend detected and active');
                return 'flask';
            }
        } catch (error) {
            console.log('Flask backend not available:', error.message);
        }

        // Try Django
        try {
            const response = await fetch(`${CONFIG.DJANGO_BASE_URL}/api/medicines/`, {
                method: 'GET',
                timeout: 3000
            });
            if (response.ok) {
                CONFIG.CURRENT_BACKEND = 'django';
                console.log('Django backend detected and active');
                return 'django';
            }
        } catch (error) {
            console.log('Django backend not available:', error.message);
        }

        // No backend available
        Utils.showNotification('No backend server detected. Please start Flask or Django server.', 'error');
        return null;
    }
};

// Event Listeners Setup
const EventListeners = {
    init: () => {
        // Diagnosis functionality
        document.getElementById('diagnoseBtn').addEventListener('click', DiagnosisHandler.diagnose);
        document.getElementById('voiceBtn').addEventListener('click', VoiceService.start);
        document.getElementById('clearBtn').addEventListener('click', DiagnosisHandler.clear);

        // Medicine functionality
        document.getElementById('searchMedicineBtn').addEventListener('click', MedicineHandler.search);

        // Quick actions
        document.getElementById('historyBtn').addEventListener('click', HistoryHandler.show);
        document.getElementById('emergencyBtn').addEventListener('click', EmergencyHandler.show);
        document.getElementById('aboutBtn').addEventListener('click', AboutHandler.show);

        // Enter key support for inputs
        document.getElementById('symptomsInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                DiagnosisHandler.diagnose();
            }
        });

        document.getElementById('medicineInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                MedicineHandler.search();
            }
        });

        // Auto-resize textarea
        const symptomsInput = document.getElementById('symptomsInput');
        symptomsInput.addEventListener('input', () => {
            symptomsInput.style.height = 'auto';
            symptomsInput.style.height = Math.min(symptomsInput.scrollHeight, 200) + 'px';
        });

        // Symptom tag functionality
        const symptomTags = document.querySelectorAll('.symptom-tag');
        symptomTags.forEach(tag => {
            tag.addEventListener('click', () => {
                const symptom = tag.getAttribute('data-symptom');
                const currentValue = symptomsInput.value.trim();
                
                if (currentValue) {
                    // Add comma and space if there's already content
                    symptomsInput.value = currentValue + ', ' + symptom;
                } else {
                    // Just add the symptom if input is empty
                    symptomsInput.value = symptom;
                }
                
                // Trigger input event to resize textarea
                symptomsInput.dispatchEvent(new Event('input'));
                
                // Add visual feedback
                tag.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    tag.style.transform = '';
                }, 150);
            });
        });

        // Voice button state management
        document.getElementById('voiceBtn').addEventListener('click', () => {
            if (AppState.isListening) {
                VoiceService.stop();
            } else {
                VoiceService.start();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl+Enter for diagnosis
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                DiagnosisHandler.diagnose();
            }

            // Ctrl+Shift+V for voice input
            if (e.ctrlKey && e.shiftKey && e.key === 'V') {
                e.preventDefault();
                VoiceService.start();
            }

            // Escape to close modals
            if (e.key === 'Escape') {
                HistoryHandler.closeModal();
                EmergencyHandler.close();
                AboutHandler.close();
            }
        });

        console.log('✅ Event listeners initialized');
    }
};

// Application Initialization
const App = {
    init: async () => {
        console.log('🚀 Initializing Medicino Application...');

        try {
            // Initialize voice recognition
            VoiceService.init();

            // Setup event listeners
            EventListeners.init();

            // Detect available backend
            await BackendSwitcher.detectAvailableBackend();

            // Show welcome message
           

            // Add loading animations
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.5s ease-in';

            setTimeout(() => {
                document.body.style.opacity = '1';
            }, 100);

            console.log('✅ Medicino Application initialized successfully');

        } catch (error) {
            console.error('❌ Error initializing application:', error);
            Utils.showNotification('Application initialization failed. Please refresh the page.', 'error');
        }
    },

    // Cleanup function
    cleanup: () => {
        // Stop voice recognition if active
        if (AppState.isListening) {
            VoiceService.stop();
        }

        // Clear any timers or intervals
        console.log('🧹 Application cleanup completed');
    }
};

// Performance monitoring
const Performance = {
    startTime: Date.now(),

    measureApiCall: (apiName, startTime) => {
        const endTime = Date.now();
        const duration = endTime - startTime;
        console.log(`📊 API Call [${apiName}]: ${duration}ms`);

        if (duration > 5000) {
            console.warn(`⚠️ Slow API call detected: ${apiName} took ${duration}ms`);
        }
    },

    logMemoryUsage: () => {
        if (performance.memory) {
            const memory = performance.memory;
            console.log('💾 Memory Usage:', {
                used: Math.round(memory.usedJSHeapSize / 1024 / 1024) + ' MB',
                total: Math.round(memory.totalJSHeapSize / 1024 / 1024) + ' MB',
                limit: Math.round(memory.jsHeapSizeLimit / 1024 / 1024) + ' MB'
            });
        }
    }
};

// Error handling
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    Utils.showNotification('An unexpected error occurred. Please try again.', 'error');
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    Utils.showNotification('A network error occurred. Please check your connection.', 'error');
});

// Application lifecycle
window.addEventListener('load', App.init);
window.addEventListener('beforeunload', App.cleanup);

// Periodic performance monitoring (development only)
if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
    setInterval(() => {
        Performance.logMemoryUsage();
    }, 30000); // Every 30 seconds
}

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CONFIG,
        AppState,
        Utils,
        ApiService,
        VoiceService,
        DiagnosisHandler,
        MedicineHandler,
        HistoryHandler,
        EmergencyHandler,
        AboutHandler
    };
}

console.log('📋 Medicino JavaScript loaded successfully');
