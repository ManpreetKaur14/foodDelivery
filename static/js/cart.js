let updateBtns = document.querySelectorAll(".update-cart");

updateBtns.forEach(function (i) {
  i.addEventListener("click", function () {
    if (user == "AnonymousUser") {
      alert("PLease login to add items to the cart");
      window.location.replace("/login/");
      return;
    }
    console.log("USER: " + user);
    console.log("product id: " + this.dataset.product);
    console.log("Action: " + this.dataset.action);
    updateUserOrder(this.dataset.product, this.dataset.action);
  });
});

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
      // alert(data);
      let notyf = new Notyf({
        duration: 10000,
        position: {
          x: "right",
          y: "bottom",
        },
        types: [
          {
            type: "success",
            background: "#5cb85c",
            duration: 3000,
            dismissible: true,
          },
        ],
      });
      notyf.success(data);
    });
}
