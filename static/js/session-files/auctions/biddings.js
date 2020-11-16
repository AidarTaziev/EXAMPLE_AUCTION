var step = parseInt($('#lot_step').text().split(' руб.').join('')); // шаг торгов
var min_price = parseInt($('#lot_price').text().split(' руб.').join('').replace(' ', '').replace(' ', '').replace(' ', '')); // минмиальная цена за тонну
var amount = parseFloat($('#lot_amount').text().split(' т.').join('').replace(/,/, '.')); // Объем лота
var fixTime = parseInt($('#fix_time').text().split(' сек.').join('')); // время фиксации лота
var new_amount = 1;
var price; // цена за колличетсво лотов с нужнм шагом
var max = parseInt($('#lots_number').text()); // Максимальное колличетсво лотов
var free_lots = max; //значение свободных лотов
var message_for_free_lots = 'Остаток лотов: ';
var val; // Колличетсво лотов в данный момент
var result = [0, 0, 0];
var auction_type = $('input[name="EXAMPLE_AUCTION-type"]').val();
var is_moderator = $('input[name="user"]').val();
var endAuctionTime = $('.timer i').text();
var deleted_bid_id = null;
var current_id;
var going_to_winners = 0;
var addedObj = {
  bet: {
    auction_id: $('h2').attr('id'),
    old_bet_id: null,
    count: 0,
    price_for_ton: 0
  }
};
var addedOffer = {
  seller_offer: {
    auction_id: $('h2').attr('id'),
    count: 0,
    price_for_ton: 0
  }
}
$('document').ready(() => {
  if (isNaN(min_price)) {
    min_price = 1;
  }
  if (isNaN(max)) {
    max = 10000;
    free_lots = max;
  }
  $('.table_min_price').children('input').val(min_price);
  loadRowsSizes();
});

$('#buyer-btn').click(function (){
  if (isNaN(min_price)) {
    min_price = 1;
    $('.table_min_price').children('input').val(min_price);
  }
  if (isNaN(max)) {
    max = 10000;
    free_lots = max;
  }
  $('#buy_hover').show();
  $('.form-td').addClass('active-form');
});

$('#accept-options').click(function(){
  if ($('input[name="lots-count"]').val() == '' || $('input[name="lots-count"]').val() == 0) {
    showAlert('Заполните поле количество лотов', '#c23616');
  } else if ($('input[name="min-price-per-ton"]').val() == '' || $('input[name="min-price-per-ton"]').val() == 0) {
    showAlert('Заполните поле минимальной цены за тонну', '#c23616');
  } else {
    addedOffer.seller_offer.count = $('input[name="lots-count"]').val();
    addedOffer.seller_offer.price_for_ton = $('input[name="min-price-per-ton"]').val();
    $('#accept-wrap').addClass('alert-active');
    $('#accept-wrap .alert-frame').addClass('active');
    $('#accept-wrap .alert-frame h2').text('Вы уверены, что хотите продать '+addedOffer.seller_offer.count+' лотов по цене '+addedOffer.seller_offer.price_for_ton+' рублей за лот?').css('font-size', '1.2em');
    $('#accept-wrap .hover').show();
  }
});

$('table').on('click', '.get-winner', function (){
  current_id = $(this).parent().parent().attr('id');
  let id = $(this).parent().parent().attr('id');
  for (let i = 0; i < bids_obj.all_bets.length; i++) {
    if (bids_obj.all_bets[i].id == +id)
      going_to_winners = i;
  }
  if ($(this).parent().parent().attr('class').indexOf('winning') != -1) {
    showAlert('Вы и так лидируете!', "#c23616");
  } else {
    $('#accept-wrap').addClass('alert-active');
    $('#accept-wrap .alert-frame').addClass('active');
    $('#accept-wrap .alert-frame h2').text('Вы уверены, что хотите выйти в лидеры?');
    $('#accept-wrap .hover').show();
  }
});

$('.close-btn').click(() => {
  $('#accept-wrap').addClass('alert-active');
  $('#accept-wrap .alert-frame').addClass('active');
  $('#accept-wrap .alert-frame h2').text('Вы уверены, что хотите завершить торги?');
  $('#accept-wrap .hover').show();
});

