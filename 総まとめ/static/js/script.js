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

//編集ボタンを押したときにフォームを出現させる
$(document).ready(function() {
  $('.edit-task').click(function() {
    var taskId = $(this).data('id');
    var taskName = $('tr[data-id="' + taskId + '"] .task_title').text().trim();
    var taskDueDate = $('tr[data-id="' + taskId + '"] .task_due_date').text().trim();
    var convertedDate = taskDueDate.replace(/年/g, '-').replace(/月/g, '-').replace(/日/g, '');
    var formHtml = `
      <td>
        <input type="text" class="form-control task-name-input-${taskId}" value="${taskName}" required>
      </td>
      <td>
        <input type="date" class="form-control task-due-date-input-${taskId}" value="${convertedDate}">
      </td>
      <td>
        <button type="submit" class="btn btn-primary edit-submit" data-id="${taskId}">編集完了</button>
      </td>
    `;
    $('tr[data-id="' + taskId + '"].edit-form-container').html(formHtml);
    $('tr[data-id="' + taskId + '"].task-display').hide();
    $('tr[data-id="' + taskId + '"].edit-form-container').show();
  });
});

//編集処理
$(document).ready(function() {
  //動的に生成された要素に対してはonイベントを追加しないといけない。
  $(document).on('click', '.edit-submit', function() {
    var taskId = $(this).data('id');
    var taskName = $('tr[data-id="' + taskId + '"]').find('.task-name-input-' + taskId).val();
    var taskDueDate = $('tr[data-id="' + taskId + '"]').find('.task-due-date-input-' + taskId).val();
    $.ajax({
      url: '/djangotodo/' + taskId + '/edit/',
      type: 'POST',
      dataType: 'json',
      data: {
        'title': taskName,
        'due_date': taskDueDate || null,
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
      },
      success: function(data, textStatus, xhr) {
        $('tr[data-id="' + taskId + '"] .task_title').text(data.title);
        var dueDate = data.due_date ? new Date(data.due_date) : null;
        var formattedDueDate = dueDate ? dueDate.getFullYear() + '年' + (dueDate.getMonth() + 1).toString().padStart(2, '0') + '月' + dueDate.getDate().toString().padStart(2, '0') + '日' : '';
        $('tr[data-id="' + taskId + '"] .task_due_date').text(formattedDueDate);
        $('tr[data-id="' + taskId + '"].task-display').show();
        $('tr[data-id="' + taskId + '"].edit-form-container').hide();
      },
    });
  });
});