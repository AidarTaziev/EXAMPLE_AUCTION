let list_array = [
  {
    index: 0,
    title: 'Список отклоненных заявок',
    requests: []
  },
  {
    index: 1,
    title: 'Список заявок на участие',
    requests: []
  },
  {
    index: 2,
    title: 'Список принятых заявок',
    requests: []
  }
];

$('document').ready(function (){

  if ($('h2').attr('data-type') == 'tender') {
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

});

$('#prev_block').click(function() {
  //Переключает список заявок назад
  slideList($(this), 'prev');
});

$('#next_block').click(function(){
  //Переключает список заявок вперед
  slideList($(this), 'next');
});

$('.requests-list').on('click', '.accept-request', function (){
  doDataForRequest($(this), 'Допущен');
});

$('.requests-list').on('click', '.disaccept-request', function() {
  doDataForRequest($(this), 'Отклонен');
});

function doDataForRequest(elem, status) {
  let data = {
    csrfmiddlewaretoken: getCookie('csrftoken'),
    auction_id: $('h2').attr('id'),
    company_id: $(elem).parent().parent().attr('data-company-id'),
    participation_status: status
  };
  let path = $('h2').attr('data-path');
  if ($('h2').attr('data-type') == 'tender') {
    delete data.auction_id;
    data.tender_id = $('h2').attr('id');
  }
  sendRequestForPlaying(data, path, false);
}

function slideList(elem, direction) {
  let title = $(elem).siblings('h2');
  let k = parseInt(title.attr('data-index'));
  if (direction == 'next') k++;
  else k--;
  if (k < 0) k = list_array.length - 1;
  else if (k > list_array.length - 1) k = 0;
  changeTitleText(title, k, direction);
  $('.requests-list').children('li').detach();
  if (list_array[k].requests.length > 0) {
    $('.empty-list').detach();
    for (var i = 0; i < list_array[k].requests.length; i++) {
      drawRequest(list_array[k].requests[i]);
    }
  } else {
    drawEmptyTitle();
  }
}

function changeTitleText(title, index, dir) {
  let moove_dist = '-15deg';
  if (dir == 'next') moove_dist = '15deg';
  title.css('transform', 'scale(0) rotate('+moove_dist+')');
  title.text(list_array[index].title);
  title.attr('data-index', index);
    setTimeout(() => {
      title.css('transform', 'scale(1)');
    }, 220);
}

function drawEmptyTitle() {
  $('.empty-list').detach();
  $('.requests-list').append(`
    <h2 class="empty-list">Список пуст</h2>
  `);
  setTimeout(() => {
    $('.empty-list').addClass('empty-list-active');
  },0);
}

function drawRequest(request) {
  let template = `
    <li class="list-item" data-company-id="`+ request.company_id +`">
        <a href="/profile/company/`+ request.company_id +`">`+ request.company_short_name +`</a>
        <div class="btn-wrap">
          <button type="button" name="button" class="accept-request">✔</button>
          <button type="button" name="button" class="disaccept-request">X</button>
        </div>
    </li>
  `;
  $('.requests-list').append(template);
  setTimeout(() => {
    $('li[data-company-id="'+request.company_id+'"]').addClass('list-item-active');
  }, 0);
}
