/* ============================================================
   SUPPORT TICKET CLASSIFIER — Apple-Style Cinematic Scrollytelling
   GSAP 3.12.5 • ScrollTrigger • HTML5 Canvas
   ============================================================ */

// ─── Constants & Configuration ────────────────────────────────
const frameCount = 229;
const framePath = (index) => `animation_frames/ezgif-frame-${String(index).padStart(3, '0')}.jpg?v=9`;

const preloadedImages = [];
let loadedCount = 0;

// Easing and state variables
const mouse = { x: 0, y: 0, clientX: 0, clientY: 0 };
const scrollObj = { frame: 0 };

// ─── 1. Custom Cursor ─────────────────────────────────────────
(function initCustomCursor() {
    const cursor = document.getElementById('custom-cursor');
    const dot = document.querySelector('.cursor-dot');
    const ring = document.querySelector('.cursor-ring');
    if (!cursor || !dot || !ring) return;

    const pos = { x: 0, y: 0 };
    const ringPos = { x: 0, y: 0 };

    document.addEventListener('mousemove', (e) => {
        mouse.clientX = e.clientX;
        mouse.clientY = e.clientY;
        pos.x = e.clientX;
        pos.y = e.clientY;
    });

    function lerp(a, b, t) {
        return a + (b - a) * t;
    }

    function animateCursor() {
        dot.style.transform = `translate(${pos.x}px, ${pos.y}px) translate(-50%, -50%)`;
        
        ringPos.x = lerp(ringPos.x, pos.x, 0.15);
        ringPos.y = lerp(ringPos.y, pos.y, 0.15);
        ring.style.transform = `translate(${ringPos.x}px, ${ringPos.y}px) translate(-50%, -50%)`;

        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Hover triggers
    const hoverTargets = document.querySelectorAll('a, button, .glass-card, .magnetic-btn, .nav-link');
    hoverTargets.forEach((el) => {
        el.addEventListener('mouseenter', () => {
            ring.style.width = '48px';
            ring.style.height = '48px';
            ring.style.borderColor = '#F59E0B';
            ring.style.background = 'rgba(245, 158, 11, 0.05)';
        });
        el.addEventListener('mouseleave', () => {
            ring.style.width = '32px';
            ring.style.height = '32px';
            ring.style.borderColor = 'rgba(255, 255, 255, 0.4)';
            ring.style.background = 'transparent';
        });
    });
})();

// ─── 2. Magnetic Buttons ──────────────────────────────────────
(function initMagneticButtons() {
    const buttons = document.querySelectorAll('.magnetic-btn');
    buttons.forEach((btn) => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            const offsetX = e.clientX - centerX;
            const offsetY = e.clientY - centerY;
            // Shift button slightly towards mouse
            btn.style.transform = `translate(${offsetX * 0.25}px, ${offsetY * 0.25}px)`;
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0px, 0px)';
        });
    });
})();

// ─── 3. Canvas aspect-ratio cover drawer ──────────────────────
function drawImageProp(ctx, img, x, y, w, h, offsetX, offsetY) {
    if (arguments.length < 2) return;
    if (typeof x === 'undefined') x = 0;
    if (typeof y === 'undefined') y = 0;
    if (typeof w === 'undefined') w = ctx.canvas.width;
    if (typeof h === 'undefined') h = ctx.canvas.height;
    if (typeof offsetX === 'undefined') offsetX = 0.5;
    if (typeof offsetY === 'undefined') offsetY = 0.5;

    let iw = img.width,
        ih = img.height,
        r = Math.min(w / iw, h / ih),
        nw = iw * r,
        nh = ih * r,
        cx, cy, cw, ch;

    if (nw < w) {
        r = w / iw;
        nw = iw * r;
        nh = ih * r;
    }
    if (nh < h) {
        r = h / ih;
        nw = iw * r;
        nh = ih * r;
    }

    cw = iw / (nw / w);
    ch = ih / (nh / h);

    cx = (iw - cw) * offsetX;
    cy = (ih - ch) * offsetY;

    if (cx < 0) cx = 0;
    if (cy < 0) cy = 0;
    if (cw > iw) cw = iw;
    if (ch > ih) ch = ih;

    ctx.drawImage(img, cx, cy, cw, ch, x, y, w, h);
}

