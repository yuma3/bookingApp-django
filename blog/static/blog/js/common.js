'use strict';

$(function () {

    // menu-btn
    $("#toggle").click(function () {
        $(this).toggleClass("activate");
        if ($(this).hasClass("activate")) {
            $(".nav-main").fadeIn(200);
            $("#search").css('display', 'none');
        } else {
            $(".nav-main").fadeOut(200);
            $("#search").css('display', 'block');
        }
        return false;
    })

    // search-btn
    $("#search").click(function () {
        $(this).toggleClass("activate");
        if ($(this).hasClass("activate")) {
            $("#toggle").css('display', 'none');
            $("#cancel").css('display', 'inline-block');
            $(this).css('display', 'none');
            $(".search-main").fadeIn(200);
        }
        // else {
        //     $(".search-main").fadeOut(200);
        //     $("#toggle").css('display', 'block');
        // }
        return false;
    })
    $("#cancel").click(function () {
        $(".search-main").fadeOut(200);
        $("#toggle").css('display', 'block');
        $("#cancel").css('display', 'none');
        $("#search").css('display', 'inline-block');
        return false;
    })


    // page top

    $('.totop').hide();
    $(window).scroll(function () {
        if ($(this).scrollTop() > 600) {
            $('.totop').fadeIn();
        } else {
            $('.totop').fadeOut();
        }
    });

    $('.totop').click(function () {
        $('html, body').animate({
            'scrollTop': 0
        }, 1200, 'easeInOutExpo')
    })

})
