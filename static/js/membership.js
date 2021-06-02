$(function () {
  var $success = false;
  var $btn_action = "";
  var $is_closed = false;
    $t = $('#datatable').DataTable({
        "paging": true,
        "searching": true,
        "lengthMenu": [[5, 10, 25, -1], [5, 10, 25, "All"]],
        "ordering": true,
        "info": true,
        "responsive": true,
        "columnDefs": [
          { "width": '30%', "targets": 2 }
      ],
      "fixedColumns": true
      });

      $('#modal').on('show.bs.modal',function(e){
        var $btn = $(e.relatedTarget);
        var $action = $btn.data('action');
        var $lbl = $('#modalFormLabel');
        var $btnAction = $('#btnAction');
        $btnAction.data('action',$action);
        $lbl.text($action+" membership");
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
                $('#name').val(response.name);
                $('#description').text(response.description);
                $('#price').val(response.price);
                $('#is_standard').val(response.is_standard?'True':'False');
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
          text: 'Membership successfully '+$btn_action+'!',
        })
        $is_closed = false;
      }
    });

    $('body').on('click','.btnDelete',function(e){
      e.preventDefault();
      $id = $(this).data('id');
      $url = $(this).data('url');
      $csrf = $("#datatable").data('csrf');
      Swal.fire({
        title: 'Do you want to delete this membership?',
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

    $('#form').submit(function (e) {
      e.preventDefault();
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
      })
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
                  response.name,
                  response.price > 0?response.price:'Free',
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
            $t.cell({row:$rowindex,column: 1}).data(response.price)
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

  });