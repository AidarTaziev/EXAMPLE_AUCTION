function addRequest(data) { // Добавление заявки
  $.ajax({
    url: '/create_trade_offer',
    type: 'POST',
    data: data,
    success: (res) => {
      if (res == 'Ваша заявка отправлена') {
        showAlert(res, '#66ab55');
        setTimeout(function(){
          location.href = '/trade_offers';
        }, 2000);
      } else {
        showAlert(res, '#c23616');
      }

      setTimeout(function (){
        $('.alert-wrap').removeClass('alert-active');
        $('.alert-frame').removeClass('active');
        $('.alert-frame').removeAttr('style');
      }, 2000);
    },
    error: (res) => {
      showAlert('Ошибка сервера', '#c23616');
    }
  });
}

function getSberBankLink(data) {
  $.ajax({
    url: '/bank_account/credit_request',
    type: 'POST',
    data: data,
    success: (res) => {
      if (!res.error) {
        if (res.data.redirect_url != undefined)
          location.href = res.data.redirect_url;
        else
          showAlert('Сбербанк временно недоступен', '#c23616');
      } else {
        showAlert(res.data, '#c23616');
      }
    },
    error: () => {
      showAlert('Сервер временно недоступен', '#c23616');
    }
  });
}

function userAction(data, flag) { // Вход и регистрация
  let url_ajax;
  let alertSpan;
  flag ? url_ajax = '/auth/login' : url_ajax = '/auth/signup';
  flag ? alertSpan = '.alert-span-log' : alertSpan = '.alert-span-sign';
  $.ajax({
    url: url_ajax,
    type: 'POST',
    data: data,
    success: (res) => {
      if (res.error) {
        let parent_class = '.sign-in';
        let num = 550;
        step = 50;
        if ($('.sign-in').attr('style') == 'display:none;') parent_class = '.sign-up';
        if (parent_class == '.sign-in') {
          num = 300;
          step = 25;
        }
        $(parent_class + ' .Salert').detach();
        $(parent_class + ' input').removeAttr('style');
        $('.lock').removeAttr('style');
        $('.sign-wrap').css('height', num + 'px');
        for (var key in res.data) {
          if (key == '__all__') $(alertSpan).text(res.data[key]).css('color', '#fff');
          let item = $(parent_class + ' input[name="'+key+'"]');
          if (key == 'password')
            $('.lock').css('top', '45%');
          item.css('border', '2px solid red');
          item.parent().append(`
            <span style="color: #fff; font-size: .8em;" class="Salert"> ` +res.data[key]+  ` </span>
          `);
          num += step;
          $('.sign-wrap').css('height' , num + 'px');
        }
      } else {
        $(alertSpan).text(res.data).css('color', '#fff');
        $('.Salert').detach();
        $('input').removeAttr('style');
        $('.lock').removeAttr('style');
        setTimeout(function (){
          location.href = '/trade_offers';
        }, 500);
      }
    },
    error: (res) => {
      $(alertSpan).text('Нет соединения с сервером').css('color', '#fff');
    }
  });
}

let table_id = '';

function getRequestsList(data) {
  return $.ajax({
    url: '/get_trade_offers',
    type: 'GET',
    data: data,
    beforeSend: () => {
      table_id = $('.slides').attr('data-slider');
      $('#' + table_id).removeClass('active-table');
      $('.preload-wrap').show().css('display', 'flex');
    },
    success: (res) => {
      $('.tr_from_server').detach();
      if (data.neededBids == 'all') {
        requests_obj = {
          active_arr: [],
          planning_arr: [],
          finished_arr: [],
          not_valid: []
        }
        sortBidsByStatus(res);
      } else {
        $.each(res.auctions, function(index) {
          drawTr(res.auctions, index, 'auctions');
        });
        $.each(res.tenders, function(index) {
          drawTr(res.tenders, index, 'tenders');
        });
      }
      if (data.neededBids == 'archive') {
        $('.archive-hidden').hide();
      } else {
        $('.archive-hidden').show();
      }
      if (res.auctions.length < 12 || res.auctions == undefined) {
        $('table#auctions').css('height', 'auto');
      } else {
        $('table#auctions').removeAttr('style');
      }
      if (res.tenders.length < 12 || res.tenders == undefined) {
        $('table#tenders').css('height', 'auto');
      } else {
        $('table#auctions').removeAttr('style');
      }
    },
    error: (res) => {
      console.log(res);
      showAlert('Нет соединения с сервером', '#c23616');
    },
    complete: () => {
      $('#' + table_id).addClass('active-table');
      setTimeout(() => {
        $('.preload-wrap').hide();
      }, 1000);
      getRequestsList_xhr = null;
    }
  });
}

