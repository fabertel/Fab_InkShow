
/**
 * =======================================
 * FAB INKSHOW - SCRIPT.JS
 * =======================================
 * This script handles dynamic content loading, gallery rendering, 
 * and modal interactions for the Fab Inkshow website.
 * 
 * FUNCTIONS:
 * ---------------------------------------
 * 1️⃣ loadHeader()      -> Loads the header dynamically from `/static/header.html`.
 * 2️⃣ loadFooter()      -> Loads the footer dynamically from `/static/footer.html`.
 * 3️⃣ loadGallery()     -> Fetches artwork data from `/static/data.json` and generates thumbnails.
 * 4️⃣ setupModal()      -> Sets up event listeners for the image modal (open, close, and navigation).
 * 5️⃣ showModal(index)  -> Displays artwork details in a modal when a thumbnail is clicked.
 * 6️⃣ [EVENT] Keydown   -> Listens for 'Escape' (close modal), 'ArrowLeft' (prev), and 'ArrowRight' (next).
 * 7️⃣ DOMContentLoaded  -> Ensures scripts run only after the page has fully loaded.
 * 
 * =======================================
 * AUTHOR: Fab Inkshow 
 * VERSION: 1.0.0
 * LAST UPDATED: 250209
 * =======================================
 */


let currentIndex = 0;
let artworks = [];



// 🟢 Load Header
async function loadHeader() {
    const response = await fetch('/static/header.html');
    const headerHTML = await response.text();
    document.getElementById('header-container').innerHTML = headerHTML;

    // Ensure theme switcher initializes after header loads
    setTimeout(() => {
        if (typeof initializeStyleSwitcher === "function") {
            initializeStyleSwitcher();
        }
    }, 100);
}

// 🟢 Load Footer
async function loadFooter() {
    const response = await fetch('/static/footer.html');
    const footerHTML = await response.text();
    document.getElementById('footer-container').innerHTML = footerHTML;
}

// 🟢 Load Gallery
async function loadGallery() {
    const galleryId = window.location.pathname.split('/').pop();
    const response = await fetch(`/static/data_${galleryId}.json`);
    artworks = await response.json();
    const gallery = document.querySelector('.gallery');

    artworks.forEach((art, index) => {
        const baseName = art.filename || art.src.split('/').pop();
        const thumbnailPath = '/static/images/thumbnails/' + baseName.replace(/(\.[a-zA-Z0-9]+)$/, '_TH$1');
        const imgElement = document.createElement('img');
        imgElement.src = thumbnailPath;
        imgElement.alt = art.title;
        imgElement.dataset.index = index;
        gallery.appendChild(imgElement);
    });

    const metaResponse = await fetch('/static/galleries_meta.json');
    const metaData = await metaResponse.json();

    const meta = metaData[galleryId] || { title: "", text: "" };
    document.getElementById('gallery-title').textContent = meta.title;
    document.getElementById('gallery-text').textContent = meta.text;


    setupModal();
}


// 🟢 Setup Modal
function setupModal() {
    const modal = document.querySelector('.modal');
    const modalClose = document.querySelector('.modal-close');

    document.querySelector('.gallery').addEventListener('click', (e) => {
        if (e.target.tagName === 'IMG') {
            currentIndex = parseInt(e.target.dataset.index, 10);
            showModal(currentIndex);
        }
    });

    if (modalClose) {
        modalClose.addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            modal.classList.remove('active');
        } else if (e.key === 'ArrowLeft') {
            currentIndex = (currentIndex > 0) ? currentIndex - 1 : artworks.length - 1;
            showModal(currentIndex);
        } else if (e.key === 'ArrowRight') {
            currentIndex = (currentIndex < artworks.length - 1) ? currentIndex + 1 : 0;
            showModal(currentIndex);
        }
    });
}

// 🟢 Show Modal with Artwork Details
function showModal(index) {
    const art = artworks[index];
    const fullImagePath = '/static/' + art.src;


    const modal = document.querySelector('.modal');

    if (!modal) return; // Ensure modal exists

    const modalImage = document.getElementById('modal-image');
    modalImage.src = fullImagePath;
    document.getElementById('modal-title').textContent = art.title;
    document.getElementById('modal-description').textContent = art.description;
    document.getElementById('modal-size').innerHTML = `<strong>Size:</strong> ${art.size}`;
    document.getElementById('modal-price').innerHTML = `<strong>Price:</strong> ${art.price}`;
    document.getElementById('modal-availability').innerHTML = `<strong>Availability:</strong> ${art.availability}`;
    document.getElementById('modal-category').innerHTML = `<strong>Category:</strong> ${art.category}`;
    document.getElementById('modal-medium').innerHTML = `<strong>Medium:</strong> ${art.medium}`;
    document.getElementById('modal-tags').innerHTML = `<strong>Tags:</strong> ${art.tags}`;
    document.getElementById('modal-date').innerHTML = `<strong>Date:</strong> ${art.created_date}`;

    modal.classList.add('active');

    // ✅ Add Click Event for Fullscreen
    modalImage.addEventListener('click', () => enableFullscreen(modalImage));
}



// 🟢 Initialize everything
document.addEventListener("DOMContentLoaded", () => {
    loadHeader();
    loadFooter();

    // Determina se siamo su una pagina con titolo e testo dinamici
    const titleEl = document.getElementById("gallery-title");
    const textEl = document.getElementById("gallery-text");

    if (titleEl && textEl) {
        // Estrae "video" o altro ID dalla path
        let galleryId = window.location.pathname.split('/').pop();
        if (galleryId === "videos.html" || galleryId === "videos") galleryId = "video";

        fetch('/static/galleries_meta.json')
            .then(res => res.json())
            .then(meta => {
                const data = meta[galleryId];
                if (data) {
                    titleEl.textContent = data.title;
                    textEl.textContent = data.text;
                }
            });
    }

    if (document.querySelector('.gallery')) {
        loadGallery(); // solo nelle pagine con galleria immagini
    }
});


// 🟢 Enable Fullscreen on Image Click
function enableFullscreen(imageElement) {
    if (!document.fullscreenElement) {
        if (imageElement.requestFullscreen) {
            imageElement.requestFullscreen();
        } else if (imageElement.mozRequestFullScreen) { // Firefox
            imageElement.mozRequestFullScreen();
        } else if (imageElement.webkitRequestFullscreen) { // Chrome, Safari, Opera
            imageElement.webkitRequestFullscreen();
        } else if (imageElement.msRequestFullscreen) { // IE/Edge
            imageElement.msRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { // Firefox
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { // Chrome, Safari, Opera
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { // IE/Edge
            document.msExitFullscreen();
        }
    }
}

