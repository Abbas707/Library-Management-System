$("#id_username").change(function () {
  var username = $(this).val();
  // console.log(username)

  $.ajax({
    url: '/ajax/validate_username/',
    method:'POST',
    data: {
      'username': username,
      csrfmiddlewaretoken: TemplateVari.csrf_token,
    },
    dataType: 'json',
    success: function (data) {
      if (data.is_taken) {
        alert("A user with this username already exists.");
      }
    }
  });
});
