let requests_obj = {
	active_arr: [],
	planning_arr: [],
	finished_arr: [],
	not_valid: []
}

$(document).ready(function (){
	// работа с хранилищем данных браузера на странице списка торгов
   if (true) {
     if (localStorage.getItem('request-type-name') == 'tenders') {
       $('.request-type-wrap h2:nth-child(2)').click();
     }
     let storage_data = {
       neededBids: localStorage.getItem('needed_requests'),
       polymer_shortcode: localStorage.getItem('polymer_shortcode'),
       polymer_type: localStorage.getItem('polymer_type'),
       polymer_plant: localStorage.getItem('polymer_plant'),
       show_my_auctions: localStorage.getItem('show_my_auctions')
     }
     if (storage_data.polymer_shortcode != undefined) $('input[name="polymer_shortcode"]').val(storage_data.polymer_shortcode);
     if (storage_data.polymer_type != undefined) $('select[name="polymer_type"]').val(storage_data.polymer_type);
     if (storage_data.polymer_plant != undefined) $('select[name="polymer_plant"]').val(storage_data.polymer_plant);
     if (storage_data.show_my_auctions != undefined) {
       if (storage_data.show_my_auctions === 'true') {
         changeRequestsChecker('#check-label-my', true);
       } else if (storage_data.show_my_auctions === 'false') {
         changeRequestsChecker('#check-label-all', false);
       }
     }
     if (storage_data.neededBids != undefined && storage_data.neededBids != '') {
       neededBid = storage_data.neededBids;
       getRequestsList(storage_data);
       $('span[data-id="'+storage_data.neededBids+'"]').addClass('active');
       $('.choosen-title span').text($('span[data-id="'+storage_data.neededBids+'"]').text() + ' торги');
     } else {
       getRequestsList({
        neededBids: neededBid,
        polymer_shortcode: null,
        polymer_type: null,
        polymer_plant: null,

      });
      $('span[data-id="active"]').addClass('active');
     }
     loadRowsSizes();
  }
});

// Переадресация по клику на строку таблицы
$('table').on('click', 'tr', function (){
  let link = $(this).children('td').eq(0).children('a').attr('href');
  if (link) {
    window.open(link, '_blank');
  }
});

$('.titles span').click(function (){
  let title = $(this).text();
  let data = {
    neededBids: '',
    polymer_shortcode: $('input[name="polymer_shortcode"]').val(),
    polymer_type: $('select[name="polymer_type"]').val(),
    polymer_plant: $('select[name="polymer_plant"]').val(),
    show_my_auctions: $('#check-label-my').attr('data-bool')
  };
  localStorage.setItem('polymer_shortcode', data.polymer_shortcode);
  localStorage.setItem('polymer_type', data.polymer_type);
  localStorage.setItem('polymer_plant', data.polymer_plant);
  localStorage.setItem('show_my_auctions', data.show_my_auctions);
  if (title == 'Активные') {
    neededBid = 'active';
  } else if (title == 'Планируемые') {
    neededBid = 'unactive';
  } else if (title == 'Текущие') {
    neededBid = 'all';
  } else {
    neededBid = 'archive';
  }
  data.neededBids = neededBid;
  localStorage.setItem('needed_requests', data.neededBids);
  if (getRequestsList_xhr)
    getRequestsList_xhr.abort();
  else
    getRequestsList_xhr = getRequestsList(data);
  $('.titles span.active').removeClass('active');
  $(this).addClass('active');
  $('.choosen-title span').text(title + ' торги');
  $('.choosen-title').click();
});

$('.choosen-title').click(function () {
  $('.titles').slideToggle('fast');
  $(this).children('img').toggleClass('rotated');
});

$('.search').submit((e) => {
  let data = {
    neededBids: neededBid,
    polymer_shortcode: $('input[name="polymer_shortcode"]').val(),
    polymer_type: $('select[name="polymer_type"]').val(),
    polymer_plant: $('select[name="polymer_plant"]').val(),
    show_my_auctions: $('#check-label-my').attr('data-bool')
  };
  if ((data.polymer_type != undefined) && (data.polymer_plant != undefined) && (data.polymer_shortcode != undefined)) {
    getRequestsList(data);
    localStorage.setItem('needed_requests', data.neededBids);
    localStorage.setItem('polymer_shortcode', data.polymer_shortcode);
    localStorage.setItem('polymer_type', data.polymer_type);
    localStorage.setItem('polymer_plant', data.polymer_plant);
    localStorage.setItem('show_my_auctions', data.show_my_auctions);
  }
  e.preventDefault();
});

$('#search_opener').click(function (){
  $('#search_input').toggleClass('active-input');
  $(this).toggleClass('close-search');
  if ($(this).attr('class')) {
    $('#search_input').val('');
  }
  let field = $(this).siblings('div').children('input');
  let list = $(this).siblings('div').children('select');
  let text = $(this).siblings('div').children('label');
  let box_children = $(this).siblings('div').children('.check-wrap').children();
  if (field.attr('style') == 'display: inline-block;') {
    field.removeAttr('style');
    list.removeAttr('style');
    text.removeAttr('style');
    box_children.removeAttr('style');
  } else {
    setTimeout(function (){
      field.toggle();
      list.toggle();
      text.toggle();
      box_children.toggle();
    }, 300);
  }
});

$('.request-type-wrap h2').click(function (){
  let name = $(this).attr('data-slider');
  localStorage.setItem('request-type-name', name);
  $(this).removeClass('unactive-title');
  $(this).siblings('h2').addClass('unactive-title');
  $('#' + name).addClass('active-table');
  $('#' + name).siblings('table').removeClass('active-table');
});

$('#check-label-my').click(function(){
  changeRequestsChecker('#check-label-my', true);
});

$('#check-label-all').click(function(){
  changeRequestsChecker('#check-label-all', false);
});
