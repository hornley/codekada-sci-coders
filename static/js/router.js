// Router for Rekada Lens Application
class RekadaRouter {
  constructor() {
    this.currentPage = null;
    this.init();
  }

  async init() {
    // Check if user has a profile
    const userProfile = localStorage.getItem('rekada_user_profile');
    
    if (userProfile) {
      // User has a profile, go to dashboard
      await this.loadPage('dashboard');
    } else {
      // No profile, go to landing page
      await this.loadPage('landing');
    }
  }

  async loadPage(pageName) {
    const appContainer = document.getElementById('app-container');
    const pageLoader = document.getElementById('page-loader');
    
    try {
      // Show loader
      pageLoader.classList.remove('d-none');
      appContainer.classList.add('d-none');
      
      // Fetch the page content
      const response = await fetch(`${pageName}.html`);
      if (!response.ok) {
        throw new Error(`Failed to load ${pageName} page`);
      }
      
      const html = await response.text();
      
      // Extract body content from the fetched HTML
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const bodyContent = doc.body.innerHTML;
      
      // Load content into app container
      appContainer.innerHTML = bodyContent;
      
      // Hide loader and show content
      pageLoader.classList.add('d-none');
      appContainer.classList.remove('d-none');
      
      // Initialize page-specific functionality
      this.initializePageScripts(pageName);
      
      this.currentPage = pageName;
      
    } catch (error) {
      console.error('Error loading page:', error);
      this.showError('Failed to load page. Please refresh and try again.');
    }
  }

  initializePageScripts(pageName) {
    switch (pageName) {
      case 'landing':
        this.initLandingPage();
        break;
      case 'user-setup':
        this.initUserSetupPage();
        break;
      case 'dashboard':
        this.initDashboardPage();
        break;
      case 'product-analyzer':
        this.initProductAnalyzerPage();
        break;
      case 'product-scanner':
        this.initProductScannerPage();
        break;
    }
  }

  initLandingPage() {
    const getStartedBtn = document.getElementById('get-started-btn');
    if (getStartedBtn) {
      getStartedBtn.addEventListener('click', () => {
        this.loadPage('user-setup');
      });
    }
  }

