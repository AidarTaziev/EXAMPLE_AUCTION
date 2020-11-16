var bids_obj = {
  all_bets: [],
  winning_bet_ids_list: []
};

function drawBids(bid, flag, offset_ms) { // прорисовка торгов
  // console.log(bid.lot_amount * amount);
  let def_amount = bid.total_amount;
  console.log(bid);
  console.log(bid.total_amount);
  let reserve_time = null;

  if (flag && bids_obj.all_bets.indexOf(bid) == 0) { appendTr(' added_lot', bid, def_amount, offset_ms); }
  else { appendTr('', bid, def_amount, offset_ms); }

  if (bid.client_id != null && is_moderator == undefined) {
    $('#' + bid.id).children('td.empty').append(`
      <img src="/static/images/user.png" width="30px" height="30px" title="Ваша ставка">
    `);
    $('#' + bid.id).children('td.price_per_tone').append(`
      <button type="button" class="upper"><div></div></button>
      <img src="/static/images/ft-arrow.png" width="16px" class="get-winner"/>
    `);
    if ($('#' + bid.id).attr('class') == 'biddings_tr_from_server lost' && auction_type == 'counter') {
      $('#' + bid.id).children('td.price_per_tone').append(`
        <button type="button" class="upper deleter"><div></div></button>
      `);
    }
  } else if (is_moderator == 'moderator') {
    $('#' + bid.id).children('td.empty').append(`
      <a href="/profile/`+ bid.client_id +`" target="_blank">`+ bid.client_first_name +` `+ bid.client_last_name +`</a>
    `);
  }
}

function appendTr(class_name, elem, def_amount, offset_ms) {
  let isWinning = 'lost';
  let timerTostring = '';
  let trFlag = 'lost';
  if (bids_obj.winning_bet_ids_list.indexOf(elem.id) != -1) {
    isWinning = 'winning';
    trFlag = 'winning';
    let sum = free_lots;
    for (var i = 0; i < bids_obj.all_bets.length; i++) {
      sum -= bids_obj.all_bets[i].lot_amount;
      if (bids_obj.all_bets[i].id == elem.id) {
        break;
      }
    }
    if (sum < 0) trFlag = 'not-full';
    timerTostring = pureDate(elem.end_fixation_datetime)[0] + ':' + pureDate(elem.end_fixation_datetime)[1];
  }
  let content = `
    <tr class="biddings_tr_from_server `+ trFlag +`" id="`+elem.id+`">
      <td><span class="`+ isWinning +`">`+ timerTostring +`</span></td>
      <td>`+ parseInt(elem.lot_amount).toLocaleString() +`</td>
      <td>`+ def_amount.toLocaleString() +`</td>
      <td class="price_per_tone"><span>`+ parseInt(elem.bet_price_per_tone).toLocaleString() +`</span></td>
      <td>`+ parseInt(elem.total_price).toLocaleString() +`</td>
      <td class="empty"></td>
    </tr>
  `;
  if (class_name == '') {
    $('.all_bids_table').append(content);
  } else {
    $(content).insertAfter($('.all_bids_table tbody'));
  }
  reserveTimer(elem, elem.end_fixation_datetime, offset_ms);
}

function reserveTimer(bid, timer, offset_ms) {
  let message = '';
  if (timer == '') return '';
  else {
    let arr = pureDate(timer, offset_ms);
    if (arr[0] == undefined) message = '00:00';
    else {
      if (bid == false) {
        let strHours = ' часов';
        let strMins = ' минут';
        let strSecs = ' секунд'
        if (parseInt(arr[2].substr(arr[2].length-1,1)) < 5 && parseInt(arr[2].substr(arr[2].length-1,1)) > 1) strHours = ' часа';
        else if (parseInt(arr[2].substr(arr[2].length-1,1)) == 1) strHours = ' час';
        if (parseInt(arr[0].substr(arr[2].length-1,1)) < 5 && parseInt(arr[0].substr(arr[2].length-1,1)) > 1) strMins = ' минуты';
        else if (parseInt(arr[0].substr(arr[2].length-1,1)) == 1) strMins = ' минута';
        if (parseInt(arr[1].substr(arr[2].length-1,1)) < 5 && parseInt(arr[1].substr(arr[2].length-1,1)) > 1) strSecs = ' секунды';
        else if (parseInt(arr[1].substr(arr[2].length-1,1)) == 1) strSecs = ' секунда';
        message = arr[2] + strHours + ' ' + arr[0] + strMins + ' ' + arr[1] + strSecs;
      } else {
        message = arr[0] + ':' + arr[1];
        changeTimerColor(arr, bid);
      }
    }
    if (bid != false) {
      $('#' + bid.id).children().children('.winning').text(message);
      if (!isWinner(bid.id)) {
        $('#' + bid.id).children().children('.winning').text('').css('padding', '0');
        return false;
      }
      if (arr == false) {
        deleteWinBid(bid.id);
        return false;
      }
      setTimeout(() => {reserveTimer(bid, bid.end_fixation_datetime, offset_ms)}, 1000);
    } else {
      $('.timer').children('i').text(message).css('display', 'inline');
      setTimeout(() => {reserveTimer(false, timer, offset_ms)}, 1000);
    }
  }
}

function pureDate(timer, offset_ms) {
  let t = Date.parse(timer) - (Date.parse(new Date()) - offset_ms);
  var seconds = Math.floor( (t/1000) % 60 );
  var minutes = Math.floor( (t/1000/60) % 60 );
  var hours = Math.floor( (t/(1000*60*60)) % 24 );
  var full_secs = minutes * 60 + seconds;
  if (minutes == 0 && seconds == 0) return false;
  if (minutes < 10) minutes = '0' + minutes;
  if (seconds < 10) seconds = '0' + seconds;
  if (hours < 10) hours = '0' + hours;
  return [minutes.toString(), seconds.toString(), hours.toString(), full_secs];
}

function changeTimerColor(arr, bid) {
  if (arr[3] >= (fixTime * 2 / 3)) {
    $('#' + bid.id).children().children('.winning').css('background-color', '#66ab55');
  } else if ((arr[3] < (fixTime *2 / 3)) && (arr[3] >= fixTime / 3)) {
    $('#' + bid.id).children().children('.winning').css('background-color', '#f89406');
  } else if ((arr[3] < (fixTime / 3)) && (arr[3] >= 0)) {
    $('#' + bid.id).children().children('.winning').css('background-color', '#e95c3c');
  } else {
    $('#' + bid.id).children().children('.winning').css('display', 'none');
  }
}

function isWinner(id) {
  for (var i = 0; i < bids_obj.winning_bet_ids_list.length; i++) {
    if (id == bids_obj.winning_bet_ids_list[i]) { return true; }
  }
  return false;
}

function deleteWinBid(id) { // стирание старых торгов со сраницы
  $('#' + id).addClass('some').animate({
    opacity: '0'
  }, 200, function () {
    $(this).detach();
    let k = 0;
    for (var i = 0; i < bids_obj.all_bets.length; i++) {
      if (bids_obj.all_bets[i].id == id) k = i;
    }
    bids_obj.all_bets.splice(k,k+1);
  });
  checkLength(bids_obj.all_bets.length);
}
