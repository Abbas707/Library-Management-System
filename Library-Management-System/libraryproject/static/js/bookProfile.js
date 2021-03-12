$(function()
{
    let x = $('#copy');
    console.log(x)
    let y = $('#avail');
    console.log(y)

    // no of copy increment
    $('#plus').on('click',function() {

      $.ajax({
          url: TemplateVariable.url,
          method:'POST',
          data: {
              id: TemplateVariable.id,
              csrfmiddlewaretoken: TemplateVariable.csrf_token,
              symbol: 'plus'
            },
          success:function(data){
              // console.log(data.status)
              if(data.status == "1"){
                  x.text(data.book_copy);
                  y.text(data.avail);
                }
            }
         })
    });

        
    // no of copy decreement
    $('#minus').on('click',function(){
            
      let noOfCopy = $('#copy').text();
      if(noOfCopy < 1){
          alert('Number of copies cannot be negative')  
          throw error('Minus Copy not valid')
      }
      
      $.ajax({
          url: TemplateVariable.url,
          method:'POST',
          data: {
              id: TemplateVariable.id,
              csrfmiddlewaretoken: TemplateVariable.csrf_token,
              symbol: 'minus'
            },
          success: function(data){
              //console.log(data.status)
              if(data.status == "1"){
                  x.text(data.book_copy);
                  y.text(data.avail);
                }
            }
        })
    });
});