function changeUserParameters(data, flag, refresh) {
  let adress = '/profile/reqs_update';
  let parent_class = '.requisites';
  if (flag) {
    adress = '/profile/update/';
    parent_class = '.profile-changer';
  }
  $.ajax({
    url: adress,
    type: 'POST',
    data: data,
    success: (res) => {
      if (res.error) {
        for (var key in res.data) {
          let item;
          if (key == '__all__') {
            $('.password-alert').text('Пароли не совпадают');
            item = $('input[name="password2"]');
          } else {
            $('.password-alert').text('');
            item = $(parent_class + ' input[name="'+key+'"]');
          }
          item.css('border', '2px solid red');
          item.val('');
          item.attr('placeholder', res.data[key]);
        }
      } else {
        showAlert('Успешно', '#66ab55');
        if (refresh) {
          setTimeout(function(){
            location.reload();
          }, 1000);
        }

      }
    },
    error: (res) => {
      showAlert('Нет соединения с сервером', '#c23616');
    }
  });
}

function createCompany(data) {
  $.ajax({
    url: '/profile/addCompany/',
    type: 'POST',
    data: data,
    success: (res) => {
      $('.Salert').detach();
      if (res.error) {
        for (var key in res.data) {
          let item = $('.create-company input[name="'+key+'"]');
          if (item == undefined) item = $('.create-company select[name="'+key+'"]');
          item.css('border', '2px solid red');
          item.parent().append(`
            <span class="Salert"> ` +res.data[key]+  ` </span>
          `);
        }
      } else {
        showAlert('Успешно', '#66ab55');
      }
    }
  });
}

function joinCompany(invite_code) {
  $.ajax({
    url: '/profile/join/',
    type: 'POST',
    data: invite_code,
    success: (res) => {
      showAlert('Успешно', '#66ab55');
      setTimeout(function () {
        location.reload();
      }, 500);
    }
  });
}

function disableBidSession(data, path) {
  $.ajax({
    url: path,
    type: 'POST',
    data: data,
    success: (res) => {
      if (res.auction_cancel) {
        showAlert(res.message, '#66ab55');
        setTimeout(() => {
            location.href = '/trade_offers';
        }, 1000);
      } else {
        showAlert(res.message, '#c23616');
      }

    },
    error: (res) => {
      showAlert('Сервер временно недоступен', '#c23616');
    }
  });
}

function searchHistory(data) {
  $.ajax({
    url: '/profile/filter/',
    type: 'POST',
    data: data,
    success: (res) => {
      if (res.error === false) {
        $('.history-auctions-wrapper').removeAttr('style');
        $('.date-subtitle').removeAttr('style');
        $('.history-auctions-wrapper').each(function (key, elem){
          for (var i = 0; i < res.data.length; i++) {
            if (res.data[i] == $(elem).attr('data')) {
              $(elem).hide();
            }
          }
        });
        $('.date-subtitle').each(function (key, elem){
          for (var i = 0; i < res.data.length; i++) {
            if (res.data[i] == $(elem).attr('data')) {
              $(elem).hide();
            }
          }
        });
      } else {
        $('.history-auctions-wrapper').hide();
        $('.date-subtitle').hide();
        showAlert(res.data, '#c23616');
      }

    }
  });
}

