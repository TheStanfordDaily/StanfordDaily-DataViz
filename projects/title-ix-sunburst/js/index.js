const width = window.innerWidth,
	height = window.innerHeight,
	maxRadius = Math.min(width, height) / 2 - 5

const TOTAL_CASES = 191
const POLICY_VIOLATIONS_NAME = "Policy Violations"

const x = d3
	.scaleLinear()
	.range([0, 2 * Math.PI])
	.clamp(true)

const y = d3.scaleSqrt().range([maxRadius * 0.1, maxRadius])

const colorPalette = {
	paloAlto: '#175e54',
	gold: '#b26f16',
	sandhill: '#b3995d',
	cardinalRed: '#8c1515'
}

const color = d3.scaleOrdinal([colorPalette.paloAlto, colorPalette.sandhill, colorPalette.gold])

const partition = d3.partition()

const arc = d3
	.arc()
	.startAngle(d => x(d.x0))
	.endAngle(d => x(d.x1))
	.innerRadius(d => Math.max(0, y(d.y0)))
	.outerRadius(d => Math.max(0, y(d.y1)))

const middleArcLine = d => {
	const halfPi = Math.PI / 2
	const angles = [x(d.x0) - halfPi, x(d.x1) - halfPi]
	const r = Math.max(0, (y(d.y0) + y(d.y1)) / 2)
	
	const middleAngle = (angles[1] + angles[0]) / 2
	const invertDirection = middleAngle > 0 && middleAngle < Math.PI // On lower quadrants write text ccw
	if (invertDirection) {
		angles.reverse()
	}
	
	const path = d3.path()
	path.arc(0, 0, r, angles[0], angles[1], invertDirection)
	return path.toString()
}

const textFits = d => {
	const CHAR_SPACE = 6
	
	const deltaAngle = x(d.x1) - x(d.x0)
	const r = Math.max(0, (y(d.y0) + y(d.y1)) / 2)
	const perimeter = r * deltaAngle
	
	return d.data.name.length * CHAR_SPACE < perimeter
}



// Create static portions of visualization: svg and annotations
var div = d3.select("body .toolTip")

const svg = d3
	.select("body")
	.append("svg")
	.style("width", "100vw")
	.style("height", "100vh")
	.attr("viewBox", `${-width / 2} ${-height / 2} ${width} ${height}`) // center viewbox over vis (rather than vice versa)

const centerText = svg.append("g")
	.attr("text-anchor", "middle")
	.append('text')

// Total text
const paddingBetweenNumberAndText = 26
centerText
	.append('tspan')
	.attr('x', 0)
	.attr('y', 0)
	.attr('style', 'font-size: 80px')
	.text(TOTAL_CASES.toString())

centerText
	.append('tspan')
	.attr('x', 0)
	.attr('y', paddingBetweenNumberAndText)
	.text('total reports from Sept. 2016 - Aug. 2017')

// Policy Violations annotation in upper right (which we append to center, then shift)
const topRightX = 0.21 * width
const topRightY = - 0.4 * height
centerText
	.append('tspan')
	.attr("text-anchor", "start")
	.attr('x', topRightX)
	.attr('y', topRightY)
	.attr('style', 'font-size: 80px')
	.attr('fill', colorPalette.cardinalRed)
	.text('32')

centerText
	.append('tspan')
	.attr("text-anchor", "start")
	.attr('x', topRightX)
	.attr('y', topRightY + paddingBetweenNumberAndText)
	.text('cases deemed Policy Violations')
	



const root = d3.hierarchy(getData())
	.sum(d => d.size)

const slice = svg.selectAll("g.slice").data(partition(root).descendants())

const injectTooltipWithText = (d) => {
  const percent = parseInt(100 * d.value / TOTAL_CASES)
  div.select(".title").html(d.data.name)
	div.select(".value").html(`${d.value} cases (${percent}%)`)
	div.select(".info").html(d.data.tooltipInfo)
}

