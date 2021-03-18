$(function() {

  // If available book is 0 then remove Issue Button
  if (Number($('#avail').text()) < 1){
    $('#issue-book').remove();
  }

  $('#issue-book').on('click', function(){
    $.ajax({
      url:'/book_issue/',
      method:'POST',
      data: {
        book_id: $('#book-id').text(),
        user_id: $('#user-id').val(),
        csrfmiddlewaretoken: $('#csr').val(),
      },
      success: function(data) {
        if(data.status==0) {
          alert(data.msg);
        }
        else if(data.status==2) {
          alert(data.msg);
        }
        else {
        $('#avail').text(data.avail);
        let btn = $('#issue-book');
       
        if (confirm("Are u want to issue this book?")) {
          btn.text('Book Issued')
        } else {
          btn.text('Issue Book')
        }
      }
      }
  })
});


























});