$(function() {

    // ========================================================================= //
    //    Add remove class active has menu
    // ========================================================================= //

    jQuery(".has-submenu").click(function() {
        jQuery(".has-submenu").removeClass("active");
        $(this).toggleClass("active");
    });

    // ========================================================================= //
    //    Toggle Aside Menu
    // ========================================================================= //

    jQuery(".hamburger").click(function() {
        jQuery("aside.left-panel").toggleClass("collapsed");
        jQuery("body").toggleClass("sidebar-toggled");
        jQuery("#main-wrapper").toggleClass("menu-toggle");
    });

    // ========================================================================= //
    //    Set attibute isnide body
    // ========================================================================= //

    jQuery('body').attr({
        'data-typography': "rubik",
        'data-sidebar-style': "full",
        'data-sidebar-position': "fixed",
        'data-header-position': "fixed",
    })

    // ========================================================================= //
    //    resize 
    // ========================================================================= //

    function resize() {
        if (window.matchMedia("(max-width: 767px)").matches) {
            $('body').attr('data-sidebar-style', 'overlay');
            $("#main-wrapper").addClass('overlay');

        } else if (window.matchMedia("(max-width: 1199px)").matches) {

            $('body').attr('data-sidebar-style', 'mini');
            $("#main-wrapper").addClass('mini');


        } else {
            $('body').attr('data-sidebar-style', 'full');
            $("#main-wrapper").removeClass('mini');
        }
    }

    resize();

    jQuery(window).resize(function() {
        resize();
    })

});

// ========================================================================= //
//    upload image in drag
// ========================================================================= //

function showPreview(event) {
    if (event.target.files.length > 0) {
        var src = URL.createObjectURL(event.target.files[0]);
        var preview = document.getElementById("file-ip-1-preview");
        preview.src = src;
        preview.style.display = "block";
    }
}

// ========================================================================= //
//   Preview Pictures
// ========================================================================= //

$(".widget-3 input[type='file']").on("change", function() {
    $(".widget-3").addClass("custom-text");
});

// ========================================================================= //
//   Date Range
// ========================================================================= //


$('input[name="daterange"]').daterangepicker({
    opens: 'right'
}, function(start, end, label) {
    console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
});


// ========================================================================= //
//   Button Add Drugs
// ========================================================================= //


// ========================================================================= //
//  Change dates patient
// ========================================================================= //

$(function() {
    $('input[name="dates"]').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        minYear: 1901,
        maxYear: parseInt(moment().format('YYYY'), 10)
    }, function(start, end, label) {
        var years = moment().diff(start, 'years');
    });
});



// ========================================================================= //
//   refrech select picker inside modal
// ========================================================================= //
$('.selectRefresh').on('shown', function() {
    $('.selectpicker').selectpicker('refresh');
});


// ========================================================================= //
//   Responsive
// ========================================================================= //


function resize() {
    if (window.matchMedia("(max-width: 1199px)").matches) {
        $(".has-submenu").removeClass('active');
    }
}

resize();

jQuery(window).resize(function() {
    resize();
})


jQuery(function($) {
    var path = window.location.href;
    $('ul li a').each(function() {
        if (window.matchMedia("(max-width: 1199px) and (max-width: 1199px)").matches) {
            if (this.href === path) {
                if ($(this).parent().hasClass("has-submenu")) {
                    $(this).parent().addClass("active-submenu");
                } else {
                    $(this).parent().parent().parent().addClass('active-submenu');
                }
            }
        }
        
    });
});