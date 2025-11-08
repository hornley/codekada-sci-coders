// Product Analyzer Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
  // Back to dashboard button
  const backBtn = document.getElementById('back-to-dashboard');
  if (backBtn) {
    backBtn.addEventListener('click', () => {
      window.location.href = 'index.html#dashboard';
    });
  }

  // Analyze buttons for each category
  const analyzeButtons = document.querySelectorAll('.analyze-btn');
  analyzeButtons.forEach(button => {
    button.addEventListener('click', () => {
      const category = button.getAttribute('data-category');
      loadProductScanner(category);
    });
  });

  // Card click handlers for better UX
  const categoryCards = document.querySelectorAll('[data-category]');
  categoryCards.forEach(card => {
    if (!card.querySelector('.analyze-btn')) {
      card.addEventListener('click', () => {
        const category = card.getAttribute('data-category');
        if (category) {
          loadProductScanner(category);
        }
      });
    }
  });

  // Add hover effects
  categoryCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-5px)';
      card.style.transition = 'transform 0.3s ease';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0)';
    });
  });

  function loadProductScanner(category) {
    // Store category for the scanner page
    sessionStorage.setItem('scanner_category', category);
    window.location.href = 'product-scanner.html';
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