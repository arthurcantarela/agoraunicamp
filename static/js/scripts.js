$(document).ready(function() {
  // @TODO: deal with publication added after
  // class Publication {
  //
  // }

  function loadOlderPost(n=1) {
    if(n>0) {
      if($('.post').length > 0) {
        var url = 'AGR/' + $('.post').last().attr('id').slice(1) + '/older';
      } else {
        var url = 'AGR/newest';
      }
      $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
          $('#postsContainer').append(response);
          loadOlderPost(n-1);
        }
      });
    }
  }

  function loadNewerPost(n=1) {
    if(n>0) {
      if($('.post').length > 0) {
        var url = 'AGR/' + $('.post').first().attr('id').slice(1) + '/newer';
      } else {
        var url = 'AGR/newest';
      }
      $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
          $('#postsContainer').append(response);
          loadNewerPost(n-1);
        }
      });
    }
  }

  loadOlderPost(3);
  $(window).on('scroll', function() {
    if($('.post').length >= 3 && $(window).scrollTop() + $(window).height() - $(document).height() == 0) {
      loadOlderPost();
    }
  });

  $(document).on('click', 'form.question-form button[type="submit"]', function(e) {
    e.preventDefault();
    var form = $(this).closest('form');
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
    });
  });

  $(document).on('click', '.add-proposal', function(e) {
    var field = $(this).closest('form').find('.proposal').last();
    var index = parseInt(field.find('textarea').attr('name').split('-')[1]) + 1;
    var new_field = field.clone().insertAfter(field).find('textarea').attr('name', 'proposal-'+index).val('').focus();
  });

  $(document).on('click', '.proposal .delete-btn', function() {
    $(this).closest('.proposal').remove();
  });

  $(document).on('click', 'form.comment-form button[type="submit"], form.reply-form button[type="submit"]', function(e) {
    e.preventDefault();
    var form = $(this).closest('form');
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

  $(document).on('click', 'form.edit-comment-form button[type="submit"]', function(e) {
    e.preventDefault();
    var form = $(this).closest('form');
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

  $(document).on('click', 'form.comment-delete-form button[type="submit"]', function(e) {
    e.preventDefault();
    var form = $(this).closest('form');
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

  $(document).on('click', 'form.reply-delete-form button[type="submit"]', function(e) {
    e.preventDefault();
    var form = $(this).closest('form');
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

  $(document).on('click', '.edit-comment-btn[type="button"]', function() {
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
