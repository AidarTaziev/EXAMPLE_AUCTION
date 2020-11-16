var client_deals = [];

function drawDeals(elem) {
  let class_tr = '';
  if ($('.small').children('.active').length > 0) class_tr = ' small-active';
  else if ($('.medium').children('.active').length > 0) class_tr = ' medium-active';
  // let hours = (new Date(elem.betDatetime).getHours());
  // elem.betDatetime = new Date(elem.betDatetime).setHours(hours);
  let content;
  if (is_moderator == 'moderator') {
    content = `
      <tr class="biddings_tr_from_server` + class_tr + `" id="`+elem.id+`">
        <td>`+ new Date(elem.published_datetime).toLocaleString().substr(11) + `</td>
        <td>`+ parseInt(elem.lot_amount).toLocaleString() +`</td>
        <td>`+ elem.total_amount.toLocaleString() +` т.</td>
        <td class="price_per_tone"><span>`+ parseInt(elem.bet_price_per_tone).toLocaleString() +` руб.</span></td>
        <td>`+ parseInt(elem.total_price).toLocaleString() +` руб.</td>
        <td><a href="/profile/`+ elem.client_id +`" target="_blank">`+ elem.client_first_name +` `+ elem.client_last_name +`</a></td>
      </tr>
    `;
  } else {
    content = `
      <tr class="biddings_tr_from_server` + class_tr + `" id="`+elem.id+`">
        <td>`+ new Date(elem.published_datetime).toLocaleString().substr(11) + `</td>
        <td>`+ parseInt(elem.lot_amount).toLocaleString() +`</td>
        <td>`+ elem.total_amount.toLocaleString() +` т.</td>
        <td class="price_per_tone"><span>`+ parseInt(elem.bet_price_per_tone).toLocaleString() +` руб.</span></td>
        <td>`+ parseInt(elem.total_price).toLocaleString() +` руб.</td>
      </tr>
    `;
  }

  $('.user-bids').append(content);
}
