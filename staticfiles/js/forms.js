// Turn ".js-date" inputs into a flatpickr that DISPLAYS dd/mm/yyyy while the
// real (hidden) input still submits ISO YYYY-MM-DD, which Django parses cleanly.
(function () {
  if (typeof flatpickr === "undefined") return;
  flatpickr(".js-date", {
    dateFormat: "Y-m-d", // value sent to the server
    altInput: true, // show a friendly input to the user...
    altFormat: "d/m/Y", // ...formatted as dd/mm/yyyy
    altInputClass: "form-control js-date-alt",
    allowInput: true,
  });
})();
