$(document).ready(function () {
  var $success = false;
  var $btn_action = "";
  var $is_closed = false;
  var dateNow = new Date();
  $('#divdate').datetimepicker({
    format:'yyyy-MM-DD',
    defaultDate:dateNow
  });
  $('.select2div').select2({
    width:'resolve'
  });
  $('[data-mask]').inputmask()

    $t = $('#datatable').DataTable({
        "paging": true,
        "searching": true,
        "lengthMenu": [[5, 10, 25, -1], [5, 10, 25, "All"]],
        "ordering": true,
        "info": true,
        "responsive": true,
        "columnDefs": [
          { "width": '30%', "targets": [1,2] }
      ],
      "fixedColumns": true
      });


    $('body').on('click','.btnDelete',function(e){
      e.preventDefault();
      $id = $(this).data('id');
      $url = $(this).data('url');
      $csrf = $("#datatable").data('csrf');
      Swal.fire({
        title: 'Do you want to delete this member?',
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Yes',
        denyButtonText: 'No',
        showLoaderOnConfirm: true,
        preConfirm: () => {
          $.ajax({
            type:'DELETE',
            headers:{
              'X-CSRFToken':$csrf
            },
            url: $url,
            success: function(response,textStatus,xhr){
              if(xhr.status == 200){
                Swal.fire('Deleted', response.res, 'success').then((result)=>{
                  $t.row($('#' + $id)).remove().draw();
                });
                
              }else{
                $success = false;
              }
          },
          error: function(response){
              console.log(response);
          }
          });
        }
      })
    });

    $.validator.addMethod("greaterThan",
    function (value, element, param) {
          var $otherElement = $(param);
          return parseInt(value, 10) >= parseInt($otherElement.val(), 10);
    });

    $('#form').validate({
      rules: {
        member: {
          required: true,
        },
        document_date: {
          required: true,
        },
        paid_amount:{
          required: true,
          min:1,
          greaterThan:"#total_amount",
          number: true,
        }
      },
      messages: {
        member: "Please select member",
        document_date: "Please enter document date",
        paid_amount: {
          required:"Please enter paid amount",
          greaterThan:"Total amount is higher than paid amount."
        }
      },
      errorElement: 'span',
      errorPlacement: function (error, element) {
        error.addClass('invalid-feedback');
        element.closest('.form-group').append(error);
      },
      highlight: function (element, errorClass, validClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function (element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
      },
      submitHandler: function () {
        $('#posting_date').prop('disabled',false);
        $('#document_status').prop('disabled',false);
        $('.excludethis').prop('disabled',true);
        var serializedData = $('#form').serialize();
        console.log(serializedData);
        $('#posting_date').prop('disabled',true);
        $('#document_status').prop('disabled',true);
        $('.excludethis').prop('disabled',false);
        var $url = $('#form').attr('action');
        var $method = $('#form').attr('method');
        var $csrf = $("#datatable").data('csrf');
  
        Swal.fire({
          title: 'Do you want to proceed?',
          showDenyButton: true,
          showCancelButton: false,
          confirmButtonText: 'Yes',
          denyButtonText: 'No',
          showLoaderOnConfirm: true,
          preConfirm: () => {
            sendRequest(serializedData,$url,$method,$csrf);
          }
        })
        return false;
        }
    });

  function sendRequest(serializedData,$url,$method,$csrf){
    $.ajax({
      type:$method,
      url: $url,
      headers:{
        'X-CSRFToken':$csrf
      },
      data: serializedData,
      success: function(response,textStatus,xhr){
          if(xhr.status == 201 && $method == "POST"){
            Swal.fire({
              icon: 'success',
              text: 'Sales Order successfully posted!',
            })
          }else if($method == "POST"){
            $success = false;
          }else if(xhr.status == 200 && $method == "PUT"){
            $row = $t.row('#' + response.id);
            $rowindex = $row.index();
            $t.cell({row:$rowindex,column: 0}).data(response.name)
            $t.cell({row:$rowindex,column: 1}).data(response.membership_status_display)
              $success = true;
              $is_closed = true;
              $('#modal').modal('hide');
          }
      },
      error: function(response){
          console.log(response);
      }
  });
  }

//TABLE ROW CLICK
$('#products tbody').on('dblclick','tr',function(e){
  $('#v_product').val($(this).find('input[name="products"]').val());
  $('#v_product').trigger('change');
  $('#v_product').data('row',$(this).index())
  $('#v_quantity').val($(this).find('input[name="quantity"]').val());
  $('#productAdd').prop('disabled',true);
  $('#productUpdate').prop('disabled',false);
  $('#productDelete').prop('disabled',false);
});

//PRODUCTCHANGE
$('#v_product').on('change',function(e){
  if($('#v_product').val().trim().length === 0){
    return false;
  }
  $id = $(this).val();
  $url =$(this).find('option:selected').data('url');
  $csrf = $("#form input[name*='csrfmiddlewaretoken']:first").val();
  $.ajax({
    type:'GET',
    headers:{
      'X-CSRFToken':$csrf
    },
    url: $url,
    success: function(response,textStatus,xhr){
      if(xhr.status == 200){
        $('#v_price').val(response.price);
        if($('#v_quantity').val()){
          st = $('#v_quantity').val() * response.price
          $('#v_subtotal').val(st)
        }
      }
    }
  });

});

$('#v_quantity').on('input',function(e){
  if($('#v_product').val().trim().length === 0){
    return false;
  }
  st = $('#v_quantity').val() * $('#v_price').val();
  $('#v_subtotal').val(st)
});

//Add Button Table
$('#productAdd').on('click',function(e){
  if($('#v_product').val().trim().length === 0 || $('#v_quantity').val().trim().length===0 ||$('#v_quantity').val()===0){
    return false;
  }
  tr = $('<tr></tr>');
  product = $("<input type='hidden' name='products' value='"+ $('#v_product').val() +"' />");
  td = $('<td></td>');
  $(td).append(product);
  $(td).append($('option:selected',$('#v_product')).text());
  $(tr).append(td);
  price = $("<input type='hidden' name='price' value='"+ $('#v_price').val() +"' />");
  td = $('<td></td>');
  $(td).append(price);
  $(td).append($("#v_price").val());
  $(tr).append(td);
  quantity = $("<input type='hidden' name='quantity' value='"+ $('#v_quantity').val() +"' />");
  td = $('<td></td>');
  $(td).append(quantity);
  $(td).append($("#v_quantity").val());
  $(tr).append(td);
  td = $('<td></td>');
  $(td).append($("#v_subtotal").val());
  $(tr).append(td);
  $('#products tbody').append(tr);
  total = Number( $('#total_amount').val());
  total+= Number( $("#v_subtotal").val());
  $('#total_amount').val(total);
  $('#v_product').prop("selectedIndex",0);
  $('#v_price').val("");
  $('#v_quantity').val("");
  $('#v_subtotal').val("");
  $('#v_product').trigger('change');
});

$('#productUpdate').on('click',function(e){
  if($('#v_product').val().trim().length === 0 || $('#v_quantity').val().trim().length===0 ||$('#v_quantity').val()===0){
    return false;
  }
  index = Number($('#v_product').data('row'));
  
  tr = $('#products tbody tr').eq(index);
  $(tr).find('input[name="products"]').val($('#v_product').val())
  $(tr).find('td').eq(0).text($('option:selected',$('#v_product')).text());
  $(tr).find('input[name="price"]').val($('#v_price').val())
  $(tr).find('td').eq(1).text($('#v_price').val());
  $(tr).find('input[name="quantity"]').val($('#v_quantity').val())
  $(tr).find('td').eq(2).text($('#v_quantity').val());
  total = Number( $('#total_amount').val());
  total-= Number(  $(tr).find('td:last').text());
  $('#total_amount').val(total);
  $(tr).find('td:last').empty();
  $(tr).find('td:last').append($("#v_subtotal").val())

  total = Number( $('#total_amount').val());
  total+= Number( $("#v_subtotal").val());
  $('#total_amount').val(total);
  $('#v_product').prop("selectedIndex",0);
  $('#v_price').val("");
  $('#v_quantity').val("");
  $('#v_subtotal').val("");
  $('#v_product').trigger('change');
});


})