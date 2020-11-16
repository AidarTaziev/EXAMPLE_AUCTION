$('#copyier').click(function (){
  window.getSelection().removeAllRanges();
  let elem = document.getElementsByClassName('company-items');
  let range = document.createRange();
  for (var i = 0; i < elem.length; i++) {
    range.selectNode(elem[i]);
    window.getSelection().addRange(range);

    try {
      document.execCommand('copy');
    } catch(err) {
      console.log(err);
    }
  }
  window.getSelection().removeAllRanges();
});
