$(document).ready(function() {
  $('form.question-form').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    form.children('textarea').each(function(i) {
      $(this).attr('name', 'proposal'+i);
    })
    var url = form.attr('action');
    var data = form.serialize();
    var method = form.attr('method');
    $.ajax({
      type: method,
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

  $(document).on('click', '.add-proposal', function(e) {
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
    var method = form.attr('method');
    $.ajax({
      type: method,
      url: url,
      data: data,
      success: function(response) {
        form.find('textarea').val('');
        form.find('.new-reply').addClass('reply-collapse');
        form.before(response);
      }
    });
  });

  $('form.edit-comment-form').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();
    var method = form.attr('method');
    $.ajax({
      type: method,
      url: url,
      data: data,
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function(response) {
        form.closest('.post-comment').replaceWith(response);
      }
    });
  });

  $(document).on('click', '.reply-btn', function(e) {
    if($(this).closest('.new-reply').hasClass('reply-collapse')) {
      e.preventDefault();
      $('.new-reply').addClass('reply-collapse');
      $('.new-reply button').attr('type', 'button');
      $(this).closest('.new-reply').removeClass('reply-collapse');
      $(this).closest('.new-reply').find('textarea').focus();
      $(this).attr('type', 'submit');
    }
  });

  $('form.comment-delete-form').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();
    var method = form.attr('method');
    $.ajax({
      type: method,
      url: url,
      data: data,
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function(response) {
        form.closest('.post-comment').remove();
      }
    });
  });

  $('form.reply-delete-form').submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize();
    var method = form.attr('method');
    $.ajax({
      type: method,
      url: url,
      data: data,
      success: function(response) {
        form.closest('.reply').remove();
      }
    });
  });

  $(document).on('click', '.comment-history-btn', function() {
    $(this).toggleClass('post-btn-active');
    $(this).closest('.post-comment').find('.comment-history').toggleClass('history-collapse');
  });

  $(document).on('click', '.edit-btn', function() {
    $(this).toggleClass('post-btn-active');
    $(this).closest('.post-comment').toggleClass('new-comment');
    var comment = $(this).closest('.post-comment').find('.comment-text').html();
    $(this).closest('.post-comment').find('.comment-body textarea').val(comment.trim());
  });
});

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
