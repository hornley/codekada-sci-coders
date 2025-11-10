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
    showToast('Starting camera for barcode scanning...', 'info');
    
    // Simulate camera activation
    const cameraPreview = document.getElementById('camera-preview');
    if (cameraPreview) {
      cameraPreview.innerHTML = `
        <div class="d-flex flex-column align-items-center justify-content-center h-100">
          <div class="spinner-border text-primary mb-3" role="status"></div>
          <p class="text-muted mb-2">Camera is starting...</p>
          <small class="text-muted">Point camera at product barcode</small>
        </div>
      `;
      
      // Simulate camera scanning and barcode detection
      setTimeout(() => {
        cameraPreview.innerHTML = `
          <div class="text-center">
            <div class="bg-primary bg-opacity-10 border border-primary border-3 rounded p-4 mb-3" style="display: inline-block;">
              <div class="row">
                <div class="col-12 mb-2">
                  <div class="bg-dark" style="height: 3px; width: 100%;"></div>
                </div>
                <div class="col-12 mb-2">
                  <div class="bg-dark" style="height: 2px; width: 80%; margin: 0 auto;"></div>
                </div>
                <div class="col-12 mb-2">
                  <div class="bg-dark" style="height: 3px; width: 100%;"></div>
                </div>
                <div class="col-12 mb-2">
                  <div class="bg-dark" style="height: 2px; width: 60%; margin: 0 auto;"></div>
                </div>
                <div class="col-12">
                  <small class="text-primary fw-bold">1234567890123</small>
                </div>
              </div>
            </div>
            <div class="alert alert-success mb-0">
              <i class="fas fa-check-circle me-2"></i>
              Barcode detected! Processing product...
            </div>
          </div>
        `;
        
        showToast('Barcode detected successfully!', 'success');
        
        // Show analysis results after barcode detection
        setTimeout(() => {
          const mockProductData = {
            name: 'Coca-Cola Original (Camera Scanned)',
            brand: 'The Coca-Cola Company',
            barcode: '1234567890123',
            ingredients: 'Carbonated Water, Sugar, Natural Flavors, Caramel Color, Phosphoric Acid, Natural Flavor, Caffeine',
            category: category,
            nutrition: 'Calories: 140, Total Carbs: 39g, Sugars: 39g, Sodium: 45mg, Caffeine: 34mg',
            scannedViaCamera: true
          };
          
          showAnalysisResults(mockProductData);
        }, 1500);
        
      }, 3000); // 3 second delay to simulate camera startup and scanning
    }
  }

  function processUploadedImage(file) {
    // Show loading state
    showToast('Processing image...', 'info');
    
    // Show image preview
    const cameraPreview = document.getElementById('camera-preview');
    if (cameraPreview) {
      const reader = new FileReader();
      reader.onload = function(e) {
        cameraPreview.innerHTML = `
          <div class="text-center">
            <img src="${e.target.result}" alt="Uploaded Image" class="img-fluid rounded mb-3" style="max-height: 200px;">
            <div class="d-flex align-items-center justify-content-center">
              <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
              <span class="text-muted">Analyzing barcode...</span>
            </div>
          </div>
        `;
      };
      reader.readAsDataURL(file);
    }
    
    // Simulate processing delay and show results
    setTimeout(() => {
      // Mock product data from barcode scan
      const mockProductData = {
        name: 'Sample Product (Scanned)',
        brand: 'Brand Name',
        barcode: '1234567890123',
        ingredients: 'Water, Sugar, Natural Flavors, Citric Acid, Sodium Benzoate (Preservative)',
        category: category,
        nutrition: 'Calories: 150, Sugar: 39g, Sodium: 45mg',
        imageFile: file.name
      };
      
      showToast('Barcode scanned successfully!', 'success');
      showAnalysisResults(mockProductData);
      
      // Update camera preview to show success
      if (cameraPreview) {
        cameraPreview.innerHTML = `
          <div class="text-center">
            <img src="${URL.createObjectURL(file)}" alt="Scanned Product" class="img-fluid rounded mb-3" style="max-height: 200px;">
            <div class="alert alert-success mb-0">
              <i class="fas fa-check-circle me-2"></i>
              Barcode detected and product found!
            </div>
          </div>
        `;
      }
    }, 2000); // 2 second delay to simulate processing
    
    // In a real application, you would send this to your Flask backend:
    // uploadImageToFlask(file);
  }

  function searchProduct(query) {
    if (!query.trim()) {
      showToast('Please enter a product name to search', 'warning');
      return;
    }
    
    showToast('Searching for products...', 'info');
    
    // Simulate search delay
    setTimeout(() => {
      // Mock search results
      const searchResults = document.getElementById('search-results');
      if (searchResults) {
        searchResults.classList.remove('d-none');
        searchResults.innerHTML = `
          <div class="list-group">
            <div class="list-group-item list-group-item-action" onclick="selectSearchResult('${query} - Product 1')">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1">${query} - Premium Brand</h6>
                  <p class="mb-1">Natural ingredients, organic certified</p>
                  <small class="text-muted">Category: ${category}</small>
                </div>
                <span class="badge bg-success rounded-pill">95% Match</span>
              </div>
            </div>
            <div class="list-group-item list-group-item-action" onclick="selectSearchResult('${query} - Product 2')">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1">${query} - Standard Brand</h6>
                  <p class="mb-1">Common ingredients, affordable option</p>
                  <small class="text-muted">Category: ${category}</small>
                </div>
                <span class="badge bg-warning rounded-pill">78% Match</span>
              </div>
            </div>
            <div class="list-group-item list-group-item-action" onclick="selectSearchResult('${query} - Product 3')">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1">${query} - Budget Brand</h6>
                  <p class="mb-1">Basic ingredients, economy choice</p>
                  <small class="text-muted">Category: ${category}</small>
                </div>
                <span class="badge bg-info rounded-pill">65% Match</span>
              </div>
            </div>
          </div>
        `;
      }
      
      showToast('Found 3 matching products!', 'success');
    }, 1000);
  }

  // Global function for search result selection
  window.selectSearchResult = function(productName) {
    const mockProductData = {
      name: productName,
      brand: 'Selected Brand',
      ingredients: 'Water, Sugar, Natural Flavors, Citric Acid, Preservatives (E202, E211)',
      category: category,
      nutrition: 'Calories: 140, Sugar: 35g, Sodium: 40mg, Vitamin C: 60mg',
      searchQuery: productName
    };
    
    showToast('Product selected!', 'success');
    showAnalysisResults(mockProductData);
    
    // Hide search results
    const searchResults = document.getElementById('search-results');
    if (searchResults) {
      searchResults.classList.add('d-none');
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
      // Generate mock analysis based on category
      const analysisData = generateMockAnalysis(productData);
      
      resultsContent.innerHTML = `
        <div class="row">
          <!-- Product Information -->
          <div class="col-lg-6 mb-4">
            <div class="card border-0 bg-light">
              <div class="card-body">
                <h6 class="card-title fw-bold text-primary mb-3">
                  <i class="fas fa-info-circle me-2"></i>Product Information
                </h6>
                <ul class="list-unstyled mb-0">
                  <li class="mb-2"><strong>Name:</strong> ${productData.name}</li>
                  <li class="mb-2"><strong>Brand:</strong> ${productData.brand || 'Not specified'}</li>
                  <li class="mb-2"><strong>Category:</strong> ${capitalizeFirst(productData.category)}</li>
                  ${productData.barcode ? `<li class="mb-2"><strong>Barcode:</strong> ${productData.barcode}</li>` : ''}
                  ${productData.imageFile ? `<li class="mb-2"><strong>Source:</strong> Image scan (${productData.imageFile})</li>` : ''}
                  ${productData.searchQuery ? `<li class="mb-2"><strong>Source:</strong> Search result</li>` : ''}
                </ul>
              </div>
            </div>
          </div>
          
          <!-- Safety Score -->
          <div class="col-lg-6 mb-4">
            <div class="card border-0 bg-light">
              <div class="card-body text-center">
                <h6 class="card-title fw-bold text-primary mb-3">
                  <i class="fas fa-shield-alt me-2"></i>Safety Score
                </h6>
                <div class="position-relative mb-3">
                  <div class="progress" style="height: 20px;">
                    <div class="progress-bar bg-${analysisData.scoreColor}" style="width: ${analysisData.safetyScore}%"></div>
                  </div>
                  <span class="position-absolute top-50 start-50 translate-middle fw-bold text-dark">
                    ${analysisData.safetyScore}/100
                  </span>
                </div>
                <span class="badge bg-${analysisData.scoreColor} fs-6">${analysisData.safetyLabel}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Ingredients Analysis -->
        <div class="card border-0 mb-4">
          <div class="card-header bg-transparent border-0">
            <h6 class="fw-bold text-primary mb-0">
              <i class="fas fa-list me-2"></i>Ingredients Analysis
            </h6>
          </div>
          <div class="card-body">
            <div class="bg-light p-3 rounded mb-3">
              <strong>Ingredients:</strong> ${productData.ingredients}
            </div>
            <div class="row">
              <div class="col-md-6">
                <h6 class="text-success fw-bold">✓ Safe Ingredients</h6>
                <ul class="list-unstyled text-success">
                  ${analysisData.safeIngredients.map(ingredient => `<li>• ${ingredient}</li>`).join('')}
                </ul>
              </div>
              <div class="col-md-6">
                <h6 class="text-warning fw-bold">⚠ Caution Ingredients</h6>
                <ul class="list-unstyled text-warning">
                  ${analysisData.cautionIngredients.map(ingredient => `<li>• ${ingredient}</li>`).join('')}
                </ul>
              </div>
            </div>
          </div>
        </div>

        ${productData.nutrition ? `
        <!-- Nutrition Information -->
        <div class="card border-0 mb-4">
          <div class="card-header bg-transparent border-0">
            <h6 class="fw-bold text-primary mb-0">
              <i class="fas fa-chart-bar me-2"></i>Nutrition Information
            </h6>
          </div>
          <div class="card-body">
            <div class="bg-light p-3 rounded">
              ${productData.nutrition}
            </div>
          </div>
        </div>
        ` : ''}

        <!-- Recommendations -->
        <div class="card border-0 mb-4">
          <div class="card-header bg-transparent border-0">
            <h6 class="fw-bold text-primary mb-0">
              <i class="fas fa-lightbulb me-2"></i>Personalized Recommendations
            </h6>
          </div>
          <div class="card-body">
            <div class="row">
              ${analysisData.recommendations.map((rec, index) => `
                <div class="col-12 mb-2">
                  <div class="alert alert-${rec.type} mb-2">
                    <i class="fas fa-${rec.icon} me-2"></i>${rec.message}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="text-center">
          <button class="btn btn-success me-2" onclick="saveToProfile('${productData.name}')">
            <i class="fas fa-bookmark me-2"></i>Save to Profile
          </button>
          <button class="btn btn-primary me-2" onclick="shareResults('${productData.name}')">
            <i class="fas fa-share me-2"></i>Share Results
          </button>
          <button class="btn btn-outline-secondary" onclick="analyzeAnother()">
            <i class="fas fa-plus me-2"></i>Analyze Another
          </button>
        </div>
      `;
      
      resultsSection.classList.remove('d-none');
      resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
  }

  function generateMockAnalysis(productData) {
    // Mock analysis logic based on category and ingredients
    let safetyScore = Math.floor(Math.random() * 30) + 70; // 70-100
    let scoreColor = safetyScore >= 85 ? 'success' : safetyScore >= 65 ? 'warning' : 'danger';
    let safetyLabel = safetyScore >= 85 ? 'Safe' : safetyScore >= 65 ? 'Caution' : 'Avoid';
    
    const ingredients = productData.ingredients.split(',').map(ing => ing.trim());
    const safeIngredients = ingredients.filter(ing => 
      ['Water', 'Natural Flavors', 'Vitamin C'].some(safe => ing.includes(safe))
    );
    const cautionIngredients = ingredients.filter(ing => 
      ['Sugar', 'Sodium', 'Preservative', 'Citric Acid'].some(caution => ing.includes(caution))
    );

    const recommendations = [
      {
        type: 'info',
        icon: 'info-circle',
        message: `This ${productData.category} product has been analyzed based on your health profile.`
      },
      {
        type: safetyScore >= 85 ? 'success' : 'warning',
        icon: safetyScore >= 85 ? 'check-circle' : 'exclamation-triangle',
        message: safetyScore >= 85 
          ? 'This product appears to be safe for your consumption based on your allergen profile.'
          : 'Please review the caution ingredients against your personal allergen list.'
      },
      {
        type: 'primary',
        icon: 'heart',
        message: 'Consider your dietary preferences and health goals when consuming this product.'
      }
    ];

    return {
      safetyScore,
      scoreColor,
      safetyLabel,
      safeIngredients,
      cautionIngredients,
      recommendations
    };
  }

  function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // Global functions for action buttons
  window.saveToProfile = function(productName) {
    showToast(`${productName} saved to your profile!`, 'success');
  };

  window.shareResults = function(productName) {
    showToast(`Analysis results for ${productName} ready to share!`, 'info');
  };

  window.analyzeAnother = function() {
    window.location.reload();
  };

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