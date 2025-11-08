// Rekada Lens - Product Analyzer Application

// App State
let currentPage = 'home';
let userProfile = null;
let currentAnalysis = null;
let intakeHistory = [];

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    console.log('Rekada Lens Product Analyzer Loaded!');
    
    // Load saved data from localStorage
    loadUserData();
    
    // Initialize the app
    initializeApp();
    
    // Set up event listeners
    setupEventListeners();
});

// Load user data from localStorage
function loadUserData() {
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile) {
        userProfile = JSON.parse(savedProfile);
        currentPage = 'dashboard';
    }

    const savedIntake = localStorage.getItem('intakeHistory');
    if (savedIntake) {
        intakeHistory = JSON.parse(savedIntake);
    }
}

// Initialize the application
function initializeApp() {
    showPage(currentPage);
    updateUserInterface();
}

// Set up all event listeners
function setupEventListeners() {
    // Home page events
    const getStartedBtn = document.getElementById('get-started-btn');
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', () => navigateToPage('setup'));
    }

    // Profile setup events
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', handleProfileSubmit);
    }

    const backToHomeBtn = document.getElementById('back-to-home-btn');
    if (backToHomeBtn) {
        backToHomeBtn.addEventListener('click', () => navigateToPage('home'));
    }

    // Dashboard events
    const analyzeProductsBtn = document.getElementById('analyze-products-btn');
    if (analyzeProductsBtn) {
        analyzeProductsBtn.addEventListener('click', () => navigateToPage('analyzer'));
    }

    const intakeHistoryBtn = document.getElementById('intake-history-btn');
    if (intakeHistoryBtn) {
        intakeHistoryBtn.addEventListener('click', () => navigateToPage('intake'));
    }

    const aboutBtn = document.getElementById('about-btn');
    if (aboutBtn) {
        aboutBtn.addEventListener('click', () => navigateToPage('about'));
    }

    const viewProfileBtn = document.getElementById('view-profile-btn');
    if (viewProfileBtn) {
        viewProfileBtn.addEventListener('click', () => navigateToPage('profile'));
    }

    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
}

// Navigation functions
function navigateToPage(page) {
    currentPage = page;
    showPage(page);
    updateUserInterface();
}

function showPage(page) {
    // Hide all pages
    const pages = document.querySelectorAll('.page-content');
    pages.forEach(p => p.classList.add('d-none'));

    // Show current page
    const currentPageElement = document.getElementById(`${page}-page`);
    if (currentPageElement) {
        currentPageElement.classList.remove('d-none');
    }
}

// Update user interface elements
function updateUserInterface() {
    // Update user name in dashboard
    const userNameElement = document.getElementById('user-name');
    if (userNameElement && userProfile) {
        userNameElement.textContent = userProfile.fullName.split(' ')[0];
    }

    // Update stats
    updateDashboardStats();
}