// ─── 4. Preload Image Sequence ────────────────────────────────
(function preloadFrames() {
    const preloader = document.getElementById('preloader');
    const ringCircle = document.querySelector('.progress-ring-circle');
    const percentageText = document.querySelector('.loader-percentage');
    const statusText = document.querySelector('.loader-status');

    if (!preloader || !ringCircle || !percentageText) return;

    // Progress circle stroke dash calculations
    const radius = ringCircle.r.baseVal.value;
    const circumference = radius * 2 * Math.PI;
    ringCircle.style.strokeDasharray = `${circumference} ${circumference}`;
    ringCircle.style.strokeDashoffset = circumference;

    const loaderStatusMessages = [
        "Initializing AI Engine...",
        "Preloading Sensory Data...",
        "Stabilizing Command Interface...",
        "Mapping Decision Tree Matrices...",
        "Resolving Classifier Neural Paths..."
    ];

    function updateProgress(progress) {
        const percent = Math.round(progress * 100);
        percentageText.textContent = `${percent}%`;

        // Update stroke progress ring
        const offset = circumference - (progress * circumference);
        ringCircle.style.strokeDashoffset = offset;

        // Cycle status messages
        const msgIdx = Math.floor(progress * loaderStatusMessages.length);
        if (loaderStatusMessages[msgIdx] && statusText) {
            statusText.textContent = loaderStatusMessages[msgIdx];
        }
    }

    function onAllLoaded() {
        setTimeout(() => {
            preloader.style.opacity = '0';
            preloader.style.visibility = 'hidden';

            // Show Nav
            const nav = document.getElementById('main-nav');
            if (nav) nav.classList.add('visible');

            // Initialize Scrolly Animations
            initScrollyAnimations();
        }, 600);
    }

    for (let i = 1; i <= frameCount; i++) {
        const img = new Image();
        img.src = framePath(i);
        img.onload = () => {
            loadedCount++;
            updateProgress(loadedCount / frameCount);
            if (loadedCount === frameCount) {
                onAllLoaded();
            }
        };
        img.onerror = () => {
            // Fallback: increment loaded count anyway to avoid hanging preloader
            console.warn(`Failed to load frame: ${framePath(i)}`);
            loadedCount++;
            updateProgress(loadedCount / frameCount);
            if (loadedCount === frameCount) {
                onAllLoaded();
            }
        };
        preloadedImages.push(img);
    }
})();

// ─── 5. Main Scrollytelling Setup ─────────────────────────────
let canvas, ctx;

function drawFrame(index) {
    if (!ctx || !preloadedImages[index]) return;
    drawImageProp(ctx, preloadedImages[index], 0, 0, canvas.width, canvas.height);
}

