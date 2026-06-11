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

  // Expirations over the next 12 months
  new Chart(document.getElementById("timelineChart"), {
    type: "line",
    data: {
      labels: d.timeline.labels,
      datasets: [
        {
          label: "Expiring",
          data: d.timeline.data,
          borderColor: c("--orange-color"),
          backgroundColor: "rgba(247, 147, 26, 0.2)",
          fill: true,
          tension: 0.3,
          pointRadius: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: grid } },
        y: { grid: { color: grid }, ticks: { precision: 0 }, beginAtZero: true },
      },
    },
  });
})();
