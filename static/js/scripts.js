$(document).ready(function() {
  $('form.question-form').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    form.children('textarea').each(function(i) {
      $(this).attr('name', 'proposal'+i);
    })
    var url = form.attr('action');
    var data = form.serialize();
    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      success: function(response) {
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

  $('form.comment-form, form.reply-form').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();
    $.ajax({
      type: 'POST',
      url: url,
      data: data,
      success: function(response) {
        form.before(response);
      }
    });
  });

  $('.reply-btn').click(function(e) {
    if($(this).closest('.new-reply').hasClass('reply-collapse')) {
      e.preventDefault();
      $('.new-reply').addClass('reply-collapse');
      $('.new-reply button').attr('type', 'button');
      $(this).closest('.new-reply').removeClass('reply-collapse');
      $(this).closest('.new-reply').find('textarea').focus();
      $(this).attr('type', 'submit');
    }
  })
});
