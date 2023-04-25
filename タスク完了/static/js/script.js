//完了、未完了ボタンを押したときの動き
$(document).ready(function() {
    $('.toggle-completed').click(function() {
      var taskId = $(this).data('id');
      $.ajax({
        url: '/djangotodo/' + taskId + '/complete/',
        type: 'POST',
        dataType: 'json',
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
        },
        success: function(data, textStatus, xhr) {
          if (data.is_completed) {
            $('tr[data-id="' + taskId + '"]').addClass('completed');
            $('.toggle-completed[data-id="' + taskId + '"]').text('未完了にする');
          } else {
            $('tr[data-id="' + taskId + '"]').removeClass('completed');
            $('.toggle-completed[data-id="' + taskId + '"]').text('完了にする');
          }
        },
      });
    });
  });