document.querySelectorAll(".mark-as-read").forEach(elem => {
  let book_id = elem.getAttribute("data-book-id");

  elem.addEventListener("click", e => {
    fetch(`/add/?book_id=${book_id}`)
      .then(resp => resp.json())
      .then(json => {
        if (json.success) {
          elem.textContent = "Read";
        } else {
          json.errors.forEach(error => console.error(error));
        }
      })
      .catch(error => console.error(error));
  });
});
