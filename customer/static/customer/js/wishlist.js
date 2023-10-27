// $(".btnRemoveFave").find('i.fa-heart').css('color', '#007c7a');
// $(".btnAddFave").find('i.fa-heart').css('color', '#f7296a');

// $('.btnRemoveFave').wrap('<span id="ctl00_BodyContentHolder_lblfavourite-471110"><span>');

// $('button.btnRemoveFave').click(function(){
// 	$(this).find('i.fa-heart').css('color', '#f7296a');
// });

document.addEventListener("DOMContentLoaded", function() {
	const wishlistIcon = document.querySelector(".wishlist-icon");
	let isRed = false;
  
	wishlistIcon.addEventListener("click", function() {
	  if (isRed) {
		// If the icon is already red, remove the data from the backend
		removeDataFromBackend();
	  } else {
		// If the icon is not red, change its color to red
		wishlistIcon.style.color = "red";
		isRed = true;
	  }
	});
  
	function removeDataFromBackend() {
	  // Send an AJAX request to Django view to remove data from the backend
	  // You can use libraries like Axios or jQuery for making AJAX requests
	  // Example using fetch:
	  fetch("/remove_data_from_backend/", {
		method: "POST",
		headers: {
		  "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
		},
	  })
		.then(response => response.json())
		.then(data => {
		  // Handle the response from the backend (if needed)
		  console.log("Data removed from backend:", data);
		})
		.catch(error => {
		  console.error("Error removing data:", error);
		});
	}
  
	// Function to get the CSRF token from cookies (for Django)
	function getCookie(name) {
	  const value = `; ${document.cookie}`;
	  const parts = value.split(`; ${name}=`);
	  if (parts.length === 2) return parts.pop().split(";").shift();
	}
  });
  