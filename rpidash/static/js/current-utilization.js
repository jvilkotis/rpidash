function fetchCurrentUtilization() {
  fetch("/services/current_utilization")
    .then(response => response.json())
    .then(data => {
      displayCurrentUtilization(data);
    })
    .catch(error => {
      console.error("There was a problem fetching the data:", error);
    });
}
function displayCurrentUtilization(data) {
  const cpuUtilizationElement = document.getElementById("current-cpu-utilization");
  const cpuTemperatureElement = document.getElementById("current-cpu-temperature");
  const memoryUtilizationElement = document.getElementById("current-memory-utilization");
  const storageUtilizationElement = document.getElementById("current-storage-utilization");

  const {
  cpu_percentage,
  cpu_temperature,
  memory_used,
  memory_percentage,
  memory_total,
  storage_used,
  storage_percentage,
  storage_total
  } = data;

  cpuUtilizationElement.innerHTML = `&#8594; ${cpu_percentage}%`;
  cpuTemperatureElement.innerHTML = `&#8594; ${cpu_temperature} °C`;
  memoryUtilizationElement.innerHTML = `&#8594; ${memory_used} MB (${memory_percentage}%) of ${memory_total} MB`;
  storageUtilizationElement.innerHTML = `&#8594; ${storage_used} GB (${storage_percentage}%) of ${storage_total} GB`;
}

fetchCurrentUtilization();
setInterval(fetchCurrentUtilization, 10000);