function updateCartItemQuantity(itemId, newQuantity) {
    fetch(`/update-cart-item/${itemId}`, {
      method: "PATCH",
      body: JSON.stringify({ newQuantity }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(response => {
        if (response.ok) {

        } else {
        }
      })
      .catch(error => {
        console.error("Error:", error);
      });
  };

export { updateCartItemQuantity };