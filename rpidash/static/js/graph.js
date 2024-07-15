const fetchDataAndUpdateGraph = async (graph) => {
  try {
    let endpoint = graph.endpoint;
    if (graph.latestDate) {
      endpoint += `?recorded_after=${graph.latestDate}`;
    }

    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();

    const dates = data.dates.map(date => new Date(date));
    const values = data.values;

    if (dates.length > 0) {
      graph.dates.push(...dates)
      graph.values.push(...values)

      const chartData = [{
        x: graph.dates,
        y: graph.values,
        mode: "lines",
        type: "scatter",
        line: { color: "#B80C09" }
      }];

      const layout = {
        xaxis: { zeroline: false },
        yaxis: { zeroline: false },
        dragmode: "pan",
        margin: { t: 20 },
        font: { family: "'Prompt', sans-serif" }
      };

      const config = {
        scrollZoom: true,
        displayModeBar: false
      };

      if (!graph.latestDate) {
        Plotly.newPlot(graph.id, chartData, layout, config);
        graph.initializedFlag = true;
      } else {
        const updatedData = { x: [graph.dates], y: [graph.values] };
        Plotly.update(graph.id, updatedData);
      }

      graph.latestDate = data.dates[data.dates.length - 1];
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
    dates: [],
    values: [],
    latestDate: null
  },
  {
    endpoint: "/services/cpu_temperature",
    id: "cpu-temperature",
    valueKey: "temperature",
    dates: [],
    values: [],
    latestDate: null
  },
  {
    endpoint: "/services/memory_utilization",
    id: "memory-utilization",
    valueKey: "percentage",
    dates: [],
    values: [],
    latestDate: null
  }
];

initializeGraphs();