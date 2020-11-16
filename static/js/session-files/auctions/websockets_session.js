var roomName = window.location.pathname;
var webSocket;
var newbidAuido = new Audio();
newbidAuido.src = "/static/js/session-files/auctions/audio/newbid.mp3";
newbidAuido.autoplay = true;
newbidAuido.muted = true;
if (window.location.host.indexOf('127.0.0.1') != -1 || window.location.host.indexOf('localhost') != -1) {
  bidding_session_host = '127.0.0.1:8888';
  webSocket = new WebSocket(
    'ws://' + bidding_session_host +
    '/ws/' + auction_type + '' + roomName + '/'
  );
} else {
  bidding_session_host = window.location.host;
  webSocket = new WebSocket(
    'wss://' + bidding_session_host +
    '/ws/' + auction_type + '' + roomName + '/'
  );
}

webSocket.onmessage = function(res) {
  res = JSON.parse(res.data);
  console.log(res);
  let offset_ms = new Date() - new Date(res.now_datetime);
  if (res.middle_price_per_tone != undefined) {
    let price_str = new String(res.middle_price_per_tone);
    price_str = replaceAt(price_str, price_str.indexOf('.'), ',');
    $('#current_lot_price').text(price_str + ' руб.');
  }
  if (res.all_bets != null && res.all_bets != undefined && res.auction_is_finished != true) {
    // проверяем пришло ли время конца аукциона, если да запускаем таймер
    if (res.end_bidding != undefined) {
      endAuctionTime = res.end_bidding;
    }
    // очищаем все таймеры на странице
    let max_id = setTimeout(function () {});
    while (max_id--) {
        clearTimeout(max_id);
    }
    reserveTimer(false, endAuctionTime, offset_ms);

    if (res.current_seller_offer != undefined && auction_type == 'counter') {
      $('#lots_number').text(res.current_seller_offer.lot_amount);
      $('#lot_price').text(res.current_seller_offer.min_price_per_tone + ' руб.');
      $('input[name="lots-count"]').val(res.current_seller_offer.lot_amount);
      min_price = parseInt(res.current_seller_offer.min_price_per_tone);
      $('input[name="min-price-per-ton"]').val(min_price);
      free_lots = res.num_free_lots;
      max = res.current_seller_offer.lot_amount;
      if (min_price < parseInt($('.table_min_price').children('input').val())) min_price = parseInt($('.table_min_price').children('input').val());
      else $('.table_min_price').children('input').val(min_price);
    } else if (res.current_seller_offer == undefined && auction_type == 'counter') {
      $('span[data-id="counter_amount"]').text('Не указано');
      $('span[data-id="counter_price"]').text('Не указано');
      $('input[name="lots-count"]').val('');
      $('input[name="min-price-per-ton"]').val('');
      min_price = 1;
      max = 10000;
    }

    if ($('#alert-wrap').attr('class') == 'alert-wrap alert-active') {//Скрываем всплывающее окно если оно открыто
      $('.alert-wrap .hover').hide();
      $('#alert-wrap').removeClass('alert-active');
      $('#alert-wrap .alert-frame').removeClass('active');
    }
    // копируем массивы и отрисовывем их
    bids_obj.all_bets = res.all_bets;
    checkForFixationTime(res);
    if (bids_obj.all_bets.length > 0) {
      $('.biddings_tr_from_server').detach();
      $('.user-bids').children('tr').detach();
      $.each(bids_obj.all_bets, (index) => {
        drawBids(bids_obj.all_bets[index], false, offset_ms);
      });
      let free_lots_local = max;
      for (var i = 0; i < bids_obj.all_bets.length; i++) {
        free_lots_local -= bids_obj.all_bets[i].lot_amount;
        if (bids_obj.all_bets != undefined && bids_obj.all_bets.length > 0 && free_lots_local <= 0) {
          min_price = parseInt(bids_obj.all_bets[bids_obj.winning_bet_ids_list.length-1].bet_price_per_tone) + step;
          $('.table_min_price').children('input').val(min_price);
        }
      }
      checkLength(bids_obj.all_bets.length, '.all_bids_table');
    }
    updateCounters(res); // обновляем счетчики
    if (res.client_deals.length > 0) dealsCommit(res); // обновляем сделки
    if (res.added_bet != undefined && res.added_bet.client_id != null) {
      showAlert('Успешно', '#66ab55');
      $('.form-td').removeClass('active-form');
      $('#buy_hover').hide();
      $('#table_price span:last-child').text('0');
      $('#table_amount span:last-child').text('0');
      $('.lot_amount_input').val('');
    } else if (res.added_bet != undefined && $('input[name="user"]').val() == 'moderator') {
        let promise = newbidAuido.play();
        if (promise !== undefined) {
          promise.catch(error => {
          // Auto-play was prevented
          // Show a UI element to let the user manually start playback
            console.log('asd');
          }).then(() => {
          // Auto-play started
          });
        }
    }
    setTimeout(function (){
      // deleteOldBids(res.deletedBetsIds);
      let free_lots_local = max;
      for (var i = 0; i < bids_obj.all_bets.length; i++) {
        free_lots_local -= bids_obj.all_bets[i].lot_amount;
      }
      if (free_lots_local <= 0) {
        min_price = parseFloat(res.all_bets[res.fixation_bets_ids_list.length-1].bet_price_per_tone) + step;
        $('.table_min_price').children('input').val(min_price);
      }
    }, 1000);
    checkLength(bids_obj.all_bets.length, '.all_bids_table');
  } else if (res.client_deals != undefined && res.auction_is_finished == undefined) {
    dealsCommit(res);
    if (auction_type == 'counter') checkForFixationTime(res);
  } else if (res.auction_is_finished) {
    let timer = 0;
    if ($('#alert-wrap').attr('class') == 'alert-wrap alert-active') {
      timer = 2000;
    }
    setTimeout(function (){
      $('#accept-wrap .alert-frame').children('.btn-wrap').children('button').detach();
      $('#accept-wrap .alert-frame').children('.btn-wrap').append(`
        <button class="finisher">OK</button>
      `);
      $('#accept-wrap .alert-frame').children('h2').text('Аукцион окончен!');
      $('#accept-wrap').addClass('alert-active');
      $('.alert-wrap .hover').show();
      $('#accept-wrap .alert-frame').addClass('active');
    }, timer);
  } else if (res.deleted_bet != undefined) {
    deleteWinBid(res.deleted_bet);
    deleted_bid_id = null;
  }
};

