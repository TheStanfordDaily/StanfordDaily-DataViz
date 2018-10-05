console.clear()
const offenseNames = [
  "Rape",
  "Fondling",
  "Statutory Rape",
  "Dating Violence",
  "Domestic Violence",
  "Stalking"
]
const years = ["2013", "2014", "2015", "2016"]
const offensesByYear = [
  { // 2013
    "Rape": 16,
    "Fondling": 10,
    "Statutory Rape": 0,
    "Dating Violence": 2,
    "Domestic Violence": 10,
    "Stalking": 6,
  },
  { // 2014
    "Rape": 26,
    "Fondling": 4,
    "Statutory Rape": 0,
    "Dating Violence": 0,
    "Domestic Violence": 13,
    "Stalking": 14,
  },
  { // 2015
    "Rape": 25,
    "Fondling": 11,
    "Statutory Rape": 3,
    "Dating Violence": 1,
    "Domestic Violence": 12,
    "Stalking": 18,
  },
  { // 2016
    "Rape": 33,
    "Fondling": 12,
    "Statutory Rape": 0,
    "Dating Violence": 0,
    "Domestic Violence": 9,
    "Stalking": 21,
  }
]

const generateClassStr = str => {
  return str.replace(/\s+/g, '-').toLowerCase()
}

let n     = offenseNames.length, // number of layers
    m     = offensesByYear.length, // number of samples per layer
    stack = d3.stack().keys(offenseNames)

let layers = stack(offensesByYear) // calculate the stack layout

layers.forEach(function(d, i) {
  // add keys to every datapoint
  d.forEach(function(dd, j) {
    dd.year = years[j]
    dd.offenseName = offenseNames[i]
    dd.class = generateClassStr(dd.offenseName)
    dd.value =  dd.data[dd.offenseName]
  })
})

let yStackMax = d3.max(layers, function(layer) {
    return d3.max(layer, function(d) {
      return d[1]
    })
  })
let margin = { top: 70, right: 120, bottom: 40, left: 50 },
  fullChartWidth = fullChartHeight = 700,
  width  = fullChartWidth  - margin.left - margin.right,
  height = fullChartHeight - margin.top  - margin.bottom

d3.select("#stacked-bar-chart-container")
  .style("width",  fullChartWidth)
  .style("height", fullChartHeight)

let x = d3
  .scaleBand()
  .domain(years)
  .rangeRound([0, width])
  .padding(0.3)

let y = d3
  .scaleLinear()
  .domain([0, yStackMax])
  .range([height, 0])
let z = d3
  .scaleBand()
  .domain(offenseNames)
  .rangeRound([0, x.bandwidth()])

const colorPalette = {
	paloAlto: '#175e54',
	gold: '#b26f16',
	sandhill: '#b3995d',
	cardinalRed: '#8c1515',
  purple: '#53284f',
  lagunita: '#007c92',
}

const colors = Object.values(colorPalette)

let svg = d3
  .select("#stacked-bar-chart-container")
  .append("svg")
  .attr("width", width + margin.left + margin.right + 20)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + (margin.left + 20) + "," + margin.top + ")")

let layer = svg
  .selectAll(".layer")
  .data(layers)
  .enter()
  .append("g")
  .attr("class", "layer")
  .style("fill", function(d, i) {
    return colors[i]
  })

// Define the div for the tooltip
let tooltip = d3.select("body").append("div") 
    .attr("class", "tooltip")       
    .style("opacity", 0)

const focusBar = (_class) => {
  d3.selectAll(".bar")
    .filter(dd => dd.class !== _class)
    .style("opacity", 0.25)
}
let rect = layer
  .selectAll(".bar")
  .data(function(d) {
    return d
  })
  .enter()
  .append("rect")
  .attr("class", d => generateClassStr(d.offenseName) + " bar")
  .attr("x", function(d) {
    return x(d.year)
  })
  .attr("y", height)
  .attr("width", x.bandwidth() / m - 8)
  .attr("height", 0)
  .on("mouseover", d => {
    focusBar(d.class)
  })
  .on("mousemove", function(d) {   
    tooltip
      .style("opacity", .9) 
      .html("<b>" + d.value + "</b> reports of " + d.offenseName + " in " + d.year)  
      .style("left", (d3.mouse(this)[0]) + "px")   
      .style("top",  (d3.mouse(this)[1]) + 40 + "px")
    })          
  .on("mouseout", function(d) {  
    d3.selectAll(".bar").style("opacity", 1) 
    tooltip.style("opacity", 0)
  })

rect
  .transition()
  .delay(function(d, i) {
    return i * 10
  })
  .attr("y", function(d) {
    return y(d[1])
  })
  .attr("height", function(d) {
    return y(d[0]) - y(d[1])
  })

svg
  .append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x).tickSizeOuter(0))

  // add the Y gridlines
svg.append("g")     
  .attr("class", "grid")
  .call(d3.axisLeft(y)
    .ticks(10)
    .tickSize(-width)
    .tickFormat("")
  )

// Add the y Axis
svg.append("g")
  .call(d3.axisLeft(y))

// text label for the y axis
svg.append("text")
  .attr("transform", "rotate(-90)")
  .attr("y", 0 - margin.left - 30)
  .attr("x", 0 - (height / 2))
  .attr("dy", "3em")
  .style("text-anchor", "middle")
  .text("Offenses per Year")

const legendGroup = svg.append('g')
  .attr("transform", `translate(${0.85*width}, 10)`)

let legend = legendGroup
  .selectAll(".legend")
  .data(offenseNames.reverse()) // match stack order
  .enter()
  .append("g")
  .attr("class", d => "legend " + generateClassStr(d))
  .attr("transform", function(d, i) {
    return "translate(0," + i * 20 + ")"
  })
  .on("mouseover", d => {
    focusBar(generateClassStr(d))
  })       
  .on("mouseout", function(d) {  
    d3.selectAll(".bar").style("opacity", 1) 
  })

legend
  .append("rect")
  .attr("x", 0)
  .attr("width", 20)
  .attr("height", 20)
  .style("fill", function(d, i) {
    return colors[offenseNames.length - 1 - i] // match stack order
  })

legend
  .append("text")
  .attr("x", 30)
  .attr("y", 9)
  .attr("dy", ".35em")
  .style("text-anchor", "start")
  .text(function(d) {
    return d
  })

d3.selectAll("input").on("change", change)

function change() {
  (this.value === "grouped") ? transitionGrouped() : transitionStacked()
}

function transitionGrouped() {
  rect
    .transition()
    .duration(500)
    .delay(function(d, i) {
      return i * 10
    })
    .attr("x", function(d) {
      return x(d.year) + z(d.offenseName)
    })
    .transition()
    .attr("y", function(d) {
      return y(d.data[d.offenseName])
    })
    .attr("height", function(d) {
      return height - y(d.data[d.offenseName])
    })
}

function transitionStacked() {
  rect
    .transition()
    .duration(500)
    .delay(function(d, i) {
      return i * 10
    })
    .attr("y", function(d) {
      return y(d[1])
    })
    .attr("height", function(d) {
      return y(d[0]) - y(d[1])
    })
    .transition()
    .attr("x", function(d) {
      return x(d.year)
    })
}