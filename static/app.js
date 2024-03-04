console.debug('Checking guess ->')

$('form').on('submit', function(e){
  e.preventDefault();

  let guess = $('#guess').val();

  $.ajax({
    url: '/check-guess',
    data: $('form').serialize(),
    type: 'POST',
    success: function(response){
      console.log(`// response result: ${response.result}`);
    },
    error: function(error){
        console.log(error)
    }
  });
});