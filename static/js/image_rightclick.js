document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.blockspace .block .img').forEach(function(image) {
        image.addEventListener('contextmenu', function(event) {
            event.preventDefault();
            alert('Plné rozlíšenie fotografíi nájdete po rozkliknutí alebo vo fotogalérii.');
        });
    });
});

function submitForm(id) {
    document.getElementById('postForm_' + id).submit();
}