$('#buy_hover').click(function (){
  $(this).hide();
  $('.form-td').removeClass('active-form');
});

$('.lot_amount_input').on('input', function(){
  val = $(this).val();
  let amount_class = $(this).attr('class');
  if (amount_class == 'lot_amount_input first_amount') {
    $('.second_amount').val($(this).val());
  } else {
    $('.first_amount').val($(this).val());
  }
  if (val > max && auction_type == 'typical') {
    $(this).val(val.substring(0, val.length - 1));
    showAlert('Максимальное колличество лотов ' + max, '#c23616');
    val = $(this).val();
    if (amount_class == 'lot_amount_input first_amount') {
      $('.second_amount').val($(this).val());
    } else {
      $('.first_amount').val($(this).val());
    }
  } else if (val < 0) {
    $(this).val(1);
    showAlert('Минимальное количество лотов 1 ' + max, '#c23616');
    val = $(this).val();
    if (amount_class == 'lot_amount_input first_amount') {
      $('.second_amount').val($(this).val());
    } else {
      $('.first_amount').val($(this).val());
    }
  }// Конец Валидации поля лотов
  new_amount = amount * val;
  if ($('.min_price').val() != min_price) price = $('.min_price').val() * new_amount;
  else price = min_price * new_amount;
  if (isNaN(new_amount)) {
    $('#table_amount span:last-child').text(0);
    $('#table_price span:last-child').text(0);
  } else {
    $('#table_amount span:last-child').text(new_amount.toLocaleString() + ' т.');
    $('#table_price span:last-child').text(price.toLocaleString() + ' руб.');
  }

});

$('.min_price').on('input', function() {
  let betPricePerTon = parseFloat($(this).val().replace(',','.').replace(' ',''));
  if (isNaN(betPricePerTon)) {
    $(this).val($(this).val().substring(0, $(this).val().length - 1));
  } else if ($(this).val() == '') {
    price = 0;
    $('#table_price span:last-child').text(price.toLocaleString() + ' руб.');
  } else {
    price = betPricePerTon * new_amount;
    $('#table_price span:last-child').text(price.toLocaleString() + ' руб.');
  }
  compareInputs(this);
});

$('.min_price').on('change', function() {
  let bet_price_per_tone = parseFloat($(this).val());
  let start_price = parseInt($('#lot_price').text().split(' руб.').join('').replace(' ', '').replace(' ', '').replace(' ', ''));
  if (isNaN(start_price)) start_price = 1;
  let error = false;
  if (bet_price_per_tone < min_price && auction_type == 'typical') {
    showAlert('Минимальная цена ' + min_price, '#c23616');
    error = true;
  } else if ((bet_price_per_tone - start_price) % step != 0 && auction_type == 'typical') {
    showAlert('Цена должна быть кратна ' + start_price, '#c23616');
    error = true;
  }
  if (error) {
    $(this).val(min_price);
    price = min_price * new_amount;
    $('#table_price span:last-child').text(parseInt(price).toLocaleString() + ' руб.');
  }
  compareInputs(this);
});

$('.link-for-session').click(function (){
  let identificator = $('h2').attr('id');
  window.open('/EXAMPLE_AUCTION/bidding_session/'+identificator+'','', 'scrollbars=1,width=1000,height=600');
});

$('.add_lots').submit(function(e) {
  addedObj.bet.count = parseInt($('.lot_amount_input').val());
  addedObj.bet.price_for_ton = $('.min_price').val();
  if (addedObj.bet.price_for_ton < min_price && auction_type == 'typical') {
    showAlert('Минимальая ставка ' + min_price + ' руб.', '#c23616');
  } else if (isNaN(addedObj.bet.count) || addedObj.bet.count == 0) {
    showAlert('Заполните поле количество лотов', '#c23616');
  } else if (isNaN(addedObj.bet.price_for_ton) || addedObj.bet.price_for_ton == 0) {
    showAlert('Заполните поле цена за тонну', '#c23616');
  } else {
    $('#accept-wrap').addClass('alert-active');
    $('#accept-wrap .alert-frame').addClass('active');
    $('#accept-wrap .alert-frame h2').text('Вы уверены, что хотите купить '+addedObj.bet.count+' лотов по цене '+addedObj.bet.price_for_ton+' рублей за лот?').css('font-size', '1.2em');
    $('#accept-wrap .hover').show();
  }
  e.preventDefault();
});


