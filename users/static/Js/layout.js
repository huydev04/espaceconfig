document.querySelector('.list-video').addEventListener('wheel', (evt) => {
    evt.preventDefault();
    document.querySelector('.list-video').scrollBy({
        left: evt.deltaY < 0 ? -40 : 40, // Adjust the scrolling speed
        behavior: 'smooth'
    });
});


