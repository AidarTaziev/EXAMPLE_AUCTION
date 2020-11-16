function toggleColor(elem, enemy, enemy_sec) {
  $(enemy).children('span').removeClass('active');
  $(enemy_sec).children('span').removeClass('active');
  $(elem).children('span').addClass('active');
}

function doDate(time) {
  let hours = parseInt(time.substr(0,3)) * 60;
  let mins = parseInt(time.substr(3,6));
  return hours + mins;
}

function getFormData(form){
  var ser_object = form.serializeArray();
  var res_object = {};

  $.map(ser_object, function(n, i){
      res_object[n['name']] = n['value'];
  });

  return res_object;
}

function dateToString(date) {
  let f_substr = date.substr(0, date.indexOf('-'));
  let s_substr = new Date().getFullYear();
  date = date.replace(s_substr, f_substr);
  date = date.replace(f_substr, s_substr);
  return date;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function drawTr(res, index, table_name) {
  let class_tr = '';
  let offset = new Date().getTimezoneOffset() / 60;
  if (localStorage.getItem('table_rows_size') === 'small') class_tr = 'small-active';
  else if (localStorage.getItem('table_rows_size') === 'medium') class_tr = 'medium-active';
  let hrs = parseInt(res[index].start_bidding.substr(0,2)) + offset;
  let obj = res[index];
  let path = 'EXAMPLE_AUCTION/properties/';
  for (var key in obj) {
    if (obj[key] == null) obj[key] = '-';
  }
  if (obj.start_price_per_tone == undefined) {
    obj.min_price_per_tone = obj.recommended_price;
    path = 'tender/property/';
  }
  $('#' + table_name).append(`
    <tr class="tr_from_server `+ class_tr +`">
        <td><a href="`+ path +``+ res[index].id +`">`+ res[index].id +`</a></td>
        <td>`+ obj.type +`<br>(Продажа)</td>
        <td>`+ obj.polymer + `</td>
        <td>`+ obj.seller__company_short_name + `</td>
        <td>`+ obj.total_amount +`</td>
        <td class="archive-hidden">`+ obj.start_price_per_tone +`</td>
        <td>`+ obj.payment_term__name +`</td>
        <td>`+ obj.storage_location +`</td>
        <td>`+ obj.start_bidding +`</td>
        <td>`+ obj.end_bidding +`</td>
    </tr>
  `);
}

function sortBidsByStatus(obj) {
  $.each(obj.auctions, function(index, el) {
    if (el.status == 'finished')
      requests_obj.finished_arr.push(el);
    else if (el.status == 'active')
      requests_obj.active_arr.push(el);
    else if (el.status == 'planning')
      requests_obj.planning_arr.push(el);
    else if (el.status == 'finished_today')
      requests_obj.not_valid.push(el);
  });
  for (var item in requests_obj) {
    for (var i = 0; i < requests_obj[item].length; i++) {
      drawTr(requests_obj[item], i, 'auctions');
    }
  }
}

function showAlert(message, color) {
  // $('#accept-wrap').removeClass('alert-active');
  // $('#accept-wrap .alert-frame').removeClass('active');
  // $('.alert-wrap .hover').hide();
  // $('#alert-wrap').removeClass('alert-active');
  // $('#alert-wrap .alert-frame').removeClass('active');
  $('#alert-wrap .alert-frame').children('h2').text(message).css('color', color);
  $('#alert-wrap').addClass('alert-active');
  $('#alert-wrap .alert-frame').addClass('active');
  $('.alert-wrap .hover').show();
  console.log($('#alert-wrap'));

  setTimeout(function (){
    $('.alert-wrap .hover').hide();
    $('#alert-wrap').removeClass('alert-active');
    $('#alert-wrap .alert-frame').removeClass('active');
  }, 1500);
}

function toDateInputValue(date) {
  var local = new Date(date);
  local.setMinutes(date.getMinutes() - date.getTimezoneOffset());
  return local.toJSON().slice(0,10);
}

function changeRequestsChecker(elem, flag) {
  console.log(flag);
  $('#check-label-my').attr('data-bool', flag);
  $(elem).addClass('active-check-label');
  if (elem == '#check-label-my')
    $('#check-label-all').removeClass('active-check-label');
  else
    $('#check-label-my').removeClass('active-check-label');
  localStorage.setItem('show_my_auctions', flag);
}

function loadRowsSizes() {
  if (localStorage.getItem('table_rows_size') != undefined || localStorage.getItem('table_rows_size') != null)
    $('.' + localStorage.getItem('table_rows_size')).children('span').addClass('active');
  else
    $('.large').children('span').addClass('active');
}

function isChecked(checkbox) {
  if (checkbox.prop('checked')) return true;
  else return false;
}

function addUserPermissions(id) {
  if (is_seller == 'seller') {
    $('tr[data-id="' + id + '"]').append(`
      <td><input type="checkbox" class="check-for-sale"></td>
    `);
  } else {
    $('tr[data-id="' + id + '"]').children('td.price_per_tone').append(`
      <button type="button" class="upper deleter"><div></div></button>
    `);
  }
}

function searchCompanybyId(id) {
  let k = 0;
  for (var i = 0; i < white_list.length; i++) {
    if (white_list[i].company_id == parseInt(id)) k = i;
  }
  return k;
}

function replaceAt(str, index, symbol) {
    if(index > str.length-1) return str;
    return str.substr(0,index) + symbol + str.substr(index+1);
}

function setCookie(name, value, props) {

    props = props || {};

    var exp = props.expires;

    if (typeof exp == "number" && exp) {

        var d = new Date();

        d.setTime(d.getTime() + exp*1000);

        exp = props.expires = d;

    }

    if(exp && exp.toUTCString) { props.expires = exp.toUTCString(); }

    value = encodeURIComponent(value);

    var updatedCookie = name + "=" + value;

    for(var propName in props){

        updatedCookie += "; " + propName;

        var propValue = props[propName];

        if(propValue !== true){ updatedCookie += "=" + propValue; }
    }

    document.cookie = updatedCookie;

}

// удаляет cookie
function deleteCookie(name) {

    setCookie(name, null, { expires: -1 })

}

function deleteBasis(elem) {
  let index = $(elem).parent().parent().attr('data-index');
  basis_list.splice(parseInt(index), 1);
  $(elem).parent().parent().detach();
  $('.basis-count').text(basis_list.length);
}

function tableToExcel(table, name, fileName) {
  var link = document.createElement("a");
  var uri = 'data:application/vnd.ms-excel;base64,'
  , template = `<html xmlns:x="urn:schemas-microsoft-com:office:excel">
                  <head>
                    <xml>
                      <x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>
                      <x:Name>Test Sheet</x:Name>
                      <x:WorksheetOptions><x:Panes></x:Panes></x:WorksheetOptions></x:ExcelWorksheet>
                      </x:ExcelWorksheets></x:ExcelWorkbook>
                    </xml>
                  </head>
                  <body>
                  <table>
                    {table}
                  </table>
                  </body>
                </html>
    `
  , base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }
  , format = function(s, c) {
    return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; })
  }
  , downloadURI = function(uri, name) {
      link.download = name;
      link.href = uri;
      link.click();
  }

  if (!table.nodeType) table = document.getElementById(table);
  var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
  var resuri = uri + base64(format(template, ctx));
  var blob = new Blob([format(template, ctx)], {type: 'application/csv;charset=utf-8;'});



  if (navigator.userAgent.search("Edge") != -1) { // IE
    navigator.msSaveOrOpenBlob(blob, fileName)
  } else if (navigator.userAgent.search("Firefox") !== -1) { // Firefox
    $(link).css({display: 'none'});
    $('body').append(link);

    $(link).attr({
      href: resuri,
      target: '_blank',
      download: fileName
    })[0].click();

    $(link).remove();
  } else { // Chrome
    $(link).attr({
      href: resuri,
      target: '_blank',
      download: fileName
    })[0].click();
  }


  // downloadURI(resuri, fileName);
};

function deleteFromArr(elem, arr) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].id == elem) {
      arr.splice(i, 1);
    }
  }
  return arr;
}

function checkForEmptyBox(box, id) {
  let checkers = $('.hidden-list[data-idx="'+id+'"]').children('.row').children('input');
  console.log(checkers);
  let k = 0;
  for (let i = 0; i < checkers.length; i++) {
    console.log($(checkers[i]));
    if (isChecked($(checkers[i])))
      k++;
  }
  console.log(k);
  if (isChecked($(box)) && k < checkers.length) {
    $(box).prop('checked', false);
  } else if (!isChecked($(box)) && k == checkers.length) {
    $(box).prop('checked', true);
  }
}
