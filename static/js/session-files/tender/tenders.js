var step = parseInt($('#lot_step').text().split(' руб.').join('')); // шаг торгов
var min_price = parseInt($('#lot_price').text().split(' руб.').join('').replace(' ', '').replace(' ', '').replace(' ', '')); // минмиальная цена за тонну
var amount = parseInt($('#lot_amount').text().split(' т.').join('')); // Объем лота
var new_amount = 1;
var price; // цена за колличетсво лотов с нужнм шагом
var max = parseInt($('#lots_number').text()); // Максимальное колличетсво лотов
var free_lots = max; //значение свободных лотов
var message_for_free_lots = 'Остаток лотов: ';
var val; // Колличетсво лотов в данный момент
var deleted_bid_id = null;
var bets_for_sale = [];
var is_seller = $('input[name="user"]').val();
var all_bets = [];
var addedObj = {
  csrfmiddlewaretoken: getCookie('csrftoken'),
  tender: $('h2').attr('id'),
  lot_amount: 0,
  bet_price_per_tone: 0
};
$('document').ready(() => {
  $('.all_bids_table').css('overflow-y', 'scroll');
  $('.table_min_price').children('input').val(min_price);
  loadRowsSizes();
  let data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    tender_id: addedObj.tender
  }
  sendDataFromTender(data, '/tender/get_bets');
});

$('#buyer-btn').click(function (){
  if ($(this).attr('class') == 'buy-btn accept-btn') {
    $('.form-td').addClass('large-form-td');
    for (var i = 0; i < all_bets.length; i++) {
      if (all_bets[i].is_sale) {
        bets_for_sale.push(all_bets[i]);
        $('.add_lots').append(`
          <label class="bet-for-sale">
            <span>`+all_bets[i].client__first_name+` `+all_bets[i].client__last_name+`</span>
            <div class="">
              <input type="number" name="" value="`+all_bets[i].lot_amount+`" class="bid_lots_field" data-id="`+ all_bets[i].id +`">
              <span>лотов</span>
            </div>
            <span>по цене `+all_bets[i].bet_price_per_tone+` руб. за тонну</span>
          </label>
        `);
      }
    }
    if (bets_for_sale.length > 0) {
      $('.add_lots').append(`
        <input type="submit" name="" value="Подтвердить" id="sale_offer">
      `);
      $('#buy_hover').show();
      $('.form-td').addClass('active-form');
    } else {
      showAlert('Выберите хотябы одну ставку', '#c23616');
    }
  } else {
    $('#buy_hover').show();
    $('.form-td').addClass('active-form');
  }
});


$('#buy_hover').click(function (){
  $(this).hide();
  $('.form-td').removeClass('active-form');
  bets_for_sale = [];
  $('.bet-for-sale').detach();
  $('#sale_offer').detach();
});

