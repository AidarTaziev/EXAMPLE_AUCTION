let checkers_arr = $('.first_checker');
let types = [];
let values = [];

$(document).ready(() => {
  for (var i = 0; i < checkers_arr.length; i++) {
    if (isChecked($(checkers_arr[i]))) $('#more_notifications_btn').show();
  }
});

$('.toggle-btn').click(function (){
  let id = $(this).parent().attr('data-idx');
  if ($(this).text() == '+')
    $(this).text('-');
  else
    $(this).text('+');
  $('.hidden-list[data-idx="'+id+'"]').toggleClass('active');
});

$('h2 .close').click(function (){
  history.go(-1);
});

$('#more_notifications_btn').click(function (){
  $('.pop-up-notifications-wrap').show();
});

$('#notifications_closer').click(function (){
  $('.pop-up-notifications-wrap').hide();
});

$('.main_check').click(function() {
  let id = $(this).parent().attr('data-idx');
  if (isChecked($(this))) {
    let checkers = $('.hidden-list[data-idx="'+id+'"]').children('.row').children('input');
    for (var i = 0; i < checkers.length; i++) {
      $(checkers[i]).prop('checked', true);
      types.push({
        id: $(checkers[i]).attr('data-id'),
        value: true
      });
    }
  } else {
    let checkers = $('.hidden-list[data-idx="'+id+'"]').children('.row').children('input');
    for (var i = 0; i < checkers.length; i++) {
      $(checkers[i]).prop('checked', false);
      if (!types.includes({ id: $(checkers[i]).attr('data-id'), value: true })) {
        types.push({
          id: $(checkers[i]).attr('data-id'),
          value: false
        });
      } else
        types = deleteFromArr($(checkers[i]).attr('data-id'), types);
    }
  }
  console.log(types);
});

$('.polymer_mark').click(function (){
  let id = $(this).parent().parent().attr('data-idx');
  if (isChecked($(this))) {
    types.push({
      id: $(this).attr('data-id'),
      value: true
    });
  } else {
    if (!types.includes({ id: $(this).attr('data-id'), value: true })) {
      types.push({
        id: $(this).attr('data-id'),
        value: false
      });        
    } else {
      types = deleteFromArr($(this).attr('data-id'), types);
    }
  }
  checkForEmptyBox($('div[data-idx="'+id+'"]').children('input'), id);
  console.log(types);
});

$('#accept_more_notifications').click(function (e){
  e.preventDefault();
  console.log(types);
  let data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    polymers: JSON.stringify(types)
  };
  let user_params_data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    creating_auction_notification: isChecked($('input[name="creating_auction_notification"]')),
    starting_auction_notification: isChecked($('input[name="starting_auction_notification"]')),
    cancel_auction_notification: isChecked($('input[name="cancel_auction_notification"]'))
  }
  changeUserParameters(user_params_data, true, false);
  sendForMoreOptions(data);
});

$('.first_checker').click(function (){
  checkers_arr = $('.first_checker');
  let k = 0;
  for (var i = 0; i < checkers_arr.length; i++) {
    if (isChecked($(checkers_arr[i]))) k++;
  }
  if (k > 0) $('#more_notifications_btn').show();
  else $('#more_notifications_btn').hide();
});