function sendDataFromTender(data, path) {
  $.ajax({
    url: path,
    type: 'POST',
    data: data,
    success: (res) => {
      if (!res.error && res.data.bets == undefined && res.data != 'Ставка успешно удалена' && res.data != 'ОК') {
        let content = `
          <tr class="biddings_tr_from_server" data-id="`+res.data.id+`" data-is-sale="false">
            <td>`+ new Date(res.data.published_datetime).toLocaleString() +`</td>
            <td>`+ parseInt(res.data.lot_amount).toLocaleString() +`</td>
            <td>`+ parseInt(res.data.total_amount).toLocaleString() +`</td>
            <td class="price_per_tone">`+ parseInt(res.data.bet_price_per_tone).toLocaleString() +`</td>
            <td>`+ parseInt(res.data.total_price).toLocaleString() +`</td>
            <td>
              <a href="/profile/`+res.data.client_id+`" target="_blank">`
                +res.data.client__first_name+` `+ res.data.client__last_name +
              `</a>
            </td>
          </tr>
        `;
        all_bets.push(res.data);
        $(content).insertAfter($('.all_bids_table tbody'));
        addUserPermissions(res.data.id);
        showAlert('Успешно', '#66ab55');
        $('#buy_hover').click();
      } else if (!res.error && res.data.bets != undefined) {
        all_bets = res.data.bets;
        $.each(res.data.bets, (i) => {
          $('.all_bids_table').append(`
            <tr class="biddings_tr_from_server" data-id="`+res.data.bets[i].id+`" data-is-sale="false">
              <td>`+ new Date(res.data.bets[i].published_datetime).toLocaleString() +`</td>
              <td>`+ parseInt(res.data.bets[i].lot_amount).toLocaleString() +`</td>
              <td>`+ parseInt(res.data.bets[i].total_amount).toLocaleString() +`</td>
              <td class="price_per_tone">`+ parseInt(res.data.bets[i].bet_price_per_tone).toLocaleString() +`</td>
              <td>`+ parseInt(res.data.bets[i].total_price).toLocaleString() +`</td>
              <td>
                <a href="/profile/`+res.data.bets[i].client_id+`" target="_blank">`
                  +res.data.bets[i].client__first_name+` `+ res.data.bets[i].client__last_name +
                `</a>
              </td>
            </tr>
          `);
          addUserPermissions(res.data.bets[i].id);
        });
      }
      if (!res.error && res.data.lots_remainder != undefined) $('#free_lots').text('Свободно лотов: ' + res.data.lots_remainder);
      if (!res.error && res.data.deals != undefined) {
        $.each(res.data.deals, (i) => {
          $('.user-bids').append(`
            <tr data-id="`+res.data.deals[i].id+`">
              <td>`+ new Date(res.data.deals[i].published_datetime).toLocaleString() +`</td>
              <td>`+ parseInt(res.data.deals[i].lot_amount).toLocaleString() +`</td>
              <td>`+ parseInt(res.data.deals[i].total_amount).toLocaleString() +`</td>
              <td class="price_per_tone">`+ parseInt(res.data.deals[i].bet_price_per_tone).toLocaleString() +`</td>
              <td>`+ parseInt(res.data.deals[i].total_price).toLocaleString() +`</td>
              <td>
                <a href="/profile/`+res.data.deals[i].client_id+`" target="_blank">`
                  +res.data.deals[i].client__first_name+` `+ res.data.deals[i].client__last_name +
                `</a>
              </td>
            </tr>
          `);
        });
      }
      if (!res.error && res.data == 'Ставка успешно удалена') {
        deleteBet(data.bet_id);
        deleted_bid_id = null;
      }
      if (!res.error && res.data == 'ОК') {
        $('.user-bids').children('tr').detach();
        sendDataFromTender({
          csrfmiddlewaretoken: getCookie('csrftoken'),
          tender_id: $('h2').attr('id')
        }, '/tender/get_bets');
        showAlert('Успешно', '#66ab55');
        $('#buy_hover').click();
        for (var i = 0; i < data.bets.length; i++) {
          deleteBet(data.bets[i]);
        }
      }
      if (res.error) {
        showAlert(res.data, '#c23616');
      }
    },
    error: (res) => {
      showAlert('Сервер временно недоступен', '#c23616');
    }
  });
}


function sendForMoreOptions(data) {
  $.ajax({
    url: '/profile/notifications/types',
    type: 'POST',
    data: data,
    success: (res) => {
      $('#notifications_closer').click();
    },
    error: (res) => { showAlert('Сервер временно недоступен', '#c23616'); }
  });
}

function changeTemplateName(data, list, flag) {
  $.ajax({
    url: '/get_trade_offer_info',
    type: 'POST',
    data: data,
    success: (res) => {
      console.log(res);
      if (res.trade_offer != undefined) {
        for (var key in res.trade_offer) {
          $(list).children('span[data-request="'+key+'"]').text(res.trade_offer[key]);
        }
      }
      if (flag) {
        if (res.allowed_companys_info != undefined && res.allowed_companys_info.length > 0) {
          white_list = [];
          for (var i = 0; i < res.allowed_companys_info.length; i++) {
            res.allowed_companys_info[i]
            white_list.push({
              company_id: i,
              inn: res.allowed_companys_info[i].company_inn,
              name: res.allowed_companys_info[i].company_short_name,
              is_checked: true,
              data_base_id: res.allowed_companys_info[i].company_id
            });
            $('div[data-opening-name="companys-list"]').children('label').detach();
            $('div[data-opening-name="companys-list"]').append(`
              <label class="companys-list active-label" data-id="`+i+`">
                <div class="first">
                  <span>ИНН компании:</span>
                  <input type="text" placeholder="Введите инн компании" class="company_inn" value="`+res.allowed_companys_info[i].company_inn+`">
                </div>
                <div class="second">
                  <span>Название компании:</span>
                  <span class="company-name def_company">`+res.allowed_companys_info[i].company_short_name+`</span>
                </div>
                <div class="third">
                  <button type="button" name="button" class="check_company">Проверить</button>
                  <button type="button" name="button" class="delete_company">Удалить</button>
                </div>
              </label>
            `);
          }
        }
        let fields = $(list).children('span');
        console.log(fields);
        for (var i = 0; i < fields.length; i++) {
          if ($(fields[i]).text() != '') {
            console.log($(fields[i]).attr('data-name'));
            if ($('input[name="'+$(fields[i]).attr('data-name')+'"]').length != 0) {
              if ($('input[name="'+$(fields[i]).attr('data-name')+'"]').attr('id') == 'polymer-input') {
                $('.div-option[data-value="'+$(fields[i]).text()+'"]').click();
              } else
                $('input[name="'+$(fields[i]).attr('data-name')+'"]').val($(fields[i]).text());
            } else if ($('select[name="'+$(fields[i]).attr('data-name')+'"]').length != 0)
                $('select[name="'+$(fields[i]).attr('data-name')+'"]').val($(fields[i]).text());
          }
        }
        if (res.trade_offer.is_apply_for_participation == true) {
          $('input[name="is_apply_for_participation"]').click();
        }
        $('select[name="type"]').change();
        $('select[name="level"]').change();
        is_rename = false;
      } else {
        if (res.rename_trade_offer == true)
          showAlert('Названия шаблона успешно изменено', '#66ab55');
        else
          showAlert('Некоректное название', '#c23616');
      }
    },
    error: (res) => { showAlert('Сервер временно недоступен', '#c23616'); }
  });
}

