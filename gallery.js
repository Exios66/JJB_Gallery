// Gallery and Lightbox functionality

(function() {
  'use strict';

  // Gallery images array - populate with your actual images
  // Format: { src: 'path/to/image.jpg', alt: 'Description' }
  const galleryImages = [
    // Add your images here
    // Example:
    // { src: 'images/image1.jpg', alt: 'Image 1 Description' },
    // { src: 'images/image2.jpg', alt: 'Image 2 Description' },
  ];

  // Initialize gallery when DOM is ready
  document.addEventListener('DOMContentLoaded', function() {
    const viewAllBtn = document.getElementById('view-all-btn');
    const galleryContainer = document.getElementById('gallery-container');
    const galleryGrid = document.getElementById('gallery-grid');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxClose = document.querySelector('.lightbox-close');
    const lightboxPrev = document.querySelector('.lightbox-prev');
    const lightboxNext = document.querySelector('.lightbox-next');

    let currentImageIndex = 0;

    // If no images are configured, disable the UI affordance.
    if (viewAllBtn && galleryImages.length === 0) {
      viewAllBtn.disabled = true;
      viewAllBtn.textContent = 'Gallery (coming soon)';
      viewAllBtn.setAttribute('aria-disabled', 'true');
    }

    // Populate gallery grid with images
    function populateGallery() {
      if (galleryImages.length === 0) {
        galleryGrid.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; padding: 2rem;">No images available. Please add images to the galleryImages array in gallery.js</p>';
        return;
      }

      galleryGrid.innerHTML = '';
      galleryImages.forEach((image, index) => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';
        galleryItem.setAttribute('data-index', index);
        
        const img = document.createElement('img');
        img.src = image.src;
        img.alt = image.alt || `Image ${index + 1}`;
        img.loading = 'lazy';
        
        galleryItem.appendChild(img);
        galleryItem.addEventListener('click', () => openLightbox(index));
        galleryGrid.appendChild(galleryItem);
      });
    }

    // Toggle gallery visibility
    if (viewAllBtn && galleryContainer) {
      viewAllBtn.addEventListener('click', function() {
        const isVisible = galleryContainer.style.display !== 'none';
        
        if (!isVisible) {
          populateGallery();
          galleryContainer.style.display = 'block';
          viewAllBtn.textContent = 'Hide Gallery';
          // Smooth scroll to gallery
          galleryContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
          galleryContainer.style.display = 'none';
          viewAllBtn.textContent = 'View All Images';
        }
      });
    }

    // Open lightbox
    function openLightbox(index) {
      if (galleryImages.length === 0) return;
      
      currentImageIndex = index;
      updateLightboxImage();
      lightbox.classList.add('active');
      lightbox.style.display = 'flex';
      document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    // Close lightbox
    function closeLightbox() {
      lightbox.classList.remove('active');
      lightbox.style.display = 'none';
      document.body.style.overflow = ''; // Restore scrolling
    }

    // Update lightbox image
    function updateLightboxImage() {
      if (galleryImages[currentImageIndex]) {
        lightboxImg.src = galleryImages[currentImageIndex].src;
        lightboxImg.alt = galleryImages[currentImageIndex].alt || `Image ${currentImageIndex + 1}`;
      }
    }

    // Navigate to previous image
    function showPreviousImage() {
      if (galleryImages.length === 0) return;
      currentImageIndex = (currentImageIndex - 1 + galleryImages.length) % galleryImages.length;
      updateLightboxImage();
    }

    // Navigate to next image
    function showNextImage() {
      if (galleryImages.length === 0) return;
      currentImageIndex = (currentImageIndex + 1) % galleryImages.length;
      updateLightboxImage();
    }

    // Event listeners
    if (lightboxClose) {
      lightboxClose.addEventListener('click', closeLightbox);
    }

    if (lightboxPrev) {
      lightboxPrev.addEventListener('click', (e) => {
        e.stopPropagation();
        showPreviousImage();
      });
    }

    if (lightboxNext) {
      lightboxNext.addEventListener('click', (e) => {
        e.stopPropagation();
        showNextImage();
      });
    }

    // Close lightbox when clicking outside the image
    if (lightbox) {
      lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
          closeLightbox();
        }
      });
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
      if (lightbox.classList.contains('active')) {
        if (e.key === 'Escape') {
          closeLightbox();
        } else if (e.key === 'ArrowLeft') {
          showPreviousImage();
        } else if (e.key === 'ArrowRight') {
          showNextImage();
        }
      }
    });

    // Touch/swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    if (lightbox) {
      lightbox.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      lightbox.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
      }, { passive: true });
    }

    function handleSwipe() {
      const swipeThreshold = 50;
      const diff = touchStartX - touchEndX;

      if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
          // Swipe left - next image
          showNextImage();
        } else {
          // Swipe right - previous image
          showPreviousImage();
        }
      }
    }
  });
})();
