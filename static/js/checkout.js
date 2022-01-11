//* API to update user order in the database

function updateUserOrder(productId, action) {
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // location.reload();
      console.log(data);
    });
}

const items = document.querySelectorAll(".card");
const debug = document.querySelector(".card");
function updateItemTotal(item) {
  const qtyElement = item.querySelector(".item-qty");
  const priceElement = item.querySelector(".item-val");
  //   console.log("Item Price: " + item.dataset.price);
  //   console.log("item quantity: " + amtElement.value);
  //   console.log(priceElement.innerText);
  priceElement.innerText =
    parseInt(qtyElement.value) * parseInt(item.dataset.price);
}

items.forEach(function (i) {
  const qtyElement = i.querySelector(".item-qty");
  i.querySelector(".subtract").addEventListener("click", function () {
    if (qtyElement.value == 1) {
      updateUserOrder(i.dataset.product, "delete");
      i.parentNode.removeChild(i);
      let totalItem = document
        .querySelector(".py-4")
        .innerText.match(/(\d+)/)[0];

      document.querySelector(".py-4").innerText = `Cart (${
        parseInt(totalItem) - 1
      } items)`;
      cartTotal();
      return;
    }
    qtyElement.value = parseInt(qtyElement.value) - 1;
    updateItemTotal(i);
    updateUserOrder(i.dataset.product, "remove");
    cartTotal();
  });

  i.querySelector(".add").addEventListener("click", function () {
    qtyElement.value = parseInt(qtyElement.value) + 1;
    updateItemTotal(i);
    updateUserOrder(i.dataset.product, "add");
    cartTotal();
  });
});

function cartTotal() {
  const prices = document.querySelectorAll(".item-val");
  let total = 0;
  prices.forEach((i) => (total += parseInt(i.innerText)));
  product_total_amt.innerText = total + ".00";
  total_cart_amt.innerText = total + 5;
  hidden_total.value = total_cart_amt.innerText;
}

function init() {
  items.forEach((i) => updateItemTotal(i));
  cartTotal();
}

init();
