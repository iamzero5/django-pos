$(document).ready(function () {
  var $success = false;
  var $btn_action = "";
  var $is_closed = false;

  $('#divbirthdate').datetimepicker({
    format:'yyyy-MM-DD'
  });
  $('#divmembershipdate').datetimepicker({
    format:'yyyy-MM-DD'
  });
  $('.select2div').select2({
    width:'resolve'
  });
  $('#access_key_released').on('change',function(e){
      if($('#access_key').val().length == 0){
        $(this).prop('checked',false);
      }
  })
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

      $('#modal').on('show.bs.modal',function(e){
        var $btn = $(e.relatedTarget);
        var $action = $btn.data('action');
        var $lbl = $('#modalFormLabel');
        var $btnAction = $('#btnAction');
        $btnAction.data('action',$action);
        $lbl.text($action+" Member");
        $btnAction.text($action);
        if($action == 'Edit'){
          $id = $($btn).data('id');
          $url = $($btn).data('url');
          $csrf = $("#datatable").data('csrf');
          $btn_action = "updated";
          $.ajax({
            type:'GET',
            headers:{
              'X-CSRFToken':$csrf
            },
            url: $url,
            success: function(response,textStatus,xhr){
              if(xhr.status == 200){
                $('#first_name').val(response.first_name);
                $('#middle_name').val(response.middle_name);
                $('#last_name').val(response.last_name);
                $('#gender').val(response.gender);
                $('#birthdate').val(response.birthdate);
                $('#street').val(response.street);
                $('#barangay').val(response.barangay);
                $('#city').val(response.city);
                $('#province').val(response.province);
                $('#telephone').val(response.telephone);
                $('#mobile').val(response.mobile);
                $('#email').val(response.email);
                $('#membership').val(response.membership);
                $('#membership_start').val(response.membership_start);
                $('#membership_term').val(response.membership_term);
                $('#sales_person').val(response.sales_person);
                $('#access_key').val(response.access_key);
                $('#access_key_released').prop('checked',response.access_key_released)
                $('#personal_trainer').val(response.personal_trainer);
                $('#form').attr('action',$url);
                $('#form').attr('method','PUT');
              }else{
                $success = false;
              }
          },
          error: function(response){
              console.log(response);
          }
          })
        }else{
          $('#form').prop('action',$('#form').data('create'));
          $('#form').prop('method','POST');
          $btn_action = "created"
        }
    });

    $('#modal').on('hidden.bs.modal',function(e){
      if($success && $is_closed){
        Swal.fire({
          icon: 'success',
          text: 'Member successfully '+$btn_action+'!',
        })
        $is_closed = false;
      }
      $('#form').trigger('reset');
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

    $('#form').validate({
      rules: {
        first_name: {
          required: true,
        },
        last_name: {
          required: true,
        },
        gender: {
          required: true
        },
        birthdate: {
          required: true
        },
        street: {
          required: true
        },
        barangay: {
          required: true
        },
        city: {
          required: true
        },
        province: {
          required: true
        },
        mobile: {
          required: true
        },
      },
      messages: {
        first_name: {
          required: "Please enter first name",
        },
        last_name: {
          required: "Please enter last name",
        },
        gender: "Please select gender",
        birthdate: "Please enter birthdate",
        street: "Please enter street",
        barangay: "Please enter barangay",
        city: "Please enter city",
        province: "Please enter province",
        mobile: "Please enter mobile number"
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
      submitHandler: function (form) {
        var serializedData = $('#form').serialize();
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
        });
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
              $('#form').trigger('reset');
              $editBtn = '<button class="btn btn-warning" data-id="'+ response.id +'" data-url="'+response.url+'" data-toggle="modal" data-target="#modal" data-action="Edit"  title="Edit"><i class="fas fa-user-edit"></i></button>';
              $deleteBtn = '<button type="button" class="btn btn-danger btnDelete" data-id="'+ response.id +'" data-url="'+response.url+'" data-action="Delete"  title="Delete"><i class="fas fa-user-minus"></i></button>';
              $t.row.add([
                  response.first_name + " " + response.last_name,
                  response.membership_status_display,
                  '<div class="btn-group float-right" id="action-'+ response.id +'">'+
                  '</div>'
              ]).draw(false).node().id = response.id;
              $('#action-'+response.id).append($($editBtn));
              $('#action-'+response.id).append($($deleteBtn))
              $success = true;
              $is_closed = true;
              $('#modal').modal('hide');
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
})