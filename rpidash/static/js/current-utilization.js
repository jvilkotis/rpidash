const fetchCurrentUtilization = async () => {
  try {
    const response = await fetch("/services/current_utilization");
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    displayCurrentUtilization(data);
  } catch (error) {
    console.error("There was a problem fetching the data:", error);
  }
};

const displayCurrentUtilization = ({
  cpu_percentage,
  cpu_temperature,
  memory_used,
  memory_percentage,
  memory_total,
  storage_used,
  storage_percentage,
  storage_total
}) => {
  const cpuUtilizationElement = document.getElementById("current-cpu-utilization");
  const cpuTemperatureElement = document.getElementById("current-cpu-temperature");
  const memoryUtilizationElement = document.getElementById("current-memory-utilization");
  const storageUtilizationElement = document.getElementById("current-storage-utilization");

  cpuUtilizationElement.textContent = `${cpu_percentage}%`;
  cpuTemperatureElement.textContent = `${cpu_temperature} °C`;
  memoryUtilizationElement.textContent = `${memory_used} MB (${memory_percentage}%) of ${memory_total} MB`;
  storageUtilizationElement.textContent = `${storage_used} GB (${storage_percentage}%) of ${storage_total} GB`;

  const cpuUtilizationProgress = document.getElementById("cpu-utilization-progress");
  const cpuTemperatureProgress = document.getElementById("cpu-temperature-progress");
  const memoryUtilizationProgress = document.getElementById("memory-utilization-progress");
  const storageUtilizationProgress = document.getElementById("storage-utilization-progress");

  cpuUtilizationProgress.style.width = `${100 - cpu_percentage}%`;
  cpuTemperatureProgress.style.width = `${100 - cpu_temperature}%`;
  memoryUtilizationProgress.style.width = `${100 - memory_percentage}%`;
  storageUtilizationProgress.style.width = `${100 - storage_percentage}%`;
};

fetchCurrentUtilization();
setInterval(fetchCurrentUtilization, 10000);