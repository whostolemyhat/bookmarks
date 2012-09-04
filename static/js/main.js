$(document).ready(function() {
    // Add
    $('.add-bookmark').hide();
    $('#add-new').click(function() {
        $('.add-bookmark').slideToggle();
    });

    // $('.add-bookmark').submit(function(event) {
    //     event.preventDefault();


    //     var form = $(this);
    //     console.log(form.serialize());

    //     var url = form.attr('action');

    //     $.post('/add', form.serialize(), function(data) {
    //         $('.entries').load(data);
    //     });
    // });

    // Delete
    // $('.delete-bookmark').click(function() {
    //     $('<div id="popup" />').appendTo('body');
    //     $('#popup').load($(this).attr('href'));
    //     return false;
    // });

    // Order
    $('#a-z').click(function() {
        $('.entries').load('/az');
        return false;
    });

    $('#newest').click(function() {
        $('.entries').load('/newest');
        return false;
    });


});