$('table').on('click', '.upper', function (){
  current_id = $(this).parent().parent().attr('id');
  $('#accept-wrap').addClass('alert-active');
  $('#accept-wrap .alert-frame').addClass('active');
  $('#accept-wrap .alert-frame h2').text('Вы уверены?');
  $('#accept-wrap .hover').show();
});

$('table').on('click', '.deleter', function (){
  deleted_bid_id = $(this).parent().parent().attr('id');
  $('#accept-wrap').addClass('alert-active');
  $('#accept-wrap .alert-frame').addClass('active');
  $('#accept-wrap .alert-frame h2').text('Вы уверены?');
  $('#accept-wrap .hover').show();
});

$('#hide_accept').click(function (){
  $('#accept-wrap .hover').hide();
  $('#accept-wrap').removeClass('alert-active');
  $('#accept-wrap .alert-frame').removeClass('active');
  $('#accept-wrap .alert-frame h2').text('Вы уверены?').removeAttr('style');
});

$('#success_accept').click(function (){
  if ($(this).parent().parent().children('h2').text() != 'Вы уверены, что хотите завершить торги?') {
    if ($(this).parent().siblings('h2').attr('style') != 'font-size: 1.2em;') {
      console.log($(this).parent().parent().children('h2').text());
      addedObj.bet.old_bet_id = current_id;
      for (var i = 0; i < bids_obj.all_bets.length; i++) {
        if (bids_obj.all_bets[i].id == current_id) {
          let current_val = parseInt(bids_obj.all_bets[i].bet_price_per_tone);
          addedObj.bet.price_for_ton = current_val + step;
          addedObj.bet.count = bids_obj.all_bets[i].lot_amount;
        }
      }
      if ($(this).parent().parent().children('h2').text() == 'Вы уверены, что хотите выйти в лидеры?') {
        let free = +free_lots;
        let flag = false;
        for (let i = 0; i < bids_obj.all_bets.length; i++) { 
          free -= bids_obj.all_bets[i].lot_amount;
          if (free < bids_obj.all_bets[going_to_winners].lot_amount) {
            addedObj.bet.price_for_ton = +bids_obj.all_bets[i].bet_price_per_tone + (+step);
            break;
          }
        }

      }
    } else {
      $('.input-td input[type="text"]').val('');
    }
    let data;
    if (addedOffer.seller_offer.count != 0) {
      data = JSON.stringify(addedOffer);
    } else if (addedOffer.seller_offer.count == 0 && deleted_bid_id != null) {
      data = {
        deleted_bet: deleted_bid_id
      };
      data = JSON.stringify(data);
    } else {
      data = JSON.stringify(addedObj);
    }
    dataSender(data);
  } else {
    let data = {
      auction_need_to_finish: true
    }
    data = JSON.stringify(data);
    dataSender(data);
  }
  $('#accept-wrap .hover').hide();
  $('#accept-wrap').removeClass('alert-active');
  $('#accept-wrap .alert-frame').removeClass('active');
  $('#accept-wrap .alert-frame h2').text('Вы уверены?').removeAttr('style');
});

$('.alert-frame').on('click', '.reload-page', function (){
  document.location.reload();
});

$('#accept-wrap .btn-wrap').on('click', '.finisher', function(){
  let identificator = $('h2').attr('id');
  location.href = '/EXAMPLE_AUCTION/properties/'+identificator;
});

$('#accept-wrap').on('click', '.accepter', function (){
  $('#accept-wrap .alert-frame').children('.btn-wrap').children('button').removeAttr('style');
  $(this).detach();
  $('#accept-wrap .alert-frame').children('h2').text('');
  $('#accept-wrap').removeClass('alert-active');
  $('.alert-wrap .hover').hide();
  $('#accept-wrap .alert-frame').removeClass('active');
});

function compareInputs(elem) {
  let value = $(elem).val();
  let amount_class = $(elem).attr('class');
  if (amount_class == 'min_price first_price') {
    $('.second_price').val(value);
  } else {
    $('.first_price').val(value);
  }
}
