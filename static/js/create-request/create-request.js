var white_list = [{
  company_id: 0,
  inn: 0,
  name: 'Неизвестно',
  is_checked: false
}];
var allowed_companys = [];
var is_rename = false;
var basis_list = [];
$(document).ready(() => {
  $('.bonus-fields-wrap').css('display', 'flex').hide();
});
//Очистить форму
$('.clear').click(function() {
  let label = $(this).parent().parent().children('label');
  for (var i = 0; i < label.length; i++) {
    if (label.eq(i).children('select').val() == undefined) {
      label.eq(i).children('input').val('').blur();
    }
    else {
      label.eq(i).children('select').val('default');
      label.eq(i).children('select').removeAttr('style');
    }
  }
});

$('.request-wrap input[type="number"]').attr('min', 1);
$('.request-wrap input[name="lot_size"]').attr('min', 0.1);
$('.request-wrap input[name="fixation_duration"]').attr('min', 0);

// $('input[name="t_startAuction"]').change(function (){
//   $('input[name="t_endAuction"]').attr('min', $('input[name="t_startAuction"]').val());
// });
//
// $('input[name="t_endAuction"]').change(function (){
//   $('input[name="t_startAuction"]').attr('max', $('input[name="t_endAuction"]').val());
// });

let now = new Date();
let day = now.getDate();
let month = now.getMonth()+1;
let year = now.getFullYear();
month < 10 ? month = '0' + month : month = month;
day < 10 ? day = '0' + day : day = day;
let fullDate = year + '-' + month + '-' + day;
$('input[name="auction_date"]').attr('min', fullDate);

$('.request-wrap').submit(function (e){
  e.preventDefault();
  let some_val = $('input[name="t_startAuction"]').val();
  let hrs = some_val.substr(0,2);
  let mns = some_val.substr(3,5);
  // let current_time = new Date().setHours(parseInt(hrs),parseInt(mns));
  let current_time = new Date();
  if (($('input[name="auction_date"]').val() == fullDate) && (new Date(current_time) < new Date())) {
    showAlert('Время начала аукциона в прошлом', '#c23616');
    $('input[name="t_startAuction"]').css('border-color', 'red');
  } else {
    let end_bidding_date = $('input[name="auction_date"]');
    // if ($('select[name="type"]').val() == 3)
    end_bidding_date = $('input[name="auction_end_date"]');
    let start_date;
    let end_date;
    start_date = new Date($('input[name="auction_date"]').val()).setMilliseconds(-3 * 60 * 60 * 1000);
    end_date = new Date(end_bidding_date.val()).setMilliseconds(-3 * 60 * 60 * 1000);
    start_date = new Date(start_date).setSeconds(doDate($('input[name="t_startAuction"]').val()) * 60);
    end_date = new Date(end_date).setSeconds(doDate($('input[name="t_endAuction"]').val()) * 60);
    start_date = new Date(start_date).toLocaleString().split(',').join('').split('.').join('-');
    end_date = new Date(end_date).toLocaleString().split(',').join('').split('.').join('-');
    let data = {
      csrfmiddlewaretoken: $('input[type="hidden"]').val(),
      level: $('select[name="level"]').val(),
      polymer_id: $('input[name="polymer_id"]').attr('data-id'),
      lot_size: $('input[name="lot_size"]').val(),
      lot_amount: $('input[name="lot_amount"]').val(),
      start_price_per_tone: $('input[name="start_price_per_tone"]').val(),
      stop_price_per_tone: $('input[name="stop_price_per_tone"]').val(),
      recommended_price: $('input[name="recommended_price"]').val(),
      stop_price_per_tone: $('input[name="stop_price_per_tone"]').val(),
      payment_term: $('input[name="payment_term"]').val(),
      step: $('input[name="step"]').val(),
      shipment_condition: $('select[name="shipment_condition"]').val(),
      // shipment_method: $('select[name="shipment_method"]').val(),
      delivery: $('input[name="delivery"]').val(),
      storage_location: $('input[name="storage_location"]').val(),
      start_bidding: dateToString(start_date),
      end_bidding: dateToString(end_date),
      fixation_duration: $('input[name="fixation_duration"]').val(),
      seller: $('input[name="seller"]').val(),
      type: $('select[name="type"]').val(),
      special_conditions: $('textarea').val(),
      is_template: 'off',
      is_price_with_nds: 'off',
      docs: $('input[name="docs"]').val(),
    }
    if (isChecked($('input[name="template_is"]'))) {
      data.is_template = 'on';
    }
    if (isChecked($('input[name="is_price_with_nds"]'))) {
      data.is_price_with_nds = 'on';
    }
    if (basis_list.length > 0) data.storage_location = basis_list.join(', ');
    let flag = true;
    let names = [];
    let date_input = $('input[name="auction_date"]').val();
    if (data.type == 1) {
      delete data.min_price_per_tone;
      delete data.lot_amount;
      delete data.recommended_price;
      delete data.stop_price_per_tone;
    } else if (data.type == 2) {
      delete data.recommended_price;
      delete data.stop_price_per_tone;
    } else if (data.type == 3) {
      delete data.min_price_per_tone;
      delete data.stop_price_per_tone;
      delete data.step;
      delete data.fixation_duration;
    } else if (data.type == 4) {
      delete data.recommended_price;
    }
    if (data.special_conditions == '' || data.special_conditions == undefined)
      delete data.special_conditions;
    for (var key in data) {
      if (data[key] == '' || data[key] == '2019Invalid Date' || data[key] == "default") {
        flag = false;
        if (key == 'start_bidding') {
          if (date_input == '' || date_input == undefined) {
            names.push('auction_date');
          } else {
            names.push('t_startAuction');
          }
        } else if (key == 'end_bidding') {
          if (date_input == '' || date_input == undefined) {
            names.push('auction_date');
          } else {
            names.push('t_endAuction');
          }
        } else names.push(key);
      }
    }
    if (data.level == 2) {
      data.allowed_companys = [];
      for (var i = 0; i < white_list.length; i++) {
        let flag = true;
        for (var j = 0; j < data.allowed_companys.length; j++) {
          if (data.allowed_companys[j] == white_list[i].data_base_id)
            flag = false;
        }
        if (flag) data.allowed_companys.push(white_list[i].data_base_id);
      }
      if (data.allowed_companys[0] == undefined) delete data.allowed_companys;
      if (isChecked($('input[name="is_apply_for_participation"]')))
        data.is_apply_for_participation = true;
      else
        data.is_apply_for_participation = false;
    }
    if (flag) {
      if (data.is_template == 'on') data.is_template = true;
      else data.is_template = false;
      if (data.is_price_with_nds == 'on') data.is_price_with_nds = true;
      else data.is_price_with_nds = false;
      addRequest(data);
    } else {
      showAlert('Заполните все поля', '#c23616');
      for (var i = 0; i < names.length; i++) {
        $('input[name="'+names[i]+'"').css('border-color', 'red');
        $('select[name="'+names[i]+'"').css('border-color', 'red');
      }
    }
  }
});

