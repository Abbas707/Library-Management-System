$(function()
{
    let x = $('#id_no_of_copy');
    console.log(x)
    x.after(`<a href="#" id='plus' class="btn btn-primary btn-lg">+</a>`);
    x.after(`<a href="#" id='minus' class="btn btn-danger btn-lg">-</a>`);
    let y = $('#id_available_copy');
    console.log(y)
    y.attr("disabled","disabled");
    x.attr("disabled","disabled");
  
    // no of copy increment
    $('#plus').on('click',function() {
      // console.log({{books.id}}) 

      $.ajax({
          url: TemplateVar.url,
          method:'POST',
          data: {
              id: TemplateVar.id,
              csrfmiddlewaretoken: TemplateVar.csrf_token,
              symbol: 'plus'
            },
          success:function(data){
               // console.log(data.status)
              if(data.status == "1"){
                  x.val(data.book_copy);
                  y.val(data.avail);
                }
            }
         })
    });

        
    // no of copy decreement
    $('#minus').on('click',function(){
            
      let noOfCopy = Number($('#id_no_of_copy').val());
      if(noOfCopy < 1){
          alert('Number of copies cannot be negative')  
          throw error('Minus Copy not valid')
      }
      //console.log({{books.id}})
      
      $.ajax({
          url: TemplateVar.url,
          method:'POST',
          data: {
              id: TemplateVar.id,
              csrfmiddlewaretoken: TemplateVar.csrf_token,
              symbol: 'minus'
            },
          success: function(data){
              console.log(data.status)
              if(data.status == "1"){
                  x.val(data.book_copy);
                  y.val(data.avail);
                }
            }
        })
    });
});
