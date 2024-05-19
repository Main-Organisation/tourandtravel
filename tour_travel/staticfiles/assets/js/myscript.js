// Owlcarousel
$('.banner-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:false,
    dots:false,
    autoplay:true,
    autoplayTimeout: 5000, // Change slide interval (milliseconds)
    animateOut: 'fadeOut', // Change the animation effect
    nav: true, // Show navigation buttons
    navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"], // Custom navigation icons,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        }
    }
});

// Owlcarousel detination
$('.tour-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:false,
    dots:false,
    autoplay:true,
    autoplayTimeout: 5000, // Change slide interval (milliseconds)
    animateOut: 'fadeOut', // Change the animation effect
    nav: true, // Show navigation buttons
    navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"], // Custom navigation icons,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:4
        }
    }
});
// Owlcarousel offer
$('.offer-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:false,
    dots:false,
    autoplay:true,
    autoplayTimeout: 4000, // Change slide interval (milliseconds)
    animateOut: 'fadeOut', // Change the animation effect
    nav: true, // Show navigation buttons
    navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"], // Custom navigation icons,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:2
        }
    }
});
// Owlcarousel Properties
$('.properties-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:false,
    dots:false,
    autoplay:true,
    autoplayTimeout: 4000, // Change slide interval (milliseconds)
    animateOut: 'fadeOut', // Change the animation effect
    nav: true, // Show navigation buttons
    navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"], // Custom navigation icons,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:4
        }
    }
});
// Owlcarousel trip
$('.trip-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:false,
    dots:false,
    autoplay:false,
    autoplayTimeout: 4000, // Change slide interval (milliseconds)
    animateOut: 'fadeOut', // Change the animation effect
    nav: true, // Show navigation buttons
    navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"], // Custom navigation icons,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:5
        }
    }
});
// tabs banner
$(".hover").mouseleave(
    function () {
      $(this).removeClass("hover");
    }
  );