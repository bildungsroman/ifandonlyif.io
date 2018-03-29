$(document).ready(function() {
  smoothScroll();
  // initialize Materialize components
  $('.modal').modal();
  $(".dropdown-button").dropdown();
  $('ul.tabs').tabs();
  $(".button-collapse").sideNav();
});
$(function () {
  $(document).scroll(function () {
    let $nav = $("#navbar-custom");
    $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
  });
});

// close message toast
$(".close-toast").click(function(e) {
  e.preventDefault();
  $("#message-container").fadeOut();
});
let toast = document.querySelector('#message-container');
toast.addEventListener('webkitAnimationEnd', function(event) { toast.style.display = 'none'; }, false);

// sign-in
let $input = $('.form-fieldset > input');

$input.blur(function (e) {
  $(this).toggleClass('filled', !!$(this).val());
});

// navbar
$(window).scroll(function() {
  if ($(".navbar").offset().top > 50) {
    $('#custom-nav').addClass('affix');
    $(".navbar-fixed-top").addClass("top-nav-collapse");
  } else {
    $('#custom-nav').removeClass('affix');
    $(".navbar-fixed-top").removeClass("top-nav-collapse");
  }
});

// Smooth the scroll action
function smoothScroll() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 500);
        return false;
      }
    }
  });
}



/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');
