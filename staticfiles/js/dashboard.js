// Dashboard charts. Data comes from the <script id="chart-data"> JSON block
// rendered by Django (see common/views.py -> chart_data + json_script).
(function () {
  if (typeof Chart === "undefined") return;

  var dataEl = document.getElementById("chart-data");
  if (!dataEl) return;
  var d = JSON.parse(dataEl.textContent);

  var css = getComputedStyle(document.documentElement);
  var c = function (name) {
    return css.getPropertyValue(name).trim();
  };
  var grid = "rgba(216, 222, 233, 0.12)";
  Chart.defaults.color = c("--white-color");
  Chart.defaults.font.family = "system-ui, sans-serif";

  // Status doughnut
  new Chart(document.getElementById("statusChart"), {
    type: "doughnut",
    data: {
      labels: d.status.labels,
      datasets: [
        {
          data: d.status.data,
          backgroundColor: [c("--green-color"), c("--yellow-color"), c("--red-color")],
          borderColor: c("--black-color"),
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "bottom" } },
    },
  });

  // Warranties by supplier
  new Chart(document.getElementById("supplierChart"), {
    type: "bar",
    data: {
      labels: d.supplier.labels,
      datasets: [
        {
          label: "Warranties",
          data: d.supplier.counts,
          backgroundColor: c("--blue-color"),
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: grid } },
        y: { grid: { color: grid }, ticks: { precision: 0 } },
      },
    },
  });

  // Total spend per year (by purchase date)
  var cur = d.spend_year.currency || "";
  var money = function (v) {
    return cur + Number(v).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };
  new Chart(document.getElementById("spendYearChart"), {
    type: "bar",
    data: {
      labels: d.spend_year.labels,
      datasets: [
        {
          label: "Spend",
          data: d.spend_year.data,
          backgroundColor: c("--orange-color"),
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: function (ctx) { return money(ctx.parsed.y); } } },
      },
      scales: {
        x: { grid: { color: grid } },
        y: {
          grid: { color: grid },
          beginAtZero: true,
          ticks: { callback: function (v) { return money(v); } },
        },
      },
    },
  });
})();
