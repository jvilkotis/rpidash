function fetchCurrentUtilization() {
  fetch("/services/current_utilization")
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then(data => {
      displayCurrentUtilization(data);
    })
    .catch(error => {
      console.error("There was a problem fetching the data:", error);
    });
}
function displayCurrentUtilization(data) {
  const currentUtilizationDiv = document.getElementById("currentUtilization");
  const htmlContent = `
    <p>CPU utilization: ${data.cpu_percentage}%</p>
    <p>CPU temperature: ${data.cpu_temperature} °C</p>
    <p>Memory utilization: ${data.memory_used} MB (${data.memory_percentage}%) of ${data.memory_total} MB</p>
    <p>Storage utilization: ${data.storage_used} GB (${data.storage_percentage}%) of ${data.storage_total} GB</p>
  `;
  currentUtilizationDiv.innerHTML = htmlContent;
}
fetchCurrentUtilization();
setInterval(fetchCurrentUtilization, 10000);