function checkCompanyINN(data, index, elem) {
  $.ajax({
    url: '/check_company',
    type: 'POST',
    data: data,
    success: (res) => {
      if ($(elem).parent().siblings('.second').children('.company-name').hasClass('undefined_company'))
        $(elem).parent().siblings('.second').children('.company-name').removeClass('undefined_company');
      else if ($(elem).parent().siblings('.second').children('.company-name').hasClass('def_company'))
        $(elem).parent().siblings('.second').children('.company-name').removeClass('def_company');
      let result;
      let res_class;
      let flag = true;
      if (res.company_exist === false) {
        result = 'Не существует';
        white_list[index].is_checked = false;
        res_class = 'undefined_company';
      } else if (res.company_short_name) {
        result = res.company_short_name;
        res_class = 'def_company';
        white_list[index].data_base_id = res.company_id;
        white_list[index].is_checked = true;
      }
      white_list[index].name = result;
      $(elem).parent().siblings('.second').children('.company-name').text(result).addClass(res_class);
    },
    error: (res) => {
      showAlert('Сервер временно недоступен', '#c23616');
      white_list[index].name = 'Неизвестно';
      $(elem).parent().siblings('.second').children('.company-name').text('Неизвестно');
    }
  });
}

function sendRequestForPlaying(data, path, flag) {
  $.ajax({
    url: path,
    type: 'POST',
    data: data,
    success: (res) => {
      if (res.application_accepted) {
        showAlert('Успешно');
        if (flag) {
          setTimeout(()=>{
            location.reload();
          }, 1000);
        } else {
          $('li[data-company-id="'+data.company_id+'"]').detach();
          if (path.substr(0,2) == '/t') {
            getRequestsLists({
              csrfmiddlewaretoken: getCookie('csrftoken'),
              tender_id: $('h2').attr('id')
            });
          } else {
            getRequestsLists({
              csrfmiddlewaretoken: getCookie('csrftoken'),
              auction_id: $('h2').attr('id')
            });
          }
        }
      } else
        showAlert('Что-то пошло не так', '#c23616');
    },
    error: (res) => {
      showAlert('Сервер временно недоступен', '#c23616');
    }
  });
}

function getRequestsLists(data) {
  let path = '/tender/participation_orders';
  if (data.auction_id != undefined)
    path = '/EXAMPLE_AUCTION/participation_orders';
  $.ajax({
    url: path,
    type: 'POST',
    data: data,
    success: (res) => {
      for (var i = 0; i < list_array.length; i++) {
        if (list_array[i].requests.length > 0) list_array[i].requests = [];
      }
      for (var i = 0; i < res.participation_orders.length; i++) {
        if (res.participation_orders[i].participation_status_id == 2)
          list_array[1].requests.push(res.participation_orders[i]);
        else if (res.participation_orders[i].participation_status_id == 1)
          list_array[2].requests.push(res.participation_orders[i]);
        else
          list_array[0].requests.push(res.participation_orders[i]);
      }
      if (list_array[1].requests.length > 0) {
        for (var i = 0; i < list_array[1].requests.length; i++) {
          drawRequest(list_array[1].requests[i]);
        }
      } else {
        drawEmptyTitle();
      }
    },
    error: (res) => {
      showAlert('Сервер временно недоступен', '#c23616');
    }
  });
}