// Handle profile form submission
function handleProfileSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    // Get basic info
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const age = document.getElementById('age').value;
    const birthday = document.getElementById('birthday').value;

    // Get food allergens - biological
    const foodAllergensAnimal = [];
    const animalAllergens = ['milk', 'eggs', 'fish', 'shellfish'];
    animalAllergens.forEach(allergen => {
        if (document.getElementById(`${allergen}-allergy`)?.checked) {
            foodAllergensAnimal.push(allergen);
        }
    });

    const foodAllergensPlant = [];
    const plantAllergens = ['peanuts', 'tree-nuts', 'soybeans', 'wheat', 'sesame'];
    plantAllergens.forEach(allergen => {
        if (document.getElementById(`${allergen}-allergy`)?.checked) {
            foodAllergensPlant.push(allergen);
        }
    });

    // Get chemical irritants
    const chemicalIrritants = [];
    const chemicalTypes = ['msg', 'preservatives', 'artificial-colors', 'artificial-sweeteners', 'acids', 'emulsifiers', 'flavoring'];
    chemicalTypes.forEach(irritant => {
        if (document.getElementById(`${irritant}-irritant`)?.checked) {
            chemicalIrritants.push(irritant);
        }
    });

    // Get beauty product allergens - fragrance
    const fragranceAllergens = [];
    const fragranceTypes = ['fragrance', 'limonene', 'linalool', 'citronellol', 'geraniol', 'eugenol', 'cinnamal', 'balsam-peru'];
    fragranceTypes.forEach(fragrance => {
        if (document.getElementById(`${fragrance}-allergy`)?.checked) {
            fragranceAllergens.push(fragrance);
        }
    });

    // Get beauty preservatives
    const beautyPreservatives = [];
    const preservativeTypes = ['parabens', 'formaldehyde', 'isothiazolinones', 'phenoxyethanol', 'beauty-sodium-benzoate', 'benzyl-alcohol'];
    preservativeTypes.forEach(preservative => {
        if (document.getElementById(`${preservative}-allergy`)?.checked) {
            beautyPreservatives.push(preservative);
        }
    });

    // Get botanical allergens
    const botanicalAllergens = [];
    const botanicalTypes = ['essential-oils', 'aloe-vera', 'chamomile', 'calendula', 'coconut-oil', 'shea-butter', 'almond-oil', 'eucalyptus'];
    botanicalTypes.forEach(botanical => {
        if (document.getElementById(`${botanical}-allergy`)?.checked) {
            botanicalAllergens.push(botanical);
        }
    });

    // Get diet preferences - plant-based
    const plantBasedDiets = [];
    const plantDietTypes = ['vegetarian', 'vegan', 'pescatarian', 'plant-based'];
    plantDietTypes.forEach(diet => {
        if (document.getElementById(`${diet}-diet`)?.checked) {
            plantBasedDiets.push(diet);
        }
    });

    // Get diet preferences - animal-based/low-carb
    const animalBasedDiets = [];
    const animalDietTypes = ['keto', 'paleo', 'carnivore', 'low-carb'];
    animalDietTypes.forEach(diet => {
        if (document.getElementById(`${diet}-diet`)?.checked) {
            animalBasedDiets.push(diet);
        }
    });

    // Get religion/culture-based diets
    const religiousDiets = [];
    const religiousTypes = ['halal', 'kosher', 'hindu', 'buddhist', 'rastafarian'];
    religiousTypes.forEach(diet => {
        if (document.getElementById(`${diet}-diet`)?.checked) {
            religiousDiets.push(diet);
        }
    });

    // Get health preferences
    const healthPreferences = [];
    const healthTypes = ['gluten-free-health', 'lactose-free-health', 'low-sodium-health', 'low-fat-health', 'low-carb-health', 'diabetic-diet-health', 'allergen-free-health'];
    healthTypes.forEach(health => {
        if (document.getElementById(health)?.checked) {
            healthPreferences.push(health.replace('-health', ''));
        }
    });

    // Get cardiovascular conditions
    const cardiovascularConditions = [];
    const cardioTypes = ['hypertension', 'hyperlipidemia', 'coronary-artery-disease', 'heart-failure', 'atrial-fibrillation', 'peripheral-artery-disease'];
    cardioTypes.forEach(condition => {
        if (document.getElementById(condition)?.checked) {
            cardiovascularConditions.push(condition);
        }
    });

    // Get metabolic conditions
    const metabolicConditions = [];
    const metabolicTypes = ['type2-diabetes', 'obesity', 'hypothyroidism', 'hyperthyroidism', 'pcos', 'gout'];
    metabolicTypes.forEach(condition => {
        if (document.getElementById(condition)?.checked) {
            metabolicConditions.push(condition);
        }
    });

    // Get respiratory conditions
    const respiratoryConditions = [];
    const respiratoryTypes = ['asthma', 'copd', 'chronic-bronchitis', 'sleep-apnea', 'pulmonary-hypertension'];
    respiratoryTypes.forEach(condition => {
        if (document.getElementById(condition)?.checked) {
            respiratoryConditions.push(condition);
        }
    });

    // Create comprehensive user profile
    userProfile = {
        // Basic Information
        fullName: `${firstName} ${lastName}`,
        firstName: firstName,
        lastName: lastName,
        age: parseInt(age),
        birthday: birthday,
        
        // Food Allergens & Irritants
        foodAllergens: {
            animal: foodAllergensAnimal,
            plant: foodAllergensPlant
        },
        chemicalIrritants: chemicalIrritants,
        
        // Beauty Product Allergens
        beautyAllergens: {
            fragrance: fragranceAllergens,
            preservatives: beautyPreservatives,
            botanical: botanicalAllergens
        },
        
        // Diet Preferences
        dietPreferences: {
            plantBased: plantBasedDiets,
            animalBased: animalBasedDiets,
            religious: religiousDiets
        },
        
        // Health Preferences
        healthPreferences: healthPreferences,
        
        // Medical Conditions
        medicalConditions: {
            cardiovascular: cardiovascularConditions,
            metabolic: metabolicConditions,
            respiratory: respiratoryConditions
        },
        
        // Metadata
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString()
    };

    // Save to localStorage
    localStorage.setItem('userProfile', JSON.stringify(userProfile));
    
    // Show success message
    showToast('Comprehensive profile created successfully!', 'success');
    
    // Navigate to dashboard
    navigateToPage('dashboard');
}

// Handle logout
function handleLogout() {
    // Clear localStorage
    localStorage.removeItem('userProfile');
    localStorage.removeItem('intakeHistory');
    localStorage.removeItem('currentProduct');
    
    // Reset app state
    userProfile = null;
    intakeHistory = [];
    currentAnalysis = null;
    
    // Show success message
    showToast('Logged out successfully!', 'success');
    
    // Navigate to home
    navigateToPage('home');
}

