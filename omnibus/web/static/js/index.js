//
// Update read status
//

document.querySelectorAll(".mark-as-read").forEach(elem => {
  const bookId = elem.getAttribute("data-book-id");

  elem.addEventListener("click", e => {
    fetch(`/add/?book_id=${bookId}`)
      .then(resp => resp.json())
      .then(json => {
        if (json.success) {
          elem.textContent = "Read";
        } else {
          console.error(json.error);
        }
      })
      .catch(error => console.error(error));
  });
});

//
// Pagination
//

const prev = document.querySelector(".prev-page");
if (prev) {
  prev.addEventListener("click", e => changePage(-1));
}

const next = document.querySelector(".next-page");
if (next) {
  next.addEventListener("click", e => changePage(+1));
}

const changePage = modifier => {
  let page = parseInt(document.querySelector("#page-number").value, 10);
  page += modifier;

  window.location.href = window.location.href.replace(
    /page=\d+/,
    `page=${page}`,
  );
};
