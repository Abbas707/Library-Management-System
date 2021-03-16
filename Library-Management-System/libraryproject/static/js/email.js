$("#id_email").change(function() {
  var email = $(this).val();

  // console.log(email);

  $.ajax({
    url: '/validate_email/',
    method: 'POST',
    data: {
      'email': email,
      csrfmiddlewaretoken: TemplateVari.csrf_token,
    },
    dataType: 'json',
    success: function(data){
      if (data.is_taken) {
        alert("This email is already in use!!")
      }
    }
  }); 
});