const newSlice = slice
	.enter()
	.append("g")
	.attr("class", d => {
		if (!d.parent) {
			return "invisible-root-node slice" // Hide root node, replace with custom display
		} else if (d.data.name === POLICY_VIOLATIONS_NAME) {
			return "policy-violations slice"
		} else {
			return "slice"
		}
	})
	.on("mousemove", function(d){
		div.style("left", d3.event.pageX+10+"px")
		div.style("top", d3.event.pageY-25+"px")
		div.style("display", "inline-block")
		injectTooltipWithText(d)
	})
	.on("mouseout", function(d){
		div.style("display", "none")
	})

newSlice
	.append("path")
	.attr("class", "main-arc")
	.style("fill", d => {
		if (d.data.name === POLICY_VIOLATIONS_NAME) {
			return colorPalette.cardinalRed
		}
		return color((d.children ? d : d.parent).data.name)
	})
	.attr("d", arc)

newSlice
	.append("path")
	.attr("class", "hidden-arc")
	.attr("id", (_, i) => `hiddenArc${i}`)
	.attr("d", middleArcLine)

const text = newSlice
	.append("text")
	.attr("display", d => (textFits(d) ? null : "none"))

// Add white contour
text
	.append("textPath")
	.attr("startOffset", "50%")
	.attr("xlink:href", (_, i) => `#hiddenArc${i}`)
	.text(d => d.data.name)
	.style("fill", "none")
	.style("stroke-linejoin", "round")

text
	.append("textPath")
	.attr("startOffset", "50%")
	.attr("xlink:href", (_, i) => `#hiddenArc${i}`)
	.text(d => d.data.name)

function getData() {
	return {
		name: '',
		children: [
			{
				name: "Formal investigation",
				tooltipInfo: " Formal University investigations are conducted when the complainant requests it or when Stanford determines that the allegation, if true, would violate University policy.",
				children: [
					{
						name: POLICY_VIOLATIONS_NAME,
						size: 32,
						tooltipInfo: "A finding of a policy violation against the responding party, which leads to formal disciplinary action."
					},{
						name: "Non-hearing resolution",
						size: 16,
						tooltipInfo: "An outcome unique to investigations conducted under the Student Title IX Process. After a case is investigated and charged, complainants and respondents may choose to accept a case outcome proposed by the Title IX Coordinator without going through the hearing process."
					},{
						name: "No charge",
						size: 11,
						tooltipInfo: "A finding after a full investigation that 'a reasonable decision-maker or panel could not conclude by a preponderance of the evidence that a policy violation occurred.' (In Student Title IX cases, this outcome results whenever the three-person panel fails to deliver an unanimous finding of responsibility.)"
					},
				] // closes children of "Formal Investigation"
			},
			{
				name: "No investigation",
				children: [
					{
						name: "Determination",
						size: 3,
						tooltipInfo: "A determination is a University decision that moving forward to an investigation is 'not appropriate' because the allegation, if true, would not be a policy violation, or because the allegation is judged incredible after a factual review."
					},{
						name: "Inquiry",
						size: 12,
						tooltipInfo: "At the inquiry stage, the University reviews available information to decide if a formal investigation is warranted and/or feasible. Reasons a report might not proceed beyond an inquiry include lack of cooperation, lack of available evidence and a situation where the concern has already been resolved."
					},{
						name: "University Intervention",
						size: 37,
						tooltipInfo: "An intervention is an action to address a concern without a formal investigation. They take place when Stanford determines that the allegation, if true, would not be a policy violation, or when the complainant does not want a full University investigation."
					},{
						name: "External party action",
						size: 27,
						tooltipInfo: "If the University determines the respondent is not part of the Stanford community, it can still take action to assist the individual (e.g. campus bans, safety planning) in the absence of direct disciplinary authority over the complainant."
					},{
						name: "Insufficient information to proceed",
						size: 53,
						tooltipInfo: "Reports that 'lack detail and remain unverified despite attempts to contact the reported complainant.'"
					},
				]
			}
		] // CLOSES ALL CHILD NODES
	}
}