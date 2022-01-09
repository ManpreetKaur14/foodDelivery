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
      return;
    }
    qtyElement.value = parseInt(qtyElement.value) - 1;
    updateItemTotal(i);
    updateUserOrder(i.dataset.product, "remove");
  });

  i.querySelector(".add").addEventListener("click", function () {
    qtyElement.value = parseInt(qtyElement.value) + 1;
    updateItemTotal(i);
    updateUserOrder(i.dataset.product, "add");
  });
});

function init() {
  items.forEach((i) => updateItemTotal(i));
}

init();
