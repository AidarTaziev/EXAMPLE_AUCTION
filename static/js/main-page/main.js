$(document).ready(() => {
  console.log($('div[data-preload]').attr('data-preload'));
  if ($('div[data-preload]').attr('data-preload') == undefined) {
    setTimeout(() => {
      $('.preload-wrap').hide();
    }, 1000);
  }
  if ((new URL(document.location)).searchParams.get('lang') !== 'ru') {
      $('.ruLang').show();
  }
});

$('.profile-image').click(function () {
    let names = ['sber', 'man', 'menu'];
    let name = $(this).attr('data-id');
    for (let i in names) {
      if (name != names[i]) {
        $('div[data-id="'+names[i]+'"]').siblings('.profile-list').slideUp('slow');
        $('div[data-id="'+names[i]+'"]').parent().addClass('hide-list');
        $('img[data-id="'+names[i]+'"]').siblings('.profile-list').slideUp('slow');
        $('img[data-id="'+names[i]+'"]').parent().addClass('hide-list');
      }
    }
    $(this).siblings('.profile-list').slideToggle('slow').css('display', 'flex');
    $(this).siblings('.mobile-menu-close').toggleClass('active-closer');
});

$('.mobile-menu-close').click(function () {
    $('.profile-list').slideUp('slow');
    $(this).removeClass('active-closer');
    setTimeout(function () {
        $('div[data-id="man"]').parent().removeClass('hide-list');
        $('img[data-id="menu"]').parent().removeClass('hide-list');
        $('div[data-id="sber"]').parent().removeClass('hide-list');
    }, 500);
});

$('.profile-item').click(function () {
    let link = $(this).children('a').attr('href');
    if (link != undefined)
      location.href = link;
});

$('#open_sber').click((e) => {
  e.preventDefault();
  $('.modal-wrap').addClass('active-wrap');
	$('.mobile-menu-close').click();
});

$('#sberbank').submit(function(e) {
  e.preventDefault();
  let data = getFormData($(this));
  data.csrfmiddlewaretoken = getCookie('csrftoken');
  data.order_url = location.href;
  getSberBankLink(data);
});

$('.close-modal').click(() => {
  $('.modal-wrap').removeClass('active-wrap');
});

$('.modal-wrap .hover').click(() => {
  $('.modal-wrap').removeClass('active-wrap');
});

$('.sberbank-button').click(function (){
	if ($(this).attr('href') != undefined && $(this).attr('href') != null)
		location.href = $(this).attr('href');
});

$('.excel-download').click(function () {
	let table = $(this).attr('data-table');
	let name = $(this).attr('data-name');
	let fileName = $(this).attr('data-file');
  tableToExcel(table, name, fileName);
});
