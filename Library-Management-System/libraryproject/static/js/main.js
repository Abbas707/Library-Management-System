let pass1 = document.getElementById('id_password1')
let pass2 = document.getElementById('id_password2')

pass2.addEventListener('blur', function() {

  if(pass1.value != pass2.value) {
    alert('Please enter same password!!!')
  }
});



