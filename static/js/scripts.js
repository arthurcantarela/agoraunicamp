$(document).ready(function() {
  $('.question-form').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    form.children('textarea').each(function(i) {
      console.log('hey');
      $(this).attr('name', 'proposal'+i);
    })
    var url = form.attr('action');
    var data = form.serialize();
    console.log(data);
    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      success: function(response) {
        console.log(data);
        console.log(response);
        form.closest('.post').addClass('collapse');
      },
      error: function() {
        console.error('Nao foi');
      }
    });
  });

  $('.add-proposal').click(function(e) {
    var field = $(this).closest('form').find('.proposal').last();
    var index = parseInt(field.find('textarea').attr('name').split('-')[1]) + 1;
    var new_field = field.clone().insertAfter(field).find('textarea').attr('name', 'proposal-'+index).val('').focus();
  });

  $(document).on('click', '.proposal .delete-btn', function() {
    console.log($(this).closest('.proposal'));
    $(this).closest('.proposal').remove();
  });

  $('.reply-btn').click(function() {
    $('.new-reply').addClass('reply-collapse');
    $(this).closest('.new-reply').removeClass('reply-collapse');
    $(this).closest('.new-reply').find('textarea').focus();
  })
});
