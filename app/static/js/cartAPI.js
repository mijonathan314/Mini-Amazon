document.querySelectorAll(".increment-quantity").forEach(button => {
  button.addEventListener("click", () => {
    const itemId = button.getAttribute("data-item-id");
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    const currentQuantity = parseInt(quantityElement.innerText);
    const newQuantity = currentQuantity + 1;
    quantityElement.innerText = newQuantity;
    const totalElement = document.getElementById(`total-price-${itemId}`);
    const itemPriceElement = document.getElementById(`unit-price-${itemId}`);
    const itemPrice = parseFloat(itemPriceElement.innerText);
    totalElement.innerText = newQuantity * itemPrice;
    calcTotalPrice();
    updateCartItemQuantity(itemId, newQuantity);
  });
});

document.querySelectorAll(".decrement-quantity").forEach(button => {
  button.addEventListener("click", () => {
    const itemId = button.getAttribute("data-item-id");
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    const totalElement = document.getElementById(`total-price-${itemId}`);
    const itemPriceElement = document.getElementById(`unit-price-${itemId}`);
    const itemPrice = parseFloat(itemPriceElement.innerText);
    const currentQuantity = parseInt(quantityElement.innerText);
    if (currentQuantity > 1) {
      const newQuantity = currentQuantity - 1;
      quantityElement.innerText = newQuantity;
      totalElement.innerText = newQuantity * itemPrice;
      updateCartItemQuantity(itemId, newQuantity);
      calcTotalPrice();
    }
  });
});

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

function deleteItem(itemId) {
  fetch(`/delete-cart-item/${itemId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  }).then(response => {
      if (response.ok) {
        const rowToDelete = document.getElementById(`row-${itemId}`);
        if (rowToDelete) {
              rowToDelete.remove();
              calcTotalPrice();
        } else {
              console.error("Row not found for item ID:", itemId);
        }
      } else {
      }
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

function calcTotalPrice() {
  const totalPriceCells = document.querySelectorAll('td:nth-child(4)');
  let totalPriceSum = 0;
  totalPriceCells.forEach((cell) => {
    const totalPrice = parseFloat(cell.textContent);
    totalPriceSum += totalPrice;
  });
  const sumContainer = document.querySelector('#overallSumContainer h2');
  sumContainer.innerHTML = `Overall Sum: $${totalPriceSum.toFixed(2)}`;
}
calcTotalPrice();