'use strict';

$(function () {

    let loadingImg = $('.loading');
    let loadingBack = $('.loading-back');
    let header = $('#header');
    let main = $('#main');
    let footer = $('#footer');

    // load window
    $(window).on('load', function () {
        loadingImg.fadeOut(1100)
        loadingBack.fadeOut(1100);

        setTimeout(function () {
            header.addClass('fadein');
        }, 800);
        setTimeout(function () {
            main.addClass('fadein');
        }, 1300);
        setTimeout(function () {
                footer.addClass('fadein');
            }, 1400);
    })

    // $(window).scroll(function () {
    //     if ($(this).scrollTop() > footer.offset().top - 300) {
    //         footer.addClass('fadein');
    //     };
    // });

    // loadingImg.fadeOut(2000, contFadeIn);
    // loadingBack.fadeOut(2000, contFadeIn);

    // function contFadeIn() {
    //     $('#contents').addClass('fadein')
    // }


})
