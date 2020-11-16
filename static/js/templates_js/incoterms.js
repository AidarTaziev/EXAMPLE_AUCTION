$('document').ready(() => {
  $('.incoterms-container').css('height' , $('.main-inc').css('height'));
}); //Расчет высоты страницы

var sprav = [
  {
    name: 'EXW',
    desc: [
      `Термин "Франко завод" означает, что продавец считается выполнившим свои обязанности по поставке,
       когда он предоставит товар в распоряжение покупателя на своем предприятии или в другом названном месте
        (например: на заводе, фабрике, складе и т.п.). Продавец не отвечает за погрузку товара на транспортное средство,
         а также за таможенную очистку товара для экспорта.`,
      `Данный термин возлагает, таким образом, минимальные обязанности на продавца, и покупатель должен нести все расходы и риски в связи
       с перевозкой товара от предприятия продавца к месту назначения. Однако, если стороны желают, чтобы продавец взял на себя
        обязанности по погрузке товара на месте отправки и нес все риски и расходы за такую отгрузку, то это должно быть четко оговорено
         в соответствующем дополнении к договору купли-продажи.3 Этот термин не может применяться, когда покупатель не в состоянии выполнить
          прямо или косвенно экспортные формальности. В этом случае должен использоваться термин FCA, при условии, что продавец
           согласится нести расходы и риски за отгрузку товара.`
    ],
    subtitle: '- Франко завод/склад'
  },
  {
    name: 'FCA',
    desc: [
      `Термин "Франко перевозчик" означает, что продавец доставит прошедший таможенную очистку товар указанному покупателем перевозчику до названного места.
      Следует отметить, что выбор места поставки повлияет на обязательства по погрузке и разгрузке товара на данном месте.
      Если поставка осуществляется в помещении продавца, то продавец несет ответственность за отгрузку.
      Если же поставка осуществляется в другое место, продавец за отгрузку товара ответственности не несет.`,
      `Данный термин может быть использован при перевозке любым видом транспорта, включая смешанные перевозки.`,
      `Под словом "Перевозчик" понимается любое лицо, которое на основании договора перевозки обязуется осуществить или обеспечить перевозку товара по железной дороге,
       автомобильным, воздушным, морским и внутренним водным транспортом или комбинацией этих видов транспорта.
      Если покупатель доверяет другому лицу, не являющемуся перевозчиком, принять товар, то продавец считается выполнившим свои обязанности по поставке товара с момента передачи его данному лицу.`
    ],
    subtitle: '- Франко перевозчик'
  },
  {
    name: 'FAS',
    desc: [
      `Термин "Франко вдоль борта судна" означает, что продавец выполнил поставку, когда товар размещен вдоль
       борта судна на причале или на лихтерах в указанном порту отгрузки.
       Это означает, что с этого момента все расходы и риски потери или повреждения товара должен нести покупатель.
        По условиям термина FAS на продавца возлагается обязанность по таможенной очистке товара для экспорта.
         ЭТИМ ДАННОЕ ИЗДАНИЕ ОТЛИЧАЕТСЯ ОТ ПРЕДЫДУЩИХ ИЗДАНИЙ "ИНКОТЕРМС",
       В КОТОРЫХ ОБЯЗАННОСТЬ ПО ТАМОЖЕННОЙ ОЧИСТКЕ ДЛЯ ЭКСПОРТА ВОЗЛАГАЛАСЬ НА ПОКУПАТЕЛЯ. Однако, если стороны желают,
        чтобы покупатель взял на себя обязанности по таможенной очистке товара для экспорта, то это должно быть четко оговорено в
         соответствующем дополнении к договору купли-продажи. `,
      `Данный термин может применяться только при перевозке товара морским или внутренним водным транспортом.`
    ],
    subtitle: '- Франко вдоль борта судна'
  },
  {
    name: 'FOB',
    desc: [
      `Термин "Франко борт" означает, что продавец выполнил поставку, когда товар перешел через поручни судна в названном
       порту отгрузки. Это означает, что с этого момента все расходы и риски потери или повреждения товара должен нести покупатель.
        По условиям термина FOB на продавца возлагается обязанность по таможенной очистке товара для экспорта.
         Данный термин может применяться только при перевозке товара морским или внутренним водным транспортом.
          Если стороны не собираются поставить товар через поручни судна, следует применять термин FCA.`
    ],
    subtitle: '- Франко борт'
  },
  {
    name: 'CFR',
    desc: [
      `Термин "Стоимость и фрахт" означает, что продавец выполнил поставку, когда товар перешел через поручни судна
       в порту отгрузки. `,
      `Продавец обязан оплатить расходы и фрахт, необходимые для доставки товара в названный порт назначения,
       ОДНАКО, риск потери или повреждения товара, а также любые дополнительные расходы, возникающие после отгрузки товара,
        переходят с продавца на покупателя. `,
      `По условиям термина CFR на продавца возлагается обязанность по таможенной очистке товара для экспорта.`,
      `Данный термин может применяться только при перевозке товара морским или внутренним водным транспортом.
       Если стороны не собираются поставить товар через поручни судна, следует применять термин CPT.`
    ],
    subtitle: '- Стоимость и фрахт'
  },
  {
    name: 'CIF',
    desc: [
      `Термин "Стоимость, страхование и фрахт" означает, что продавец выполнил поставку, когда товар перешел через поручни
       судна в порту отгрузки. Продавец обязан оплатить расходы и фрахт, необходимые для доставки товара в указанный порт
        назначения, НО риск потери или повреждения товара, как и любые дополнительные расходы, возникающие после отгрузки товара,
         переходят с продавца на покупателя.`,
      `Однако, по условиям термина CIF на продавца возлагается также обязанность приобретения морского страхования в пользу
       покупателя против риска потери и повреждения товара во время перевозки.`,
      `Следовательно, продавец обязан заключить договор страхования и оплатить страховые взносы.
       Покупатель должен принимать во внимание, что согласно условиям термина CIF, от продавца требуется обеспечение страхования
        лишь с минимальным покрытием. В случае, если покупатель желает иметь страхование с большим покрытием,
         он должен либо специально договориться об этом с продавцом, либо сам принять меры по заключению дополнительного
          страхования. `,
      `По условиям термина CIF не продавца возлагается обязанность по таможенной очистке товара для экспорта.
      Данный термин может применяться только при перевозке товара морским или внутренним водным транспортом.
      Если стороны не собираются поставить товар через поручни судна, следует применять термин CIP.`
    ],
    subtitle: '- Стоимость, страхование и фрахт'
  },
  {
    name: 'CPT',
    desc: [
      `Термин "Фрахт/перевозка оплачены до" означает, что продавец доставит товар названному им перевозчику.
       Кроме этого, продавец обязан оплатить расходы, связанные с перевозкой товара до названного пункта назначения.
        Это означает, что покупатель берет на себя все риски потери или повреждения товара, как и другие расходы после
         передачи товара перевозчику. `,
      `Под словом "перевозчик" понимается любое лицо, которое на основании договора перевозки берет на себя обязательство
       обеспечить самому или организовать перевозку товара по железной дороге, автомобильным, воздушным, морским и
        внутренним водным транспортом или комбинацией этих видов транспорта.`,
      `В случае осуществления перевозки в согласованный пункт назначения несколькими перевозчиками,
       переход риска произойдет в момент передачи товара в попечение первого из них.`,
      `По условиям термина СРТ на продавца возлагается обязанность по таможенной очистке товара для экспорта.
      Данный термин может применяться при перевозке товара любым видом транспорта, включая смешенные перевозки.`
    ],
    subtitle: '- Фрахт/перевозка оплачены до'
  },
  {
    name: 'CIP',
    desc: [
      `Термин "Фрахт/перевозка и страхование оплачены до" означает, что продавец доставит товар названному им перевозчику.
       Кроме этого, продавец обязан оплатить расходы, связанные с перевозкой товара до названного пункта назначения.
        Это означает, что покупатель берет на себя все риски и любые дополнительные расходы до доставки таким образом товара.
         Однако, по условиям CIP на продавца также возлагается обязанность по обеспечению страхования от рисков потери и
          повреждения товара во время перевозки в пользу покупателя. Следовательно, продавец заключает договор страхования и
           оплачивает страховые взносы. Покупатель должен принимать во внимание, что согласно условиям термина CIP от продавца
            требуется обеспечение страхования с минимальным покрытием.`,
      `В случае, если покупатель желает иметь страхование с большим покрытием, он должен либо специально договориться
       об этом с продавцом, либо сам принять меры по заключению дополнительного страхования. `,
      `Под словом "перевозчик" понимается любое лицо, которое на основании договора перевозки берет на себя обязательство
       обеспечить самому или организовать перевозку товара по железной дороге, автомобильным, воздушным, морским и внутренним
        водным транспортом или комбинацией этих видов транспорта.`,
      `В случае осуществления перевозки в пункт назначения несколькими перевозчиками, переход риска произойдет в момент передачи
       товара в попечение первого перевозчика.`,
       `По условиям термина СIР на продавца возлагается обязанность по таможенной очистке товара для экспорта.
       Данный термин может применяться при перевозке товара любым видом транспорта, включая смешенные перевозки.`
    ],
    subtitle: '- Фрахт/перевозка и страхование оплачены до'
  },
  {
    name: 'DAP',
    desc: [
      `Термин "Поставка в пункте" означает, что продавец выполнил поставку, когда он предоставил неразгруженный товар,
       прошедший таможенную очистку для экспорта, но еще не для импорта на прибывшем транспортном средстве в распоряжение
        покупателя в названном пункте или месте на границе до поступления товара на таможенную границу сопредельной страны.
         Под термином "граница" понимается любая граница, включая границу страны экспорта. Поэтому, весьма важно точное
          определение границы путем указания на конкретный пункт или место.`,
      `Однако, если стороны желают, чтобы продавец взял на себя обязанности по разгрузке товара с прибывшего транспортного
       средства и нес все риски и расходы за такую разгрузку, то это должна быть четко оговорено в соответствующем дополнении
        к договору купли-продажи.`,
      `Данное условие используется вместо DAF, DES и DDU (ИНКОТЕРМС 2000).`
    ],
    subtitle: '- Поставка в пункте'
  },
  {
    name: 'DAT',
    desc: [
      `Термин "Поставка с пристани" означает, что продавец выполнил свои обязанности по поставке, когда товар,
       не прошедший таможенную очистку для импорта, предоставлен в распоряжение покупателя на пристани в названном
        порту назначения. Продавец обязан нести все расходы и риски, связанные с транспортировкой и выгрузкой товара
         на пристань. Термин DAT возлагает на покупателя обязанность таможенной очистки для импорта товара, также как
          и уплату налогов, пошлин и других сборов при импорте.`,
      `Однако, если стороны желают, чтобы продавец взял на себя все или часть расходов по импорту товара,
       то это должно быть четко оговорено в соответствующем дополнении к договору купли-продажи.`,
      `Данный термин может применяться только при перевозке морским или внутренним водным транспортом или в
       смешанных перевозках, когда товар выгружается с судна на пристань в порту назначения. Однако, если
        стороны желают включить в обязанности продавца риски и расходы, связанные с перемещением товара с пристани
         в другое место (склад, терминал и т.д.) в порту, либо за пределами порта, должен быть использован термин DAP.`
    ],
    subtitle: '- Поставка с пристани'
  },{
    name: 'DDP',
    desc: [
      `Термин «Поставка с оплатой пошлины» означает, что продавец предоставит прошедший таможенную очистку
       и неразгруженный с прибывшего транспортного средства товар в распоряжение покупателя в названном месте назначения.
        Продавец обязан нести все расходы и риски, связанные с транспортировкой товара, включая (где это потребуется)
         (См. Введение п.14) любые сборы для импорта в страну назначения (под словом «сборы» здесь подразумевается
            ответственность и риски за проведение таможенной очистки, а также за оплату таможенных формальностей,
             таможенных пошлин, налогов и других сборов).`
    ],
    subtitle: '- Поставка с оплатой пошлины'
  }
]

$('ul li a').click(function () {
  let name = $(this).text();

  $.each(sprav, (index) => {
    if (sprav[index].name == name) {
      for (var i = 0; i < sprav[index].desc.length; i++) {
        $('.passive-inc').append(`
          <span>`+sprav[index].desc[i]+`</span>
        `);
      }
      $(window).scrollTop(0);
      $('h1').text(sprav[index].name + ' ' + sprav[index].subtitle);
      $('.back-to-inc').show();
      $('.main-inc').css('left', '-100%');
      $('.passive-inc').css('left', '0');
      if (name == 'EXW') {
          $('.passive-inc').append(EXW_temp);
          $('.incoterms-container').css('height' , $('.passive-inc').css('height'));
      }
    }
  });
});

$('.back-to-inc').click(function (){
  $(this).hide();
  $('.main-inc').css('left', '0');
  $('.passive-inc').css('left', '100%').empty();
  if ($('h1').text() == 'EXW - Франко завод/склад') {
    $('.incoterms-container').css('height' , $('.main-inc').css('height'));
  }
  $('h1').text('Инкотермс');
});