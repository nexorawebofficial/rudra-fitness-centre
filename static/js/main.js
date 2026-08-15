(function () {
    'use strict';

    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Animated count-up for elements marked [data-counter="123"]. The element's
    // initial text is already the real number (safe if JS never runs); the
    // animation briefly resets to 0 and counts back up. No IntersectionObserver
    // dependency -- it just runs once on load, so it can never leave content
    // stuck invisible on a mobile browser that handles scroll timing differently.
    var counters = document.querySelectorAll('[data-counter]');
    function runCounter(el) {
        var target = parseInt(el.getAttribute('data-counter'), 10) || 0;
        if (target === 0) return;
        var duration = 1000;
        var start = null;
        function step(timestamp) {
            if (!start) start = timestamp;
            var progress = Math.min((timestamp - start) / duration, 1);
            var value = Math.floor(progress * target);
            el.textContent = value.toLocaleString('en-IN');
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                el.textContent = target.toLocaleString('en-IN');
            }
        }
        window.requestAnimationFrame(step);
    }
    if (!reduceMotion) {
        counters.forEach(runCounter);
    }
})();
