// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;

// Check for saved theme preference or default to light mode
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);
if (savedTheme === 'dark') {
  themeToggle.classList.add('active');
}

themeToggle.addEventListener('click', () => {
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';
  
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  themeToggle.classList.toggle('active');
});

// Mobile Menu Toggle
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobile-menu');
const closeMenu = document.getElementById('close-menu');

// Open mobile menu
hamburger.addEventListener('click', () => {
  mobileMenu.classList.add('open');
});

// Close mobile menu
closeMenu.addEventListener('click', closeMobileMenu);

function closeMobileMenu() {
  mobileMenu.classList.remove('open');
}

// Close mobile menu when a menu item is clicked
const mobileMenuLinks = mobileMenu.querySelectorAll('a[href^="#"]');
mobileMenuLinks.forEach(link => {
  link.addEventListener('click', closeMobileMenu);
});

// Popup logic with safety check
const hireButton = document.getElementById('hire-me');
const contactPopup = document.getElementById('contact-popup');
const popupClose = document.getElementById('popup-close');

if (hireButton && contactPopup && popupClose) {
    hireButton.addEventListener('click', () => {
        contactPopup.classList.remove('hidden');
        // Optional: Disable scrolling when popup is open
        document.body.style.overflow = 'hidden';
    });

    popupClose.addEventListener('click', () => {
        contactPopup.classList.add('hidden');
        document.body.style.overflow = 'auto';
    });

    contactPopup.addEventListener('click', (e) => {
        if (e.target === contactPopup) {
            contactPopup.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    });
}
// Safety check for mobile menu
if (typeof mobileMenu !== 'undefined' && typeof hamburger !== 'undefined' && mobileMenu && hamburger) {
    document.addEventListener('click', (e) => {
        const isClickInsideMenu = mobileMenu.contains(e.target);
        const isClickOnHamburger = hamburger.contains(e.target);

        if (!isClickInsideMenu && !isClickOnHamburger && mobileMenu.classList.contains('open')) {
            closeMobileMenu();
        }
    });
}
document.addEventListener("DOMContentLoaded", () => {

    // ==========================================
    // 1. Mobile Menu Logic (Click Outside)
    // ==========================================
    // Assumes mobileMenu and hamburger variables are defined either globally or here.
    // If not, you may need to define them: const mobileMenu = document.querySelector('.mobile-menu');
    if (typeof mobileMenu !== 'undefined' && typeof hamburger !== 'undefined' && mobileMenu && hamburger) {
        document.addEventListener('click', (e) => {
            const isClickInsideMenu = mobileMenu.contains(e.target);
            const isClickOnHamburger = hamburger.contains(e.target);

            if (!isClickInsideMenu && !isClickOnHamburger && mobileMenu.classList.contains('open')) {
                if (typeof closeMobileMenu === 'function') {
                    closeMobileMenu();
                } else {
                    mobileMenu.classList.remove('open');
                }
            }
        });
    }

    // ==========================================
    // 2. Hero Section: Profession Text Animation
    // ==========================================
    const professionTextEl = document.querySelector('.profession-text');

if (professionTextEl) {
    const professions = ['Data Analyst', 'Python Developer', 'Web App Developer'];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typeSpeed = 150;

    function type() {
        const currentWord = professions[wordIndex];
        
        // Logic for typing vs deleting
        if (isDeleting) {
            professionTextEl.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
            typeSpeed = 75; // Faster when deleting
        } else {
            professionTextEl.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
            typeSpeed = 150; // Normal typing speed
        }

        // Switching states
        if (!isDeleting && charIndex === currentWord.length) {
            typeSpeed = 2000; // Pause at the end of the word
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % professions.length;
            typeSpeed = 500; // Short pause before starting next word
        }

        setTimeout(type, typeSpeed);
    }

    type();
}

    // ==========================================
    // 3. Hero Section: Particle Background
    // ==========================================
    const hero = document.querySelector('.hero');
    const heroCanvas = document.getElementById('hero-dots-canvas');

    if (hero && heroCanvas) {
        const ctx = heroCanvas.getContext('2d');
        const html = document.documentElement; // Added to reliably check data-theme
        
        let particles = [];
        let mouseX = 0;
        let mouseY = 0;
        let devicePixelRatio = window.devicePixelRatio || 1;

        function resizeHeroCanvas() {
            const rect = hero.getBoundingClientRect();
            heroCanvas.width = Math.floor(rect.width * devicePixelRatio);
            heroCanvas.height = Math.floor(rect.height * devicePixelRatio);
            heroCanvas.style.width = `${rect.width}px`;
            heroCanvas.style.height = `${rect.height}px`;
            ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
            initParticles(rect.width, rect.height);
        }

        function initParticles(width, height) {
            particles = [];
            const count = window.innerWidth < 768 ? 14 : 28;
            for (let i = 0; i < count; i++) {
                particles.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    vx: (Math.random() - 0.5) * 0.4,
                    vy: (Math.random() - 0.5) * 0.4,
                    radius: Math.random() * 1.6 + 1,
                    alpha: Math.random() * 0.4 + 0.15,
                });
            }
        }

        function getColor(theme) {
            if (theme === 'dark') {
                return { dot: 'rgba(196, 147, 253,', line: 'rgba(196, 147, 253,' };
            }
            return { dot: 'rgba(124, 58, 237,', line: 'rgba(124, 58, 237,' };
        }

        function drawParticles() {
            const theme = html.getAttribute('data-theme') || 'light';
            const colors = getColor(theme);
            ctx.clearRect(0, 0, heroCanvas.width, heroCanvas.height);

            const width = heroCanvas.width / devicePixelRatio;
            const height = heroCanvas.height / devicePixelRatio;

            ctx.fillStyle = theme === 'dark' ? 'rgba(17, 24, 39, 0.16)' : 'rgba(243, 240, 255, 0.1)';
            ctx.fillRect(0, 0, width, height);

            for (let p of particles) {
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < -20) p.x = width + 20;
                if (p.x > width + 20) p.x = -20;
                if (p.y < -20) p.y = height + 20;
                if (p.y > height + 20) p.y = -20;

                const mx = (mouseX - width / 2) * 0.005;
                const my = (mouseY - height / 2) * 0.005;
                p.x += mx;
                p.y += my;

                const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius * 7);
                grad.addColorStop(0, `${colors.dot} ${p.alpha * 0.4})`);
                grad.addColorStop(1, 'rgba(124, 58, 237, 0)');
                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius * 3, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = `${colors.dot} ${p.alpha})`;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fill();
            }

            const maxDistance = window.innerWidth < 768 ? 75 : 120;
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.hypot(dx, dy);
                    if (dist < maxDistance) {
                        const alpha = (1 - dist / maxDistance) * 0.09;
                        ctx.strokeStyle = `${colors.line} ${alpha})`;
                        ctx.lineWidth = 0.65;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }

            requestAnimationFrame(drawParticles);
        }

        window.addEventListener('mousemove', (event) => {
            const rect = hero.getBoundingClientRect();
            mouseX = (event.clientX - rect.left) / rect.width * (heroCanvas.width / devicePixelRatio);
            mouseY = (event.clientY - rect.top) / rect.height * (heroCanvas.height / devicePixelRatio);
        });

        hero.addEventListener('mouseleave', () => {
            mouseX = heroCanvas.width / devicePixelRatio / 2;
            mouseY = heroCanvas.height / devicePixelRatio / 2;
        });

        window.addEventListener('resize', resizeHeroCanvas);

        // Initialize the canvas and start the loop
        resizeHeroCanvas();
        drawParticles();
    }

    // ==========================================
    // 4. Global Scroll Animations
    // ==========================================
    const scrollElements = document.querySelectorAll('.animate-on-scroll');

    if (scrollElements.length > 0) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        }, observerOptions);

        scrollElements.forEach(el => {
            observer.observe(el);
        });
    }

});


