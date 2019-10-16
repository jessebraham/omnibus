//
// Update read status
//

document.querySelectorAll(".mark-as-read").forEach(elem => {
  elem.addEventListener("click", e => {
    const bookId = elem.getAttribute("data-book-id");
    if (elem.textContent.toLowerCase().trim() === "read") {
      updateReadStatus("remove", bookId, elem);
    } else {
      updateReadStatus("add", bookId, elem);
    }
  });
});

const updateReadStatus = (action, bookId, elem) => {
  fetch(`/${action}/?book_id=${bookId}`)
    .then(resp => resp.json())
    .then(json => {
      if (json.success) {
        elem.textContent = action === "add" ? "Read" : "Mark as read";
      } else {
        console.error(json.error);
      }
    })
    .catch(error => console.error(error));
};

//
// Pagination
//

const prev = document.querySelector("#prev-page");
if (prev) {
  prev.addEventListener("click", e => changePage(-1));
}

const next = document.querySelector("#next-page");
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
