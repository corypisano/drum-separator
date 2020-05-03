// custom javascript

// https://stackoverflow.com/questions/14525029/display-a-loading-message-while-a-time-consuming-function-is-executed-in-flask
$( document ).ready(() => {
    console.log('Sanity Check!');
  });

$('#inputGroupFile01').on('change',function(){
  console.log('im in the jquery change');
  var fileName = $(this).val().replace(/C:\\fakepath\\/i, '');
  //replace the "Choose a file" label
  $(this).next('.custom-file-label').html(fileName);
});

  $('.btngg').on('click', function() {
    $.ajax({
      url: '/tasks',
      data: { type: $(this).data('type') },
      method: 'POST'
    })
    .done((res) => {
      getStatus(res.data.task_id)
    })
    .fail((err) => {
      console.log(err)
    });
  });
  
  function getStatus(taskID) {
    $.ajax({
      url: `/tasks/${taskID}`,
      method: 'GET'
    })
    .done((res) => {
      const html = `
        <tr>
          <td>${res.data.task_id}</td>
          <td>${res.data.task_status}</td>
          <td>${res.data.task_result}</td>
        </tr>`
      $('#tasks').prepend(html);
      const taskStatus = res.data.task_status;
      if (taskStatus === 'finished' || taskStatus === 'failed') return false;
      setTimeout(function() {
        getStatus(res.data.task_id);
      }, 10000);
    })
    .fail((err) => {
      console.log(err)
    });
  }