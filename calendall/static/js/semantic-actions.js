$(document).ready(function () {
    // Load forms
    $('.ui.form');

    // message quit buttons
    $('.message .close').on('click', function() {
        $(this).closest('.message').fadeOut();
    });

    // Dropdown
    $('.ui.dropdown')
        .dropdown();
});