const certificateItems = document.querySelectorAll('.certificate-item');
const certificatePrev = document.getElementById('certificate-prev');
const certificateNext = document.getElementById('certificate-next');
let certificateIndex = 0;

function updateCertificateSlider() {
    certificateItems.forEach((item, idx) => {
        if (idx === certificateIndex) {
            // Show Active Slide
            item.classList.remove('opacity-0', 'translate-x-12', 'pointer-events-none');
            item.classList.add('opacity-100', 'translate-x-0', 'z-10');
        } else {
            // Hide Others
            item.classList.remove('opacity-100', 'translate-x-0', 'z-10');
            item.classList.add('opacity-0', 'translate-x-12', 'pointer-events-none');
        }
    });
}

// Optimization: Check if elements exist before adding listeners
if (certificateItems.length > 0) {
    if (certificatePrev) {
        certificatePrev.addEventListener('click', () => {
            certificateIndex = (certificateIndex - 1 + certificateItems.length) % certificateItems.length;
            updateCertificateSlider();
        });
    }

    if (certificateNext) {
        certificateNext.addEventListener('click', () => {
            certificateIndex = (certificateIndex + 1) % certificateItems.length;
            updateCertificateSlider();
        });
    }

    // Initialize the slider
    updateCertificateSlider();

    // Auto-play (Optional: Changes slide every 5 seconds)
    let autoPlay = setInterval(() => {
        certificateIndex = (certificateIndex + 1) % certificateItems.length;
        updateCertificateSlider();
    }, 6000);

    // Pause auto-play when user interacts
    [certificatePrev, certificateNext].forEach(btn => {
        if(btn) btn.addEventListener('mouseenter', () => clearInterval(autoPlay));
    });
}


