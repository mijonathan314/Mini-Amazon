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
    calcTotalPrice(-itemPrice);
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
      calcTotalPrice(itemPrice);
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
              const totalElement = document.getElementById(`total-price-${itemId}`).innerHTML;
              rowToDelete.remove();
              calcTotalPrice(totalElement);
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

function calcTotalPrice(amountToDelete) {
  const prevPriceArray = document.querySelector('#overallSumContainer h2').innerHTML
  const prevPrice = prevPriceArray.split(" ")[2].substring(1)
  let newPrice = prevPrice - amountToDelete;
  const sumContainer = document.querySelector('#overallSumContainer h2');
  sumContainer.innerHTML = `Overall Sum: $${newPrice.toFixed(2)}`;
}

var discountCodes = {
  "TAKE25": 0.75,
  "DISCOUNT50":0.5,
}

function isValidDiscountCode(code) {
  return discountCodes.hasOwnProperty(code);
}

function applyVerifyDiscount() {
  var discountCodeInput = document.getElementById('discountCode');
  var appliedCodeContainer = document.getElementById('appliedCodeContainer');
  var appliedCode = document.getElementById('appliedCode');
  var applyVerifyButton = document.getElementById('applyVerifyButton');
  var messageElement = document.getElementById('message');
  var code = discountCodeInput.value.trim();

  if (code !== '') {
      if (isValidDiscountCode(code)) {
        messageElement.textContent = 'Discount successfully applied!';
        messageElement.className = 'success';
        const prevPriceArray = document.querySelector('#overallSumContainer h2').innerHTML
        const prevPrice = prevPriceArray.split(" ")[2].substring(1)
        let newPrice = prevPrice*discountCodes[code]
        const sumContainer = document.querySelector('#overallSumContainer h2');
        sumContainer.innerHTML = `Overall Sum: $${newPrice.toFixed(2)}`;
        appliedCode.textContent = 'Applied Code: ' + code;
        appliedCodeContainer.style.display = 'block';
        applyVerifyButton.disabled = true;
    } else {
        messageElement.textContent = 'Invalid code';
        messageElement.className = 'error';
    }
  }
}

function removeDiscount() {
  var appliedCodeContainer = document.getElementById('appliedCodeContainer');
  var appliedCode = document.getElementById('appliedCode');
  var applyVerifyButton = document.getElementById('applyVerifyButton');

  const prevPriceArray = document.querySelector('#overallSumContainer h2').innerHTML
  const prevPrice = prevPriceArray.split(" ")[2].substring(1)
  const code = appliedCode.innerHTML.split(" ")[2]
  let newPrice = prevPrice/discountCodes[code]
  const sumContainer = document.querySelector('#overallSumContainer h2');
  sumContainer.innerHTML = `Overall Sum: $${newPrice.toFixed(2)}`;
  var messageElement = document.getElementById('message');
  messageElement.textContent = '';

  appliedCode.textContent = '';
  appliedCodeContainer.style.display = 'none';
  applyVerifyButton.disabled = false;
}