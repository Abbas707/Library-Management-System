$(function(){
  let preHtml = document.getElementById('pre-table');

  // console.log(preHtml);
  $('#search').on('input', function() {
    let record = $('#search').val();
    if (record != "") {
      $.ajax ({
        url: '/search_record/',
        data: {
          title: record
        },
        success: function (data) {
          if (data.records.length > 0) {
            $('#pre-table').remove();

            th = `
            <table class="table table-striped" id='new-table' style="background-color:#c9d2db">
            <thead class="thead-light">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">User</th>
                <th scope="col">Title</th>
                <th scope="col">Issue Date</th>
                <th scope="col">Due date</th>
                <th scope="col">Return date</th>
              </tr>
            </thead>
            <tbody>`

            for (let i=0; i < data.records.length; i++){
              th += `<tr>
                      <td>${data.records[i]['id']}</td>
                      <td>${data.records[i]['user']}</td>
                      <td>${data.records[i]['title']}</td>
                      <td>${data.records[i]['issue_date']}</td>
                      <td>${data.records[i]['due_date']}</td>`

                      if (data.records[i]['return_date']==null) {
                        th += `<td>----</td>`
                      }
                      else {
                        th += `<td>${data.records[i]['return_date']}</td>`
                      }
                      th += `</tr>`
            }
            th += `</tbody> </table>`
            
            $('#mycontain').html(th);
          }

          else {
            $('#mycontain').html(`<div class="alert alert-danger">
                            <strong>Oopss!!</strong> Record not available!!
                        </div>`)
          }
        },

      })
    }

    else {
      $('#new-table').remove();
      let new_th = preHtml.outerHTML;
      $('#mycontain').html(new_th);
    }
  });
});