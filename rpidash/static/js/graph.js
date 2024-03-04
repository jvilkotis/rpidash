function fetchDataAndUpdateGraph(endpoint, id, valueKey, initializedFlag, index) {
  fetch(endpoint)
    .then(response => response.json())
    .then(data => {
      const dates = data.map(entry => new Date(entry.date));
      const values = data.map(entry => parseFloat(entry[valueKey]));
      const chartData = [{
        x: dates,
        y: values,
        mode: "lines",
        type: "scatter",
        line: {color: "#B80C09"}
      }];
      const layout = {
        xaxis: {zeroline: false},
        yaxis: {zeroline: false},
        dragmode: "pan",
        margin: {t: 20}
      };
      const config = {
        scrollZoom: true,
        displayModeBar: false
      };
      if (!initializedFlag) {
        Plotly.newPlot(id, chartData, layout, config);
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
    id: "cpu-utilization",
    valueKey: "percentage",
    initializedFlag: false
  },
  {
    endpoint: "/services/cpu_temperature",
    id: "cpu-temperature",
    valueKey: "temperature",
    initializedFlag: false
  },
  {
    endpoint: "/services/memory_utilization",
    id: "memory-utilization",
    valueKey: "percentage",
    initializedFlag: false
  }
];

graphs.forEach((graph, index) => {
  fetchDataAndUpdateGraph(
    graph.endpoint,
    graph.id,
    graph.valueKey,
    graph.initializedFlag,
    index
  );

  setInterval(() => {
    fetchDataAndUpdateGraph(
      graph.endpoint,
      graph.id,
      graph.valueKey,
      graph.initializedFlag,
      index
    );
  }, 10000);
});