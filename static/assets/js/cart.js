$(document).ready(function() {
    $('.btn-detele-item').on('click', function() {
      var title = $(this).data('title');
  
      $.ajax({
        url: '/delete_cart_item',
        type: 'POST',
        data: { item_name: title },
        success: function(response) {
          console.log(response);
          window.location.href = '/show_cart';
        },
        error: function(xhr, status, error) {
          // Handle any errors that occur during the request
          // For example, display an error message or log the error
          alert('Error deleting cart item: ' + error);
        }
      });
    });
  });
  