$(document).ready(function() {
    $('.add-bookmark').hide();
    $('#add-new').click(function() {
        $('.add-bookmark').slideToggle();
    });

    $('.delete-bookmark').click(function() {
        $('<div id="popup" />').appendTo('body');
        $('#popup').load($(this).attr('href'));
        return false;
    });

    $('#a-z').click(function() {
        $('.entries').load('/az');
        return false;
    });

    $('#newest').click(function() {
        $('.entries').load('/newest');
        return false;
    });
});
