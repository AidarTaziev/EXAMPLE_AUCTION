let patternObj = [
  {
    name: 'username',
    pattern: /^.+?/,
    valid: false
  },
  {
    name: 'password1',
    pattern: /^.+?/,
    valid: false
  },
  {
    name: 'password2',
    pattern: /^.+?/,
    valid: false
  },
  {
    name: 'first_name',
    pattern: /^[а-яА-ЯёЁa-zA-Z]{1,32}$/,
    valid: false
  },
  {
    name: 'last_name',
    pattern: /^[а-яА-ЯёЁa-zA-Z]{1,32}$/,
    valid: false
  },
  {
    name: 'email',
    pattern: /^.+?/,
    valid: false
  }
  // {
  //   name: 'contact_phone',
  //   pattern: /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/,
  //   valid: false
  // },
  // {
  //   name: 'contact_email',
  //   pattern: /^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$/,
  //   valid: false
  // }
];

$('.sign-up input').on('input' , function (){
  let i = 0;
  if ($(this).attr('style') == 'border: 2px solid red;') {
    $(this).siblings('.Salert').detach();
    console.log($(this).siblings('.Salert').text());
    $(this).removeAttr('style');
  }
  $.each(patternObj, (index) => {
    if (patternObj[index].name == $(this).attr('name')) {
      i = index;
    }
  });
  validate(this, i);
});

$('input[name="password2"]').on('input', function () {
  comparePass(this, 1);
});

$('input[name="password1"]').on('input', function () {
  comparePass(this, 2);
});

function validate(elem, index) {
	if (patternObj[index].pattern.test($(elem).val())) {
    $(elem).removeAttr('style');
    patternObj[index].valid = true;
    $(elem).css('background-color', '#fff');
	}
	else {
    $(elem).removeAttr('style');
		$(elem).css('border' , '1px solid #c23616');
    patternObj[index].valid = false;
	}

  let j = 0;
  $.each(patternObj, function (i) {
    if (patternObj[i].valid) {
      j++;

    }
    if (j == patternObj.length) {
      console.log('yeah');
      $('.sign-btn').removeAttr('disabled');
      $('.sign-btn').removeClass('disabled-btn');
    } else {
      $('.sign-btn').attr('disabled', 'disable');
      $('.sign-btn').addClass('disabled-btn');
    }
  });
}

function comparePass(elem, index) {
  if ($(elem).val() != $('input[name="password' + index + '"]').val()) {
    patternObj[index].valid = false;
    console.log($('.password' + index).val());
    $('.alert-span-sign').text('Пароли не совпадают');
  } else {
    patternObj[index].valid = true;
    console.log(true);
    $('.alert-span-sign').text('');
  }
  let i = 1;
  index == 2 ? i = 1 : i = 2;
  validate(elem, i);
}
