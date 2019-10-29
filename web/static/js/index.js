//
// Update read status
//

document.querySelectorAll(".mark-as-read").forEach(elem => {
  elem.addEventListener("click", e => {
    const bookId = elem.getAttribute("data-book-id");
    const spinner = elem.parentElement.lastElementChild;

    elem.classList.add("hidden");
    spinner.classList.remove("hidden");

    if (elem.textContent.toLowerCase().trim() === "read") {
      updateReadStatus("remove", bookId, elem, spinner);
    } else {
      updateReadStatus("add", bookId, elem, spinner);
    }
  });
});

const updateReadStatus = (action, bookId, elem, spinner) => {
  fetch(`/${action}/?book_id=${bookId}`)
    .then(resp => resp.json())
    .then(json => {
      if (json.success) {
        elem.textContent = action === "add" ? "Read" : "Mark as read";

        elem.classList.remove("hidden");
        spinner.classList.add("hidden");
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

//
// Syncing
//

const sync = document.querySelector("#sync");
const lds = document.querySelector(".lds-ring");
if (sync && lds) {
  sync.addEventListener("click", () => {
    sync.innerText = "syncing...";
    sync.classList.add("cursor-default");
    sync.classList.add("hover:no-underline");

    lds.classList.remove("hidden");
  });
}
