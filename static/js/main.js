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
});
