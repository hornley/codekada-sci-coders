// User Setup Page JavaScript for Flask
document.addEventListener('DOMContentLoaded', function() {
  // Multi-step form functionality
  let currentStep = 1;
  const totalSteps = 6;
  
  // Initialize the form
  showStep(currentStep);
  
  function showStep(step) {
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
  }

  function validateStep(step) {
    if (step === 1) {
      const fullName = document.getElementById('fullName')?.value;
      const age = document.getElementById('age')?.value;
      return fullName && age;
    }
    return true; // Other steps are optional
  }

  // Navigation event listeners
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const completeBtn = document.getElementById('complete-btn');

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
        showToast('Please fill in the required fields', 'warning');
      }
    });
  }

  if (completeBtn) {
    completeBtn.addEventListener('click', () => {
      if (validateStep(currentStep)) {
        handleProfileCompletion();
      } else {
        showToast('Please fill in the required fields', 'warning');
      }
    });
  }

  function handleProfileCompletion() {
    const formData = collectFormData();
    
    // Create user profile
    const profile = {
      id: Date.now(),
      ...formData,
      createdAt: new Date().toISOString()
    };

    localStorage.setItem('rekada_user_profile', JSON.stringify(profile));
    
    showToast('Profile created successfully!', 'success');
    
    // Navigate to dashboard after a short delay
    setTimeout(() => {
      window.location.href = '/dashboard';
    }, 1500);
  }

  function collectFormData() {
    const formData = {
      fullName: document.getElementById('fullName')?.value || '',
      birthday: document.getElementById('birthday')?.value || '',
      age: parseInt(document.getElementById('age')?.value) || 0,
      foodAllergens: collectCheckboxData([
        'milk-allergy', 'eggs-allergy', 'fish-allergy', 'shellfish-allergy',
        'peanuts-allergy', 'tree-nuts-allergy', 'soybeans-allergy', 'wheat-allergy', 'sesame-allergy',
        'flavor-enhancers', 'preservatives-irritant', 'artificial-colors', 'artificial-sweeteners',
        'acids-irritant', 'emulsifiers-irritant', 'flavoring-agents'
      ]),
      beautyAllergens: collectCheckboxData([
        'fragrance-allergy', 'limonene-allergy', 'linalool-allergy', 'citronellol-allergy',
        'geraniol-allergy', 'eugenol-allergy', 'cinnamal-allergy', 'balsam-peru-allergy',
        'parabens-allergy', 'formaldehyde-allergy', 'isothiazolinones-allergy', 'phenoxyethanol-allergy',
        'sodium-benzoate-beauty', 'benzyl-alcohol-allergy', 'essential-oils-allergy', 'aloe-vera-allergy',
        'chamomile-allergy', 'calendula-allergy', 'coconut-oil-allergy', 'shea-butter-allergy',
        'almond-oil-allergy', 'eucalyptus-allergy'
      ]),
      comorbidities: collectCheckboxData([
        'hypertension', 'hyperlipidemia', 'coronary-artery-disease', 'heart-failure',
        'atrial-fibrillation', 'peripheral-artery-disease', 'type2-diabetes', 'obesity',
        'hypothyroidism', 'hyperthyroidism', 'pcos', 'gout', 'asthma', 'copd',
        'chronic-bronchitis', 'sleep-apnea', 'pulmonary-hypertension'
      ]),
      dietPreferences: collectCheckboxData([
        'plant-based', 'animal-based-low-carb', 'halal-diet', 'kosher-diet',
        'hindu-diet', 'buddhist-diet', 'rastafarian-diet'
      ]),
      healthPreferences: collectCheckboxData([
        'gluten-free', 'lactose-free', 'low-sodium', 'low-fat',
        'low-carb', 'diabetic-diet', 'allergen-free'
      ])
    };

    return formData;
  }

  function collectCheckboxData(ids) {
    const result = [];
    ids.forEach(id => {
      const checkbox = document.getElementById(id);
      if (checkbox && checkbox.checked) {
        result.push(checkbox.value);
      }
    });
    return result;
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