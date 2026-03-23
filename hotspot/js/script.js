
const hotspotId = 1;
//const baseUrl = 'http://localhost:5000';
const baseUrl = 'https://matrix-hotspot.vercel.app'

/**
 * Portal state — populated after API fetch
 */
var portalData = {};
var isSubscribed = false;
var player;
var slideCounter = 1;
var slideInterval;

function fetchPortalData() {
    $.getJSON(baseUrl + '/api/portal-data/' + hotspotId)
        .done(function (data) {
            portalData = data;
            renderPortal(data);
        })
        .fail(function (xhr) {
            $('#notice').html('Failed to load portal. Please refresh.');
            console.error('Portal data fetch failed', xhr);
        });
}

/**
 * 2. Render everything once data arrives
 */
function renderPortal(d) {
    var client = d.client;
    var hotspot = d.hotspot;
    var video = d.video;
    var images = d.images;

    //Title
    $('#title').html(client.name + ' FREE WiFi');

    // Header
    $('#header').css('background-color', client.background_color);
    $('#header-title')
        .text(client.name + ' FREE Wi-Fi')
        .css({ 'background-color': client.background_color, 'color': client.foreground_color });

    // Favicon
    $('link[rel="icon"]').attr('href', 'images/logo.PNG');

    // Page title
    document.title = client.name + ' FREE Wi-Fi';

    // Tagline
    $('#tagline').html(
        'Enter Your Valid Phone Number Below and Enjoy Super Fast Free WIFI' +
        '<br/> Powered by ' + client.name
    );

    // Slides
    renderSlides(images);

    // Restore saved phone
    var saved = localStorage.getItem('userPhone');
    if (saved) $('#adphone').val(saved);
    $('#adphone').focus();

    // Video iframe
    var src = 'https://www.youtube.com/embed/' + video.source_id +
        '?playlist=' + video.source_id +
        '&loop=1&enablejsapi=1&rel=0&modestbranding=1' +
        '&showinfo=0&controls=0&disablekb=1&autoplay=1&mute=0';
    $('#advideo').attr('src', src);
}

/**
 * 3. Build image slider dynamically
 */
function renderSlides(images) {
    var $slider = $('.slider').empty(); // clear everything inside .slider

    // 1. Inject radio inputs directly into .slider first
    images.forEach(function (img, i) {
        var idx = i + 1;
        $slider.append(
            $('<input>', { type: 'radio', name: 'radio-btn', id: 'radio' + idx })
        );
    });

    // 2. Build .slides div with slide children
    var $slidesDiv = $('<div>').addClass('slides');
    images.forEach(function (img, i) {
        var $slide = $('<div>').addClass('slide' + (i === 0 ? ' first' : ''));
        var $img = $('<img>').attr({
            src: 'https://i.postimg.cc/' + img.source_id,
            alt: '',
            height: '320'
        });
        $slidesDiv.append($slide.append($img));
    });
    $slider.append($slidesDiv);

    // 3. Build navigation-auto div
    var $nav = $('<div>').addClass('navigation-auto');
    images.forEach(function (img, i) {
        $nav.append($('<div>').addClass('auto-btn' + (i + 1)));
    });
    $slider.append($nav);

    // 4. Check first radio
    document.getElementById('radio1').checked = true;

    // 5. Auto-slide loop
    clearInterval(slideInterval);
    var total = images.length;
    slideCounter = 1;
    slideInterval = setInterval(function () {
        var radio = document.getElementById('radio' + slideCounter);
        if (radio) radio.checked = true;
        slideCounter = (slideCounter % total) + 1;
    }, 3000);
}

/**
 * 4. YouTube Player API
 */
function onYouTubeIframeAPIReady() {
    player = new YT.Player('advideo', {
        events: { onReady: onPlayerReady }
    });
}

function onPlayerReady(event) {
    document.onclick = function () {
        if (player.isMuted()) player.unMute();
        setTimeout(function () {
            var btn = document.getElementById('adconnectbutton');
            if (btn) {
                btn.innerHTML = 'Connect';
                btn.disabled = false;
                connect();
            }
        }, 30000);
    };
}

/**
 * 5. Subscribe — POST phone number
 */
function subscribe() {
    var phone = $('#adphone').val().trim();
    if (phone.length === 10) {
        $('#notice').html('');
        $.post(baseUrl + '/api/subscribe', {
            phone: '254' + phone.slice(-9),
            hotspot_id: portalData.hotspot ? portalData.hotspot.id : ''
        }, function () {
            localStorage.setItem('userPhone', phone);
            isSubscribed = true;
        });
    } else {
        $('#notice').html('Enter Valid Phone Number');
    }
}

/**
 * 6. Connect — POST login credentials to hotspot
 */
function connect() {
    if (isSubscribed) {
        $('input[name="username"]').val(portalData.hotspot.hotspot_username);
        $('input[name="password"]').val(portalData.hotspot.hotspot_password);
        $('#sendin').submit();
    } else {
        subscribe();
        connect();
    }
    return false;
}

// Subscribe on each keyup
$('#adphone').on('keyup', function () { subscribe(); });

// Bootstrap
$(document).ready(function () { fetchPortalData(); });