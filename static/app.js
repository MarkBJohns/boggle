console.debug('Checking guess ->')

$('form').on('submit', function(e){
  e.preventDefault();

  let guess = $('#guess').val();

  $.ajax({
    url: '/check-guess',
    data: $('form').serialize(),
    type: 'POST',
    cache: false,
    success: function(response){
      console.log(response === undefined)
      $('#score').text(`Score: ${response.score}`)
      console.log(`// response score: ${response.score}`)
      console.log(`// response result: ${response.result}`);

      if (response.result === 'ok') {
        $('#found').val(function(i, val) {
          return val + (val ? ', ' : '') + guess;
        });

        // $('#score').text(response.score);

      } else if (response.result === 'not-on-board') {
        $('#not-on-board').val(function(i, val) {
          return val + (val ? ', ' : '') + guess;
        });
      } else if (response.result === 'not-word') {
        $('#not-word').val(function(i, val) {
          return val + (val ? ', ' : '') + guess;
        });
      }

      $('#guess').val('');
    },
    complete: function(xhr, status) {
      console.log("Request completed with status:", status)
      console.log("Response status code:", xhr.status)
    },
    error: function(error){
        console.log(error)
    }
  });
});

$('h1').on('click', function(e){
  e.preventDefault();

  $.ajax({
    url: '/reshuffle',
    type: 'POST',
    success: function(response){

      $('#score').text('0')
      $('table').empty();

      for(let row of response.board){
        let tr = $('<tr>');

        for(let letter of row){
          tr.append($('<td>').text(letter));
        }

        $('table').append(tr);
      }

      // $('#score').text('Score: 0');
    },
    error: function(error){
      console.error(error)
    }
  });
});