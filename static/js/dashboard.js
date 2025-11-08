// Dashboard Page JavaScript for Flask
document.addEventListener('DOMContentLoaded', function() {
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
      window.location.href = '/analyzer';
    });
  }

  if (aboutBtn) {
    aboutBtn.addEventListener('click', () => {
      showToast('About page coming soon!', 'info');
    });
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('rekada_user_profile');
      window.location.href = '/';
    });
  }

  if (viewProfileBtn) {
    viewProfileBtn.addEventListener('click', () => {
      window.location.href = '/setup';
    });
  }

  // Update stats (placeholder)
  updateStats();

  function updateStats() {
    // Placeholder stats - in real app, these would come from backend
    document.getElementById('products-analyzed').textContent = '0';
    document.getElementById('safe-products').textContent = '0';
    document.getElementById('caution-products').textContent = '0';
    document.getElementById('avoid-products').textContent = '0';
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