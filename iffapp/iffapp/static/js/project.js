$(document).ready(function() {
  smoothScroll();
  // initialize Materialize components
  Materialize.updateTextFields();
  $('select').material_select();
  $('.modal').modal();
  $(".button-collapse").sideNav();
  $('.collapsible').collapsible();
});

// for some reason, this is required to make the modals work (though it shouldn't be)
let $reg = $('#register');
let $log = $('#login');

$('.register-trigger').click(function () {
  $('#register-modal').modal().modal('open');
  $('#register-tab').addClass('active-tab');
  $('#login-tab').removeClass('active-tab');
  $reg.removeClass('hidden');
  $log.addClass('hidden');
});
$('.login-trigger').click(function () {
  $('#register-modal').modal().modal('open');
  $('#login-tab').addClass('active-tab');
  $('#register-tab').removeClass('active-tab');
  $log.removeClass('hidden');
  $reg.addClass('hidden');
});
// to switch the modal between sign up and login
$(".register-bt").click(function() {
    $reg.removeClass('hidden');
    $log.addClass('hidden');
    $('#register-tab').addClass('active-tab');
    $('#login-tab').removeClass('active-tab');
});
$(".login-bt").click(function() {
    $reg.addClass('hidden');
    $log.removeClass('hidden');
    $('#register-tab').removeClass('active-tab');
    $('#login-tab').addClass('active-tab');
});
$('.about-trigger').click(function () {
  $('#about-modal').modal().modal('open');
});
$('.signout-trigger').click(function () {
  $('#signout-modal').modal().modal('open');
  document.body.classList.toggle('sidenav-active');
  document.body.classList.toggle('noscroll');
});

// open mobile menu
$('.js-toggle-menu').click(function(e){
  e.preventDefault();
  $('.mobile-header-nav').slideToggle();
  $(this).toggleClass('open');
});


// user sidebar
let main_div = document.querySelector('.cover');
function toggleSidenav(bool) {
  document.body.classList.toggle('sidenav-active');
  document.body.classList.toggle('noscroll');
  main_div.classList.toggle('z-depth-3');
}

// pretty navbar background on scroll
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

// for matching passwords
let register_bt = document.querySelector('#register_bt');
let id_password1 = document.querySelector('#id_password1');
let id_password2 = document.querySelector('#id_password2');
register_bt.onclick = function() {
  if (id_password1.value !== id_password2.value) {
    alert("Your passwords don't match!");
    console.log("Your passwords don't match!");
    return false; // cancels form submission! This or prevent default needed
  }
};

// $('.form-group').removeClass('row');