$('.lot_amount_input').on('input', function(){
  val = $(this).val();
  let amount_class = $(this).attr('class');
  if (amount_class == 'lot_amount_input first_amount') {
    $('.second_amount').val($(this).val());
  } else {
    $('.first_amount').val($(this).val());
  }
    // Валидация поля лотов
  let j = 0;
  let check_arr = [0,1,2,3,4,5,6,7,8,9];
  for (let i = 0; i < check_arr.length; i++) {
    if (val.substring(val.length - 1, val.length) == check_arr[i]) {
      j++;
    }
  }
  if (j != 1) $(this).val(val.substring(0, val.length - 1));
  if (val > max) {
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
  new_amount = amount * parseInt(val);
  if ($('.min_price').val() != min_price) price = $('.min_price').val() * new_amount;
  else price = min_price * new_amount;
  if (isNaN(new_amount)) {
    $('#table_amount span:last-child').text(0);
    $('#table_price span:last-child').text(0);
  } else {
    $('#table_amount span:last-child').text(parseInt(new_amount).toLocaleString() + ' т.');
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

$('.add_lots').submit(function(e) {
  e.preventDefault();
  if (is_seller == 'seller') {
    $('#accept-wrap').addClass('alert-active');
    $('#accept-wrap .alert-frame').addClass('active');
    $('#accept-wrap .alert-frame h2').text('Вы уверены?');
    $('#accept-wrap .hover').show();
  } else {
    addedObj.lot_amount = parseInt($('.lot_amount_input').val());
    addedObj.bet_price_per_tone = $('.min_price').val();
    if (isNaN(addedObj.lot_amount) || addedObj.lot_amount == 0) {
      showAlert('Заполните поле количество лотов', '#c23616');
    } else if (isNaN(addedObj.bet_price_per_tone) || addedObj.bet_price_per_tone == 0) {
      showAlert('Заполните поле цена за тонну', '#c23616');
    } else {
      $('#accept-wrap').addClass('alert-active');
      $('#accept-wrap .alert-frame').addClass('active');
      $('#accept-wrap .alert-frame h2').text('Вы уверены, что хотите купить '+addedObj.lot_amount+' лотов по цене '+addedObj.bet_price_per_tone+' рублей за лот?').css('font-size', '1.2em');
      $('#accept-wrap .hover').show();
    }
  }
});

$('table').on('click', '.deleter', function (){
  deleted_bid_id = $(this).parent().parent().attr('data-id');
  $('#accept-wrap').addClass('alert-active');
  $('#accept-wrap .alert-frame').addClass('active');
  $('#accept-wrap .alert-frame h2').text('Вы уверены?');
  $('#accept-wrap .hover').show();
});

$('.add_lots').on('input', '.bid_lots_field', function() {
  let val = $(this).val();
  let id = $(this).attr('data-id');
  for (var i = 0; i < bets_for_sale.length; i++) {
    if (bets_for_sale[i].id == id) bets_for_sale[i].lot_amount = parseInt(val);
  }
});

$('.close-btn').click(() => {
  $('#accept-wrap').addClass('alert-active');
  $('#accept-wrap .alert-frame').addClass('active');
  $('#accept-wrap .alert-frame h2').text('Вы уверены, что хотите завершить торги?');
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
    $('.input-td input[type="text"]').val('');
    let data;
    if (deleted_bid_id != null) {
      data = {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        bet_id: deleted_bid_id
      };
      sendDataFromTender(data, '/tender/delete_bet');
    } else if (bets_for_sale.length > 0) {
      data = {
        csrfmiddlewaretoken: getCookie('csrftoken'),
        tender_id: $('h2').attr('id'),
        bets: new Array(),
        lots: new Array()
      }
      for (var i = 0; i < bets_for_sale.length; i++) {
        data.bets.push(bets_for_sale[i].id);
        data.lots.push(bets_for_sale[i].lot_amount);
      }
      sendDataFromTender(data, '/tender/make_deal');
    } else {
      data = addedObj;
      sendDataFromTender(data, '/tender/add_bet');
    }
  } else {
    let data = {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      tender_id: $('h2').attr('id')
    }
    sendDataFromTender(data, '/tender/finish');
  }
  $('#accept-wrap .hover').hide();
  $('#accept-wrap').removeClass('alert-active');
  $('#accept-wrap .alert-frame').removeClass('active');
  $('#accept-wrap .alert-frame h2').text('Вы уверены?').removeAttr('style');
});

$('#accept-wrap .btn-wrap').on('click', '.finisher', function(){
  let identificator = $('h2').attr('id');
  location.href = '/tender/property/'+identificator;
});

$('#accept-wrap').on('click', '.accepter', function (){
  $('#accept-wrap .alert-frame').children('.btn-wrap').children('button').removeAttr('style');
  $(this).detach();
  $('#accept-wrap .alert-frame').children('h2').text('');
  $('#accept-wrap').removeClass('alert-active');
  $('.alert-wrap .hover').hide();
  $('#accept-wrap .alert-frame').removeClass('active');
});

$('.all_bids_table').on('click', '.check-for-sale', function (){
  let flag = isChecked($(this));
  $(this).parent().parent().attr('data-is-sale', flag);
  let id = $(this).parent().parent().attr('data-id');
  for (var i = 0; i < all_bets.length; i++) {
    if (all_bets[i].id == id) all_bets[i].is_sale = flag;
  }
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

function deleteBet(id) {
  $('tr[data-id="'+ id +'"]').addClass('some').animate({
    opacity: '0'
  }, 200, function () {
    $(this).detach();
    let k = 0;
    for (var i = 0; i < all_bets.length; i++) {
      if (all_bets[i].id == id) k = i;
    }
    all_bets.splice(k,k+1);
  });
}
