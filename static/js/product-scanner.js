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
    showToast('Processing image...', 'info');
    
    // Get user_id from localStorage if available
    const user_id = localStorage.getItem('rekada_user_id');
    
    // Create FormData to send file
    const formData = new FormData();
    formData.append('image', file);
    if (user_id) {
      formData.append('user_id', user_id);
    }
    
    // Show loading state
    const resultsContainer = document.getElementById('results-container');
    if (resultsContainer) {
      resultsContainer.innerHTML = `
        <div class="text-center p-5">
          <i class="fas fa-spinner fa-spin fa-3x text-primary mb-3"></i>
          <p class="text-muted">Analyzing product image...</p>
        </div>
      `;
      resultsContainer.classList.remove('d-none');
    }
    
    // Call the analyze API
    fetch('/api/analyze/image', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        displayAnalysisResults(data);
        showToast('Analysis complete!', 'success');
      } else {
        throw new Error(data.error || 'Analysis failed');
      }
    })
    .catch(error => {
      console.error('Error analyzing image:', error);
      showToast('Failed to analyze image: ' + error.message, 'error');
      if (resultsContainer) {
        resultsContainer.innerHTML = `
          <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            Error: ${error.message}
          </div>
        `;
      }
    });
  }

  function searchProduct(query) {
    if (!query.trim()) {
      showToast('Please enter a product name to search', 'warning');
      return;
    }
    
    showToast('Searching products...', 'info');
    
    // Call the search API
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success' && data.results) {
        displaySearchResults(data.results, query);
      } else {
        throw new Error('Search failed');
      }
    })
    .catch(error => {
      console.error('Error searching:', error);
      showToast('Search failed: ' + error.message, 'error');
      
      // Show empty results
      const searchResults = document.getElementById('search-results');
      if (searchResults) {
        searchResults.classList.remove('d-none');
        searchResults.innerHTML = `
          <div class="alert alert-warning">
            <i class="fas fa-exclamation-triangle me-2"></i>
            No results found for "${query}"
          </div>
        `;
      }
    });
  }

  function displaySearchResults(results, query) {
    const searchResults = document.getElementById('search-results');
    if (!searchResults) return;
    
    if (results.length === 0) {
      searchResults.classList.remove('d-none');
      searchResults.innerHTML = `
        <div class="alert alert-info">
          <i class="fas fa-info-circle me-2"></i>
          No results found for "${query}"
        </div>
      `;
      return;
    }
    
    let html = '<div class="list-group">';
    results.forEach(result => {
      html += `
        <div class="list-group-item">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h6 class="mb-1">${result.name}</h6>
              <small class="text-muted">
                ${result.category} 
                ${result.times_seen ? `(seen ${result.times_seen} times)` : ''}
              </small>
            </div>
            <button class="btn btn-sm btn-outline-primary" onclick="selectSearchResult('${result.name}')">
              Select
            </button>
          </div>
        </div>
      `;
    });
    html += '</div>';
    
    searchResults.classList.remove('d-none');
    searchResults.innerHTML = html;
  }

  window.selectSearchResult = function(name) {
    const searchInput = document.getElementById('product-search-input');
    if (searchInput) {
      searchInput.value = name;
    }
    showToast(`Selected: ${name}`, 'success');
  };

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

  function displayAnalysisResults(data) {
    const resultsContainer = document.getElementById('results-container');
    if (!resultsContainer) return;
    
    // Extract data with fallbacks
    const productName = data.product_name || 'None';
    const productType = (data.product_type || 'unknown').toUpperCase();
    const classificationConfidence = data.classification_confidence || 0;
    const confidencePercent = Math.round(classificationConfidence * 100);
    
    // Ingredients
    const ingredientsText = data.ingredients_text || 'No ingredients detected';
    
    // Health Assessment
    const healthinessRating = data.healthiness_rating || 5;
    const fdaApproval = data.fda_approval || 'Unverified';
    
    // Build rating stars (10-star system)
    const filledStars = '⭐'.repeat(healthinessRating);
    const emptyStars = '☆'.repeat(10 - healthinessRating);
    
    // Warnings & Alerts
    const harmful = data.harmful_ingredients || [];
    const allergens = data.allergens || [];
    const irritants = data.irritants || [];
    const warnings = data.warnings_for_user || [];
    
    // Detailed Breakdown
    const additives = data.additives || [];
    const preservatives = data.preservatives || [];
    const chemicals = data.chemicals || [];
    
    // Certifications
    const certifications = data.certifications || [];
    
    // Recommendations
    const recommendation = data.recommendation || 'No recommendation available';
    const healthSuggestion = data.health_suggestion || '';
    const personalizedRec = data.personalized_recommendation || '';
    
    // Build HTML in MD format style
    let html = `
      <div class="card shadow-lg border-0 mb-4">
        <div class="card-header bg-dark text-white py-3">
          <h3 class="mb-0 text-center fw-bold" style="font-family: monospace;">
            ════════════════════════════════════════════════════════════════════════════════<br>
            INGREDIENT INTELLIGENCE ANALYSIS REPORT<br>
            ════════════════════════════════════════════════════════════════════════════════
          </h3>
          <p class="mb-0 text-center mt-2"><small>Generated: ${new Date().toLocaleString()}</small></p>
        </div>
        
        <div class="card-body p-4" style="font-family: 'Courier New', monospace; background-color: #f8f9fa;">
          
          <!-- Product Information -->
          <div class="mb-4">
            <h5 class="fw-bold text-primary">📦 PRODUCT INFORMATION</h5>
            <hr class="my-2" style="border-top: 2px dashed #dee2e6;">
            <div class="ms-3">
              <p class="mb-1"><strong>Product Name:</strong> ${productName}</p>
              <p class="mb-1"><strong>Product Type:</strong> ${productType}</p>
              <p class="mb-1"><strong>Classification Confidence:</strong> ${confidencePercent}%</p>
            </div>
          </div>
          
          <!-- Ingredients -->
          <div class="mb-4">
            <h5 class="fw-bold text-primary">🧪 INGREDIENTS</h5>
            <hr class="my-2" style="border-top: 2px dashed #dee2e6;">
            <div class="ms-3 p-3 bg-white rounded border">
              <p class="mb-0" style="white-space: pre-wrap; word-wrap: break-word;">${ingredientsText}</p>
            </div>
          </div>
          
          <!-- Health Assessment -->
          <div class="mb-4">
            <h5 class="fw-bold text-primary">💚 HEALTH ASSESSMENT</h5>
            <hr class="my-2" style="border-top: 2px dashed #dee2e6;">
            <div class="ms-3">
              <p class="mb-1"><strong>Healthiness Rating:</strong> <span class="fs-5">${healthinessRating}/10 ${filledStars}${emptyStars}</span></p>
              <p class="mb-1"><strong>FDA Approval Status:</strong> ${fdaApproval}</p>
            </div>
          </div>
          
          <!-- Warnings & Alerts -->
          <div class="mb-4">
            <h5 class="fw-bold text-primary">⚠️  WARNINGS & ALERTS</h5>
            <hr class="my-2" style="border-top: 2px dashed #dee2e6;">
            <div class="ms-3">
              ${harmful.length > 0 ? `
                <div class="mb-3">
                  <p class="mb-2 text-danger fw-bold">❌ Harmful Ingredients (${harmful.length}):</p>
                  <ul class="mb-0">
                    ${harmful.map(h => `<li>• ${h}</li>`).join('')}
                  </ul>
                </div>
              ` : '<p class="text-success">✅ No known harmful ingredients detected</p>'}
              
              ${allergens.length > 0 ? `
                <div class="mb-3">
                  <p class="mb-2 text-warning fw-bold">🔴 Allergens (${allergens.length}):</p>
                  <ul class="mb-0">
                    ${allergens.map(a => `<li>• ${a}</li>`).join('')}
                  </ul>
                </div>
              ` : '<p class="text-success">✅ No common allergens detected</p>'}
              
              ${irritants.length > 0 ? `
                <div class="mb-3">
                  <p class="mb-2 text-warning fw-bold">⚡ Irritants (${irritants.length}):</p>
                  <ul class="mb-0">
                    ${irritants.map(i => `<li>• ${i}</li>`).join('')}
                  </ul>
                </div>
              ` : ''}
              
              ${warnings.length > 0 ? `
                <div class="alert alert-warning mt-3">
                  <p class="mb-2 fw-bold">⚡ Personalized Warnings:</p>
                  <ul class="mb-0">
                    ${warnings.map(w => `<li>• ${w}</li>`).join('')}
                  </ul>
                </div>
              ` : ''}
            </div>
          </div>
          
          <!-- Detailed Breakdown -->
          <div class="mb-4">
            <h5 class="fw-bold text-primary">📋 DETAILED BREAKDOWN</h5>
            <hr class="my-2" style="border-top: 2px dashed #dee2e6;">
            <div class="ms-3">
              ${additives.length > 0 ? `
                <p class="mb-1"><strong>Additives (${additives.length}):</strong> ${additives.join(', ')}</p>
              ` : ''}
              ${preservatives.length > 0 ? `
                <p class="mb-1"><strong>Preservatives (${preservatives.length}):</strong> ${preservatives.join(', ')}</p>
              ` : ''}
              ${chemicals.length > 0 ? `
                <p class="mb-1"><strong>Chemicals (${chemicals.length}):</strong> ${chemicals.join(', ')}</p>
              ` : ''}
              ${!additives.length && !preservatives.length && !chemicals.length ? `
                <p class="mb-0">No significant additives or chemicals detected</p>
              ` : ''}
            </div>
          </div>
          
          <!-- Certifications -->
          <div class="mb-4">
            <h5 class="fw-bold text-primary">✨ CERTIFICATIONS</h5>
            <hr class="my-2" style="border-top: 2px dashed #dee2e6;">
            <div class="ms-3">
              ${certifications.length > 0 ? `
                ${certifications.map(c => `<p class="mb-1">✓ ${c}</p>`).join('')}
              ` : '<p class="mb-0">No certifications detected</p>'}
            </div>
          </div>
          
          <!-- Recommendations -->
          <div class="mb-4">
            <h5 class="fw-bold text-primary">💡 RECOMMENDATIONS</h5>
            <hr class="my-2" style="border-top: 2px dashed #dee2e6;">
            <div class="ms-3">
              <p class="mb-2"><strong>Expert Opinion:</strong> ${recommendation}</p>
              ${healthSuggestion ? `<p class="mb-2"><strong>Health Tip:</strong> ${healthSuggestion}</p>` : ''}
              ${personalizedRec ? `
                <div class="alert alert-info mt-2">
                  <p class="mb-0"><strong>Personalized:</strong> ${personalizedRec}</p>
                </div>
              ` : ''}
            </div>
          </div>
          
          <!-- Action Buttons -->
          <div class="text-center mt-4 pt-3 border-top">
            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
              <button class="btn btn-success btn-lg px-4" onclick="logIntake(${JSON.stringify(data).replace(/"/g, '&quot;')})">
                <i class="fas fa-save me-2"></i>Log to History
              </button>
              <button class="btn btn-primary btn-lg px-4" onclick="downloadJSON(${JSON.stringify(data).replace(/"/g, '&quot;')})">
                <i class="fas fa-download me-2"></i>Download JSON
              </button>
              <button class="btn btn-outline-secondary btn-lg px-4" onclick="downloadMarkdown(${JSON.stringify(data).replace(/"/g, '&quot;')})">
                <i class="fas fa-file-alt me-2"></i>Download MD Report
              </button>
            </div>
          </div>
          
        </div>
        
        <div class="card-footer bg-dark text-white text-center py-2" style="font-family: monospace;">
          <small>════════════════════════════════════════════════════════════════════════════════</small><br>
          <small>Report generated by Ingredient Intelligence Analyzer</small><br>
          <small>Analysis Date: ${new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</small><br>
          <small>════════════════════════════════════════════════════════════════════════════════</small>
        </div>
      </div>
    `;
    
    resultsContainer.innerHTML = html;
    resultsContainer.classList.remove('d-none');
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Global function to log intake
  window.logIntake = function(analysisData) {
    const user_id = localStorage.getItem('rekada_user_id');
    if (!user_id) {
      showToast('Please set up your profile first', 'warning');
      return;
    }
    
    fetch('/api/intake/log', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: user_id,
        analysis_result: analysisData
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showToast('Product logged to history!', 'success');
      } else {
        throw new Error(data.error || 'Failed to log intake');
      }
    })
    .catch(error => {
      console.error('Error logging intake:', error);
      showToast('Failed to log intake: ' + error.message, 'error');
    });
  };

  // Global function to download report
  window.downloadReport = function(analysisData) {
    downloadJSON(analysisData);
  };
  
  // Global function to download JSON
  window.downloadJSON = function(analysisData) {
    const blob = new Blob([JSON.stringify(analysisData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const productName = (analysisData.product_name || 'product').replace(/\s+/g, '_').toLowerCase();
    a.download = `${productName}_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('JSON report downloaded!', 'success');
  };
  
  // Global function to download Markdown report
  window.downloadMarkdown = function(analysisData) {
    const md = generateMarkdownReport(analysisData);
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const productName = (analysisData.product_name || 'product').replace(/\s+/g, '_').toLowerCase();
    a.download = `${productName}_${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Markdown report downloaded!', 'success');
  };
  
  // Generate Markdown report (same format as simple_analyzer.py)
  function generateMarkdownReport(data) {
    const separator = '='.repeat(80);
    const dashedLine = '-'.repeat(80);
    
    const productName = data.product_name || 'None';
    const productType = (data.product_type || 'unknown').toUpperCase();
    const classificationConfidence = data.classification_confidence || 0;
    const confidencePercent = Math.round(classificationConfidence * 100);
    
    const ingredientsText = data.ingredients_text || 'No ingredients detected';
    const healthinessRating = data.healthiness_rating || 5;
    const fdaApproval = data.fda_approval || 'Unverified';
    
    const filledStars = '⭐'.repeat(healthinessRating);
    const emptyStars = '☆'.repeat(10 - healthinessRating);
    
    const harmful = data.harmful_ingredients || [];
    const allergens = data.allergens || [];
    const irritants = data.irritants || [];
    const warnings = data.warnings_for_user || [];
    const additives = data.additives || [];
    const preservatives = data.preservatives || [];
    const chemicals = data.chemicals || [];
    const certifications = data.certifications || [];
    const recommendation = data.recommendation || 'No recommendation available';
    const healthSuggestion = data.health_suggestion || '';
    const personalizedRec = data.personalized_recommendation || '';
    
    let md = `${separator}\n`;
    md += `INGREDIENT INTELLIGENCE ANALYSIS REPORT\n`;
    md += `${separator}\n`;
    md += `Generated: ${new Date().toLocaleString()}\n\n`;
    
    md += `📦 PRODUCT INFORMATION\n`;
    md += `${dashedLine}\n`;
    md += `Product Name: ${productName}\n`;
    md += `Product Type: ${productType}\n`;
    md += `Classification Confidence: ${confidencePercent}%\n\n`;
    
    md += `🧪 INGREDIENTS\n`;
    md += `${dashedLine}\n`;
    md += `${ingredientsText}\n\n`;
    
    md += `💚 HEALTH ASSESSMENT\n`;
    md += `${dashedLine}\n`;
    md += `Healthiness Rating: ${healthinessRating}/10 ${filledStars}${emptyStars}\n`;
    md += `FDA Approval Status: ${fdaApproval}\n\n`;
    
    md += `⚠️  WARNINGS & ALERTS\n`;
    md += `${dashedLine}\n`;
    if (harmful.length > 0) {
      md += `❌ Harmful Ingredients (${harmful.length}):\n`;
      harmful.forEach(h => md += `   • ${h}\n`);
      md += `\n`;
    } else {
      md += `✅ No known harmful ingredients detected\n\n`;
    }
    
    if (allergens.length > 0) {
      md += `🔴 Allergens (${allergens.length}):\n`;
      allergens.forEach(a => md += `   • ${a}\n`);
      md += `\n`;
    } else {
      md += `✅ No common allergens detected\n\n`;
    }
    
    if (irritants.length > 0) {
      md += `⚡ Irritants (${irritants.length}):\n`;
      irritants.forEach(i => md += `   • ${i}\n`);
      md += `\n`;
    }
    
    if (warnings.length > 0) {
      md += `⚡ Personalized Warnings:\n`;
      warnings.forEach(w => md += `   • ${w}\n`);
      md += `\n`;
    }
    
    md += `📋 DETAILED BREAKDOWN\n`;
    md += `${dashedLine}\n`;
    if (additives.length > 0) {
      md += `Additives (${additives.length}): ${additives.join(', ')}\n`;
    }
    if (preservatives.length > 0) {
      md += `Preservatives (${preservatives.length}): ${preservatives.join(', ')}\n`;
    }
    if (chemicals.length > 0) {
      md += `Chemicals (${chemicals.length}): ${chemicals.join(', ')}\n`;
    }
    if (!additives.length && !preservatives.length && !chemicals.length) {
      md += `No significant additives or chemicals detected\n`;
    }
    md += `\n`;
    
    md += `✨ CERTIFICATIONS\n`;
    md += `${dashedLine}\n`;
    if (certifications.length > 0) {
      certifications.forEach(c => md += `✓ ${c}\n`);
    } else {
      md += `No certifications detected\n`;
    }
    md += `\n`;
    
    md += `💡 RECOMMENDATIONS\n`;
    md += `${dashedLine}\n`;
    md += `Expert Opinion: ${recommendation}\n`;
    if (healthSuggestion) {
      md += `Health Tip: ${healthSuggestion}\n`;
    }
    if (personalizedRec) {
      md += `Personalized: ${personalizedRec}\n`;
    }
    md += `\n`;
    
    md += `${separator}\n`;
    md += `Report generated by Ingredient Intelligence Analyzer\n`;
    md += `Analysis Date: ${new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}\n`;
    md += `${separator}\n`;
    
    return md;
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