// Contact Form Feedback Logic
const contactForm = document.getElementById('contact-form');

if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        // e.preventDefault(); // Uncomment this when you start handling backend via AJAX
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // Visual feedback
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
        submitBtn.style.opacity = '0.7';

        // Note: For now, it will proceed to the "action" URL. 
        // If testing locally, you can see the button change.
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // 1. Check if the container actually exists on the page
    const flashContainer = document.getElementById('flash-container');

    if (flashContainer) {
        // 2. Find all individual messages inside the container
        const messages = flashContainer.querySelectorAll('.flash-message');

        if (messages.length > 0) {
            messages.forEach((msg) => {
                // Wait 3 seconds
                setTimeout(() => {
                    // Add the CSS class for sliding/fading out
                    msg.classList.add('fade-out');
                    
                    // Physically remove the element after the animation finishes
                    setTimeout(() => {
                        msg.remove();
                    }, 800); 
                }, 5000); 
            });
        }
    }
});


// testimonial
document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll(".star");
    const starsInput = document.getElementById("stars-input");

    stars.forEach((star) => {
        // Hover effect: Fill stars up to the one being hovered
        star.addEventListener("mouseover", () => {
            const value = star.getAttribute("data-value");
            highlightStars(value);
        });

        // Click effect: Select the rating
        star.addEventListener("click", () => {
            const value = star.getAttribute("data-value");
            starsInput.value = value;
            setSelectedStars(value);
        });

        // Mouse out: Reset to the currently selected value
        star.addEventListener("mouseout", () => {
            highlightStars(starsInput.value);
        });
    });

    function highlightStars(value) {
        stars.forEach((s) => {
            if (s.getAttribute("data-value") <= value) {
                s.classList.replace("fa-regular", "fa-solid");
                s.classList.add("active");
            } else {
                s.classList.replace("fa-solid", "fa-regular");
                s.classList.remove("active");
            }
        });
    }

    function setSelectedStars(value) {
        stars.forEach((s) => {
            if (s.getAttribute("data-value") <= value) {
                s.classList.add("selected");
            } else {
                s.classList.remove("selected");
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const track = document.getElementById('testimonial-track');
    const slides = Array.from(track.children);
    const dots = document.querySelectorAll('.dot');
    let currentIndex = 0;
    const intervalTime = 5000; // 5 Seconds

    if (slides.length === 0) return;

    function updateSlider(index) {
        // Move track
        track.style.transform = `translateX(-${index * 100}%)`;
        
        // Update dots
        dots.forEach((dot, i) => {
            if (i === index) {
                dot.classList.add('bg-[var(--button)]', 'w-8'); // Active dot is wider
                dot.classList.remove('bg-[var(--border)]');
            } else {
                dot.classList.remove('bg-[var(--button)]', 'w-8');
                dot.classList.add('bg-[var(--border)]');
            }
        });
        currentIndex = index;
    }

    // Dot Clicks
    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            updateSlider(i);
            resetAutoPlay();
        });
    });

    // Auto Play
    let autoPlay = setInterval(() => {
        let nextIndex = (currentIndex + 1) % slides.length;
        updateSlider(nextIndex);
    }, intervalTime);

    function resetAutoPlay() {
        clearInterval(autoPlay);
        autoPlay = setInterval(() => {
            let nextIndex = (currentIndex + 1) % slides.length;
            updateSlider(nextIndex);
        }, intervalTime);
    }

    // Initialize first slide
    updateSlider(0);
});


