jQuery(function ($) {
    $.fn.hScroll = function (amount) {
        amount = amount || 120;
        $(this).bind("DOMMouseScroll mousewheel", function (event) {
            var oEvent = event.originalEvent, 
                direction = oEvent.detail ? oEvent.detail * -amount : oEvent.wheelDelta, 
                position = $(this).scrollLeft();
            position += direction > 0 ? -amount : amount;
            $(this).scrollLeft(position);
            bids_slider_pos = $(this).scrollLeft();
            event.preventDefault();
        })
    };
});

$(document).ready(function (){
    $('.viewport').hScroll(60);
    $('table').hScroll(60);
});