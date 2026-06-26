/**
 * Homepage animations & interactions
 */
document.addEventListener('DOMContentLoaded', function () {
    if (!document.body.classList.contains('page-home')) return;

    initScrollReveal();
    initCounters();
    initHeroCarouselAnimations();
    initSmoothScrollToBooking();
});

function initScrollReveal() {
    var revealElements = document.querySelectorAll(
        '.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger-children, .section-header, .gallery-card'
    );

    if (!('IntersectionObserver' in window)) {
        revealElements.forEach(function (el) { el.classList.add('is-visible'); });
        return;
    }

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px',
    });

    revealElements.forEach(function (el) { observer.observe(el); });
}

function initCounters() {
    var counters = document.querySelectorAll('[data-count]');
    if (!counters.length) return;

    var animated = false;

    function animateCounters() {
        if (animated) return;
        animated = true;

        counters.forEach(function (counter) {
            var target = parseInt(counter.getAttribute('data-count'), 10);
            var suffix = counter.getAttribute('data-suffix') || '';
            var duration = 2000;
            var start = 0;
            var startTime = null;

            function step(timestamp) {
                if (!startTime) startTime = timestamp;
                var progress = Math.min((timestamp - startTime) / duration, 1);
                var eased = 1 - Math.pow(1 - progress, 3);
                var current = Math.floor(eased * target);
                counter.textContent = current.toLocaleString() + suffix;
                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    counter.textContent = target.toLocaleString() + suffix;
                }
            }

            requestAnimationFrame(step);
        });
    }

    var statsBar = document.querySelector('.stats-bar');
    if (!statsBar) return;

    if ('IntersectionObserver' in window) {
        var statsObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCounters();
                    statsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        statsObserver.observe(statsBar);
    } else {
        animateCounters();
    }
}

function initHeroCarouselAnimations() {
    var carousel = document.getElementById('heroCarousel');
    if (!carousel) return;

    carousel.addEventListener('slid.bs.carousel', function () {
        var active = carousel.querySelector('.carousel-item.active');
        if (!active) return;

        var animated = active.querySelectorAll('.hero-badge, .hero-title, .hero-subtitle, .hero-gold-line, .hero-cta-group');
        animated.forEach(function (el) {
            el.style.animation = 'none';
            el.offsetHeight; // reflow
            el.style.animation = '';
        });
    });
}

function initSmoothScrollToBooking() {
    var scrollBtn = document.querySelector('[data-scroll-to="booking"]');
    if (!scrollBtn) return;

    scrollBtn.addEventListener('click', function (e) {
        e.preventDefault();
        var target = document.querySelector('.booking-widget-section');
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
}