function initScrollyAnimations() {
    canvas = document.getElementById('scrolly-canvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    // Initial canvas resize
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        drawFrame(Math.round(scrollObj.frame));
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Initialize GSAP & ScrollTrigger
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
        console.warn("GSAP/ScrollTrigger not loaded. Scrollytelling disabled.");
        return;
    }
    gsap.registerPlugin(ScrollTrigger);

    const tl = gsap.timeline({
        scrollTrigger: {
            trigger: '#scrolly-container',
            start: 'top top',
            end: 'bottom bottom',
            scrub: 1.1, // Smooth scrub easing
            onUpdate: (self) => {
                updateNavbarLinks(self.progress);
            }
        }
    });

    // 1. Frame Scrubbing & Camera dolly/zoom
    tl.to(scrollObj, {
        frame: frameCount - 1,
        snap: 'frame',
        ease: 'none',
        onUpdate: () => {
            drawFrame(Math.round(scrollObj.frame));
        }
    }, 0);

    tl.fromTo('#scrolly-canvas', 
        { scale: 1 }, 
        { scale: 1.15, ease: 'none' }, 
        0
    );

    // Dynamic depth of field (blur), brightness, and moving ambient glow
    
    // Transition to Chapter 2 (Operational Crisis)
    tl.to(':root', {
        '--glow-color': 'rgba(239, 68, 68, 0.3)',
        '--glow-x': '30%',
        '--glow-y': '60%',
        '--canvas-blur': '2px',
        '--canvas-brightness': '0.55',
        duration: 0.05
    }, 0.12);

    // Transition to Chapter 3 (AI Pipeline Stage 01)
    tl.to(':root', {
        '--glow-color': 'rgba(245, 158, 11, 0.28)',
        '--glow-x': '75%',
        '--glow-y': '50%',
        '--canvas-blur': '4px',
        '--canvas-brightness': '0.45',
        duration: 0.05
    }, 0.28);

    // Transition to Chapter 4 (AI Pipeline Stage 02)
    tl.to(':root', {
        '--glow-color': 'rgba(6, 182, 212, 0.3)',
        '--glow-x': '25%',
        '--glow-y': '55%',
        '--canvas-blur': '4px',
        '--canvas-brightness': '0.45',
        duration: 0.05
    }, 0.48);

    // Transition to Chapter 5 (Real-Time Output)
    tl.to(':root', {
        '--glow-color': 'rgba(212, 160, 23, 0.3)',
        '--glow-x': '50%',
        '--glow-y': '50%',
        '--canvas-blur': '1px',
        '--canvas-brightness': '0.65',
        duration: 0.05
    }, 0.68);

    // Transition to Chapter 6 (Intelligent Routing)
    tl.to(':root', {
        '--glow-color': 'rgba(34, 197, 94, 0.28)',
        '--glow-x': '50%',
        '--glow-y': '70%',
        '--canvas-blur': '0px',
        '--canvas-brightness': '0.75',
        duration: 0.04
    }, 0.83);

    // Transition to Chapter 7 (Enterprise Control)
    tl.to(':root', {
        '--glow-color': 'rgba(139, 92, 246, 0.3)',
        '--glow-x': '50%',
        '--glow-y': '30%',
        '--canvas-blur': '2px',
        '--canvas-brightness': '0.55',
        duration: 0.04
    }, 0.93);

    // 2. Chapter Overlays Transitions
    // Chapter 1: starts visible (0), fades out at 0.12
    tl.to('#chapter-1', { opacity: 1, y: 0, duration: 0.01, display: 'flex' }, 0);
    tl.to('#chapter-1', { opacity: 0, y: -40, duration: 0.11, display: 'none' }, 0.12);

    // Chapter 2: fades in at 0.15, fades out at 0.28
    tl.fromTo('#chapter-2', { opacity: 0, y: 40, display: 'none' }, { opacity: 1, y: 0, duration: 0.05, display: 'flex' }, 0.15);
    // Animate stats cards progress bars when Chapter 2 is active
    tl.fromTo('#chapter-2 .stat-card:nth-child(1) .card-bar-fill', { width: '0%' }, { width: '75%', duration: 0.04 }, 0.17);
    tl.fromTo('#chapter-2 .stat-card:nth-child(2) .card-bar-fill', { width: '0%' }, { width: '24%', duration: 0.04 }, 0.18);
    tl.fromTo('#chapter-2 .stat-card:nth-child(3) .card-bar-fill', { width: '0%' }, { width: '15%', duration: 0.04 }, 0.19);
    tl.fromTo('#chapter-2 .stat-card:nth-child(4) .card-bar-fill', { width: '0%' }, { width: '80%', duration: 0.04 }, 0.20);
    tl.to('#chapter-2', { opacity: 0, y: -40, duration: 0.08, display: 'none' }, 0.28);

    // Chapter 3: fades in at 0.31, fades out at 0.48
    tl.fromTo('#chapter-3', { opacity: 0, y: 40, display: 'none' }, { opacity: 1, y: 0, duration: 0.05, display: 'flex' }, 0.31);
    tl.to('#chapter-3', { opacity: 0, y: -40, duration: 0.12, display: 'none' }, 0.48);

    // Chapter 4: fades in at 0.51, fades out at 0.68
    tl.fromTo('#chapter-4', { opacity: 0, y: 40, display: 'none' }, { opacity: 1, y: 0, duration: 0.05, display: 'flex' }, 0.51);
    // Animate TF-IDF feature weights when Chapter 4 is active
    tl.fromTo('#chapter-4 .vector-item:nth-child(1) .weight-bar', { width: '0%' }, { width: '84.2%', duration: 0.04 }, 0.53);
    tl.fromTo('#chapter-4 .vector-item:nth-child(2) .weight-bar', { width: '0%' }, { width: '91.2%', duration: 0.04 }, 0.54);
    tl.fromTo('#chapter-4 .vector-item:nth-child(3) .weight-bar', { width: '0%' }, { width: '79.5%', duration: 0.04 }, 0.55);
    tl.fromTo('#chapter-4 .vector-item:nth-child(4) .weight-bar', { width: '0%' }, { width: '88.0%', duration: 0.04 }, 0.56);
    tl.to('#chapter-4', { opacity: 0, y: -40, duration: 0.12, display: 'none' }, 0.68);

    // Chapter 5: fades in at 0.71, fades out at 0.83
    tl.fromTo('#chapter-5', { opacity: 0, y: 40, display: 'none' }, { opacity: 1, y: 0, duration: 0.05, display: 'flex' }, 0.71);
    // Animate Card confidence bars on arrival
    tl.fromTo('.metric-card:nth-child(1) .card-bar-fill', { width: '0%' }, { width: '72.2%', duration: 0.04 }, 0.73);
    tl.fromTo('.metric-card:nth-child(2) .card-bar-fill', { width: '0%' }, { width: '74.7%', duration: 0.04 }, 0.74);
    tl.fromTo('.metric-card:nth-child(3) .card-bar-fill', { width: '0%' }, { width: '100%', duration: 0.04 }, 0.75);
    tl.fromTo('.metric-card:nth-child(4) .card-bar-fill', { width: '0%' }, { width: '100%', duration: 0.04 }, 0.76);
    tl.to('#chapter-5', { opacity: 0, y: -40, duration: 0.07, display: 'none' }, 0.83);

    // Chapter 6: fades in at 0.86, fades out at 0.93
    tl.fromTo('#chapter-6', { opacity: 0, y: 40, display: 'none' }, { opacity: 1, y: 0, duration: 0.04, display: 'flex' }, 0.86);
    tl.to('#chapter-6', { opacity: 0, y: -40, duration: 0.03, display: 'none' }, 0.93);

    // Chapter 7: fades in at 0.95
    tl.fromTo('#chapter-7', { opacity: 0, y: 40, display: 'none' }, { opacity: 1, y: 0, duration: 0.05, display: 'flex' }, 0.95);
    
    // Animate operation counters progressively when Chapter 7 is active
    const statsObj = { accuracy: 0, latency: 200, automated: 0 };
    tl.to(statsObj, {
        accuracy: 98.7,
        latency: 48,
        automated: 100,
        duration: 0.04,
        onUpdate: () => {
            const accuracyEl = document.getElementById('counter-accuracy');
            const latencyEl = document.getElementById('counter-latency');
            const automatedEl = document.getElementById('counter-automated');
            if (accuracyEl) accuracyEl.textContent = `${statsObj.accuracy.toFixed(1)}%`;
            if (latencyEl) latencyEl.textContent = `<${Math.round(statsObj.latency)}ms`;
            if (automatedEl) automatedEl.textContent = `${Math.round(statsObj.automated)}%`;
        }
    }, 0.96);

    // ─── 6. Navbar Blur Transition ────────────────────────────
    ScrollTrigger.create({
        trigger: '#scrolly-container',
        start: 'top -50',
        onEnter: () => {
            document.getElementById('main-nav')?.classList.add('scrolled');
        },
        onLeaveBack: () => {
            document.getElementById('main-nav')?.classList.remove('scrolled');
        }
    });

    // ─── 7. Replay Button ─────────────────────────────────────
    const btnReplay = document.getElementById('btn-replay');
    if (btnReplay) {
        btnReplay.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ─── 8. 3D Card Tilt Effect ───────────────────────────────
    const cards = document.querySelectorAll('.glass-card, .routing-card, .tech-card');
    cards.forEach((card) => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;

            const rX = -(y - 0.5) * 12;
            const rY = (x - 0.5) * 12;

            card.style.transform = `perspective(800px) rotateX(${rX}deg) rotateY(${rY}deg) scale(1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)';
        });
    });

    // Run text preprocessing console morphing
    runPreprocessorConsole();

    // Setup active state ScrollTriggers for static sections
    setupStaticScrollTriggers();
}

// Preprocessor Console Data and Logic
const preprocessorData = [
  {
    raw: `"HEY support!! i cant log in to my billing portal, it keeps saying 'error 404' and my password won't work... please reset it ASAP!!!"`,
    clean: "log bill portal error password reset"
  },
  {
    raw: `"the network is down in the Boston office, we cannot connect to the servers! urgent help needed."`,
    clean: "network down boston office connect server"
  },
  {
    raw: `"i need a refund on my last credit card invoice, it charged me twice for the premium tier."`,
    clean: "refund credit card invoice charge twice premium"
  },
  {
    raw: `"My laptop screen is flickering and won't turn on. Need a hardware replacement."`,
    clean: "laptop screen flicker turn hardware replacement"
  }
];

function runPreprocessorConsole() {
    const rawEl = document.getElementById('morph-raw');
    const stateEl = document.getElementById('morph-state');
    const cleanEl = document.getElementById('morph-clean');
    if (!rawEl || !stateEl || !cleanEl) return;

    let index = 0;
    const scrambleChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*";

    function scrambleText(targetLength, callback) {
        let iterations = 0;
        const interval = setInterval(() => {
            let scrambled = "";
            for (let i = 0; i < targetLength; i++) {
                scrambled += scrambleChars[Math.floor(Math.random() * scrambleChars.length)];
            }
            cleanEl.textContent = scrambled;
            iterations++;
            if (iterations > 12) {
                clearInterval(interval);
                callback();
            }
        }, 60);
    }

    function cycle() {
        const item = preprocessorData[index];
        rawEl.textContent = item.raw;
        stateEl.textContent = "INGESTING...";
        stateEl.style.color = "var(--amber)";
        cleanEl.textContent = "...";
        cleanEl.style.color = "var(--text-tertiary)";

        setTimeout(() => {
            stateEl.textContent = "PREPROCESSING...";
            scrambleText(item.clean.length, () => {
                stateEl.textContent = "SUCCESS / ROUTED";
                stateEl.style.color = "var(--green)";
                cleanEl.textContent = item.clean;
                cleanEl.style.color = "var(--green)";

                setTimeout(() => {
                    index = (index + 1) % preprocessorData.length;
                    cycle();
                }, 3500);
            });
        }, 1500);
    }

    cycle();
}

function setupStaticScrollTriggers() {
    // ScrollTrigger to highlight Architecture nav link
    ScrollTrigger.create({
        trigger: '#architecture',
        start: 'top 40%',
        end: 'bottom 40%',
        onToggle: (self) => {
            if (self.isActive) {
                document.querySelectorAll('.nav-link').forEach((l) => l.classList.remove('active'));
                document.querySelector('.nav-link[data-chapter="architecture"]')?.classList.add('active');
            }
        }
    });

    ScrollTrigger.create({
        trigger: '#tech',
        start: 'top 40%',
        end: 'bottom 40%',
        onToggle: (self) => {
            if (self.isActive) {
                document.querySelectorAll('.nav-link').forEach((l) => l.classList.remove('active'));
                document.querySelector('.nav-link[data-chapter="architecture"]')?.classList.add('active');
            }
        }
    });
}

// ─── 9. Navbar Links Synchronizer ─────────────────────────────
function updateNavbarLinks(progress) {
    // Skip if static sections are active (we let their own scroll triggers handle it)
    if (progress >= 0.99) return;

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach((link) => link.classList.remove('active'));

    if (progress < 0.3) {
        document.querySelector('.nav-link[data-chapter="1"]')?.classList.add('active');
    } else if (progress >= 0.3 && progress < 0.75) {
        document.querySelector('.nav-link[data-chapter="3"]')?.classList.add('active');
    } else if (progress >= 0.75 && progress < 0.88) {
        document.querySelector('.nav-link[data-chapter="6"]')?.classList.add('active');
    } else if (progress >= 0.88) {
        document.querySelector('.nav-link[data-chapter="7"]')?.classList.add('active');
    }
}

// Nav link click smooth scroll to exact percentage heights
(function initNavSmoothScroll() {
    const links = document.querySelectorAll('.nav-link');
    links.forEach((link) => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetCh = link.dataset.chapter;

            if (targetCh === 'architecture') {
                const targetEl = document.getElementById('architecture');
                if (targetEl) targetEl.scrollIntoView({ behavior: 'smooth' });
                return;
            }

            const chapterProgressMap = {
                '1': 0.05,
                '3': 0.40,
                '6': 0.90,
                '7': 0.97
            };

            const progress = chapterProgressMap[targetCh] || 0;
            const container = document.getElementById('scrolly-container');
            if (container) {
                const start = container.offsetTop;
                const totalScroll = container.offsetHeight - window.innerHeight;
                const scrollTo = start + (totalScroll * progress);
                window.scrollTo({ top: scrollTo, behavior: 'smooth' });
            }
        });
    });
})();
