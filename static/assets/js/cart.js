
$(document).ready(function() {
  // delete
  $('.btn-detele-item').on('click', function() {
      var title = $(this).data('title');
      event.preventDefault();
      $.ajax({
        url: '/delete_cart_item',
        type: 'POST',
        data: { item_name: title },
        success: function(response) {
          console.log(response);
        },
        error: function(xhr, status, error) {
          // Handle any errors that occur during the request
          // For example, display an error message or log the error
          alert('Error deleting cart item: ' + error);
        }
      });
    });
  // decrease
  $('.btn-decrease').click(function() {
      event.preventDefault();
      var button = $(this);
      var value = $(this).next('.book-quantity').val();
      var title = $(this).data('title');
      value = parseInt(value) - 1;
      $.ajax({
      url: '/update_quantity', // Replace with the actual server-side endpoint to handle the update
      type: 'POST',
      data: { quantity: value, item_name: title },
      success: function(response) {
        button.next('.book-quantity').val(response.quantity);
        $('.total_price').text(response.total_price);
      },
      error: function(xhr, status, error) {
          // Handle any errors that occurred during the AJAX request
          console.error(error);

      }
    });
  });

  // increase
  $('.btn-increase').click(function() {
      event.preventDefault();
      var button = $(this);
      var value = $(this).prev('.book-quantity').val();
      var title = $(this).data('title');
      value = parseInt(value) + 1;
    // Send the updated item number to the server using AJAX
      $.ajax({
      url: '/update_quantity', // Replace with the actual server-side endpoint to handle the update
      type: 'POST',
      data: { quantity: value, item_name: title },
      success: function(response) {
        button.prev('.book-quantity').val(response.quantity);
        $('.total_price').text(response.total_price);
      },
      error: function(xhr, status, error) {
        // Handle any errors that occurred during the AJAX request
        console.error(error);
      }
    });
  });

  // 確認訂單

});




