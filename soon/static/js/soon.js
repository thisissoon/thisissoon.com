jQuery(document).ready(function ($) {

    //initialise Stellar.js
    $(window).stellar();

    //Cache variables for Stellar.js in the document
    var links = $('.nav').find('li');
    slide = $('.slide');
    button = $('.button');
    mywindow = $(window);
    htmlbody = $('html,body');

    function goToByScroll(dataslide) {
        console.log(dataslide)
        htmlbody.animate({
            scrollTop: $('#slide' + dataslide).offset().top - 80
        }, 1000, 'easeInOutQuint');
    }

    //When the user clicks on the navigation links, get the data-slide attribute value of the link and pass that variable to the goToByScroll function
    links.click(function (e) {
        e.preventDefault();
        dataslide = $(this).attr('data-slide');
        goToByScroll(dataslide);
    });

    //When the user clicks on the button, get the get the data-slide attribute value of the button and pass that variable to the goToByScroll function
    button.click(function (e) {
        e.preventDefault();
        dataslide = $(this).attr('data-slide');
        goToByScroll(dataslide);
    });

    //Mouse-wheel scroll easing

    var time = 350;
    var distance = 400;
    function wheel(event) {
        if (event.wheelDelta) delta = event.wheelDelta / 50;
        else if (event.detail) delta = -event.detail / 1;
        handle();
        if (event.preventDefault) event.preventDefault();
        event.returnValue = false;
    }

    function handle() {

        $('html, body').stop().animate({
            scrollTop: $(window).scrollTop() - (distance * delta)
        }, time);
    }

    //keyboard  scroll easing
    $(document).keydown(function (e) {
        switch (e.which) {
            //up
        case 38:
            $('html, body').stop().animate({
                scrollTop: $(window).scrollTop() - distance
            }, time);
            break;
            //down
        case 40:
            $('html, body').stop().animate({
                scrollTop: $(window).scrollTop() + distance
            }, time);
            break;
        }
    });

});
