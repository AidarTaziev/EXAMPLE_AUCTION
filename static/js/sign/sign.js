//Размеры окна авторизации и регистрации
var savedHeightUp = 550;
var savedHeightIn = 300;

//Переключатели окна авторизации и регистрации
$('#up').click(function (){
   if ($(this).attr('class') == 'form-setter hidden') {
     $('.sign-header h2').toggleClass('hidden');
     $('.sign-up').removeClass('hidden-form-up').removeAttr('style');
     $('.sign-in').addClass('hidden-form-in');
     savedHeightIn = $('.sign-wrap').height();
     $('.sign-wrap').css('height', savedHeightUp + 'px');
     setTimeout(function () {
       $('.sign-in').attr('style', 'display:none;');
     }, 50);
   }
});

$('#in').click(function (){
   if ($(this).attr('class') == 'form-setter hidden') {
     $('.sign-header h2').toggleClass('hidden');
     $('.sign-up').addClass('hidden-form-up');
     $('.sign-in').removeClass('hidden-form-in').removeAttr('style');
     savedHeightUp = $('.sign-wrap').height();
     $('.sign-wrap').css('height', savedHeightIn + 'px');
     setTimeout(function () {
       $('.sign-up').attr('style', 'display:none;');
     }, 50);
   }
});

$('.sign-in').submit(function (e){
  let data = $(this).serialize();
  userAction(data, true);
  e.preventDefault();
});

$('.sign-up').submit(function (e){
  let data = $(this).serialize();
  userAction(data, false);
  e.preventDefault();
});
