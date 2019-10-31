// Update book read status
//
// If a book has not been read, mark it as read; otherwise, mark
// it as unread. Applies to search result items.

document.querySelectorAll(".mark-as-read").forEach(elem => {
  elem.addEventListener("click", () => {
    const bookId = elem.getAttribute("data-book-id");

    elem.classList.add("hidden");
    if (elem.textContent.toLowerCase() === "read") {
      updateReadStatus("remove", bookId, elem);
    } else {
      updateReadStatus("add", bookId, elem);
    }
  });
});

const updateReadStatus = (action, bookId, elem) => {
  const spinner = elem.parentElement.lastElementChild;
  spinner.classList.remove("hidden");

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

// Pagination controls
//
// Move through pages. Applies to search results.

const prev = document.querySelector("#prev-page");
if (prev) {
  prev.addEventListener("click", () => changePage(-1));
}

const next = document.querySelector("#next-page");
if (next) {
  next.addEventListener("click", () => changePage(+1));
}

const changePage = modifier => {
  const page = parseInt(document.querySelector("#page-number").value, 10);
  window.location.href = window.location.href.replace(
    /page=\d+/,
    `page=${page + modifier}`,
  );
};

// Syncing with Goodreads
//
// Since it takes so damn long, change the button text and display a loading
// spinner when the sync begins.

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