$('input').on('input', function() {
  if ($(this).val() != '') {
    $(this).removeAttr('style');
  }
});

$('select').change(function (){
  if ($(this).val() != 'default') {
    $(this).removeAttr('style');
  }
});

$('select[name="level"]').change(function (){
  let sel_value = $(this).val();
  if (sel_value == 2) {
    $('.bonus-list-opener').show().css('display', 'flex');
  } else {
    $('.bonus-list-opener').hide();
    $('div[data-opening-name="companys-list"]').slideUp();
    $('div[data-opener-name="companys-list"]').children('.bonus-opener').removeClass('rotated');
  }
});

$('.absolute-polymer-input').focus(function(){
  $(this).siblings('.div-select').show().children('div').show();
});

$('.template_name').blur(function (){
  let id = $(this).siblings('.hidden-fields').children('span[data-name="id"]').text();
  let type = $(this).siblings('.hidden-fields').children('span[data-name="type"]').text();
  let name = $(this).val();
  let data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    trade_offer_id: id,
    bidding_type_id: type,
    template_name: name
  };
  changeTemplateName(data, $(this).siblings('.hidden-fields'), is_rename);
});

$('.absolute-polymer-input').on('input', function(){
  if ($('.div-select').attr('style') == 'display: none;') $('.div-select').show().children('div').show();
  $('.div-option').show();
  let value = $(this).val().toUpperCase();
  let len = value.length;
  $('.div-option').each(function (i, elem){
    let shortcode = $(elem).attr('data-shortcode').toUpperCase();
    if (shortcode.indexOf(value) == -1) $(elem).hide();
  });
});

$('.template_chooser').click(function (){
  is_rename = true;
  $(this).siblings('.template_name').blur();
  $('.close-templates').click();
});

$('body').click(function(e){
  if (e.target.id == 'polymer-select' ||
      e.target.id == 'polymer-input' ||
      e.target.id == 'polymer-select-bonus' ||
      e.target.id == 'polymer-input-bonus' ||
      e.target.className == 'template_chooser') return;
  let k = 0;
  $('.div-option').each(function (i, elem){
    let shortcode = $(elem).attr('data-shortcode');
    if (shortcode == $('.absolute-polymer-input').val()) {
      k++;
    }
  });
  if (k == 0) $('.absolute-polymer-input').val('').attr('data-id', '').blur();
  $('.div-select').hide().children('div').hide();
});

$('.div-option').click(function (){
  let value = $(this).text();
  let parent = $(this).parent();
  let id = $(this).attr('data-value');
  parent.siblings('input').val(value).attr('data-id', id).blur();
  $(this).parent('.div-select').hide().children('div').hide();
  if (parent.siblings('input').attr('style') != '') parent.siblings('input').removeAttr('style');
});

