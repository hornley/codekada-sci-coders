// Product Scanner Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
  // Get category from URL parameters or session storage
  const urlParams = new URLSearchParams(window.location.search);
  const category = urlParams.get('category') || sessionStorage.getItem('scanner_category') || 'food';
  
  // Update page title based on category
  updateCategoryTitle(category);
  
  // Initialize page functionality
  initializeNavigation();
  initializeCameraFeatures();
  initializeSearchFeatures();
  initializeManualEntry();
  
  // Hide nutrition section for beauty products
  if (category === 'beauty') {
    const nutritionSection = document.getElementById('nutrition-section');
    if (nutritionSection) {
      nutritionSection.style.display = 'none';
    }
  }

  function updateCategoryTitle(category) {
    const categoryTitle = document.getElementById('category-title');
    if (categoryTitle) {
      const categoryNames = {
        'food': 'Food',
        'drinks': 'Drinks',
        'beauty': 'Beauty'
      };
      categoryTitle.textContent = categoryNames[category] || 'Product';
    }
  }

  function initializeNavigation() {
    // Back to analyzer button
    const backBtn = document.getElementById('back-to-analyzer');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        window.location.href = '/analyzer';
      });
    }
  }

  function initializeCameraFeatures() {
    const startCameraBtn = document.getElementById('start-camera-btn');
    const uploadImageBtn = document.getElementById('upload-image-btn');
    const barcodeUpload = document.getElementById('barcode-upload');

    if (startCameraBtn) {
      startCameraBtn.addEventListener('click', () => {
        startCameraScanning();
      });
    }

    if (uploadImageBtn && barcodeUpload) {
      uploadImageBtn.addEventListener('click', () => {
        barcodeUpload.click();
      });

      barcodeUpload.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
          processUploadedImage(e.target.files[0]);
        }
      });
    }
  }

  function initializeSearchFeatures() {
    const searchBtn = document.getElementById('search-product-btn');
    const searchInput = document.getElementById('product-search-input');

    if (searchBtn && searchInput) {
      searchBtn.addEventListener('click', () => {
        searchProduct(searchInput.value);
      });

      searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          searchProduct(searchInput.value);
        }
      });
    }
  }

  function initializeManualEntry() {
    const manualForm = document.getElementById('manual-entry-form');
    if (manualForm) {
      manualForm.addEventListener('submit', (e) => {
        e.preventDefault();
        processManualEntry();
      });
    }
  }

  function startCameraScanning() {
    showToast('Camera scanning will be integrated with Flask backend!', 'info');
    
    // Placeholder for camera functionality
    const cameraPreview = document.getElementById('camera-preview');
    if (cameraPreview) {
      cameraPreview.innerHTML = `
        <div class="d-flex flex-column align-items-center justify-content-center h-100">
          <i class="fas fa-camera text-primary mb-3 fs-1"></i>
          <p class="text-muted mb-0">Camera functionality will be implemented with Flask backend</p>
          <small class="text-muted">This will connect to your backend API</small>
        </div>
      `;
    }
  }

  function processUploadedImage(file) {
    showToast('Image processing will be handled by Flask backend!', 'info');
    
    // Placeholder for image processing
    console.log('Image uploaded:', file.name);
    
    // Here you would typically send the image to your Flask backend
    // Example: uploadImageToFlask(file);
  }

  function searchProduct(query) {
    if (!query.trim()) {
      showToast('Please enter a product name to search', 'warning');
      return;
    }
    
    showToast('Product search will query Flask backend database!', 'info');
    
    // Placeholder for search results
    const searchResults = document.getElementById('search-results');
    if (searchResults) {
      searchResults.classList.remove('d-none');
      searchResults.innerHTML = `
        <div class="list-group">
          <div class="list-group-item">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-1">Search functionality ready for Flask integration</h6>
                <p class="mb-1">Query: "${query}"</p>
                <small>Will search backend database via Flask API</small>
              </div>
              <button class="btn btn-sm btn-outline-primary">Select</button>
            </div>
          </div>
        </div>
      `;
    }
  }

  function processManualEntry() {
    const productName = document.getElementById('product-name')?.value;
    const productBrand = document.getElementById('product-brand')?.value;
    const ingredients = document.getElementById('product-ingredients')?.value;
    const nutrition = document.getElementById('product-nutrition')?.value;

    if (!productName || !ingredients) {
      showToast('Please fill in the required fields', 'warning');
      return;
    }

    // Collect form data
    const productData = {
      name: productName,
      brand: productBrand,
      ingredients: ingredients,
      nutrition: nutrition,
      category: category
    };

    showToast('Manual entry will be processed by Flask backend!', 'info');
    
    // Show analysis results placeholder
    showAnalysisResults(productData);
  }

  function showAnalysisResults(productData) {
    const resultsSection = document.getElementById('analysis-results');
    const resultsContent = document.getElementById('results-content');
    
    if (resultsSection && resultsContent) {
      resultsContent.innerHTML = `
        <div class="row">
          <div class="col-md-6">
            <h6 class="fw-bold">Product Information</h6>
            <ul class="list-unstyled">
              <li><strong>Name:</strong> ${productData.name}</li>
              <li><strong>Brand:</strong> ${productData.brand || 'Not specified'}</li>
              <li><strong>Category:</strong> ${productData.category}</li>
            </ul>
          </div>
          <div class="col-md-6">
            <h6 class="fw-bold">Flask Backend Integration</h6>
            <div class="alert alert-info">
              <i class="fas fa-info-circle me-2"></i>
              This data will be sent to your Flask backend for analysis using AI/ML models.
            </div>
          </div>
        </div>
        <div class="mt-3">
          <h6 class="fw-bold">Ingredients Analysis (Backend Placeholder)</h6>
          <div class="bg-light p-3 rounded">
            <p class="mb-0">${productData.ingredients}</p>
          </div>
        </div>
      `;
      
      resultsSection.classList.remove('d-none');
      resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
  }

  // Toast notification function
  function showToast(message, type = 'success') {
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
});