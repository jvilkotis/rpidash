const fetchDataAndUpdateGraph = async (graph) => {
  try {
    const response = await fetch(graph.endpoint);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();

    const dates = data.dates.map(date => new Date(date));
    const values = data.values;
    const chartData = [{
      x: dates,
      y: values,
      mode: "lines",
      type: "scatter",
      line: { color: "#B80C09" }
    }];

    const maxDate = new Date(Math.max(...dates));
    const minDate = new Date(Math.min(...dates));

    const fiveDaysAgo = new Date(maxDate.getTime() - 5 * 24 * 60 * 60 * 1000);

    const rangeStart = new Date(Math.max(fiveDaysAgo, minDate));
    const rangeEnd = maxDate;

    const layout = {
      xaxis: {
        zeroline: false,
        range: [rangeStart, rangeEnd]
      },
      yaxis: { zeroline: false },
      dragmode: "pan",
      margin: { t: 20 },
      font: { family: "'Prompt', sans-serif" }
    };

    const config = {
      scrollZoom: true,
      displayModeBar: false
    };

    if (!graph.initializedFlag) {
      Plotly.newPlot(graph.id, chartData, layout, config);
      graph.initializedFlag = true;
    } else {
      const updatedData = { x: [dates], y: [values] };
      Plotly.update(graph.id, updatedData, layout);
    }
  } catch (error) {
    console.error("There was a problem fetching the data:", error);
  }
};

const initializeGraphs = async () => {
  for (const graph of graphs) {
    await fetchDataAndUpdateGraph(graph);
    setInterval(() => fetchDataAndUpdateGraph(graph), 10000);
  }
};

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

initializeGraphs();