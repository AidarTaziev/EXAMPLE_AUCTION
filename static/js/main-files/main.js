var neededBid = 'all';
var getRequestsList_xhr = null;
// $(document).ready(() => {
//     let some_cookie_arr = document.cookie.split('; ');
//     let count = 0;
//     for(var i = 0; i < some_cookie_arr.length; i++){
//       if (some_cookie_arr[i].indexOf('csrftoken') == 0) {
//         count++;
//       } 
//       // document.cookie = "csrftoken=qwe; path=/; max-age=0;";
//     }
//     if (count > 1) {
//       for(var i = 0; i < count; i++){
//         document.cookie = "csrftoken=qwe; path=/; max-age=0;";
//         document.location.reload(true);
//       }
//     }
// });

$('.cookies-closer').click(function (){
  $('.cookies-wrap').fadeOut('slow');
  document.cookie = 'cookie=visited; Domain=.kartli.ch';
});

$('.lock').click(function(){
  // скрывает и показывает содержимое полей паролей
  if ($(this).siblings('.locking-input').attr('type') == 'password') {
    $(this).siblings('.locking-input').attr('type', 'text');
  } else {
    $(this).siblings('.locking-input').attr('type', 'password');
  }
  $(this).siblings('.unlock-img').removeClass('unlock-img');
  $(this).addClass('unlock-img');
});

$('.disable-EXAMPLE_AUCTION').click(() => {
  let data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    auction_id: $('h2').attr('id')
  };
  disableBidSession(data, '/EXAMPLE_AUCTION/cancel');
});

$('.disable-tender').click(() => {
  let data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    tender_id: $('h2').attr('id')
  };
  disableBidSession(data, '/tender/cancel');
});

$('.link-for-tender').click(function (){
  let identificator = $('h2').attr('id');
  window.open('../session/'+identificator+'','', 'scrollbars=1,width=1000,height=600');
});

$('#want_to_play_btn').click(function (){
  let id = $('h2').attr('id');
  let path = $('h2').attr('data-path');
  let data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    auction_id: id
  };
  if ($('h2').attr('data-type') == 'tender') {
    delete data.auction_id;
    data.tender_id = id;
  }
  sendRequestForPlaying(data, path, true);
});