  initUserSetupPage() {
    // Multi-step form functionality
    let currentStep = 1;
    const totalSteps = 6;
    
    const showStep = (step) => {
      // Hide all steps
      for (let i = 1; i <= totalSteps; i++) {
        const stepContent = document.getElementById(`step-${i}-content`);
        const progressStep = document.getElementById(`step-${i}`);
        
        if (stepContent) {
          stepContent.classList.add('d-none');
        }
        
        if (progressStep) {
          progressStep.classList.remove('bg-success');
          progressStep.classList.add('bg-secondary', 'opacity-25');
        }
      }
      
      // Show current step
      const currentStepContent = document.getElementById(`step-${step}-content`);
      if (currentStepContent) {
        currentStepContent.classList.remove('d-none');
      }
      
      // Update progress indicators
      for (let i = 1; i <= step; i++) {
        const progressStep = document.getElementById(`step-${i}`);
        if (progressStep) {
          progressStep.classList.remove('bg-secondary', 'opacity-25');
          progressStep.classList.add('bg-success');
        }
      }
      
      // Update step counter
      const stepCounter = document.getElementById('current-step');
      if (stepCounter) {
        stepCounter.textContent = step;
      }
      
      // Update navigation buttons
      const prevBtn = document.getElementById('prev-btn');
      const nextBtn = document.getElementById('next-btn');
      const completeBtn = document.getElementById('complete-btn');
      
      if (prevBtn) {
        prevBtn.classList.toggle('d-none', step === 1);
      }
      
      if (nextBtn && completeBtn) {
        nextBtn.classList.toggle('d-none', step === totalSteps);
        completeBtn.classList.toggle('d-none', step !== totalSteps);
      }
    };

    const validateStep = (step) => {
      if (step === 1) {
        const fullName = document.getElementById('fullName')?.value;
        const age = document.getElementById('age')?.value;
        return fullName && age;
      }
      return true; // Other steps are optional
    };

    // Navigation event listeners
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const completeBtn = document.getElementById('complete-btn');
    const backToHomeBtn = document.getElementById('back-to-home-btn');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (currentStep > 1) {
          currentStep--;
          showStep(currentStep);
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (validateStep(currentStep) && currentStep < totalSteps) {
          currentStep++;
          showStep(currentStep);
        } else if (!validateStep(currentStep)) {
          this.showToast('Please fill in all required fields.', 'warning');
        }
      });
    }

    if (completeBtn) {
      completeBtn.addEventListener('click', () => {
        this.handleProfileCompletion();
      });
    }

    if (backToHomeBtn) {
      backToHomeBtn.addEventListener('click', () => {
        this.loadPage('landing');
      });
    }

    // Initialize first step
    showStep(1);
  }

  initDashboardPage() {
    // Load user name
    const userProfile = JSON.parse(localStorage.getItem('rekada_user_profile') || '{}');
    const userNameElement = document.getElementById('user-name');
    if (userNameElement && userProfile.fullName) {
      userNameElement.textContent = userProfile.fullName;
    }

    // Dashboard event listeners
    const analyzeProductsBtn = document.getElementById('analyze-products-btn');
    const aboutBtn = document.getElementById('about-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const viewProfileBtn = document.getElementById('view-profile-btn');

    if (analyzeProductsBtn) {
      analyzeProductsBtn.addEventListener('click', () => {
        this.loadPage('product-analyzer');
      });
    }

    if (aboutBtn) {
      aboutBtn.addEventListener('click', () => {
        this.showToast('About page coming soon!', 'info');
      });
    }

    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('rekada_user_profile');
        this.loadPage('landing');
      });
    }

    if (viewProfileBtn) {
      viewProfileBtn.addEventListener('click', () => {
        this.loadPage('user-setup');
      });
    }
  }

  handleProfileCompletion() {
    const formData = this.collectFormData();
    
    if (!formData.fullName || !formData.age) {
      this.showToast('Please fill in all required fields.', 'error');
      return;
    }

    // Save profile to localStorage
    const profile = {
      id: Date.now().toString(),
      ...formData,
      createdAt: new Date().toISOString()
    };

    localStorage.setItem('rekada_user_profile', JSON.stringify(profile));
    
    this.showToast('Profile created successfully!', 'success');
    
    // Navigate to dashboard after a short delay
    setTimeout(() => {
      this.loadPage('dashboard');
    }, 1500);
  }

  collectFormData() {
    const formData = {
      fullName: document.getElementById('fullName')?.value || '',
      birthday: document.getElementById('birthday')?.value || '',
      age: parseInt(document.getElementById('age')?.value) || 0,
      foodAllergens: this.collectCheckboxData([
        'milk-allergy', 'eggs-allergy', 'fish-allergy', 'shellfish-allergy',
        'peanuts-allergy', 'tree-nuts-allergy', 'soybeans-allergy', 'wheat-allergy', 'sesame-allergy',
        'flavor-enhancers', 'preservatives-irritant', 'artificial-colors', 'artificial-sweeteners',
        'acids-irritant', 'emulsifiers-irritant', 'flavoring-agents'
      ]),
      beautyAllergens: this.collectCheckboxData([
        'fragrance-allergy', 'limonene-allergy', 'linalool-allergy', 'citronellol-allergy',
        'geraniol-allergy', 'eugenol-allergy', 'cinnamal-allergy', 'balsam-peru-allergy',
        'parabens-allergy', 'formaldehyde-allergy', 'isothiazolinones-allergy', 'phenoxyethanol-allergy',
        'sodium-benzoate-beauty', 'benzyl-alcohol-allergy', 'essential-oils-allergy', 'aloe-vera-allergy',
        'chamomile-allergy', 'calendula-allergy', 'coconut-oil-allergy', 'shea-butter-allergy',
        'almond-oil-allergy', 'eucalyptus-allergy'
      ]),
      comorbidities: this.collectCheckboxData([
        'hypertension', 'hyperlipidemia', 'coronary-artery-disease', 'heart-failure',
        'atrial-fibrillation', 'peripheral-artery-disease', 'type2-diabetes', 'obesity',
        'hypothyroidism', 'hyperthyroidism', 'pcos', 'gout', 'asthma', 'copd',
        'chronic-bronchitis', 'sleep-apnea', 'pulmonary-hypertension'
      ]),
      dietPreferences: this.collectCheckboxData([
        'plant-based', 'animal-based-low-carb', 'halal-diet', 'kosher-diet',
        'hindu-diet', 'buddhist-diet', 'rastafarian-diet'
      ]),
      healthPreferences: this.collectCheckboxData([
        'gluten-free', 'lactose-free', 'low-sodium', 'low-fat',
        'low-carb', 'diabetic-diet', 'allergen-free'
      ])
    };

    return formData;
  }

  collectCheckboxData(ids) {
    const result = [];
    ids.forEach(id => {
      const checkbox = document.getElementById(id);
      if (checkbox && checkbox.checked) {
        result.push(checkbox.value);
      }
    });
    return result;
  }

  showToast(message, type = 'success') {
    const toastElement = document.getElementById('toast');
    const toastBody = toastElement?.querySelector('.toast-body');
    const toastIcon = toastElement?.querySelector('.toast-header i');
    
    if (!toastElement || !toastBody) return;

    // Update message
    toastBody.textContent = message;
    
    // Update icon based on type
    if (toastIcon) {
      toastIcon.className = 'me-2';
      switch (type) {
        case 'success':
          toastIcon.classList.add('fas', 'fa-check-circle', 'text-success');
          break;
        case 'warning':
          toastIcon.classList.add('fas', 'fa-exclamation-triangle', 'text-warning');
          break;
        case 'error':
          toastIcon.classList.add('fas', 'fa-times-circle', 'text-danger');
          break;
        case 'info':
          toastIcon.classList.add('fas', 'fa-info-circle', 'text-info');
          break;
      }
    }

    // Show toast
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
  }

  showError(message) {
    const appContainer = document.getElementById('app-container');
    const pageLoader = document.getElementById('page-loader');
    
    pageLoader.classList.add('d-none');
    appContainer.classList.remove('d-none');
    appContainer.innerHTML = `
      <div class="container py-5 text-center">
        <div class="row justify-content-center">
          <div class="col-md-6">
            <i class="fas fa-exclamation-triangle text-warning display-1 mb-3"></i>
            <h3>Error Loading Page</h3>
            <p class="text-muted mb-4">${message}</p>
            <button class="btn btn-primary" onclick="location.reload()">
              <i class="fas fa-refresh me-2"></i>Refresh Page
            </button>
          </div>
        </div>
      </div>
    `;
  }

  initProductAnalyzerPage() {
    // Back to dashboard button
    const backBtn = document.getElementById('back-to-dashboard');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        this.loadPage('dashboard');
      });
    }

    // Analyze buttons for each category
    const analyzeButtons = document.querySelectorAll('.analyze-btn');
    analyzeButtons.forEach(button => {
      button.addEventListener('click', () => {
        const category = button.getAttribute('data-category');
        this.loadProductScanner(category);
      });
    });

    // Card click handlers
    const categoryCards = document.querySelectorAll('[data-category]');
    categoryCards.forEach(card => {
      card.addEventListener('click', () => {
        const category = card.getAttribute('data-category');
        if (category) {
          this.loadProductScanner(category);
        }
      });
    });
  }

  initProductScannerPage() {
    // Get category from URL or storage
    const category = sessionStorage.getItem('scanner_category') || 'food';
    
    // Update page title based on category
    const categoryTitle = document.getElementById('category-title');
    if (categoryTitle) {
      const categoryNames = {
        'food': 'Food',
        'drinks': 'Drinks',
        'beauty': 'Beauty'
      };
      categoryTitle.textContent = categoryNames[category] || 'Product';
    }

    // Back to analyzer button
    const backBtn = document.getElementById('back-to-analyzer');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        this.loadPage('product-analyzer');
      });
    }

    // Camera functionality
    const startCameraBtn = document.getElementById('start-camera-btn');
    const uploadImageBtn = document.getElementById('upload-image-btn');
    const barcodeUpload = document.getElementById('barcode-upload');

    if (startCameraBtn) {
      startCameraBtn.addEventListener('click', () => {
        this.startCameraScanning();
      });
    }

    if (uploadImageBtn && barcodeUpload) {
      uploadImageBtn.addEventListener('click', () => {
        barcodeUpload.click();
      });

      barcodeUpload.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
          this.processUploadedImage(e.target.files[0]);
        }
      });
    }

    // Search functionality
    const searchBtn = document.getElementById('search-product-btn');
    const searchInput = document.getElementById('product-search-input');

    if (searchBtn && searchInput) {
      searchBtn.addEventListener('click', () => {
        this.searchProduct(searchInput.value);
      });

      searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.searchProduct(searchInput.value);
        }
      });
    }

    // Manual entry form
    const manualForm = document.getElementById('manual-entry-form');
    if (manualForm) {
      manualForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.processManualEntry();
      });
    }

    // Hide nutrition section for beauty products
    if (category === 'beauty') {
      const nutritionSection = document.getElementById('nutrition-section');
      if (nutritionSection) {
        nutritionSection.style.display = 'none';
      }
    }
  }

  loadProductScanner(category) {
    // Store category for the scanner page
    sessionStorage.setItem('scanner_category', category);
    this.loadPage('product-scanner');
  }

  startCameraScanning() {
    this.showToast('Camera scanning feature coming soon!', 'info');
  }

  processUploadedImage(file) {
    this.showToast('Image processing feature coming soon!', 'info');
  }

  searchProduct(query) {
    if (!query.trim()) {
      this.showToast('Please enter a product name to search', 'warning');
      return;
    }
    this.showToast('Product search feature coming soon!', 'info');
  }

  processManualEntry() {
    const productName = document.getElementById('product-name')?.value;
    const ingredients = document.getElementById('product-ingredients')?.value;

    if (!productName || !ingredients) {
      this.showToast('Please fill in the required fields', 'warning');
      return;
    }

    this.showToast('Manual analysis feature coming soon!', 'info');
  }
}

// Initialize router when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new RekadaRouter();
});