// Product analysis functions
function analyzeProduct(category) {
    // This would typically make an API call to analyze the product
    // For demo purposes, we'll create mock analysis data
    
    const productData = JSON.parse(localStorage.getItem('currentProduct') || '{}');
    
    if (!productData.name) {
        showToast('No product data found. Please enter product details first.', 'error');
        return;
    }

    // Create mock analysis based on category
    const analysis = {
        id: Date.now().toString(),
        product: productData,
        category: category,
        overallScore: Math.floor(Math.random() * 100) + 1,
        recommendation: getRandomRecommendation(),
        analysis: generateMockAnalysis(category, productData),
        timestamp: new Date().toISOString()
    };

    currentAnalysis = analysis;
    showToast('Product analyzed successfully!', 'success');
    navigateToPage('report');
}

function getRandomRecommendation() {
    const recommendations = ['safe', 'caution', 'avoid'];
    return recommendations[Math.floor(Math.random() * recommendations.length)];
}

function generateMockAnalysis(category, product) {
    const analyses = {
        food: {
            nutritional: {
                calories: Math.floor(Math.random() * 300) + 50,
                protein: Math.floor(Math.random() * 20),
                carbs: Math.floor(Math.random() * 40),
                fat: Math.floor(Math.random() * 15),
                sodium: Math.floor(Math.random() * 500) + 100,
                sugar: Math.floor(Math.random() * 25)
            },
            healthImpact: 'This product contains moderate levels of nutrients suitable for your health goals.',
            ingredients: 'Analysis shows natural ingredients with minimal processing.'
        },
        drinks: {
            nutritional: {
                calories: Math.floor(Math.random() * 200) + 10,
                sugar: Math.floor(Math.random() * 30),
                sodium: Math.floor(Math.random() * 300) + 50,
                caffeine: Math.floor(Math.random() * 100)
            },
            healthImpact: 'Moderate sugar content. Consider consumption timing based on your health goals.',
            ingredients: 'Contains natural and artificial ingredients. Check for allergens.'
        },
        beauty: {
            skinCompatibility: Math.floor(Math.random() * 100) + 1,
            safetyScore: Math.floor(Math.random() * 100) + 1,
            healthImpact: 'Ingredients show good compatibility with most skin types.',
            ingredients: 'Contains beneficial ingredients with minimal irritants.'
        }
    };

    return analyses[category] || analyses.food;
}

// Save analysis to intake history
function saveToIntake() {
    if (!currentAnalysis) {
        showToast('No analysis to save', 'error');
        return;
    }

    const record = {
        id: Date.now().toString(),
        productAnalysis: currentAnalysis,
        timestamp: new Date().toISOString(),
        date: new Date().toLocaleDateString()
    };

    intakeHistory.unshift(record); // Add to beginning of array
    localStorage.setItem('intakeHistory', JSON.stringify(intakeHistory));
    
    showToast('Product saved to intake history!', 'success');
    updateDashboardStats();
}

// Update dashboard statistics
function updateDashboardStats() {
    const productsAnalyzed = document.getElementById('products-analyzed');
    const safeProducts = document.getElementById('safe-products');
    const cautionProducts = document.getElementById('caution-products');
    const avoidProducts = document.getElementById('avoid-products');

    if (productsAnalyzed) productsAnalyzed.textContent = intakeHistory.length;
    
    if (intakeHistory.length > 0) {
        const safe = intakeHistory.filter(item => item.productAnalysis.recommendation === 'safe').length;
        const caution = intakeHistory.filter(item => item.productAnalysis.recommendation === 'caution').length;
        const avoid = intakeHistory.filter(item => item.productAnalysis.recommendation === 'avoid').length;

        if (safeProducts) safeProducts.textContent = safe;
        if (cautionProducts) cautionProducts.textContent = caution;
        if (avoidProducts) avoidProducts.textContent = avoid;
    }
}

// Toast notification system
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastBody = toast.querySelector('.toast-body');
    const toastHeader = toast.querySelector('.toast-header');
    
    // Update toast content
    toastBody.textContent = message;
    
    // Update toast type
    const icon = toastHeader.querySelector('i');
    icon.className = `fas me-2 ${getToastIcon(type)} ${getToastColor(type)}`;
    
    // Show toast
    const toastInstance = new bootstrap.Toast(toast);
    toastInstance.show();
}

function getToastIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-exclamation-circle';
        case 'warning': return 'fa-exclamation-triangle';
        case 'info': return 'fa-info-circle';
        default: return 'fa-check-circle';
    }
}

function getToastColor(type) {
    switch (type) {
        case 'success': return 'text-success';
        case 'error': return 'text-danger';
        case 'warning': return 'text-warning';
        case 'info': return 'text-info';
        default: return 'text-success';
    }
}

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Utility functions
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatTime(dateString) {
    return new Date(dateString).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functions for global access
window.RekadaLens = {
    navigateToPage,
    analyzeProduct,
    saveToIntake,
    showToast,
    validateForm
};