$('select[name="type"]').change(function (){
  $('label').show();
  $('input').removeAttr('style');
  $('select').removeAttr('style');
  if ($(this).val() == 1) {
    $('label[data-name="stop_price_per_tone"]').hide().children('input').val('');
    $('label[data-name="lot-count"]').hide().children('input').val('');
    $('label[data-name="min-price-per-ton"]').hide().children('input').val('');
    $('label[data-name="recommended_price"]').hide().children('input').val('');
    // $('label[data-name="end_bidding"]').hide().children('input').val(new Date());
    $('#auction_date').text('Дата проведения торгов');
  } else if ($(this).val() == 2){
    $('label[data-name="stop_price_per_tone"]').hide().children('input').val('');
    $('label[data-name="recommended_price"]').hide().children('input').val('');
    // $('label[data-name="end_bidding"]').hide().children('input').val(new Date());
    $('#auction_date').text('Дата проведения торгов');
  } else if ($(this).val() == 3) {
    $('label[data-name="stop_price_per_tone"]').hide().children('input').val('');
    $('#auction_date').text('Дата начала торгов');
    $('label[data-name="min-price-per-ton"]').hide().children('input').val('');
    $('label[data-name="step"]').hide().children('input').val('');
    $('label[data-name="fixation-duration"]').hide().children('input').val('');
  } else if ($(this).val() == 4) {
    $('label[data-name="recommended_price"]').hide().children('input').val('');
    $('label[data-name="end_bidding"]').hide().children('input').val(new Date());
    $('#auction_date').text('Дата проведения торгов');
  }
});
let flag = false;
$('.bonus-opener').click(function (){
  let name = $(this).parent().attr('data-opener-name');
  $('div[data-opening-name="'+name+'"]').slideToggle();
  $(this).toggleClass('rotated');
});

$('#add_company_to_list').click(function (){
  if (white_list.length > 0 && white_list[white_list.length-1].is_checked == false) {
    showAlert('Заполните и проверьте все компании в списке', '#c23616');
  } else {
    let list = $(this).parent().parent().parent();
    $(list).append(`
      <label class="companys-list" data-id="`+white_list.length+`">
        <div class="first">
          <span>ИНН компании:</span>
          <input type="text" placeholder="Введите инн компании" class="company_inn">
        </div>
        <div class="second">
          <span>Название компании:</span>
          <span class="company-name">Неизвестно</span>
        </div>
        <div class="third">
          <button type="button" name="button" class="check_company">Проверить</button>
          <button type="button" name="button" class="delete_company">Удалить</button>
        </div>
      </label>
    `);
    white_list.push({
      company_id: white_list.length,
      inn: 0,
      name: 'Неизвестно',
      is_checked: false
    });
    setTimeout(() => {
      $(list).children('label:last-child').addClass('active-label');
    }, 100);
  }
});

$('.bonus-list').on('click', '.delete_company', function() {
  let company = $(this).parent().parent();
  let id = $(company).attr('data-id');
  let k = searchCompanybyId(id);
  $(company).removeClass('active-label');
  if (k == 0) white_list.splice(k,1);
  else white_list.splice(k, parseInt(k));
  setTimeout(() => {
    $(company).detach();
  }, 250);
});

$('.bonus-list').on('click', '.check_company', function (){
  let id = $(this).parent().parent().attr('data-id');
  let k = searchCompanybyId(id);
  let data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    inn: white_list[k].inn
  };
  checkCompanyINN(data, k, this);
  console.log('privet');
});

$('.bonus-list').on('input', '.company_inn', function() {
  let value = $(this).val();
  let id = $(this).parent().parent().attr('data-id');
  let k = searchCompanybyId(id);
  white_list[k].inn = value;
});

$('.close-templates').click(function (){
  $('.templates-wrap').slideUp('fast');
  $('.templates-window').removeAttr('style');
});

$('#template-opener').click(function (){
  $('.templates-wrap').slideDown('fast');
  $('.templates-window').css('top', '10%');
});

$('.new-basis').click(function (){
  let value = $('input[name="storage_location"]').val();
  if (value == '') showAlert('Заполните базис', '#c23616');
  else {
    basis_list.push(value);
    $('input[name="storage_location"]').val('');
    $('.basis-list').append(`
      <li data-index="`+(basis_list.length-1)+`">
          <span>`+value+`</span>
          <div>
              <span class="delete-basis">×</span>
              <span class="update-basis">&#x270E</span>
          </div>
      </li>
    `);
    $('.basis-count').text(basis_list.length);
  }
});

$('.basis-list-opener').click(function (){
  $(this).toggleClass('rotated-opener');
  $('.basis-list').slideToggle('fast');
});

$('.basis-list').on('click', '.delete-basis', function() {
  deleteBasis($(this));
});

$('.basis-list').on('click', '.update-basis', function() {
  $('input[name="storage_location"]').val($(this).parent().siblings('span').text());
  $('.basis-list-opener').click();
  deleteBasis($(this));
});