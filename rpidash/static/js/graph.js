function fetchDataAndUpdateGraph(endpoint, id, yAxisTitle, graphTitle, valueKey, initializedFlag, index) {
  fetch(endpoint)
    .then(response => response.json())
    .then(data => {
      const dates = data.map(entry => new Date(entry.date));
      const values = data.map(entry => parseFloat(entry[valueKey]));
      const chartData = [{
        x: dates,
        y: values,
        mode: "lines",
        type: "scatter"
      }];
      const layout = {
        xaxis: {},
        yaxis: { title: yAxisTitle },
        title: graphTitle
      };
      if (!initializedFlag) {
        Plotly.newPlot(id, chartData, layout, { displaylogo: false });
        graphs[index].initializedFlag = true;
      } else {
        const updatedData = {
          x: [dates],
          y: [values]
        };
        Plotly.update(id, updatedData);
      }
    })
    .catch(error => {
      console.error("There was a problem fetching the data:", error);
    });
}

const graphs = [
  {
    endpoint: "/services/cpu_utilization",
    id: "cpuUtilization",
    yAxisTitle: "Utilization (%)",
    graphTitle: "CPU Utilization",
    valueKey: "percentage",
    initializedFlag: false
  },
  {
    endpoint: "/services/cpu_temperature",
    id: "cpuTemperature",
    yAxisTitle: "Temperature (°C)",
    graphTitle: "CPU Temperature",
    valueKey: "temperature",
    initializedFlag: false
  },
  {
    endpoint: "/services/memory_utilization",
    id: "memoryUtilization",
    yAxisTitle: "Utilization (%)",
    graphTitle: "Memory Utilization",
    valueKey: "percentage",
    initializedFlag: false
  }
];

graphs.forEach((graph, index) => {
  fetchDataAndUpdateGraph(
    graph.endpoint,
    graph.id,
    graph.yAxisTitle,
    graph.graphTitle,
    graph.valueKey,
    graph.initializedFlag,
    index
  );

  setInterval(() => {
    fetchDataAndUpdateGraph(
      graph.endpoint,
      graph.id,
      graph.yAxisTitle,
      graph.graphTitle,
      graph.valueKey,
      graph.initializedFlag,
      index
    );
  }, 10000);
});