webSocket.onclose = function (res) {
  setTimeout(function (){
    $('#accept-wrap .alert-frame').children('.btn-wrap').children('button').detach();
    $('#accept-wrap .alert-frame').children('.btn-wrap').append(`
      <button class="reload-page">OK</button>
    `);
    $('#accept-wrap .alert-frame').children('h2').text('Соединение с сервером прервано, перезагрузите страницу').css('color', '#c23616');
    $('#accept-wrap').addClass('alert-active');
    $('.alert-wrap .hover').show();
    $('#accept-wrap .alert-frame').addClass('active');
  }, 10);
};

function dataSender(data) {
  if (data != undefined && data != null && isNaN(data))
    webSocket.send(data);
  else showAlert('Что-то пошло не так!', '#c23616');
}

function dealsUpdate(res) {
  client_deals = res.client_deals;
  $('.user-bids').children('.biddings_tr_from_server').detach();
  $.each(client_deals, (index) => {
    drawDeals(client_deals[index]);
  });
  checkLength(client_deals.length, '.user-bids');
}

function checkLength(leng, table) {
  if (leng > 3) {
    $(table).css('overflow-y', 'scroll');
  } else {
    $(table).removeAttr('style');
  }
}

function updateCounters(res) {
  if (res.num_free_lots != 'Не указано') max = res.num_free_lots;
  $('#free_lots').text(message_for_free_lots + res.num_free_lots);
  $('#fixed_lots').text('Зарезервировано лотов: ' + (res.num_reserved_lots));
}

function dealsCommit(res) {
  let flag = false;
  for (var i = 0; i < res.client_deals.length; i++) {
    if (res.client_deals[i].added_now == true) { flag = true; }
  }
  if (flag) {
    let timer = 0;
    if ($('#alert-wrap').attr('class') == 'alert-wrap alert-active') {
      timer = 2000;
    }
    setTimeout(function (){
      $('#accept-wrap .alert-frame').children('.btn-wrap').children('button').css('display', 'none');
      $('#accept-wrap .alert-frame').children('.btn-wrap').append(`
        <button class="accepter">OK</button>
      `);
      $('#accept-wrap .alert-frame').children('h2').text('Ваша ставка выиграла!');
      $('#accept-wrap').addClass('alert-active');
      $('.alert-wrap .hover').show();
      $('#accept-wrap .alert-frame').addClass('active');
    }, timer);
  }
  dealsUpdate(res);
  updateCounters(res);
}

function checkForFixationTime(res) {
  if (res.fixation_bets_ids_list == undefined || res.fixation_bets_ids_list.length == 0) {
    bids_obj.winning_bet_ids_list = [];
    $('#accept-options').removeAttr('disabled').removeClass('disabled-btn');
    $('.close-btn').removeAttr('disabled').removeClass('disabled-btn');
  }
  else {
    bids_obj.winning_bet_ids_list = res.fixation_bets_ids_list;
    $('#accept-options').attr('disabled', 'disabled').addClass('disabled-btn');
    $('.close-btn').attr('disabled', 'disabled').addClass('disabled-btn');
  }
}
